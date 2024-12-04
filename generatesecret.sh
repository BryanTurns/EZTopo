#!/bin/bash
key=$(cat key.json | base64 -w 0)

echo "apiVersion: v1" > secret.yaml
echo "kind: Secret" >> secret.yaml
echo "metadata:" >> secret.yaml
echo "  name: service-key" >> secret.yaml
echo "data:" >> secret.yaml
echo "  service-account: $key" >> secret.yaml