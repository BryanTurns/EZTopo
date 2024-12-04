VERSION=v1.1.1.1.4
DOCKERUSER=bryanturns

build:
	docker build -f Dockerfile -t eztopo-output .

push:
	docker tag eztopo-output $(DOCKERUSER)/eztopo-output:$(VERSION)
	docker push $(DOCKERUSER)/eztopo-output:$(VERSION)
	docker tag eztopo-output $(DOCKERUSER)/eztopo-output:latest
	docker push $(DOCKERUSER)/eztopo-output:latest
