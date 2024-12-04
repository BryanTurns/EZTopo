#!/bin/bash

./generatesecret.sh

kubectl apply -f ./secret.yaml

kubectl apply -f ./message-queue/redis-deployment.yaml
kubectl apply -f ./message-queue/redis-service.yaml

kubectl apply -f ./web-server/web-deployment.yaml
kubectl apply -f ./web-server/web-service.yaml

kubectl apply -f ./rest-server/rest-deployment.yaml
kubectl apply -f ./rest-server/rest-service.yaml

kubectl apply -f ./data-processing/video-chopper/chopper-deployment.yaml
kubectl apply -f ./data-processing/video-chopper/chopper-service.yaml

kubectl apply -f ./data-processing/position-predictor/predictor-deployment.yaml
kubectl apply -f ./data-processing/position-predictor/predictor-service.yaml

kubectl apply -f ./data-processing/output-generator/output-deployment.yaml
kubectl apply -f ./data-processing/output-generator/output-service.yaml

kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.0.4/deploy/static/provider/cloud/deploy.yaml
kubectl apply -f ./networking/ingress.yaml