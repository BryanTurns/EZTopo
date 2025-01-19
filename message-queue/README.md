Currently the message queue is implemented via Redis. The easiest way to run this "locally" is to run it as a kubernetes deployment then port forward the service.
There are three queues:

- chopper-queue
- predictor-queue
- output-queue
