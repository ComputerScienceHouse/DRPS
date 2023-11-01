#!/bin/sh
echo "--- Moving to correct directory ---"
cd ..

echo "--- Building docker image ---"
docker build -t drps:dev .

echo "--- Running docker container ---"
docker run --rm -it --name drps-dev -p 8000:8000 -p 8543:8543 drps:dev
