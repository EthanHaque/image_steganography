#!/usr/bin/env python

"""Encodes and decodes messages into and from images.

This module provides functions for encoding and decoding messages into
and from images using the LSB encoding scheme.

Examples
--------

    $ python encoder.py encode "Hello, world!" ./images/black.png
    $ python encoder.py decode ./images/black.png

"""

import argparse

from PIL import Image


def read_image(path):
    """Reads an image from a path and returns it as a PIL image.

    Parameters
    ----------
    path: str
        The path to the image.

    Returns
    -------
    image: PIL.Image
        The image.

    """
    img = Image.open(path)
    return img


def validate_message(message):
    """Validates a message to be encoded.

    Checks that the message is a string and that it contains only ASCII
    characters from the (non-extended) ASCII table (i.e. characters
    between 0 and 127).

    Parameters
    ----------
    message: str
        The message to validate.

    Returns
    -------
    valid: bool
        True if the message is valid, False otherwise.

    """
    return message.isascii()


def _encode_message_into_image(image, message, bits_per_char=7,
                               no_channels=3, metadata_bytes=4):
    """Encodes a message into an image.

    Encodes a message into an image by writing the message into the
    least significant bits of each pixel.

    Parameters
    ----------
    image: PIL.Image
        The image to encode the message into.
    message: str
        The message to encode.
    bits_per_char: int (optional)
        The number of bits per character. Defaults to 7. The default
        value is 7 because the range of valid characters is between
        0 and 127.
    no_channels: int (optional)
        The number of channels per pixel. Defaults to 3 (RGB).
    metadata_bytes: int (optional)
        The number of bytes to use for metadata. Defaults to 4 bytes to
        store the message length as a 32-bit integer.

    Returns
    -------
    image: PIL.Image
        The image with the message encoded.

    Notes
    -----
    This function is not intended to be used directly. Instead, use the
    encode() function to validate the message.


    The specific encoding scheme used is as follows:

    1. The message length is encoded as a 32-bit integer by default into
    the least significant bits of each individual channel of each pixel
    in the first few pixels of the image.

    2. The message is encoded into the least significant bits of each
    channel of each pixel in the image after the message length. By
    default each character is encoded into 7 bits.

    """
    if not validate_message(message):
        raise ValueError("Message is not valid.")

    pixel_map = image.load()
    bits_per_byte = 8
    metadata_bits = metadata_bytes * bits_per_byte
    max_message_length = 2 ** metadata_bits - 1

    # bounds checking
    message_length = len(message)
    pixel_count = image.width * image.height
    bits_available = pixel_count * no_channels
    bits_needed = message_length * bits_per_char + metadata_bits
    if bits_needed > bits_available or message_length > max_message_length:
        raise ValueError("Message is too long to encode.")

    # Message length encoding
    bits_changed_count = 0
    # Iterating over range backwards
    for i in range(metadata_bytes - 1, -1, -1):
        byte = (message_length >> (i * bits_per_byte)) & 0xFF
        for bit_position in range(bits_per_byte - 1, -1, -1):
            update_pixel_channel(byte, bit_position, bits_changed_count,
                                 image.width, no_channels, pixel_map)
            bits_changed_count += 1

    # Compute message encodings and update bitmap
    for i in range(message_length):
        ascii_val = ord(message[i])
        for bit_position in range(bits_per_char - 1, -1, -1):
            update_pixel_channel(ascii_val, bit_position, bits_changed_count,
                                 image.width, no_channels, pixel_map)
            bits_changed_count += 1

    return image


def update_pixel_channel(byte, bit_position, count, image_width, no_channels,
                         pixel_map):
    """Updates the least significant bit of a pixel channel.

    Finds the location of and updates the least significant bit of a
    channel of a pixel in the image.

    Parameters
    ----------
    byte: int
        The byte containing the bit which will be used to set the
        least significant bit of the calculated channel..
    bit_position: int
        The position of the bit in `byte` from the left.
    count: int
        The number of bits updated so far.
    image_width: int
        The width of the image in pixels.
    no_channels: int
        The number of channels per pixel.
    pixel_map: PIL.Image.load()
        The pixel map of the image.

    """
    bit = (byte >> bit_position) & 0x01
    channel, col, row = compute_map_location(count, image_width, no_channels)
    new_value = (pixel_map[col, row][channel] & 0xFE) | bit
    pixel_val = list(pixel_map[col, row])
    pixel_val[channel] = new_value
    pixel_map[col, row] = tuple(pixel_val)


def compute_map_location(count, width, no_channels):
    """Calculates which pixel and channel to update.

    Calculates which pixel and channel to update based on the number of
    bits updated so far.

    Parameters
    ----------
    count: int
        The number of bits updated so far.
    width: int
        The width of the image in pixels.
    no_channels: int
        The number of channels per pixel.

    Returns
    -------
    channel: int
        The channel to update.
    col: int
        The column of the pixel to update.
    row: int
        The row of the pixel to update.

    """
    row = count // (width * no_channels)
    col = count // no_channels % width
    channel = count % no_channels
    return channel, col, row


def encode(image_path, message, output_path, bits_per_char=7, no_channels=3,
           metadata_bytes=4):
    """Encodes a message into an image.

    Encodes a message into an image by writing the message into the
    least significant bits of each pixel.

    Parameters
    ----------
    image_path: str
        The path to the image to encode the message into.
    message: str
        The message to encode.
    output_path: str
        The path to the output image.
    bits_per_char: int (optional)
        The number of bits per character. Defaults to 7. The default
        value is 7 because the range of valid characters is between
        0 and 127.
    no_channels: int (optional)
        The number of channels per pixel. Defaults to 3 (RGB).
    metadata_bytes: int (optional)
        The number of bytes to use for metadata. Defaults to 4 bytes to
        store the message length as a 32-bit integer.

    Returns
    -------
    image: PIL.Image
        The image with the message encoded.

    """
    image = read_image(image_path)
    encoded_image = _encode_message_into_image(image, message, bits_per_char,
                                               no_channels, metadata_bytes)
    encoded_image.save(output_path)
    return encoded_image


def _decode_message_from_image(image, bits_per_char=7, no_channels=3,
                               metadata_bytes=4):
    """Decodes a message from an image.

    Decodes a message from an image by reading the message from the
    least significant bits of each channel in each pixel of the image.

    Parameters
    ----------
    image: PIL.Image
        The image to decode the message from.
    bits_per_char: int (optional)
        The number of bits per character. Defaults to 7. The default
        value is 7 because the range of valid characters is between
        0 and 127.
    no_channels: int (optional)
        The number of channels per pixel. Defaults to 3 (RGB).
    metadata_bytes: int (optional)
        The number of bytes to use for metadata. Defaults to 4 bytes to
        store the message length as a 32-bit integer.

    Returns
    -------
    message: str
        The message decoded from the image.

    See Also
    --------
    _encode_message_into_image: For the encoding algorithm.

    """
    pixel_map = image.load()
    bits_per_byte = 8
    metadata_bits = metadata_bytes * bits_per_byte

    # Bounds checking
    pixel_count = image.width * image.height
    bits_available = pixel_count * no_channels
    if bits_available < (metadata_bytes * bits_per_byte):
        raise ValueError("Image is too small to decode.")

    # Message length decoding
    bits_read_count = 0
    message_length = 0
    for i in range(metadata_bits):
        message_length = append_bit(message_length, bits_read_count,
                                    image.width, no_channels, pixel_map)
        bits_read_count += 1
    message_length >>= 1

    # Decoding message
    message = []
    for i in range(message_length):
        ascii_val = 0
        for j in range(bits_per_char):
            ascii_val = append_bit(ascii_val, bits_read_count, image.width,
                                   no_channels, pixel_map)
            bits_read_count += 1
        ascii_val >>= 1

        message.append(chr(ascii_val))

    return "".join(message)


def append_bit(running_value, bits_read_count, image_width, no_channels,
               pixel_map):
    """Appends a bit to the end of an int.

    Calculates the position of and appends a bit to the least
    significant bit of an int and shifts the int to the left.

    Parameters
    ----------
    running_value: int
        The int to append the bit to.
    bits_read_count: int
        The number of bits read so far.
    image_width: int
        The width of the image in pixels.
    no_channels: int
        The number of channels per pixel.
    pixel_map: PIL.Image.load()
        The pixel map of the image.

    Returns
    -------
    running_value: int
        The int with the bit appended.

    """
    channel, col, row = compute_map_location(bits_read_count, image_width,
                                             no_channels)
    running_value |= pixel_map[col, row][channel] & 0x01
    running_value <<= 1
    return running_value


def decode(image_path, bits_per_char=7, no_channels=3, metadata_bytes=4):
    """Decodes a message from an image.

    Decodes a message from an image by reading the message from the
    least significant bits of each channel in each pixel of the image.

    Parameters
    ----------
    image_path: str
        The path to the image to decode the message from.
    bits_per_char: int (optional)
        The number of bits per character. Defaults to 7. The default
        value is 7 because the range of valid characters is between
        0 and 127.
    no_channels: int (optional)
        The number of channels per pixel. Defaults to 3 (RGB).
    metadata_bytes: int (optional)
        The number of bytes to use for metadata. Defaults to 4 bytes to
        store the message length as a 32-bit integer.

    Returns
    -------
    message: str
        The message decoded from the image.

    """
    image = read_image(image_path)
    decoded_message = _decode_message_from_image(image, bits_per_char,
                                                 no_channels, metadata_bytes)
    return decoded_message


def init_parser():
    """Initializes the argument parser.

    Returns
    -------
    parser: argparse.ArgumentParser
        The initialized argument parser.

    """
    parser = argparse.ArgumentParser(
        description="Encodes and decodes messages into and from images.")
    subparsers = parser.add_subparsers(dest="command")

    encode_parser = subparsers.add_parser("encode",
                                          help="Encodes a message into an image.")
    encode_parser.add_argument("image_path",
                               help="The path to the image to encode the message into.")
    encode_parser.add_argument("message", help="The message to encode.")
    encode_parser.add_argument("output_path",
                               help="The path to the output image.")
    encode_parser.add_argument("-b", "--bits-per-char", type=int, default=8,
                               help="The number of bits per character.")
    encode_parser.add_argument("-c", "--channels", type=int, default=3,
                               help="The number of channels per pixel.")
    encode_parser.add_argument("-m", "--metadata-bytes", type=int, default=4,
                               help="The number of bytes used for metadata.")
    encode_parser.add_argument("-v", "--verbose", action="store_true",
                               help="Shows the encoded image.")
    encode_parser.add_argument("-d", "--debug", action="store_true",
                               help="Shows the encoded image and prints the encoded message.")
    encode_parser.set_defaults(func=encode)

    decode_parser = subparsers.add_parser("decode",
                                          help="Decodes a message from an image.")
    decode_parser.add_argument("image_path",
                               help="The path to the image to decode the message from.")
    decode_parser.add_argument("-b", "--bits-per-char", type=int, default=8,
                               help="The number of bits per character.")
    decode_parser.add_argument("-c", "--channels", type=int, default=3,
                               help="The number of channels per pixel.")
    decode_parser.add_argument("-m", "--metadata-bytes", type=int, default=4,
                               help="The number of bytes used for metadata.")
    decode_parser.add_argument("-o", "--output-path",
                               help="The path to the output text file.")
    decode_parser.add_argument("-q", "--quiet", action="store_true",
                               help="Does not print out the decoded message.")
    decode_parser.set_defaults(func=decode)

    return parser


def main():
    """Runs the program."""
    parser = init_parser()
    args = parser.parse_args()

    if args.command == "encode":
        image = args.func(args.image_path,
                          args.message,
                          args.output_path,
                          args.bits_per_char,
                          args.channels,
                          args.metadata_bytes)
        if args.verbose:
            image.show()
        if args.debug:
            print(args.message)
            image.show()

    elif args.command == "decode":
        message = args.func(args.image_path,
                            args.bits_per_char,
                            args.channels,
                            args.metadata_bytes)
        if not args.quiet:
            print(message)

        if args.output_path:
            with open(args.output_path, "w") as f:
                f.write(message)


if __name__ == '__main__':
    main()
