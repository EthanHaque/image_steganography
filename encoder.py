from PIL import Image


def read_image(path):
    """
    Reads an image from a path and returns a PIL image object.

    :param path: The path to the image.
    :return: A PIL image object.
    """
    img = Image.open(path)
    return img


def validate_message(message):
    """
    Validates if a message contains all legal characters.
    :param message: The string to validate.
    :return: True if the message is valid. False otherwise.
    """
    return message.isascii()


def _encode_message_into_image(image, message, bits_per_char=8, no_channels=3, metadata_bytes=4):
    """
    Encodes a message into an image using the least significant bit of each pixel.
    :param image: The image to encode the message into.
    :param message: The message to encode.
    :param bits_per_char: The number of bits per character.
    :param no_channels: The number of channels per pixel.
    :param metadata_bytes: The number of bytes used for metadata.
    :return: The encoded image.
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
            update_pixel_channel(byte, bit_position, bits_changed_count, image.width, no_channels, pixel_map)
            bits_changed_count += 1

    # Compute message encodings and update bitmap
    for i in range(message_length):
        ascii_val = ord(message[i])
        for bit_position in range(bits_per_char - 1, -1, -1):
            update_pixel_channel(ascii_val, bit_position, bits_changed_count, image.width, no_channels, pixel_map)
            bits_changed_count += 1

    return image


def update_pixel_channel(byte, bit_position, count, image_width, no_channels, pixel_map):
    """
    Updates a single channel of a pixel in an image.
    :param byte: The byte containing the chosen bit to update the channel with.
    :param count: The number of bits already updated.
    :param image_width: The width of the image.
    :param bit_position: The position of the bit to update from the left.
    :param no_channels: The number of channels per pixel.
    :param pixel_map: The pixel map of the image.
    """
    bit = (byte >> bit_position) & 0x01
    channel, col, row = compute_map_location(count, image_width, no_channels)
    new_value = pixel_map[col, row][channel] & (0xFE | bit)
    pixel_val = list(pixel_map[col, row])
    pixel_val[channel] = new_value
    pixel_map[col, row] = tuple(pixel_val)


def compute_map_location(count, width, no_channels):
    """
    Computes which pixel and channel the count of updated bits corresponds to.
    :param width: The width of the image.
    :param count: The number of bits already updated.
    :param no_channels: The number of channels per pixel.
    """
    row = count // (width * no_channels)
    col = count // no_channels % width
    channel = count % no_channels
    return channel, col, row


def encode(image_path, message):
    """
    Encodes a message into an image using the least significant bit of each pixel.
    :param image_path: The path to the image to encode the message into.
    :param message: The message to encode.
    :return: The encoded image.
    """
    image = read_image(image_path)
    encoded_image = _encode_message_into_image(image, message)
    return encoded_image


def decode_message_from_image(image, bits_per_char=8, no_channels=3, metadata_bytes=4):
    """
    Decodes a message from an image using the least significant bit of each pixel.
    :param image: The image to decode the message from.
    :param bits_per_char: The number of bits per character.
    :param no_channels: The number of channels per pixel.
    :param metadata_bytes: The number of bytes used for metadata.
    :return: The decoded message.
    """
    pixel_map = image.load()
    metadata_bits = metadata_bytes * 8
    max_message_length = 2 ** metadata_bits - 1

    # Bounds checking
    pixel_count = image.width * image.height
    bits_available = pixel_count * no_channels
    if bits_available < (metadata_bytes * 8):
        raise ValueError("Image is too small to decode.")

    # Message length decoding
    bits_read_count = 0
    message_length = 0
    for i in range(metadata_bits):
        channel, col, row = compute_map_location(bits_read_count, image.width, no_channels)
        message_length |= pixel_map[col, row][channel] & 0x01
        message_length <<= 1
        bits_read_count += 1
    message_length >>= 1

    # Message decoding
    message = []
    for i in range(message_length):
        ascii_val = 0
        for j in range(bits_per_char):
            channel, col, row = compute_map_location(bits_read_count, image.width, no_channels)
            ascii_val |= pixel_map[col, row][channel] & 0x01
            ascii_val <<= 1
            bits_read_count += 1
        ascii_val >>= 1

        message.append(chr(ascii_val))

    return "".join(message)


if __name__ == '__main__':
    img = encode("./images/white.png", "Hello World!")
    img.show()
    message = decode_message_from_image(img)
    print(message)
