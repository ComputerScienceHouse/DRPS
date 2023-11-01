# Pull base image from Docker Hub
FROM allebb/studio-server:latest

# Install base apt packages
WORKDIR /app
RUN apt-get -yq update
RUN apt install -yq screen python3-pip

# Copy pip requirements and install
COPY ./requirements.txt requirements.txt
RUN python3 -m pip install --no-cache-dir -r requirements.txt

# Copy everything over
COPY . .

# Entrypoint is the Studio Server boot script
ENTRYPOINT ["./run-scripts/boot-script.sh"]
#ENTRYPOINT ["cat", "/boot.sh"]
#ENTRYPOINT ["sh"]