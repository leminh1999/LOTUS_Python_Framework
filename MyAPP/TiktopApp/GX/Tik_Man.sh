#!/bin/sh
#0. Tạo network docker
docker network create --driver bridge --subnet=200.200.0.0/16 --ip-range=200.200.200.0/24 --gateway=200.200.0.1 newpyworker_network

#1. Mount thư mục Biz
mount -t cifs //192.168.68.143/home/Biz -o username=meomay22,password=H@@n24687 /mnt/Biz

#2. Tạo thư mục 0_Manager rỗng
rm -rf /Biz/0_Manager
mkdir /Biz/0_Manager

#3. Giải nén Code Manager vào thư mục 0_Manager
tar xzvf /mnt/Biz/RootManager1/code/MasterCode.tar.gz -C /Biz/0_Manager

#4. Chạy chương trình Manager để tạo các container
python3 /Biz/0_Manager/MyAPP/TiktopApp/GX/0_TaskMan.py

#5. Xem screen Manager bằng lệnh screen ls
#6. Để vào screen Manager bằng lệnh screen -r Manager. Sau khi vào có thể nhấn Ctrl+C để thoát screen Manager.
#7. "killall screen" để tắt tất cả các screen đang chạy