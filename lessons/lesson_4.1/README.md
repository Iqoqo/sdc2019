![http://dis.co](../../misc/disco-logo.png "Dis.co")

# Lesson (4.1) - Using Disco to Perform Image Processing

## At this point you should have
1. The ability to discofy images and videos
2. Basic experience and understanding of how to work with dis.co cli.

## Next steps - Use dis.co cli to perform the imaging processing remotely.

1. Run docker interactively 
    ```{r, engine='bash', interactive_disco}
    cd <project's root dir> 
    docker run -it -v `pwd`:/home/codelab/  -w /home/codelab/lessons/lesson_4.1 discofy:sdc.local
    ```
2. Run the disco command to run the script (`glasses_4.py`) remotely. Upon success, the script will download the results and save in the `<job id>-<job name>` folder in the current directory.  
    ```{r, engine='bash', run_demo}
    disco add --name disco_image --script glasses_4.py --input team.jpg --wait --run --download

    ```
3. Extract the zip file inside the `<job id>-<job name>'/results` folder. After extracted, there will be 3 files inside the zip folder:

    ```
    IqoqoTask.stderr.0.txt - the error output       
    IqoqoTask.stdout.0.txt - the stdout output
    disco_team.jpg - the result image
    ```
    
