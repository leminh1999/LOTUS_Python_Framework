FROM selenium/standalone-chrome
ADD . /code
WORKDIR /code
RUN sudo apt update
RUN sudo apt install -y python3-pip
RUN sudo pip3 install -r requirements.txt

#Install Chrome browser
RUN sudo apt install -y google-chrome-stable

#Install VNCSerrver
RUN sudo apt install -y gdm3
RUN sudo apt install -y tightvncserver
RUN sudo apt install -y xfce4-goodies
RUN sudo apt install -y scrot
RUN sudo apt install -y python3-tk
RUN sudo apt install -y python3-dev
# RUN sudo apt install -y xfce4

#Never stop the container
# ENTRYPOINT ["tail", "-f", "/dev/null"]

# CMD ["python", "test.py"]
