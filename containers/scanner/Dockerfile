FROM kalilinux/kali-rolling:latest

# Installing required tools
RUN apt update \
   && apt install -y python3 python3-pip nmap dirb nikto hydra sqlmap


RUN pip3 install asyncio websockets

# Server scripts for inter module communications
COPY server /root/server

COPY scan /bin/ 

COPY startup.sh /startup.sh

RUN chmod +x /startup.sh \
    && chmod +x /bin/scan

CMD ["/startup.sh"]
