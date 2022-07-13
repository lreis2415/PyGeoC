# Build:
#   > cd PyGeoC
#   > docker build -t <tag> -f docker/Dockerfile .
#
# Usage:
#   > docker pull crazyzlj/pygeoc:v0.3.2
#   > docker run -v /path/to/PyGeoC:/pygeoc crazyzlj/pygeoc:v0.3.2 /pygeoc/examples/ex01_begin_with_pygeoc.py
#
#
# PyGeoC depends on TauDEM.
#  Build TauDEM_ext image first.
#  https://hub.docker.com/r/crazyzlj/taudem_ext
#
FROM crazyzlj/taudem_ext:alpine-openmpi-gdal-py3-latest as builder

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apk/repositories \
    && apk add py3-pip
#  py3-tox py3-wheel py3-setuptools

WORKDIR /pygeoc
COPY . .
# Install pygeoc to .local directory
RUN pip install --user .

FROM crazyzlj/taudem_ext:alpine-openmpi-gdal-py3-latest AS final
# Running PyGeoC requires GDAL, numpy, and matplotlib, so we need to add py3-matplotlib
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apk/repositories \
    && apk add py3-matplotlib

RUN mkdir /root/.local
COPY --from=builder /root/.local/ /root/.local/

# Make sure scripts in .local are usable:
ENV PATH=/root/.local/bin:$PATH

ENTRYPOINT [ "python" ]
CMD ["-c", "import pygeoc; print('PyGeoC v%s installed' % pygeoc.__version__)"]