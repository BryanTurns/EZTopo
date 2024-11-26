VERSION=v1.1.1.1.1.1.1.1.3
DOCKERUSER=bryanturns

build:
	docker build -f Dockerfile -t eztopo-rest .

push:
	docker tag eztopo-rest $(DOCKERUSER)/eztopo-rest:$(VERSION)
	docker push $(DOCKERUSER)/eztopo-rest:$(VERSION)
	docker tag eztopo-rest $(DOCKERUSER)/eztopo-rest:latest
	docker push $(DOCKERUSER)/eztopo-rest:latest
