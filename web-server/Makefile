VERSION=v1.1.1.1.7
DOCKERUSER=bryanturns

build:
	docker build -f Dockerfile -t eztopo-web .

push:
	docker tag eztopo-web $(DOCKERUSER)/eztopo-web:$(VERSION)
	docker push $(DOCKERUSER)/eztopo-web:$(VERSION)
	docker tag eztopo-web $(DOCKERUSER)/eztopo-web:latest
	docker push $(DOCKERUSER)/eztopo-web:latest
