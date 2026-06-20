---
name: message-queue
description: Message queue patterns — RabbitMQ, Redis Streams, SQS. Task queues, pub/sub, dead letter queues, retry logic
domain: development
tags:
- coding
- message
- queue
- software-engineering
- testing
---


## Overview

Message queues decouple producers from consumers, enabling async processing, load leveling, and reliable delivery. This skill covers RabbitMQ, Redis Streams, and AWS SQS patterns for task distribution, pub/sub, dead letter handling, and retry strategies.

## Capabilities

- Design queue topologies (direct, fanout, topic, headers)
- Build task queues with priority and retry logic
- Implement dead letter queues for poison messages
- Use Redis Streams for high-throughput event processing
- Configure SQS with FIFO, standard, and dead letter queues
- Implement distributed work queues with acknowledgments

## When to Use

- Offloading heavy processing from API requests
- Distributing work across multiple workers
- Need reliable delivery with retry on failure
- Building event-driven architectures without Kafka's complexity
- Integrating systems with different throughput characteristics

## When NOT to Use

- Task is about deployment, not development (use deploy skills)
- Task is about code review, not writing (use review skills)
- You need to understand existing code first (use research skills)
- Task is about testing only (use test skills)
- Requirements are unclear (clarify first)
- Task is trivially simple (single line fix)


## Pseudo Code

The message-queue workflow follows a standard pipeline pattern.

Core flow:
```
# message-queue primary flow
input = prepare(raw_data)
result = process(input, config={dead, letter, logic, message, patterns})
validate(result)
deliver(result)
```

Error handling:
```
on error:
  log(error_details)
  retry_with_backoff(max=3)
  if still_failing: alert_and_escalate()
```


### RabbitMQ Task Queue
```python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare queue with DLQ
channel.queue_declare(
    queue='tasks',
    durable=True,               # Survive broker restart
    arguments={
        'x-dead-letter-exchange': 'dlx',
        'x-dead-letter-routing-key': 'tasks.failed',
        'x-message-ttl': 300000,        # 5 min TTL
        'x-max-priority': 10,           # Priority support
    }
)

# Producer
channel.basic_publish(
    exchange='',
    routing_key='tasks',
    body=json.dumps(task),
    properties=pika.BasicProperties(
        delivery_mode=2,        # Persistent
        priority=task['priority'],
    )
)

# Consumer
def callback(ch, method, properties, body):
    try:
        process_task(json.loads(body))
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        # Reject and requeue (with retry limit)
        ch.basic_nack(
            delivery_tag=method.delivery_tag,
            requeue=False       # Goes to DLQ
        )

channel.basic_qos(prefetch_count=1)  # Fair dispatch
channel.basic_consume(queue='tasks', on_message_callback=callback)
channel.start_consuming()
```

### Redis Streams
```python
import redis

r = redis.Redis()

# Producer
r.xadd('tasks', {
    'type': 'resize_image',
    'url': 'https://example.com/img.jpg',
    'width': '800'
})

# Consumer group
r.xgroup_create('tasks', 'workers', id='0', mkstream=True)

# Consumer
while True:
    messages = r.xreadgroup(
        groupname='workers',
        consumername='worker-1',
        streams={'tasks': '>'},
        count=1,
        block=5000
    )
    for stream, msgs in messages:
        for msg_id, data in msgs:
            try:
                process(data)
                r.xack('tasks', 'workers', msg_id)
            except Exception:
                # Message stays pending for retry
                pass

# Claim stale messages from dead consumers
stale = r.xautoclaim('tasks', 'workers', 'worker-2',
                      min_idle_time=300000, start='0-0')
```

### AWS SQS
```python
import boto3

sqs = boto3.client('sqs')

# Send message
sqs.send_message(
    QueueUrl=queue_url,
    MessageBody=json.dumps(task),
    MessageGroupId='user-123',              # FIFO: ordering
    MessageDeduplicationId=task['id'],       # FIFO: dedup
    MessageAttributes={
        'Priority': {'DataType': 'Number', 'StringValue': '1'}
    }
)

# Receive and process
while True:
    response = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=10,
        WaitTimeSeconds=20,             # Long polling
        VisibilityTimeout=30,
    )
    for msg in response.get('Messages', []):
        try:
            process(json.loads(msg['Body']))
            sqs.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=msg['ReceiptHandle']
            )
        except Exception:
            # Visibility timeout expires → message reappears
            pass
```

### Dead Letter Queue Pattern
```python
# DLQ with retry count tracking
def handle_message(msg):
    retry_count = msg.headers.get('x-retry-count', 0)

    try:
        process(msg)
        ack(msg)
    except RetryableError:
        if retry_count < 3:
            # Requeue with incremented retry count
            msg.headers['x-retry-count'] = retry_count + 1
            msg.headers['x-retry-delay'] = 2 ** retry_count * 1000  # Exponential backoff
            requeue(msg)
        else:
            # Max retries → DLQ
            send_to_dlq(msg, reason='max_retries_exceeded')
    except FatalError:
        send_to_dlq(msg, reason='fatal_error')
```

## Common Patterns

| Pattern | Use Case |
|---------|----------|
| **Work queue** | Distribute tasks across N workers |
| **Pub/Sub** | Fan-out to multiple subscribers |
| **Priority queue** | Process urgent tasks first |
| **DLQ** | Isolate failed messages for analysis |
| **Delayed queue** | Schedule future processing |
| **Idempotent consumer** | Handle duplicate delivery safely |
| **Competing consumers** | Scale processing horizontally |

## How to Use

1. Understand the requirement and existing codebase patterns
2. Design the solution with error handling and testability in mind
3. Implement incrementally with tests for each change
4. Verify against expected outcomes (manual and automated)
5. Document usage, edge cases, and integration points
6. Review with team before merging to shared branches

## Red Flags

- **Skipping tests to ship faster**: Untested code breaks in production when you least expect it
- **No error handling in production code**: Unhandled errors crash services and lose user data
- **Hardcoded configuration values**: Hardcoded values prevent environment switching and leak secrets
- **Ignoring security implications**: Missing input validation, auth bypasses, and injection vulnerabilities
- **Over-engineering simple solutions**: Premature abstraction adds complexity without proportional benefit

## Verification

- [ ] Skill output matches expected behavior
