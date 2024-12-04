VERSION=v1.1.1.1.1.6
DOCKERUSER=bryanturns

build:
	docker build -f Dockerfile -t eztopo-predictor .

push:
	docker tag eztopo-predictor $(DOCKERUSER)/eztopo-predictor:$(VERSION)
	docker push $(DOCKERUSER)/eztopo-predictor:$(VERSION)
	docker tag eztopo-predictor $(DOCKERUSER)/eztopo-predictor:latest
	docker push $(DOCKERUSER)/eztopo-predictor:latest
