import sys
import numpy as np
import PIL.Image as Imager
from encode import support_check


class Decoder:

    def __init__(self, img, passwd=None):
        self.img, self.passwd = img, passwd
        self.start_indicator, self.stop_indicator, self.msg, self.img_arr, self.img_mode = (None,) * 5

    def get_img_arr_data(self):
        with Imager.open(self.img, "r") as Image:
            self.img_arr, self.img_mode = np.array(list(Image.getdata())), Image.mode
            self.passwd = Image.filename if self.passwd is None else self.passwd
        support_check(self.img_mode)

    def get_text_msg_data(self):
        self.get_img_arr_data()
        secret_bits = ''.join([bin(channel)[-1] for pixel in self.img_arr for channel in pixel])
        secret_bytes = [secret_bits[i:i + 8] for i in range(0, len(secret_bits), 8)]
        secret_msg = ''.join([chr(int(byte, 2)) for byte in secret_bytes])
        return secret_msg

    def integrity_check(self):
        self.msg = self.get_text_msg_data()
        # start_indicator = "$NEURAL$"
        # stop_indicator = "$NINE$"
        self.start_indicator = "$" + self.passwd[:len(self.passwd) // 2] + "$"
        self.stop_indicator = "$" + self.passwd[len(self.passwd) // 2:] + "$"
        if self.start_indicator in self.msg and self.stop_indicator in self.msg:
            return 0
        else:
            if self.start_indicator not in self.msg:
                return 1
            elif self.stop_indicator not in self.msg:
                return 2
            else:
                return 3

    def display_msg(self, out_file=sys.stdout):
        x = self.integrity_check()
        if x:
            choices = [None, "couldn't find start_indicator", "couldn't find stop_indicator", "unknown error"]
            print(choices[x])
            exit(1)
        msg = self.msg[self.msg.index(self.start_indicator) + len(self.start_indicator):
                       self.msg.index(self.stop_indicator)]

        if out_file != sys.stdout:
            # noinspection PyTypeChecker
            with open(out_file, "w", encoding="utf8") as outFile:
                print(msg, file=outFile)
        else:
            print(msg)


def dcode(image="encoded.png", password="image.png", out_file=sys.stdout):
    Decoder(image, password).display_msg(out_file)


if __name__ == '__main__':
    dcode(password="abcdefgh", image="encoded1.png")
