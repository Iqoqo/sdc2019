![http://dis.co](../../misc/disco-logo.png "Dis.co")

# Lesson (6) - discomp
## At this point you should have
1. The ability to discofy images and videos
1. Basic experience and understanding of how to work with dis.co cli.
1. Use dis.co at scale

## Next steps - scaling natively from within the code with `discomp`
In this lesson we are going to do something a bit different. 
We are going to do face detection analytics on youtube videos.
1. Checkout `you_tube_face_detection.py`. `handle_url` is the entry point for 
handling a single url including downloading and analyzing video
1. There are 4 version of the `main` function:
    1. `main_single_thread` - a single threaded main
    1. `main_mp` - a multi process version running locally on your computer
    1. `main_discomp` - a multi process version where each process handles a single video remotely on disco cloud
    1. `main_discomp_mp` - a multi process version where each process handles multiple videos (in parallel) remotely on disco cloud
1. Choose one main and update the code. In order to run it. 
    ```{r, engine='bash', interactive_disco}
    cd <project's root dir> 
    docker run -it -v `pwd`:/home/codelab/  -w /home/codelab/lessons/lesson_6 discofy:dld.local python you_tube_face_detection.py <number_of_urls_to_handle>
    ```