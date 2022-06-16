# Image Steganography

Hide a message inside an image with this simple CLI tool. Clone the repo and
see usage for details on how to run.

## Usage
``` bash
$ python encoder.py encode <image-path> <message> <output-path> # encode
$ python encoder.py decode <image-path> # decode
$ python encoder.py decode <image-path> -o <output-path> # decode into a file
```
#### Examples
``` bash
$ python encoder.py encode ./images/black.png "Hello World" ./output/black.png
$ python encoder.py decode ./images/black.png
Hello World
$ python encoder.py decode ./images/black.png -o ./output/black.txt
Hello World
$ python encoder.py decode ./images/black.png -o ./output/black.txt -q # quiet
```

#### Options for encoding
- `<image-path>`: Path to the image to encode the message in.
- `<message>`: The message to encode.
- `<output-path>`: Path to the output image.
- `-b, --bits-per-char`: The number of bits to use for encoding. Defaults to 7.
- `-c, --channels`: The number of channels to use for encoding. Defaults to 3.
- `-m, --metadaya-bytes`: The number of bytes to use for metadata. Defaults 
  to 4. (This is the number of bytes used to store the message length.)
- `-v, --verbose`: Shows the encoded image once finished.
- `-d, --debug`: Shows the encoded image and prints the encoded message.
- `-h, --help`: Gives usage information.

#### Options for decoding
- `<image-path>`: Path to the image to decode.
- `-b, --bits-per-char`: The number of bits to use for decoding. Defaults to 7.
- `-c, --channels`: The number of channels to use for decoding. Defaults to 3.
- `-m, --metadaya-bytes`: The number of bytes to use for metadata. Defaults
    to 4. (This is the number of bytes used to store the message length.)
- `-o, --output-path`: Output path to a text file for the decoded message.
- `-q, --quiet`: Suppress output.

## How it works

The messages are encoded into the image by setting the least significant bit of
each channel of each pixel to a bit of data in the message. 


The message must be composed of ASCII character. However, the script can be 
easily modified to allow for Unicode characters greater than 0x7F. The drawback
would be an increased memory footprint for the encoded message as the 
script would need to encode each character with more bits of information than 
may be needed. 


The decoding algorithm just reverses the encoding process. 


There is no encryption performed on the input message.