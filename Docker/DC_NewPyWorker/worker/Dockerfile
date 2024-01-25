FROM ubuntu:23.04

################################################################################
###### A. CÁC THÀNH PHẦN ÍT THAY ĐỐI/CẬP NHẬT KHI BUILD LẠI DOCKER        ######
################################################################################
USER root
RUN apt update
RUN apt-get install -yf python3
RUN apt-get install -yf tesseract-ocr
RUN apt-get install -yf curl
RUN apt-get install -yf unzip
RUN apt-get install -y nano vim
RUN apt-get install -y poppler-utils
RUN DEBIAN_FRONTEND=noninteractive apt install -y python3-xlib python3-tk python3-dev
RUN apt install -y xvfb 
RUN apt install -y xserver-xephyr
RUN apt install -y python3-tk
RUN apt install -y python3-dev

#1 là RUN Xvfb :99 -screen 0 1024x768x24 &
#2 là RUN Xvfb :99 -ac &
#RUN export DISPLAY=:99
#Tuy nhiên code khúc này sẽ không có tác dụng vì sau khi tạo image từ docker file. Các biến môi trường sẽ bị mất.

RUN apt install -y --fix-missing python3-pip
#Cài đặt virtualenv
RUN apt install -y python3-pip
RUN pip3 install virtualenv
RUN mkdir /app
COPY requirements.txt /app
WORKDIR /app
RUN virtualenv .venv
RUN /bin/bash -c "source .venv/bin/activate"
RUN apt-get -y install --fix-missing scrot
RUN apt-get -y install --fix-missing tightvncserver
#.Xauthority cần để chạy hiển thị GUI (DISPLAY=:99 hoặc VNC)
RUN touch /root/.Xauthority
RUN chmod 600 /root/.Xauthority
RUN mkdir -p /root/.vnc
#XSEL vaf XCLIP để copy text từ terminal
RUN apt-get install -y xsel
RUN apt-get install -y xclip
#cron (crontab) để chạy lệnh theo thời gian 
RUN apt-get install -y cron
RUN apt-get install -y screen
RUN apt-get install -y iputils-ping
################################################################################
###### B. CÁC THÀNH PHẦN DỄ BUILD LẠI/CẬP NHẬT KHI BUILD LẠI IMAGE        ######
################################################################################
#1. Install Chrome
RUN apt-get install -y --fix-missing dbus-x11
# RUN curl https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o /chrome.deb
ADD ./chrome_Deb_Driver /chrome_Deb_Driver
RUN dpkg -i /chrome_Deb_Driver/chrome.deb || apt-get install --fix-missing -yf
# RUN apt-get -y install libssl1.0-dev

#2. Cập nhật chrome driver
# TẢI CÁC BẢN CHROME DRIVER TẠI: https://chromedriver.chromium.org/downloads
# RUN curl https://chromedriver.storage.googleapis.com/110.0.5481.77/chromedriver_linux64.zip -o /usr/local/bin/chromedriver.zip
# RUN cd /usr/local/bin && unzip chromedriver.zip
RUN cp /chrome_Deb_Driver/chromedriver /usr/local/bin/chromedriver
RUN chmod +x /usr/local/bin/chromedriver
# RUN rm -rf /chrome_Deb_Driver
##########################################
#zzz. Cài đặt các gói python cần thiết
RUN pip install -r requirements.txt

################################################################################
###### C. CHẠY CÁC THIẾT ĐẶT LÚC START UP                                 ######
################################################################################
ADD startup.sh /etc/profile.d/startup.sh
RUN chmod +x /etc/profile.d/startup.sh
ADD vncPass /root/.vnc/passwd
RUN chmod 600 /root/.vnc/passwd

#Remove default timezone
#RUN rm -rf /etc/localtime or sudo unlink /etc/localtime
RUN rm -rf /etc/localtime
#Link timezone to Asia/Saigon
RUN ln -s /usr/share/zoneinfo/Asia/Saigon /etc/localtime

#Giải phóng bộ nhớ
RUN apt-get clean







