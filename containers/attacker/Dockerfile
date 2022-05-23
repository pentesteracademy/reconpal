FROM kalilinux/kali-rolling:latest

# Installing required tools
RUN apt update \
   && apt install -y python3 python3-pip  metasploit-framework sqlmap screen hydra nmap dirb
   
# ttyd for future plans of an interactive shell
RUN apt-get install build-essential cmake git libjson-c-dev libwebsockets-dev -y\
   && cd /tmp \
   && git clone https://github.com/tsl0922/ttyd.git \
   && cd ttyd && mkdir build && cd build \
   && cmake .. \
   && make && make install \
   && rm -rf /tmp/ttyd

RUN apt-get install docker -y
RUN pip3 install asyncio websockets

# Server scripts for inter module communications
COPY server /root/server

COPY startup.sh /startup.sh

RUN chmod +x /startup.sh 

CMD ["/startup.sh"]
