import math
import time
import boto3
import ec2_manager as ec2_instance_manager
from credentials import REQUEST_QUEUE_URL, WEB_INSTANCE_ID

client = boto3.client('sqs', region_name='us-east-1')

def auto_scale_out_instances():
    """
    Perform auto-upscaling of app-tier instances using queue length of
    request SQS queue, spin up ec2 instances with custom AMI containing
    app-tier code. The number of instances for scaling out is defined as:
    5 messages = 1 instance
    50 messages = 10 instances
    50+ messages = 19 instances
    """

    queue_length = int(client.get_queue_attributes(
        QueueUrl=REQUEST_QUEUE_URL,
        AttributeNames=['ApproximateNumberOfMessages']
        ).get('Attributes').get('ApproximateNumberOfMessages'))

    print('Request queue length: ', queue_length)
    running_instances = ec2_instance_manager.get_running_instances()
    stopped_instances = ec2_instance_manager.get_stopped_instances()
    running_instances.remove(WEB_INSTANCE_ID)
    length_of_running = len(running_instances)
    length_of_stopped = len(stopped_instances)

    if queue_length == 0:
        pass  # Scaling down is handled in app-tier code.

    elif 1 <= queue_length <= 50:
        needed_instances = math.ceil(queue_length / 5)
        if len(running_instances) < needed_instances:
            needed_instances -= length_of_running
            if length_of_stopped >= needed_instances:
                ec2_instance_manager.bulk_start_instances(stopped_instances[:needed_instances])
            else:
                ec2_instance_manager.bulk_start_instances(stopped_instances)
                for _ in range(needed_instances - length_of_stopped):
                    ec2_instance_manager.create_instance()

    else:
        if len(running_instances) < 19:
            needed_instances = 19 - length_of_running
            if length_of_stopped >= needed_instances:
                ec2_instance_manager.bulk_start_instances(stopped_instances[:needed_instances])
            else:
                ec2_instance_manager.bulk_start_instances(stopped_instances)
                for _ in range(needed_instances - length_of_stopped):
                    ec2_instance_manager.create_instance()

if __name__ == '__main__':
    while True:
        print('Starting Auto Scaling')
        auto_scale_out_instances()
        time.sleep(5)
