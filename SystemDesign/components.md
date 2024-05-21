# Components

This dile lsits down the various components used in the system design.

## Server

This is the webserver which will be used by other microservices to

- send the real-time notifications
- schedule notifications for a future date and time

The notification microservice will be used by different systems which can send different types of requests, each request having a different data transofmations, filtering and delivery channels. Since the endpoint required creates a new resource (notification) on each call, it will be a post request with the following data requirements
```json
{
    "type": "WA", // Type of notification
    "user": 123, // id of user to which the notification should be triggered
    "data": { // data required for the notification
        "alpha": 123,
        "beta": 456,
        "gamma": 789
    },
    "scheduel_at" "2024-05-22T12:05+05:30" // optional parameter to schedule the request 
}
```

To ahndle idempotency of the notifications, each notification can be stored in a table in the databse table named notification which has the following schema

```sql
id BIGINT PRIMARY KEY,
type INT -- Enum of the notification type
data JSONB -- data corresponding to the request object
triggered BOOLEAN -- whether the request is scheuled or not
created_at DATETIME -- self-explanatory
updated_at -- self-explanatory
scheduld_at DATETIME -- in case of scheduled notification, to additionally check if the notification at a given time is scheduled or not
```

To make sure the CRUD queries on this table works fast the following thigs can be used to scale the DB

1. partition the tbale based on notification type
2. Index the table based on notification type and created_at

The server upon recieving the requests and doing all the preliminary checks can push the tasks in the Queue from where the consumers (workers) will consume the task

Furthermore, the incoming request data can be parsed for correctness using serialisation techniques. This will make sure only the notifications with correct data are scheduled

## Queue

This is a typical messaging queue like RabbitMQ, Kafka. This may have different queues depending on the type of the notification to make sure the different notifications are handled by different set of workers and increase in one type of request does not hamper the processing and delivery of other type(s) of notification(s)

Depending on the scale, a managed service or an in-house service can be maintained

## Workers

- This the where the actual code for data transformation, filterting and delivery will be placed. Different business logic for implementing transformation ,filtering based on notification type can be implemented using Factory methods. See `sample_transformation.py` for example. Filtering and delivery logic can be applied in a similar way
- Since different types of notifications will be part of different queues, we can scale the consumers who fetch data from each queue independently. Moreover, we can tweak with the concurrency with which each type of notification gets processed. Since concurrency can be achieved base don the type of notification, we can take into consideration the API rate limits of the delivery channle when tweaking with this number
- To make the system more resilient, we can implement exponential backoff while trying delivery. This can go into the implementation of the exact delivery channel code
- To make sure we do not miss any notification as well as identify if any malformed data comes from any microservice, we can implement a dead letter queue which will store the details of the task in case of an unexpected failure
- This can be implemented using a framework like Celery

## Scheduler

- This component is used to scheule future notifications
- It uses database to store the notifications (persistence and resilience) so that even in case the server goes down the notifications won't be impacted
- It polls the database regularly and fetches the required tasks that need to be scheduled, sends those tasks to the right queue
- It is stateful system. This maintains the last time till which it has processed the task so taht even in case of a down-time, the scheduled notifications may be delivered (perhaps a little off schedule)
- A framework like Celery Beat can be used for this

## Database

This will be used for storing the following details

- user related information so taht users can be contacted
- logging scheduled notifications
- scheduling notification - so that the scheduler is persistent

## Connection Pooling

- Most of the databases have limits to the number of connection taht can be used. To make sure the services are suing the connections wisely and not over-using the connection, a connection pool for the database can be used