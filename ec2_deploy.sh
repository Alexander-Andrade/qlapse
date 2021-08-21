#!/bin/sh

ssh -i "qlapse.pem" ubuntu@ec2-54-144-43-192.compute-1.amazonaws.com << EOF
  cd qlapse
  sudo git pull origin master
  pip3 install -r requirements.txt
  python3 manage.py makemigrations
  python3 manage.py migrate
  python3 manage.py collectstatic --noinput
  sed -i 's#http[^ ]*.ngrok.io#https://app.qlapse.com#g'
  sudo systemctl restart nginx
  sudo systemctl restart gunicorn
  exit
EOF
