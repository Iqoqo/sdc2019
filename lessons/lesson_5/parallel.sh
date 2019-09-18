set -x

# split the toy video (3:06 minutes) into 30 seconds parts
ffmpeg -i toy.mp4 -c copy -map 0 -segment_time 00:00:30 -f segment split%03d.mp4

# run the glasses disco on the cloud and wait for compute to finish
# the --input accepts wildcard and will invoke the glasses_5.py script per input file
# Hint: you can use the --run --wait and --download flags in the add command


# cd to results dir
cd *parallel_video/results &&

# unzip results
# either manually or in this script

# ffmpeg can concat video files to one video.
# you'll first need to create a manifest.txt file with the following format:
#   file '<part_1>'
#   file '<part_2>'
#   file '<part_3>'
#   ...
# and then stitch back the video
ffmpeg -f concat -safe 0 -i manifest.txt -c copy <output_file_name.mp4>

# move back the result to the lesson dir
mv <output_file_name.mp4> ../..

# go back home
cd ../..
 
