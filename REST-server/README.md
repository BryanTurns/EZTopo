Routes:

/api/uploadVideo: recieves a file from the frontend and uploads it to the cloud and pushes the UUID to the chopper-queue.
/api/getOutputVideo: recieves a UUID from the frontend and downloads the corresponding output video from the cloud and sends it back.
/api/checkStatus: recieves a UUID from the frontend and returns a integer corresponding to the current status of the processing.
