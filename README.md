# STEGANOGRAPHY

## LSB (v1.0.5)

Author: Shankar Narayan K

### INTRODUCTION

This is a python tool used to **hide**(encode) and **extract**(decode) messages using **'Least Significant Bit(LSB)'** steganography method.

This project is inspired from a [video][video_link] by [NeuralNine][channel_link].

While the core algorithm remains the same, I've added some of my own personal touch, like:
 
 - Adding parameter processing capabilities.
 - Starting message encoding randomly inside the message instead of from the beginning itself, assisted by the start and stop indicator.
 - Adding a password requirement. (The password is used to generate start and stop indicator)
 - Ability to take parameters from files directly, all the parameters can be written to a file, and they can be passed instead using **_ ( underscore )** as the prefix.

I will leave it to the PROs to figure out the potential of that last feature **;-)**

![EXAMPLE][pixel]

So here is the simplest explanation I can think of:

 - Consider the above image as a small slice of a large image.
 - Take this group of 9 pixels as a matrix and flatten it(meaning we are converting it from 3x3 to 9x1)
 - Now this flatted matrix has 3 colours `(RGB)` for each element(pixel), each `colour` is also called a `channel` (will be used here interchangeably).
 - Each channel has a value ranging from 0 to 255, which can be represented using 8 bits or 1 byte.
 - The right-most bit of any binary value is called the **Least Significant Bit** `(LSB)`.
 - We convert our message into a binary string and replace the `LSB` of each channel's value with one bit from our binary string.
- For securing the message, it is sandwiched between the password and stored at a random location within the image.
 - Reversing the process will give us the original message.

### DISCLAIMER

This tool does not provide any form of encryption or decryption mechanism, anyone with the knowledge of LSB steganography, can decode the message.

If you require such form of encryption look elsewhere or encrypt the message and/or password prior to encoding it to an image. 

### REQUIREMENTS

```sh
pip install -r requirements.txt
```

 - Numpy
 - Pillow
 - Filetype


### USAGE

#### GENERAL

```sh
python lsb.py -h
```
```
usage: lsb.py [-h] [-v] encode|decode ...

Hide/extract messages from an image using LSB encoding.
(LSB = Least Significant Bit)

options:
  -h, --help     show this help message and exit
  -v, --version  show program's version number and exit

Action:
  encode|decode  Choose one of the two operation.
    encode (en)  Do encoding operation.
                 For more info: "python lsb.py encode -h"
    decode (de)  Do decoding operation. 
                 For more info: "python lsb.py decode -h"

Made by [shankar12789](https://github.com/shankar12789)
```

<br>

#### ENCODING

```sh
python lsb.py en -h
```

```
usage: lsb.py encode [-h] -i IP_IMAGE -t MESSAGE|FILE [-p PASSWORD]
                     [-o OP_IMAGE]

Encode a MESSAGE inside an IMAGE.
Supported Image Formats: 'CMYK', 'HSV', 'LAB', 'RGB', 'RGBA', 'RGBX', 'YCbCr'.
Any other format will result in error.

options:
  -h, --help            show this help message and exit

Required:
  -i IP_IMAGE, --input IP_IMAGE
                        Path of the IP_IMAGE into which the MESSAGE will be encoded.
                        Note: Has been tested with PNG images only.
                        Other extensions are NOT TESTED and may produce errors.
  -t MESSAGE|FILE, --text MESSAGE|FILE
                        The MESSAGE to be encoded. The MESSAGE can be entered directly within quotes(" ") 
                        or from a file by appending '@' before the path of the FILE.
                        Ex: -t @/home/USER/Desktop/sample.txt
                        Note: 1. Only full path and relative path are supported.
                              2. "~" and other environment variables are not resolved.
                              3. MESSAGE can be anything as long as their size is less than the IMAGE 
                                 itself,including the PASSWORD.

Optional:
  -p PASSWORD, --passwd PASSWORD
                        The PASSWORD to encode your message. Default: IP_IMAGE name.
                        Note: 1. For maximum security generate a random string of minimum 8 characters.
                              2. There is no password recovery method. 
                                 So, be sure to store your password.
  -o OP_IMAGE, --output OP_IMAGE
                        Name of the resultant OP_IMAGE file. Default: "encoded.png"

Made by [shankar12789](https://github.com/shankar12789)
```

<br>

#### DECODING



```sh
python lsb.py de -h
```

```
usage: lsb.py decode [-h] -i IP_IMAGE -p PASSWORD [-o FILE]

Decode a MESSAGE from an IMAGE (if it exists).

options:
  -h, --help            show this help message and exit

Required:
  -i IP_IMAGE, --input IP_IMAGE
                        Path of the IP_IMAGE to be decoded.
  -p PASSWORD, --passwd PASSWORD
                        The PASSWORD to decode the MESSAGE. 
                        Default: The original name of the IMAGE before Encoding.

Optional:
  -o FILE, --output FILE
                        The path of the FILE where the decoded MESSAGE will be written to. 
                        Default: The terminal itself

Made by [shankar12789](https://github.com/shankar12789)
```

### EXAMPLE

<br>

### BEGINNER

##### ENCODING

```sh
python lsb.py encode --input resources/image.png --text "Hello World"
```

<p align="center"><b>OR</b></p>

```sh
python lsb.py en -i resources/image.png -t "Hello World"
```

##### DECODING

```sh
python lsb.py decode --input outputs/encoded.png --passwd "image.png"
```

<p align="center"><b>OR</b></p>

```sh
python lsb.py de -i outputs/encoded.png -p "image.png"
```

<br>

### INTERMEDIATE

##### ENCODING

```sh
python lsb.py encode --input resources/image.png --text "Hello World" --passwd "nowyouseeme" --output outputs/nowyoudont.png
```

<p align="center"><b>OR</b></p>

```sh
python lsb.py en -i resources/image.png -t "Hello World" -p "nowyouseeme" -o outputs/nowyoudont.png
```

##### DECODING

```sh
python lsb.py decode --input outputs/nowyoudont.png --passwd "nowyouseeme" --output outputs/supersecretmsg.txt
```

<p align="center"><b>OR</b></p>

```sh
python lsb.py de -i outputs/nowyoudont.png -p "nowyouseeme" -o outputs/supersecretmsg.txt
```

<br>

### ADVANCED

##### ENCODING

```sh
python lsb.py encode --input resources/image.png --text resources/sample.txt --passwd "secretmessage" --output outputs/nowyoudont2.png
```

<p align="center"><b>OR</b></p>

```sh
python lsb.py en -i resources/image.png -t resources/sample.txt -p "secretmessage" -o outputs/nowyoudont2.png
```

##### DECODING

```sh
python lsb.py decode --input outputs/nowyoudont2.png --passwd "secretmessage" --output outputs/supersecretmessage2.txt
```

<p align="center"><b>OR</b></p>

```sh
python lsb.py de -i outputs/nowyoudont2.png -p "secretmessage" -o outputs/supersecretmessage2.txt
```

<br>

### PROFESSIONAL

##### ENCODING

```sh
python lsb.py _resources/en_args.txt
```

| [Encoding Arguments][en_args] |
|:-----------------------------:|

##### DECODING

```
python lsb.py _resources/de_args.txt
```

| [Decoding Arguments][de_args] |
|:-----------------------------:|

### POWER USER

##### ENCODING

###### LINUX

```sh
python lsb.py en -i resources/image.png -t "$(cat resources/sample.txt)" -o outputs/pow_sh.png
```

###### COMMAND PROMPT

```cmd
forfiles /p resources /m sample.txt /c "cmd /c python ..\lsb.py en -i image.png -t @path -o ..\outputs\pow_cmd.png"
```

###### POWERSHELL

```ps
python .\lsb.py en -i .\resources\image.png -t "$( Get-Content .\resources\sample.txt -Raw )" -o .\outputs\pow_ps.png
```

<br><br>

| [![][original]][original] | [![][encoded]][encoded] |
|:-------------------------:|:-----------------------:|
|    **ORIGINAL IMAGE**     |    **ENCODED IMAGE**    |

### TO DO

- [ ] Add meaningful comments to the code.
- [ ] Display detailed information at run time
- [ ] Add a progress bar (preferably like the one seen in new pip3 command)
- [ ] Make a GUI for convenient usage
 


### REFERENCES

 - [NeuralNine][video_link]'s [video][video_link]
 - [Argparse Docs][pydocs]
 - [A Simple Guide To Command Line Arguments With ArgParse][towardsdatascience_1]
 - [How to Build Command Line Interfaces in Python With argparse][realpython]
 - [How to use argparse subparsers correctly?][stackoverflow_1]
 - [How to check if a file is a valid image file?][stackoverflow_2]
 - [The Ultimate Markdown Cheat Sheet][towardsdatascience_2]

[video_link]: https://youtu.be/_DhqDYLS8oY?t=593
[channel_link]: https://www.youtube.com/c/NeuralNine
[pydocs]: https://docs.python.org/3/library/argparse.html
[towardsdatascience_1]: https://towardsdatascience.com/a-simple-guide-to-command-line-arguments-with-argparse-6824c30ab1c3
[towardsdatascience_2]:https://towardsdatascience.com/the-ultimate-markdown-cheat-sheet-3d3976b31a0
[stackoverflow_1]: https://stackoverflow.com/a/17074215
[stackoverflow_2]: https://stackoverflow.com/a/61195193
[realpython]: https://realpython.com/command-line-interfaces-python-argparse/
[pixel]: resources/pixels.png
[original]: resources/image.png
[encoded]: outputs/encoded.png
[en_args]: resources/en_args.txt
[de_args]: resources/de_args.txt

### FOOTNOTE

This is my first serious project. Constructive feedbacks are welcome.

I hope you like my work.

Thanks for reading till the end.
