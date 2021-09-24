# SDS_TCPServer

Project repository for "security in distributed systems".

## Description

This project contains a ForkingTCPServer with TLS support, implemented in Python3.

## Prerequisites

* A Unix system to use ForkingTCPServer
* A Public / Private key for TLS

## Usage

Server setup:

* git clone [https://github.com/Tanikai/SDS_TCPServer.git](https://github.com/Tanikai/SDS_TCPServer.git)
* Copy Public / Private key to certs/localhost/cert.pem and certs/localhost/key.pem
* cd src
* python3 server.py

Client connection:

* openssl s_client -connect localhost:9999
