# Binary build for DaVinci Resolve
FROM docker.io/debian:12-slim AS build_resolve

WORKDIR /build

# Install dependencies
RUN apt-get -yqq update
RUN apt install -yqq ocl-icd-opencl-dev fakeroot xorriso wget unzip

# Install libssl1.1 separately
RUN wget -q http://archive.ubuntu.com/ubuntu/pool/main/o/openssl/libssl1.1_1.1.0g-2ubuntu4_amd64.deb
RUN dpkg -i libssl1.1_1.1.0g-2ubuntu4_amd64.deb

# Configure install links
ARG RESOLVE_LINK=https://csh.rit.edu/~atom/resolve/resolve_linux.zip
ARG RESOLVE_PKG_LINK=https://csh.rit.edu/~atom/resolve/make_deb.sh

# Download source files
RUN wget -q $RESOLVE_LINK
RUN wget -q $RESOLVE_PKG_LINK

# Process and install
RUN unzip resolve_linux.zip
RUN chmod 777 make_deb.sh
RUN ./make_deb.sh DaVinci_Resolve_18.6.2_Linux.run
RUN mv davinci-resolve*amd64.deb resolve.deb



# Pull base image from Docker Hub
FROM docker.io/allebb/studio-server:latest

# Install resolve
WORKDIR /app
COPY --from=build_resolve /build/resolve.deb .
RUN dpkg -i resolve.deb

# Install base apt packages
RUN apt-get -yq update
RUN apt install -yq screen python3-pip

# Install built binary from previous stage

RUN rm -rf resolvepkg/
# Copy pip requirements and install
COPY ./requirements.txt requirements.txt
RUN python3 -m pip install --no-cache-dir -r requirements.txt

# Copy everything over
COPY . .

# Entrypoint is the Studio Server boot script
#ENTRYPOINT ["./run-scripts/boot-script.sh"]
#ENTRYPOINT ["cat", "/boot.sh"]
ENTRYPOINT ["bash"]