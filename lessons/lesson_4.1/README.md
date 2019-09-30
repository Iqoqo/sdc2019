![http://dis.co](../../misc/disco-logo.png "Dis.co")

# Lesson (4.1) - Using Disco to Compute an Image Remotely
## At this point you should have
1. The ability to discofy images and videos
2. Basic experience and understanding of how to work with dis.co cli.

## Next steps - Use dis.co cli to perform the imaging processing remotely.
1. Run docker interactively 
    ```{r, engine='bash', interactive_disco}
    cd <project's root dir> 
    docker run -it -v `pwd`:/home/codelab/  -w /home/codelab/lessons/lesson_4.1 discofy:sdc.local
    ```
2. Run the disco command to run the script (glasses_4.py) remotely. 
    ```{r, engine='bash', run_demo}
    disco add --name disco_image --script glasses_4.py --input team.jpg --wait --run --download

    ```
        

 

