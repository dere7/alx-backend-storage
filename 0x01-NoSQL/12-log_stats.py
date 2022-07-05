#!/usr/bin/env python3
"""Python script that provides some stats about Nginx logs stored in MongoDB"""
from pymongo import MongoClient


if __name__ == '__main__':
    with MongoClient() as client:
        nginx = client.logs.nginx
        print(f'{nginx.count_documents({})} logs')
        print('Methods: ')
        methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
        for method in methods:
            count = nginx.count_documents({"method": method})
            print(f'    method {method}: {count}')
        status_checks = nginx.count_documents(
            {"path": "/status", "method": "GET"})
        print(f'{status_checks} status check')
