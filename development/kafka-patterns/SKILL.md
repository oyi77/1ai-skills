---
name: kafka-patterns
description: Apache Kafka patterns — producers, consumers, topics, consumer groups, exactly-once semantics, event sourcing
---

## Overview

Apache Kafka is a distributed event streaming platform. This skill covers production-grade patterns for designing topics, building producers/consumers, managing consumer groups, implementing exactly-once semantics, and building event-sourced systems.

## Capabilities

- Design topic hierarchies with partition strategies
- Build idempotent producers with exactly-once delivery
- Implement consumer groups with rebalance handling
- Use Schema Registry for Avro/Protobuf message evolution
- Build event sourcing and CQRS patterns
- Monitor lag, throughput, and consumer health

## When to Use

- Building event-driven microservices
- Need reliable message delivery with ordering guarantees
- Implementing event sourcing or CQRS architectures
- Processing high-throughput streaming data (millions of events/sec)
- Decoupling producers and consumers in distributed systems

## Pseudo Code

### Topic Design
```python
from confluent_kafka.admin import AdminClient, NewTopic

admin = AdminClient({'bootstrap.servers': 'localhost:9092'})

# Create topic with partitioning strategy
topic = NewTopic(
    topic='orders.created',
    num_partitions=12,          # Scale with consumer parallelism
    replication_factor=3,       # HA: survive 2 broker failures
    config={
        'retention.ms': str(7 * 24 * 60 * 60 * 1000),  # 7 days
        'cleanup.policy': 'delete',
        'min.insync.replicas': '2'  # Require 2 ACKs
    }
)
admin.create_topics([topic])
```

### Idempotent Producer
```python
from confluent_kafka import Producer

producer = Producer({
    'bootstrap.servers': 'localhost:9092',
    'enable.idempotence': True,     # Exactly-once producer
    'acks': 'all',                  # Wait for all replicas
    'max.in.flight.requests': 5,    # Throughput + ordering
    'retries': 2147483647,          # Infinite retries (idempotent)
    'linger.ms': 5,                 # Batch for throughput
})

def delivery_callback(err, msg):
    if err:
        print(f'Delivery failed: {err}')
    else:
        print(f'Delivered to {msg.topic()}[{msg.partition()}]@{msg.offset()}')

# Produce with key for partition affinity
producer.produce(
    topic='orders.created',
    key='user-12345',           # Same key → same partition → ordering
    value='{"order_id": "abc", "total": 99.99}',
    callback=delivery_callback
)
producer.flush()
```

### Consumer Group
```python
from confluent_kafka import Consumer, KafkaError

consumer = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'order-processor',
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': False,      # Manual commit for exactly-once
    'isolation.level': 'read_committed',  # Read only committed messages
})

consumer.subscribe(['orders.created'])

while True:
    msg = consumer.poll(1.0)
    if msg is None:
        continue
    if msg.error():
        if msg.error().code() == KafkaError._PARTITION_EOF:
            continue
        raise KafkaException(msg.error())

    try:
        process_order(msg.value())      # Idempotent processing
        consumer.commit(msg)            # Commit after success
    except Exception as e:
        handle_failure(msg, e)          # Retry or DLQ
```

### Event Sourcing Pattern
```python
# Event store topic design
events = {
    'orders.events': {
        'partitions': 12,
        'key': 'order_id',           # Events for same order in same partition
        'schema': {
            'event_type': 'string',   # OrderCreated, OrderPaid, OrderShipped
            'aggregate_id': 'string',
            'timestamp': 'long',
            'payload': 'object',
            'version': 'int'          # Optimistic concurrency
        }
    }
}

# Rebuild state by replaying events
def rebuild_order_state(order_id):
    state = {}
    for msg in consume_partition('orders.events', key=order_id):
        event = deserialize(msg)
        if event['event_type'] == 'OrderCreated':
            state = event['payload']
        elif event['event_type'] == 'OrderPaid':
            state['paid'] = True
        elif event['event_type'] == 'OrderShipped':
            state['shipped'] = True
            state['tracking'] = event['payload']['tracking']
    return state
```

### Schema Registry
```python
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer

schema_registry = SchemaRegistryClient({'url': 'http://localhost:8081'})

order_schema = '''
{
    "type": "record",
    "name": "Order",
    "fields": [
        {"name": "order_id", "type": "string"},
        {"name": "user_id", "type": "string"},
        {"name": "total", "type": "double"},
        {"name": "items", "type": {"type": "array", "items": "string"}}
    ]
}
'''

serializer = AvroSerializer(schema_registry, order_schema)
```

## Common Patterns

| Pattern | Use Case |
|---------|----------|
| **Transactional outbox** | Write DB + publish atomically |
| **Event sourcing** | Rebuild state from event log |
| **CQRS** | Separate read/write models |
| **Dead letter queue** | Handle poison messages |
| **Compacted topics** | Latest value per key (changelog) |
| **Fan-out** | Multiple consumers on same topic |
| **Exactly-once** | Idempotent producer + read_committed consumer |
