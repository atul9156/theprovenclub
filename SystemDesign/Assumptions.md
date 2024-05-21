# Assumptions

- It is assumed that the notifications and the data required with it are generated from different services. These services then contact the notification service for processing the data and sending out the notification

- Transformation/filtering etc are handled at the level of notifications microservice. The transformation/filtering happens based on the `type` of notification being triggered. This type will be required while creating the notification

- It is assumed that the notifications may of may not happen in real-time. Hence, there is also a provision of scheduling the notifications for  afuture time

- It is assumed that there are a number of channels where the notifications may go through