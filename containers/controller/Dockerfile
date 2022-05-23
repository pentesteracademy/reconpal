FROM ubuntu:20.04

# Installing requirements
RUN apt-get update \
    && apt-get install python3 python3-pip supervisor sqlite3 vim libmediainfo-dev -y
# Installing required tools
RUN pip3 install shodan python-telegram-bot websocket-client openai google-cloud-speech==2.12.0 google-cloud-storage==2.1.0 pymediainfo==5.1.0

# Copy logic scripts to container
COPY app.py /

COPY handler.py /

COPY DateFilter.py /

COPY startup.sh /

RUN chmod +x /startup.sh

# Run ReconPal logic
CMD ["/startup.sh"]
