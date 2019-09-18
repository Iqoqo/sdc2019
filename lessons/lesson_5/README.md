![http://dis.co](../../misc/disco-logo.png "Dis.co")

# Lesson (5) - Parallel compute
## At this point you should have
1. The ability to discofy images and videos
1. Basic experience and understanding of how to work with dis.co cli.

## Next steps - discofy at scale. Use dis.co cli in order to parallelize the video processing.
1. Run docker interactively 
    ```{r, engine='bash', interactive_disco}
    cd <project's root dir> 
    docker run -it -v `pwd`:/home/codelab/  -w /home/codelab/lessons/lesson_5 discofy:dld.local
    ```
1. Checkout parallel.sh for the useful commands
    1. Use `ffmpeg` to split the video to parts
    1. Invoke `glasses.py` script on all files with disco and download results
    1. `unzip` results
    1. Use `ffmpeg` to stitch results back together
1. You can do one of the following: 
    1. Run the commands one by one from inside the docker.
    2. Execute your script for inside the docker
    3. Execute the script from outside the docker 
        ```{r, engine='bash', run_in_parallel}
        cd <project's root dir>
        docker run -it -v `pwd`:/home/codelab/  -w /home/codelab/lessons/lesson_5 discofy:dld.local sh parallel.sh
        ```
        

 

