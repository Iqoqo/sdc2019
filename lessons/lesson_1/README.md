![http://dis.co](../../misc/disco-logo.png "Dis.co")

# Lesson (1) - setup your env
## At this point you should have
1. Docker installed on your computer
1. Your favourite IDE (for python)  
1. Python 3.x (preferably 3.7)
1. The code lab's git repo cloned

## Next steps
1. Download docker 
    ```{r, engine='bash', pull_docker}
    docker pull iqoqo/discofy:dld.local
    docker tag iqoqo/discofy:dld.local discofy:dld.local
    ```
1. Run pytests inside the docker container.
    1. The docker does not include the source code, so we'll give it access to 
    the root directory, and map everything to `/home/codelab/` 
    inside the docker 
    ```{r, engine='bash', run_pytest}
    cd <project's root dir> 
    docker run -it -v `pwd`:/home/codelab/ -w /home/codelab/lessons/lesson_1/ discofy:dld.local pytest
    ``` 
