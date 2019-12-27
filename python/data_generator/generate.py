import boto3 
import botocore 
from tqdm import tqdm
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# Spin up LocalStack server.

QUEUE_NAME = "samplequeue"

def main():
    # any credentials work with localstack
    aws_session = boto3.session.Session()
    sqs_client = aws_session.client(
        service_name='sqs',
        aws_access_key_id='foobar',
        aws_secret_access_key='foobar',
        endpoint_url='http://localhost:4576' # endpoint url for localstack sqs
    )

    current_sqs_queues = sqs_client.list_queues()
    queue_url = "http://localhost:4576/queue/" + QUEUE_NAME

    if "QueueUrls" not in current_sqs_queues or not any(QUEUE_NAME in queue_url for queue_url in current_sqs_queues["QueueUrls"]):
        queue_creation_response = sqs_client.create_queue(QueueName=QUEUE_NAME)
        logger.info(f'Queue created with URL :: {queue_creation_response["QueueUrl"]}')
        queue_url = queue_creation_response["QueueUrl"]
    else:
        logger.info(f'Queue with name {QUEUE_NAME} already present !')

    n = 1000
    logger.info(f'Sending {n} messages to SQS Queue Url :: {queue_url}')

    for i in tqdm(range(n)):
        sqs_client.send_message(QueueUrl=queue_url, MessageBody=f'this is message{i}')
    
if __name__ == '__main__':
    main()