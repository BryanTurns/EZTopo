Breakdown of data flow:

1. video-chopper sees theres a new video-id in the chop-video queue and chops up the video into frames. Each frame is then stored as "video-id-frame#.jpg" and added to the predict-position queue.
2. position-predictor takes each frame from the predict-position queue and generates a pair of coordinates.
3. output-generator then takes all the coordinates for a given video-id and generates a final image with the topology overlayed. MECHANISM FOR FINDING OUT ALL FRAMES COMPLETE UNKOWN.
