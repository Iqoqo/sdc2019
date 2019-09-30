docker images
docker ps -al
docker commit <container id> iqoqo/discofy:sdc.local
docker push
docker tag iqoqo/discofy:sdc.local discofy:sdc.local

