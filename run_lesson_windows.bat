@echo off

echo %1
IF "%1" == "1" (
    GOTO:run_lesson_1
) 
IF "%1"=="2" (
    GOTO:run_lesson_2
)
IF "%1"=="3" (
    GOTO:run_lesson_3
)
IF "%1"=="4" (
    GOTO:run_lesson_4
)
IF "%1"=="5" (
    GOTO:run_lesson_5
)

docker pull iqoqo/discofy:sdc.local
docker tag iqoqo/discofy:sdc.local discofy:sdc.local
 
:run_lesson_1
    echo "Running Lesson 1" 
   docker run -it -v %cd%:/home/codelab/ -w /home/codelab/lessons/lesson_1/ discofy:sdc.local pytest
GOTO End

:run_lesson_2
    echo "Running Lesson 2"
    docker run -it -v %cd%:/home/codelab/ -w /home/codelab/lessons/lesson_2/ discofy:sdc.local python glasses_2_solution.py team.png team-output.png
    echo "See your result in lessons/lesson_2 folder"
GOTO End
:run_lesson_3
    echo "Running Lesson 3"
    docker run -it -v %cd%:/home/codelab/ -w /home/codelab/lessons/lesson_3/ discofy:sdc.local python glasses_3_solution.py samsungfun.mp4 discofy-samsungfun.mp4
    echo "See your result in lessons/lesson_3 folder"
GOTO End
:run_lesson_4
    echo "Running Lesson 4"
    docker run -it -v %cd%:/home/codelab/  -w /home/codelab/lessons/lesson_4.1 discofy:sdc.local sh disco_add_solution.sh
    echo "See your result in lessons/lesson_4.1 folder"
GOTO End
:run_lesson_5
    echo "Running Lesson 5"
    docker run -it -v %cd%:/home/codelab/  -w /home/codelab/lessons/lesson_5 discofy:sdc.local sh parallel_solution.sh
    echo "See your result in lessons/lesson_2 folder"
GOTO End

:END
