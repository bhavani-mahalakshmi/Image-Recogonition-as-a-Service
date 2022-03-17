import os
import time
import json
import base64
import traceback
from wrapper_sqs import Queue
from wrapper_s3 import ObjectStore
from face_recognition import face_match
from credentials import INPUT_QUEUE, OUTPUT_QUEUE

try:
    run_cont =  bool(os.environ['RUN_CONTINUOUSLY'])
except:
    print('Did not find RUN_CONTINUOUSLY environment variable. Defaulting to False.')
    run_cont = False

def process_image(image):
    """
    Get image string from queue, store it in s3, classify it,
    store input image in input bucket and output in output bucket.

    :param image: (dict) Details of the image.
    """
    file_name = image['file_name']
    image_string = image['encoded_image']
    unique_id = image['unique_id']
    temp_path = '/tmp/' + file_name
    with open(temp_path, 'wb') as fh:
        fh.write(base64.b64decode(image_string))

    #Run classificaiton on image
    classification = face_match(temp_path, 'data.pt')

    print('Done: {} {}'.format(file_name, classification))
    key = file_name.split('.')[0]
    value = classification[0]

    response_message = {
      'unique_id': unique_id,
      'classification': value
    }
    response_message = json.dumps(response_message)
    Queue.send_message(OUTPUT_QUEUE, response_message)
    print('Result sent to output queue!')

    ObjectStore.upload_input_images(temp_path)
    print('Input image file uploaded to s3!')

    ObjectStore.upload_output_results(key, value)
    print('Output file uploaded to s3!')

    # Delete file
    os.remove(temp_path)

def run_job():
    """
    Process the message from input SQS queue and delete it from the queue.
    Sleep for 1 minute if no messages in queue and shutdown if no messages
    after 1 minute.
    """
    if Queue.get_num_messages_available(INPUT_QUEUE) > 0:
        try:
            print('Retrieving image from SQS!')
            image_request, receipt_handle = Queue.get_latest_message(INPUT_QUEUE)
            image_request = json.loads(image_request)
            process_image(image_request)
            Queue.delete_message(INPUT_QUEUE, receipt_handle)
        except Exception:
            print('Error reading message!')
            traceback.print_exc()
    else:
        print('No more messages in queue!')
        import requests
        r = requests.get('http://169.254.169.254/latest/meta-data/instance-id')
        instance_id = r.text
        time.sleep(60)
        if Queue.get_num_messages_available(INPUT_QUEUE) > 0:
            pass
        else:
            print('Stopping instance ', instance_id)
            os.system('sudo shutdown now -h')

if __name__ == '__main__':
    while True:
        run_job()