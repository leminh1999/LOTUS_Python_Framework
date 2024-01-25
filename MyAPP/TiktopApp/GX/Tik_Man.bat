rmdir "D:\Database\SynologyDrive\Biz\RootManager1\0_Manager" /s /q
mkdir "D:\Database\SynologyDrive\Biz\RootManager1\0_Manager"

"C:\Program Files\7-Zip\7z" e -y "D:\Database\SynologyDrive\Biz\RootManager1\code\MasterCode.tar.gz" -oD:\Database\SynologyDrive\Biz\RootManager1\0_Manager
"C:\Program Files\7-Zip\7z" x -sdel -y "D:\Database\SynologyDrive\Biz\RootManager1\0_Manager\MASTER_CODE.tar" -oD:\Database\SynologyDrive\Biz\RootManager1\0_Manager
python "D:\Database\SynologyDrive\Biz\RootManager1\0_Manager\MyAPP\TiktopApp\GX\0_TaskMan.py"

ping localhost -n 10