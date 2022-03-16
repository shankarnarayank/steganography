from os import path, remove
from utils import encode, decode, arguments


def main(action=None, ip_image="image.png", text='NeuralNine', password=None, op_image="encoded.png", op_text=None):
    if action in ['en', 'encode']:
        print("Encoding...")
        while True:
            if path.exists(op_image):
                remove(op_image)
            print("Start")
            encode.ncode(text, ip_image, op_image, password)
            print("Check")
            if not decode.Decoder(op_image, password).integrity_check():
                print("Done")
                break
            print("Again")
    elif action in ['de', 'decode']:
        print("Decoding...\n")
        if op_text is not None:
            decode.dcode(ip_image, password, op_text)
            print("Done.")
        else:
            decode.dcode(ip_image, password)
    else:
        print(f"Illegal Action: {action}")
        exit(1)


if __name__ == '__main__':
    parameters = arguments.get_args()
    # print(parameters['op_image'])
    if parameters["action"] in ['en', 'encode']:
        main(action=parameters['action'],
             ip_image=parameters['input'],
             password=parameters['passwd'],
             text=parameters['text'],
             op_image=parameters['op_image'])
    elif parameters["action"] in ['de', 'decode']:
        main(action=parameters['action'],
             ip_image=parameters['input'],
             password=parameters["passwd"],
             op_text=parameters['op_text'])
    else:
        print("Invalid operation.")
        exit(1)
