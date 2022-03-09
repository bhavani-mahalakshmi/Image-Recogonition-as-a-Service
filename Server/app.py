import os
import boto3
import base64
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

sqs = boto3.client('sqs', region_name='us-east-1',
                    aws_access_key_id="ACCESS_KEY_ID", 
                    aws_secret_access_key="SECRET_ACCESS_KEY")

queue_url = 'https://sqs.us-east-1.amazonaws.com/051675418934/Input-Image-Queue.fifo'

@app.route('/health-check')
def health_check():
    return "Healthy"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload():
    for uploaded_file in request.files.getlist('file'):
        if uploaded_file.filename:
            with open(uploaded_file.filename, "rb") as image_to_string:
                converted_string = base64.b64encode(image_to_string.read())
                sqs_message_body = {"image_string": converted_string,
                                    "file_name": uploaded_file.filename}
                # Send message to SQS queue.
                sqs.send_message(QueueUrl=queue_url, MessageBody=sqs_message_body, MessageGroupId='messageGroup1')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(
        host=os.getenv('LISTEN', '0.0.0.0'),
        port=int(os.getenv('PORT', '8080'))
    )