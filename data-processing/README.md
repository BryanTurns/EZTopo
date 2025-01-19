Notes:

- Each service uses a thread pool to enhance parallelism
- Running each component locally may be difficult.

Breakdown of data flow:

1. First the video-chopper sees a new UUID on the chopper-queue and pops it. Then it chops the video up into frames and stores them on the cloud bucket. Once that is done the UUID is pushed onto the predictor-queue.
2. The position-predictor then sees a new UUID on the predictor queue and pops it. Then it runs the Ultralytics YOLO pose model on each frame and creates a json file with the hip position of the highest person in the frame (in order to track the climber and not the belayer) and stores that in the cloud. Once that is done the UUID is pushed onto the output-queue. NOTE: position-predictor uses Ultralytics which has a lot of dependencies. If the code isn't working it's probably an issue with that.
3. The output queue sees a new UUID on the output-queue and pops it. Then it takes the position json and the original video from the cloud and draws the positions as a line on each frame of the original video. It then sends the new video to the cloud before setting the status of the UUID to complete. NOTE: output-generator relies on H264 encoding and ffmpeg requries this to be downloaded seperately. That is why there are the .so/.dll files.
