#!/bin/bash
# cron과 API를 동시에 테스트
service cron start;uvicorn mnist.main:app --host 0.0.0.0 --port 8080 --reload
