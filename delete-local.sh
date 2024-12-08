#!/bin/bash

kubectl delete svc/eztopo-rest
kubectl delete svc/eztopo-web
kubectl delete svc/eztopo-chopper
kubectl delete svc/eztopo-predictor
kubectl delete svc/eztopo-output
kubectl delete svc/redis

kubectl delete deployment/eztopo-rest
kubectl delete deployment/eztopo-web
kubectl delete deployment/eztopo-chopper
kubectl delete deployment/eztopo-predictor
kubectl delete deployment/eztopo-output
kubectl delete deployment/redis

kubectl delete ingress/eztopo-ingress

kubectl delete secret/service-key

# kubectl delete ingressClass/nginx
# kubectl delete clusterrole/ingress-nginx
# kubectl delete clusterrole/ingress-nginx-admission
# kubectl delete validatingwebhookconfiguration/ingress-nginx-admission
# kubectl delete namespace/ingress-nginx &
# echo "The ingress-nginx namespace is being deleted in the background. You may not be able to re-deploy for a few minutes while all of it's resources are being deleted. Run kubectl get namespaces to get more information."
