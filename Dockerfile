FROM python:3.10.11

WORKDIR /project

RUN apt-get update && apt-get install -y git && \
    git clone https://github.com/Kolin136/ShortsBoost_Gemini.git . && \

RUN pip install --no-cache-dir -r pipList.txt

EXPOSE 5000

ENTRYPOINT ["python", "app.py"]

#FROM python:3.10.11
#
#WORKDIR /project
#
#COPY .netrc /root/.netrc
#RUN chmod 600 /root/.netrc
#
#RUN apt update && apt install -y git
#
#RUN git clone https://github.com/Kolin136/ShortsBoost_Gemini.git .
#
#RUN pip install --no-cache-dir -r pipList.txt
#
#EXPOSE 5000
#
#ENTRYPOINT ["python", "app.py"]
