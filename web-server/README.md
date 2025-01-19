You can view the frontend by simply running `npm start`.

The frontend waits for a user to upload a video. Once the video is uploaded it is sent to /api/uploadVideo. Then every second the frontend sends a request to /api/checkStatus to display status information to the user. Refer to translateStatus() in App.js to see how the values correspond to the status of the upload.
