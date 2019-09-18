![http://dis.co](../../misc/disco-logo.png "Dis.co")

# Lesson (4) - Disco cli !
## At this point you should have
1. The ability to Discofy images and videos

## Next steps - detour. Get to know disco cli.
1. Run docker interactively 
    ```{r, engine='bash', interactive_disco}
    cd <project's root dir> 
    docker run -it -v `pwd`:/home/codelab/  -w /home/codelab/lessons/lesson_4 discofy:dld.local
    ```
1. `disco` is a command line interface to the Dis.co cloud backend 
1. We made sure you are logged in so you don't have to
(**NOTICE** that everyone here are logged in with the same user and password). 
Explore disco cli options 
    ```
    disco -h
    ```
1. Edit `hello_disco.py` to print something else than `Hello Disco` if you want
or do some kind of calculation. Then run it on disco cloud. 
    ```
    disco add --name <your_job_name> --script <script> --wait --run
    ```
1. Notice your job_id `jobId: [xxxxxxxxxxxxxx]`
1. Download results: 
    ```
    disco view --job <your_job_id> --download
    ``` 
1. `ls` to locate the downloaded results and unzip them
1. The downloaded artifacts will be found in `<job_id>-<job_name>/results/<task_id>.zip`
1. see the content of the `stdout.txt` file. 
