import os
import boto3
import base64
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

sqs = boto3.client('sqs', region_name='us-east-1')

queue_url = 'https://sqs.us-east-1.amazonaws.com/051675418934/Input-Image-Queue.fifo'

@app.route('/health-check')
def health_check():
    return "Healthy"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload():
    try:
        for uploaded_file in request.files.getlist('file'):
            if uploaded_file.filename:
                converted_string = base64.b64encode(uploaded_file.read())
                sqs_message_body = uploaded_file.filename + ";" + str(converted_string, "utf-8")
                # Send message to SQS queue.
                sqs.send_message(QueueUrl=queue_url, MessageBody=sqs_message_body, MessageGroupId='messageGroup1')
        return redirect(url_for('home'))
    except Exception as e:
        print(e)

@app.route('/results', methods=['GET'])
def results():
    s3_resource= boto3.resource('s3')
    my_bucket = s3_resource.Bucket('imageoutputbucket')
    results = dict()
    for obj in my_bucket.objects.all():
        results[obj.key] = obj.get()['Body'].read().decode('utf-8')
    return render_template('results.html', results=results)

if __name__ == '__main__':
    app.run(
        host=os.getenv('LISTEN', '0.0.0.0'),
        port=int(os.getenv('PORT', '8080'))
    )