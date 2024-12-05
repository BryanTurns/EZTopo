#!/bin/bash

kubectl delete svc/eztopo-rest
kubectl delete svc/eztopo-web
kubectl delete svc/eztopo-chopper
kubectl delete svc/eztopo-predictor
kubectl delete svc/eztopo-output
kubectl delete svc/redis
kubectl delete svc/ingress-nginx-controller --namespace ingress-nginx
kubectl delete svc/ingress-nginx-controller-admission --namespace ingress-nginx

kubectl delete deployment/eztopo-rest
kubectl delete deployment/eztopo-web
kubectl delete deployment/eztopo-chopper
kubectl delete deployment/eztopo-predictor
kubectl delete deployment/eztopo-output
kubectl delete deployment/redis
kubectl delete deployment/ingress-nginx-controller --namespace ingress-nginx

kubectl delete ingress/eztopo-ingress