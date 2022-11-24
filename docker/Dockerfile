# Dockerfile for Open Source Analog IC Design
# 
# Installed:
#   - Magic
#   - Xschem
#   - Netgen
# 
# 
# References:
#   - Base Image: https://github.com/fcwu/docker-ubuntu-vnc-desktop
#   - Setup Process: https://laygo2-sky130-docs.readthedocs.io/en/main/index.html
#   - Another Laygo2 + Docker: https://gitlab.com/mosaic_group/mosaic_laygo2/laygo2_docker
# 

# FROM ubuntu:20.04
FROM dorowu/ubuntu-desktop-lxde-vnc

# ==============================================================================
# Basic Setup
# ==============================================================================
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=US/Pacific
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 4EB27DB2A3B88B8B
RUN apt update && apt install -yq tzdata build-essential git python3 


# ==============================================================================
# Install Magic
# ==============================================================================
RUN apt install -y m4 tcsh csh libx11-dev tcl-dev tk-dev libcairo2-dev
RUN cd / && git clone git://opencircuitdesign.com/magic
RUN cd /magic && ./configure && make -j8 && make install


# ==============================================================================
# Install Xschem
# ==============================================================================
RUN apt install -y libx11-6 libx11-dev libxrender1 libxrender-dev libxcb1 \
    libx11-xcb-dev libcairo2 libcairo2-dev tcl8.6 tcl8.6-dev tk8.6 \
    tk8.6-dev flex bison libxpm4 libxpm-dev 
RUN cd / && git clone https://github.com/StefanSchippers/xschem.git
RUN cd /xschem && ./configure && make && make install


# ==============================================================================
# Install Netgen
# ==============================================================================
RUN cd / && git clone git://opencircuitdesign.com/netgen
RUN cd /netgen && ./configure && make -j8 && make install


# ==============================================================================
# Install Ngspice
# ==============================================================================
WORKDIR /
RUN apt install -y libxaw7-dev
RUN wget https://sourceforge.net/projects/ngspice/files/ng-spice-rework/37/ngspice-37.tar.gz \
    && tar -zxvf ngspice-37.tar.gz
WORKDIR /ngspice-37
RUN mkdir release && cd release \
    && ../configure --with-x --enable-xspice --enable-cider \
    --enable-openmp --with-readlines=yes --disable-debug \
    && make -j8 && make install


# ==============================================================================
# Install SKY130-PDK
# ==============================================================================
WORKDIR /
RUN git clone https://github.com/google/skywater-pdk
WORKDIR /skywater-pdk
RUN git submodule init libraries/sky130_fd_io/latest \
    && git submodule init libraries/sky130_fd_pr/latest \
    && git submodule update && make timing -j all


# ==============================================================================
# Install OpenPDKs
# ==============================================================================
WORKDIR /
RUN git clone git://opencircuitdesign.com/open_pdks
WORKDIR /open_pdks
RUN ./configure --enable-sky130-pdk=/skywater-pdk
RUN make -j8 && make install


# ==============================================================================
# Configure Magic and Xschem to work with SKY130
# ==============================================================================
RUN ln -s /usr/local/share/pdk/sky130A/libs.tech/magic/* /usr/local/lib/magic/sys/
RUN echo 'source /usr/local/lib/magic/sys/sky130A.magicrc' >> /root/.magicrc
RUN mkdir /root/.xschem && touch /root/.xschem/xschemrc \
    && echo 'source /usr/local/share/pdk/sky130A/libs.tech/xschem/xschemrc' \
    >> /root/.xschem/xschemrc


# ==============================================================================
# Install Laygo2 and Sky130 support
# ==============================================================================
# RUN git clone https://github.com/niftylab/laygo2_workspace_sky130.git
USER root
RUN apt install -y python3-pip vim eog
COPY . /laygo2_workspace_sky130
WORKDIR /laygo2_workspace_sky130
RUN git submodule init && git submodule update \
    && cd laygo2 && git fetch --all && git pull origin master
RUN python -m pip install pipenv
# for pipenv to recognize the Pipfile
ENV WORKON_HOME=/laygo2_workspace_sky130
RUN pipenv run pip install -r laygo2/requirements.txt \ 
    && pipenv run pip install matplotlib gdspy cairosvg ipython ipykernel \
    && pipenv run pip install -e laygo2
    # && pipenv lock
RUN pipenv run ipython profile create --profile-dir=/laygo2_profile \
    && cp ipython_config_init.py /laygo2_profile/ipython_config.py 
RUN ./mag_set_path.sh
RUN pipenv run ipython laygo2_example/logic/inv.py \
    && pipenv run ipython laygo2_example/logic/tap.py \
    && pipenv run ipython laygo2_example/logic/tinv.py \
    && pipenv run ipython laygo2_example/logic/tinv_small_1x.py \
    && pipenv run ipython laygo2_example/logic/dff.py


# ==============================================================================
# Misc
# ==============================================================================
# To solve https://stackoverflow.com/questions/68036484/qt6-qt-qpa-plugin-could-not-load-the-qt-platform-plugin-xcb-in-even-thou/68058308#68058308
# RUN sudo apt-get install -y '^libxcb.*-dev' libx11-xcb-dev libglu1-mesa-dev \
#     libxrender-dev libxi-dev libxkbcommon-dev libxkbcommon-x11-dev

# add shortcuts to desktop
COPY docker/shortcuts/* /root/Desktop/
COPY docker/lxterminal.conf /root/.config/lxterminal/lxterminal.conf
ENV PDK_ROOT=/usr/local/share/pdk