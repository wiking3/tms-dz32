<h1> Домашнее задание по теме TMS-DZ32 (Gitlab CI/docker-compose). </h1>

HOST-ы : 192.168.100.115 gitlab-ci 192.168.100.116 gitlab-runner 192.168.100.117 gitlab-node2 (сервер назначения).
Самописное приложение app.py на Flask (слушает порт 5000) разворачивает с БД MySQL через compose.yml файл.
В compose.yml реализовано:
  1. проверяет линтером на синтаксис python-код (с warning пропускает).
  2. делает build по Dockerfile (используя kaniko) и заливает в REGISTRY (https://index.docker.io/v1/)
  3. при deploy - скачиваю с DockerHub имадж и запускаю контейнер "http-server" на 192.168.100.117 gitlab-node2.
  4. приложение  (app.py) слушает порт 192.168.100.117:5000 + MySQL слушает порт 3306.
  5. делается healthcheck через curl -f http://${HOST_IP}:5000/ .


<h2> Результат сборки pipeline в Gitlab CI   </h2>
<img width="1164" height="221" alt="image" src="https://github.com/user-attachments/assets/11df41d4-5d5f-4fa2-8f7c-4396c476d4b0" />


<h2> #Проверка приложения на сервере назначения (192.168.100.117).  </h2>
<img width="1571" height="693" alt="image" src="https://github.com/user-attachments/assets/c7c5e852-8202-462a-a387-fda0e3076c7f" />








<h2> #ПРОВЕРКА БД </h2>
<img width="854" height="585" alt="image" src="https://github.com/user-attachments/assets/c538f815-29b1-4c0b-9425-9ef1ff1811f6" />

