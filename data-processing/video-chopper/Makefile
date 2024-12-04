VERSION=v1.1.1.1.6
DOCKERUSER=bryanturns

build:
	docker build -f Dockerfile -t eztopo-chopper .

push:
	docker tag eztopo-chopper $(DOCKERUSER)/eztopo-chopper:$(VERSION)
	docker push $(DOCKERUSER)/eztopo-chopper:$(VERSION)
	docker tag eztopo-chopper $(DOCKERUSER)/eztopo-chopper:latest
	docker push $(DOCKERUSER)/eztopo-chopper:latest
