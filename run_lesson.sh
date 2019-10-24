#!/bin/bash
setup_env(){
    docker pull iqoqo/discofy:sdc.local
    docker tag iqoqo/discofy:sdc.local discofy:sdc.local
}
run_lesson_1(){
    echo "Running Lesson 1"
    docker run -it -v `pwd`:/home/codelab/ -w /home/codelab/lessons/lesson_1/ discofy:sdc.local pytest
}
run_lesson_2(){
    echo "Running Lesson 2"
    echo "docker run -it -v `pwd`:/home/codelab/ -w /home/codelab/lessons/lesson_2/ discofy:sdc.local python glasses_2_solution.py team.png team-output.jpg"
    docker run -it -v `pwd`:/home/codelab/ -w /home/codelab/lessons/lesson_2/ discofy:sdc.local python glasses_2_solution.py team.png team-output.jpg
    echo "See your result in lessons/lesson_2/team-output.jpg"
}
run_lesson_3(){
    echo "Running Lesson 3"
    echo "docker run -it -v `pwd`:/home/codelab/ -w /home/codelab/lessons/lesson_3/ discofy:sdc.local python glasses_3_solution.py samsungfun.mp4 discofy-samsungfun.mp4"
    docker run -it -v `pwd`:/home/codelab/ -w /home/codelab/lessons/lesson_3/ discofy:sdc.local python glasses_3_solution.py samsungfun.mp4 discofy-samsungfun.mp4
    echo "See your result in lessons/lesson_3/discofy-samsungfun.mp4"
}
run_lesson_4(){
    echo "Running Lesson 4.1"
    echo "docker run -it -v `pwd`:/home/codelab/  -w /home/codelab/lessons/lesson_4.1 discofy:sdc.local sh disco_add_solution.sh"
    docker run -it -v `pwd`:/home/codelab/  -w /home/codelab/lessons/lesson_4.1 discofy:sdc.local sh disco_add_solution.sh
    echo "See your results in lessons/lesson_4.1/"
}
run_lesson_5(){
    echo "Running Lesson 5"
    echo "docker run -it -v `pwd`:/home/codelab/  -w /home/codelab/lessons/lesson_5 discofy:sdc.local sh parallel_solution.sh"
    docker run -it -v `pwd`:/home/codelab/  -w /home/codelab/lessons/lesson_5 discofy:sdc.local sh parallel_solution.sh
}

#always run this to ensure the environment is latest
setup_env

if [ $# -eq 0 ]
  then
    echo "Please provide the lesson number. (e.g., ./run_lesson.sh 1)"
    exit
fi

if [ "$1" == "1" ]
  then
    run_lesson_1
fi 

if [ "$1" == "2" ]
  then
    run_lesson_2
fi

if [ $1 == 3 ]
  then
    run_lesson_3
fi

if [ $1 == 4 ]
  then
    run_lesson_4
fi

if [ $1 == 5 ]
  then
    run_lesson_5
fi

echo "Lesson Script Finished"
