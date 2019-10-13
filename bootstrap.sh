#!/usr/bin/env bash

# installing latest release of ansible 

apt-add-repository --yes ppa:ansible/ansible && \
apt-get update && \
apt-get install ansible -y
