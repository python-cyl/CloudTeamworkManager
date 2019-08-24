@echo off
@echo 请确认资源文件正常
@echo 请确认数据库服务器已打开

cd CloudTeamworkManager
.\env\Scripts\python.exe manage.py runserver 0.0.0.0:8000

