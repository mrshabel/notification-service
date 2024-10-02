# Architectural and Design Considerations

### Email Notifications

The email service delivers a messages by spinning up a threadpool which contains a fixed number of threads that share the same resources. Deadlock scenarios are prevented using a mutex (lock) to hold the resource in a non-shareable state until it is freed.

Dispatch of the emails to various workers is done asynchronously while the email sending is a synchronous process which is done with an SMTP client.

### InApp Notification

Two implementation strategies are currently proposed with their pros and cons highlighted as well. Polling and Server Push are the mechanisms that can be deployed to ensure efficient delivery of notifications.

-   **Polling**: requests are sent to the server periodically to fetch latest data. A major advantage is that the server does not keep track of connections hence less memory usage. Realtime reads, however, is not assured as there are delays between polling intervals from the client to the server. Connection establishment and handshakes also result in 'unnecessary' usage of bandwidth.
-   **Server Push:** a stateless, bidirectional connection is held between client and server where data is delivered in realtime to the client with minimal bandwidth usage. Suppose _n_ clients are connected to the server, _n_ connections are held hence high memory usage on the server

### Pub/Sub over Direct Publishing to Queue

The initial consideration was to use a direct publisher where messages are forwared to their respective queues for processing. This straight-forward approach however, led to a tightly coupled architecture where event payloads are tied to a particular queue, requiring addititonal code changes if other consumers were to be added. The email, push, and in-app application consumers subscribes to the main notification where they listent to events from different services
