# Notification Event Bus

Python's Rabbitmq client, `pika` is synchronous and blocking by default for consumers since they need to be kept alive throughout the lifespan of the application. The event bus, however, consumes message from all subscribed publishers, hence the need to be online. To make this possible, a new thread is created for the event bus to run on while communicating with the main application.

The initial consideration was to use a threadpool for both threads to access the same resources but the downside experienced was that the event bus held one thread constantly for its operation, hence the purpose of the threadpool was defeated. With a separate thread for the event bus, the problem stated above will be resolved.

Communication between the main thread and event thread was challenging in initial stages after the application was crashing on restarts since both threads don't communicate. To ensure this happens, python's `Event` method from its `theading` module will be used to keep references and send synchronization signals between the threads. [Reference](https://www.pythontutorial.net/python-concurrency/python-threading-event/ "An implementation of threading Event")
