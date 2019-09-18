set -x

# split the toy video (3:06 minutes) into 30 seconds parts
ffmpeg -i toy.mp4 -c copy -map 0 -segment_time 00:00:30 -f segment split%03d.mp4

# run the glasses disco on the cloud and wait for compute to finish
disco add --name parallel_video --script glasses_5.py --wait --run --download --input "split*mp4"

# unzip results
cd *parallel_video/results &&
for f in `ls *.zip`; do unzip -o $f; done

# write the parts to a manifest
rm -f manifest.txt;
for f in `ls *.mp4`; do echo "file '$f'" >> manifest.txt; done

# stitch back the video
ffmpeg -f concat -safe 0 -i manifest.txt -c copy discofy_toy.mp4

# move back the result to the lesson dir
mv discofy_toy.mp4 ../..

# go back home
cd ../..
 
