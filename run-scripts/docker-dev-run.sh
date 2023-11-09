#!/bin/sh
echo "--- Moving to correct directory ---"
cd ..

echo "--- Building docker image ---"
podman build -t drps:dev .

echo "--- Running docker container ---"
podman ps
#docker run --rm -it --name drps-dev -p 8000:8000 -p 8543:8543 -p 5432:5432 drps:dev
podman run --rm -it --name drps-dev \
        -d \
        --network bridge \
        -e TZ=Europe/London \
		-p 5432:5432 \
        -p 50059:50059 \
        -p 8543:8543 \
        -v $PWD/studio-server/hooks/:/var/studio-server/hooks/ \
        -v $PWD/studio-server/database/:/var/studio-server/database/ \
        -v $PWD/studio-server/backups/:/var/studio-server/backups/ \
        -v $PWD/studio-server/jobs/:/etc/cron.d/ \
        drps:dev
podman attach drps-dev
