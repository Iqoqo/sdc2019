![http://dis.co](../../misc/disco-logo.png "Dis.co")

# Lesson (3) - Discofy videos !
## At this point you should have
1. The ability to discofy images 

## Next steps - Discofy a video. Animated shades.
1. Start with `glasses_3.py`
1. Complete function `discofy_video`. We've handled all the `ffmpeg` magic for 
you, including reading and writing video files. 
If you are interested you can find the documentation online. 
1. To run your code:
    ```{r, engine='bash', discofy_video}
    cd <project's root dir> 
    docker run -it -v `pwd`:/home/codelab/ -w /home/codelab/lessons/lesson_3/ discofy:dld.local python glasses_2.py <input video path> <output video path>
    ``` 
1. Test your solution. 
    ```{r, engine='bash', run_pytest}
    cd <project's root dir>
    docker run -it -v `pwd`:/home/codelab/  -w /home/codelab/lessons/lesson_3 discofy:dld.local pytest
    ```
