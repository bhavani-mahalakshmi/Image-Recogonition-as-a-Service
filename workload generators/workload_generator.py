import os
import requests
import argparse

parser = argparse.ArgumentParser(description='Upload images')
parser.add_argument('--num_request', type=int, help='One image per request')
parser.add_argument('--url', type=str, help='URL of the backend server, e.g. http://3.86.108.221/xxxx.php')
parser.add_argument('--image_folder', type=str, help='The path of the folder where images are saved on your local machine')

def send_one_request(url, image_path):
    # Define http payload, "file" is the key of the http payload
    file = {'file': open(image_path, 'rb')}
    r = requests.post(url, files=file)
    # Print error message if failed
    if r.status_code != 200:
        print('sendErr: ' + r.url)
    else:
        image_msg = image_path.split('/')[-1] + ' uploaded!'
        msg = image_msg + '\n' + 'Classification result: ' + r.text
        print(msg)

args = parser.parse_args()
url = args.url
num_request = args.num_request
image_folder = args.image_folder

# Iterate through all the images in your local folder
for i, name in enumerate(os.listdir(image_folder)):
    if i == num_request:
        break
    image_path = image_folder + name
    send_one_request(url, image_path)
