# Pull base image from Docker Hub
FROM docker.io/allebb/studio-server:latest

# Install resolve
WORKDIR /app
RUN wget -q https://csh.rit.edu/~atom/resolve/resolve.deb
RUN dpkg -i resolve.deb
RUN rm resolve.deb

# Install base apt packages
RUN apt-get -yq update
RUN apt install -yq screen python3-pip


# Copy pip requirements and install
COPY ./requirements.txt requirements.txt
RUN python3 -m pip install --no-cache-dir -r requirements.txt

# Copy everything over
COPY . .

RUN apt install -yq libglu1-mesa-dev librsvg2-2 librsvg2-dev librsvg2-common ocl-icd-opencl-dev \
    libdbus-1-3 libc-bin  libxkbcommon-x11-0

ENV RESOLVE_SCRIPT_API="/opt/resolve/Developer/Scripting/"
ENV RESOLVE_SCRIPT_LIB="/opt/resolve/libs/fusion/fusionscript.so"
ENV PYTHONPATH="$PYTHONPATH:$RESOLVE_SCRIPT_API/Modules/"

# Entrypoint is the Studio Server boot script
#ENTRYPOINT ["./run-scripts/boot-script.sh"]
#ENTRYPOINT ["cat", "/boot.sh"]
ENTRYPOINT ["bash"]