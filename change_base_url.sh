#!/bin/bash

url_substitute=${1}

sed -i "s#http[^ ]*.ngrok.io#${url_substitute}#g" .env

# take only domain name from https://abc.ngrok.io
IFS='/'
read -ra sprited_url <<< "${url_substitute}"
sed -i "s#[^ ']*.ngrok.io#${sprited_url[2]}#g" 'qlapse/settings.py'
