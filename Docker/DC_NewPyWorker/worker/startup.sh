#!/bin/bash
echo "RUN START UP FROM /ETC/PROFILE.D/STARTUP.SH" | tee >> /startup_log.txt

if [ "$DISPLAY_MODE" = "XVFB_DISPLAY" ]; then
  echo "Configurating for XVFB_DISPLAY:99 ..." | tee >> /startup_log.txt
  Xvfb :99 -screen 0 ${LOTUS_DISPLAY_WIDTH}x${LOTUS_DISPLAY_HEIGHT}x${LOTUS_DISPLAY_DEPTH} -nolock -ac &
  xhost +                             #Cho phép mọi người truy cập môi trường hiển thị
  export XAUTHORITY=/root/.Xauthority #Xauthority
  export DISPLAY=:99                  #Môi trường hiển thị được tạo bởi Xvfb:99
  echo $USER  | tee >> /startup_log.txt
  echo $DISPLAY  | tee >> /startup_log.txt
  echo $XAUTHORITY  | tee >> /startup_log.txt
elif [ "$DISPLAY_MODE" = "VNC_DISPLAY" ]; then
  echo "Configurating for VNC_DISPLAY:1 ..."  | tee >> /startup_log.txt
  #change mode for vnc password file
  if [ -f /root/.vnc/passwd ]; then
    chmod 600 /root/.vnc/passwd #Vô cùng quan trọng. Nếu khác 600 thì VNC sẽ không chạy được (Gióng như mật khẩu SSH)
  fi
  if [ "$LOTUS_DISPLAY_VNC_VIEW_ONLY" = "YES" ]; then
    vncserver -geometry ${LOTUS_DISPLAY_WIDTH}x${LOTUS_DISPLAY_HEIGHT} -depth ${LOTUS_DISPLAY_DEPTH} -viewonly -nolock :1 
  else
    vncserver -geometry ${LOTUS_DISPLAY_WIDTH}x${LOTUS_DISPLAY_HEIGHT} -depth ${LOTUS_DISPLAY_DEPTH} -nolock :1
  fi
  xhost +                             #Cho phép mọi người truy cập môi trường hiển thị
  export XAUTHORITY=/root/.Xauthority   #Xauthority
  export DISPLAY=${HOSTNAME}:1          #Môi trường hiển thị được tạo bởi VNC:1
  echo $USER  | tee >> /startup_log.txt
  echo $DISPLAY  | tee >> /startup_log.txt
  echo $XAUTHORITY  | tee >> /startup_log.txt
else
  echo "Invalid value for TIME environment variable"  | tee >> /startup_log.txt
fi

