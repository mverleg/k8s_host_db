
# *[UNDER CONSTRUCTION]*
# Reach localhost database from local Kubernetes cluster

This is a small demo for how to set up your configuration so that you can run your database, or any other service, on localhost outside kubernetes.

* Kubernetes: I'll use minikube for a local kubernetes cluster for testing
* Database: I'll use a simple python script to test reachability.

## Preparation

* You will need Python 3, Docker and Kubernetes (i.e. minikube). Find online how to install them if you don't have them already.

* Optional: if you want to start with a clean cluster (**this deletes the old one!!**), type:

      minikube delete
      minikube start --vm-driver=docker

* We need to do this step so that minikube will be able to use the Docker images we are going to build (without us having to publich them in a registry):

      eval $(minikube docker-env)
      
  or on Windows with PowerShell:
  
      eval (minikube docker-env)
    
  You will need to do this for each new terminal.

## DB on local

For the situation that the database is running on the local machine and you want to reach it from kubernetes, follow these steps.

(This will also start a database inside kubernetes, because I did not want to make two versions of the files; you can ignore it).

* Start the 'mock database' in a separate shell:

      python3 mock_db.py "outside" localhost 3005

* Build the Docker images (with these exact names):

      docker build -t mock-client -f Dockerfile.client .
      docker build -t mock-db -f Dockerfile.mockdb .

* Deploy them to minikube:

      kubectl apply -f mock-services.yml




## DB in k8s


## Hints

* To check connectivity, see [Host Access](https://minikube.sigs.k8s.io/docs/handbook/host-access/).
* How to make minikube ingress [info](https://kubernetes.io/docs/tasks/access-application-cluster/ingress-minikube/).

