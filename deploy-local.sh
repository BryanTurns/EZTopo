#!/bin/bash

kubectl apply -f ./message-queue/redis-deployment.yaml
kubectl apply -f ./message-queue/redis-service.yaml

kubectl apply -f ./object-store/minio-deployment.yaml
kubectl apply -f ./object-store/minio-external-service.yaml

kubectl apply -f ./rest-server/rest-deployment.yaml
kubectl apply -f ./rest-server/rest-service.yaml

kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.0.4/deploy/static/provider/cloud/deploy.yaml
kubectl apply -f ./networking/ingress.yaml

