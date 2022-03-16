from random import randrange
import PIL.Image as Imager
import numpy as np


def support_check(img_mode):
    if img_mode in ['HSV', 'LAB', 'RGB', 'RGBA', 'RGBX', 'YCbCr']:  # Need testing
        return len(set(img_mode))
    else:
        print(f"Image mode: {img_mode} not supported.")
        exit(1)


class Encoder:
    def __init__(self, img, msg, passwd=None):
        self.img = img
        self.msg = msg
        self.passwd = passwd
        self.fileName, self.img_arr, self.img_mode, self.channels = (None,) * 4
        self.byte_msg, self.bits, self.pixels = (None,) * 3

    def get_img_arr_data(self):
        with Imager.open(self.img, "r") as image:
            (self.width, self.height), self.fileName = image.size, image.filename
            self.img_arr, self.img_mode = np.array(list(image.getdata())), image.mode
        self.channels = support_check(self.img_mode)

    def get_byte_msg_data(self):
        # start_indicator = "$NEURAL$"
        # stop_indicator = "$NINE$"
        indicator = self.fileName
        if self.passwd is not None:
            indicator = self.passwd
        start_indicator = "$" + indicator[:len(indicator) // 2] + "$"
        stop_indicator = "$" + indicator[len(indicator) // 2:] + "$"

        msg_to_hide = start_indicator + self.msg + stop_indicator
        self.byte_msg = ''.join(f'{ord(ch):08b}' for ch in msg_to_hide)
        self.bits = len(self.byte_msg)

    def new_img_arr(self):
        index = 0
        self.get_img_arr_data()
        self.get_byte_msg_data()
        self.pixels = self.img_arr.size // self.channels
        if self.bits > self.pixels:
            print("Not enough space!!!")
            exit(1)
        for i in range(randrange((self.pixels - self.bits) // 2), self.pixels):
            for j in range(self.channels):
                if index < self.bits:
                    self.img_arr[i][j] = int(bin(self.img_arr[i][j])[2:-1] + self.byte_msg[index], 2)
                    index += 1
                else:
                    return self.img_arr.reshape((self.height, self.width, self.channels))

    def new_image(self):
        return Imager.fromarray(self.new_img_arr().astype("uint8"), self.img_mode)


def ncode(msg2hide="Secret Message", img_name="image.png", result_image_name="encoded.png", password=None):
    try:
        new_img = Encoder(img_name, msg2hide, password).new_image()
        new_img.save(result_image_name)
        new_img.close()
        # print('Success!!!')
        return 0
    except Exception as error:
        print(f'File corrupted. Delete the file named "{result_image_name}" and try again.')
        print(f'Error message: {error} \nExiting...')
        exit(1)


if __name__ == '__main__':
    with open('sample.txt', 'r') as f:
        main_msg = f.read()
    ncode(main_msg, password='abcdefg', result_image_name="encoded.png")
    print("Success")
