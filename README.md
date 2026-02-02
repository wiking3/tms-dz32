Домашнее задание по теме TMS-DZ32 (Gitlab CI/docker-compose).
HOST-ы : 192.168.100.115 gitlab-ci 192.168.100.116 gitlab-runner 192.168.100.117 gitlab-node2 (сервер назначения).
Самописное приложение app.py на Flask (слушает порт 5000) разворачивает с БД MySQL через compose.yml файл.
В compose.yml реализовано:
  1. проверяет линтером на синтаксис python-код (с warning пропускает).
  2. делает build по Dockerfile (используя kaniko) и заливает в REGISTRY (https://index.docker.io/v1/)
  3. при deploy - скачиваю с DockerHub имадж и запускаю контейнер "http-server" на 192.168.100.117 gitlab-node2.
  4. приложение  (app.py) слушает порт 192.168.100.117:5000 + MySQL слушает порт 3306.
  5. делается healthcheck через curl -f http://${HOST_IP}:5000/ .

Результат : 
root@U22GITLABNODE2:~# docker ps -a
  CONTAINER ID   IMAGE                               COMMAND                  CREATED          STATUS                    PORTS                                                    NAMES
  0dcd13acf4a6   wiking3/tms-dz32:tmsdz32-3a7a3cb2   "python app.py"          35 minutes ago   Up 35 minutes             0.0.0.0:5000->5000/tcp, [::]:5000->5000/tcp              gitlab-runner-app-1
  0552ce851b5f   mysql:8.0                           "docker-entrypoint.s…"   35 minutes ago   Up 35 minutes (healthy)   0.0.0.0:3306->3306/tcp, [::]:3306->3306/tcp, 33060/tcp   gitlab-runner-db-1



<img width="1164" height="221" alt="image" src="https://github.com/user-attachments/assets/11df41d4-5d5f-4fa2-8f7c-4396c476d4b0" />





<br>
<h2> #Проверка приложения на сервере назначения (192.168.100.117).  </h2>
root@U22GITLABNODE2:~# curl -v http://192.168.100.117:5000/
*   Trying 192.168.100.117:5000...
* Connected to 192.168.100.117 (192.168.100.117) port 5000 (#0)
> GET / HTTP/1.1
> Host: 192.168.100.117:5000
> User-Agent: curl/7.81.0
> Accept: */*
> 
* Mark bundle as not supporting multiuse
< HTTP/1.1 200 OK
< Server: Werkzeug/3.0.3 Python/3.12.12
< Date: Mon, 02 Feb 2026 09:01:08 GMT
< Content-Type: text/html; charset=utf-8
< Content-Length: 946
< Connection: close
< 
<!DOCTYPE html>
<html>

<head>
    <!-- <title>INDEX HTML </title> -->
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            margin: 0;
            font-family: Arial, Helvetica, sans-serif;
        }

        .main {
            margin-left: 30px
        }
    </style>
</head>

<body>
    <div class="main">
       
<form action="/contact" method="post" class="form-contact">
<p><label>Ping:  </label><input type="text" name="username" value="" requied />
<p><label>Traceroute: </label><input type="text" name="email"    value="" requied />
<p><textarea name="message" rows=7 cols=40></textarea>
<p><input type="submit" value="Send" />
</form>

<ul>
  <li> Установка</li>
  <li> Первое приложение</li>
  <li> Обратная связь</li>
</ul>
         </div>
        </div>
</body>
* Closing connection 0

#ПРОВЕРКА БД
root@U22GITLABNODE2:~# mysql -u dbuser -p -h 192.168.100.117 -P 3306
Enter password: 
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 92
Server version: 8.0.45 MySQL Community Server - GPL

Copyright (c) 2000, 2025, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> SHOW DATABASES;
+--------------------+
| Database           |
+--------------------+
| domaincheck        |
| information_schema |
| performance_schema |
+--------------------+
3 rows in set (0,00 sec)

mysql> 
