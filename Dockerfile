# Usage:
#   > cd PyGeoC
#   > docker build -t <tag> -f docker/Dockerfile .

# Use TauDEM_ext image,build it first
# taudem_py:V01 is an TauDEM_ext image
FROM taudem_py:V01


# install pip
RUN apk add py3-pip
# make a directory for copyed file
RUN mkdir -p /workfolder
COPY ./PyGeoC /workfolder/PyGeoC
WORKDIR /workfolder/PyGeoC
RUN chmod +x reinstall.sh
# run the install script
RUN sh reinstall.sh