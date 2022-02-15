#!/usr/bin/env bash

create_env_file() {
    touch .env
    echo "EMAIL_HOST_PASSWORD=${EMAIL_HOST_PASSWORD}" >> .env
    echo "VERIFIED_EMAIL_USER=${VERIFIED_EMAIL_USER}" >> .env
}
main(){
    create_env_file
}
main
