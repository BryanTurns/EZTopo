#!/bin/bash

kubectl apply -f ./message-queue/redis-deployment.yaml
kubectl apply -f ./message-queue/redis-service.yaml
kubectl port-forward svc/redis 6379:6379 &