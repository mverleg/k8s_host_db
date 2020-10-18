
# Reach localhost database from local Kubernetes cluster

This is a small demo for how to set up your configuration so that you can run your database, or any other service, on localhost outside kubernetes.

* Kubernetes: I'll use minikbue for a local kubernetes cluster for testing
* Database: I'll use a simple python script to test reachability.

You will need Python 3, Docker and Kubernetes (i.e. minikube).

## DB on local

* Start the 'mock database' in a separate shell:

    python3 mock_db.py "outside" localhost 1234

* Build the client images:

    docker build -t mock-client -f Dockerfile.client .

## DB in k8s


