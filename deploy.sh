#!/bin/bash

set -e
set -x

command=$1


build() {
  #docker build --tag cowboys .
  docker-compose build
}

push() {
  #aws lightsail push-container-image --region eu-west-3 --service-name cowboys --label cowboysapp --image cowboys_app:latest
  #aws lightsail push-container-image --region eu-west-3 --service-name cowboys --label cowboysnginx --image cowboys_nginx:latest

}

run() {
  #docker run -p 81:80 cowboys:latest
  docker-compose up
}

case $command in
  test)
    build
    run
    ;;
  push)
    push
    ;;
  *)
    build
    push
  esac



