#!/bin/sh

ssh -i "qlapse.pem" ubuntu@ec2-54-144-43-192.compute-1.amazonaws.com << EOF
  cd qlapse
  sudo git pull origin master
  sudo pip3 install -r requirements.txt
  python3 manage.py makemigrations
  python3 manage.py migrate
  python3 manage.py collectstatic --noinput
  sudo systemctl restart nginx
  sudo systemctl restart gunicorn
  exit
EOF
