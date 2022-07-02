#!/bin/bash

set -e
set -x

command=$1


build() {
  docker build --tag cowboys .
}

push() {
  aws lightsail push-container-image --region eu-west-3 --service-name cowboys --label cowboys --image cowboys:latest
}

run() {
  docker run -p 81:80 cowboys:latest
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



