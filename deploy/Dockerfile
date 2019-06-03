FROM archlinux/base
MAINTAINER yanganto@gmail.com

RUN mkdir /left
RUN pacman -Syu wget tar python python-pip --noconfirm; pacman -Scc --noconfirm
RUN wget https://github.com/yanganto/LEFT/archive/0.0.1.tar.gz
RUN tar zxvf 0.0.1.tar.gz -C /left --strip-components=1; rm 0.0.1.tar.gz
RUN python -m pip install -r /left/requirements.txt

WORKDIR /left
ENTRYPOINT ["python", "/left/left.py"]
CMD []
