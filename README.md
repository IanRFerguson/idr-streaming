# Real-Time Entity Resolution

The goal of this project is to design a system that can handle the following:
* User PII enters the system (name, address, phone number, email)
* We store the data in a transactional database
* Kafka passes each new record to an IDR service
* This service infers if the individual exists in the system already or not
  * If so, it links the records together

## Design
### Kafka
We're running Kafka out of the box using the official Apache image. 

You can run this service independently with `docker compose up kafka`.

### Python Services

Both of our Python services use the same Docker image with different entrypoints.

```
# This service creates the mock PII
idr-producer:
    build:
      context: .
      dockerfile: devops/Dockerfile
    entrypoint: ["python", "src/producer.py"]
    volumes:
      - .:/app
    env_file:
      - .env
    depends_on:
      kafka:
        condition: service_healthy

# This service runs our IDR process
idr-consumer:
    build:
        context: .
        dockerfile: devops/Dockerfile
    entrypoint: ["python", "src/consumer.py"]
    volumes:
        - .:/app
    env_file:
        - .env
    depends_on:
        kafka:
        condition: service_healthy
```

They rely on the Kafka broker to be healthy - if it goes down, the streaming process will break.

#### Producer
The producer uses `Faker` to generate mock PII for our purposes. It writes the PII to a local Postgres database, and artificially grabs an existing record one in `n` times (to mock a return user entering the system).



#### Consumer