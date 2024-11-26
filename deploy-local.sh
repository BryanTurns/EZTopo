#!/bin/bash

# Redis
kubectl apply -f ./message-queue/redis-deployment.yaml
kubectl apply -f ./message-queue/redis-service.yaml
kubectl port-forward svc/redis 6379:6379 &

# Minio
kubectl apply -f ./object-store/minio-deployment.yaml
# kubectl apply -f ./object-store/minio-external-service.yaml
kubectl apply -f ./object-store/minio-service.yaml
kubectl port-forward svc/minio 9000:9000 &

# REST
kubectl apply -f ./rest-server/rest-deployment.yaml
kubectl apply -f ./rest-server/rest-service.yaml
# kubectl port-forward svc/eztopo-rest 5000:5000 & 


# Web
kubectl apply -f ./web-server/web-deployment.yaml
kubectl apply -f ./web-server/web-service.yaml


# Chopper
kubectl apply -f ./data-processing/video-chopper/chopper-deployment.yaml
kubectl apply -f ./data-processing/video-chopper/chopper-service.yaml

# Ingress
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.0.4/deploy/static/provider/cloud/deploy.yaml
kubectl apply -f ./networking/ingress.yaml

