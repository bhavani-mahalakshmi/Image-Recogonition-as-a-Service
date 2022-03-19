import os
import uuid
import json
import boto3
import base64
from flask import (Flask, render_template, request)

app = Flask(__name__)

sqs = boto3.client('sqs', region_name='us-east-1')

request_queue_url = 'https://sqs.us-east-1.amazonaws.com/051675418934/Request-Queue'
response_queue_url = 'https://sqs.us-east-1.amazonaws.com/051675418934/Response-Queue'

@app.route('/health-check')
def health_check():
    """Perform health check on the web server."""
    return 'Healthy'

@app.route('/')
def home():
    """Go to the default landing page for the UI."""
    return render_template('index.html')

@app.route('/', methods=['POST'])
def process():
    """
    Process an uploaded image by pushing it in a base64-encoded
    format along with a unique identifier into request queue
    and return a response containing the classification of the 
    image from the response queue.

    :return: (str) The classification of the image.
    """
    try:
        uploaded_file = request.files.get('file')
        if uploaded_file.filename:
            identifier = str(uuid.uuid4())
            converted_string = base64.b64encode(uploaded_file.read())
            sqs_message_body = {
                'encoded_image': str(converted_string, 'utf-8'),
                'unique_id': identifier,
                'file_name': uploaded_file.filename
            }
            # Send message to SQS queue.
            sqs.send_message(
                QueueUrl=request_queue_url,
                MessageBody=json.dumps(sqs_message_body)
            )
        print('Uploaded file to the request queue!')
        # Poll the response queue to get the classfication of the image.
        while True:
            sqs_output = sqs.receive_message(
                QueueUrl=response_queue_url,
                AttributeNames=['All'],
                MaxNumberOfMessages=10,
                WaitTimeSeconds=1
            )
            messages = sqs_output.get('Messages', [])
            for item in messages:
                msg_body = json.loads(item.get('Body'))
                if msg_body['unique_id'] == identifier:  # Check the id of the image
                    sqs.delete_message(
                        QueueUrl=response_queue_url,
                        ReceiptHandle=item.get('ReceiptHandle')
                    )
                    return msg_body.get('classification')
    except Exception as e:
        print('Error occurred: {}'.format(e))
        return ''

@app.route('/results')
def results():
    """Get the results in a tabular format."""
    my_result = dict()
    for 
    return render_template('results.html', results=my_result)

if __name__ == '__main__':
    app.run(
        host=os.getenv('LISTEN', '0.0.0.0'),
        port=int(os.getenv('PORT', '8080'))
    )
