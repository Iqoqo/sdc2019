docker images
docker ps -al
docker commit <container id> iqoqo/discofy:sdc.local
docker push iqoqo/discofy:sdc.local
docker tag iqoqo/discofy:sdc.local discofy:sdc.local

