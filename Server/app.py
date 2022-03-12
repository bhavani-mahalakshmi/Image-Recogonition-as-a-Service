import os
import boto3
import base64
import uuid
import json
from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

sqs = boto3.client('sqs', region_name='us-east-1')

input_queue_url = 'https://sqs.us-east-1.amazonaws.com/051675418934/Input-Image-Queue.fifo'
output_queue_url = 'https://sqs.us-east-1.amazonaws.com/051675418934/Output-Image-Queue.fifo'

@app.route('/health-check')
def health_check():
    return "Healthy"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def process():
    try:
        uploaded_file = request.files.get('myfile')
        if uploaded_file.filename:
            identifier = str(uuid.uuid4())
            converted_string = base64.b64encode(uploaded_file.read())
            sqs_message_body = {"encoded_image": str(converted_string, "utf-8"), "unique_id": identifier, "file_name": uploaded_file.filename}
                # Send message to SQS queue.
            sqs.send_message(QueueUrl=input_queue_url, MessageBody=json.dumps(sqs_message_body), MessageGroupId='messageGroup1')
        print("Uploaded file to SQS Input Queue!")
        while True:
            sqs_output = sqs.receive_message(QueueUrl=output_queue_url, AttributeNames=['All'], MaxNumberOfMessages=5, WaitTimeSeconds=1)
            messages = sqs_output.get('Messages', [])
            for item in messages:
                msg_body = json.loads(item.get('Body'))
                if msg_body['unique_id'] == identifier:
                    sqs.delete_message(QueueUrl=output_queue_url, ReceiptHandle=item.get('ReceiptHandle'))
                    return jsonify(msg_body.get('classification'))
    except Exception as e:
        print(e)

if __name__ == '__main__':
    app.run(
        host=os.getenv('LISTEN', '0.0.0.0'),
        port=int(os.getenv('PORT', '8080'))
    )