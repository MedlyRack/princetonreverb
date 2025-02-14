import json
from celery import Celery

app = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

from redis import Redis
from celery.bin import worker
from utils import pdf


@app.task
def process_message(message):
    pdf.handler(message)

def start_custom_worker():
    redis_client = Redis(host='localhost', port=6379, db=2)
    pubsub = redis_client.pubsub()
    pubsub.subscribe('new_messages')

    for message in pubsub.listen():
        if message['type'] == 'message':
            data = json.loads(message['data'])
            if data["function"] == "export_to_pdf":
                print("invoke")
                process_message.delay(data)
                # pdf.handler(data)

    w = worker.worker(app=app)
    w.run(loglevel='INFO')

if __name__ == '__main__':
    start_custom_worker()