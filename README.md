
# *[UNDER CONSTRUCTION]*
# Reach localhost database from local Kubernetes cluster

This is a small demo for how to set up your configuration so that you can run your database, or any other service, on localhost outside Kubernetes.

* Kubernetes: I'll use minikube for a local Kubernetes cluster for testing
* Database: I'll use a simple python script to test reachability.

## Preparation

* You will need Python 3, Docker and Kubernetes (i.e. minikube). Find online how to install them if you don't have them already.

* Optional: if you want to start with a clean cluster (**this deletes the old one!!**), type:

      minikube delete
      minikube start --vm-driver=docker

* We need to do this step so that minikube will be able to use the Docker images we are going to build (without us having to publich them in a registry):

      eval $(minikube docker-env)
    
  You will need to do this for each new terminal.

* When using minikube, in another terminal with admin privileges, start

      minikube tunnel

## Start services

Both if the database is inside the service, and if it's outside, you need these steps:

* Build the Docker images (with these exact names):

      docker build -t mock-client -f Dockerfile.client .
      docker build -t mock-db -f Dockerfile.mockdb .

* Deploy them to minikube:

      kubectl apply -f mock-services.yml

* To verify that it's running,

      kubectl get services
    
   should show `mock-client-service` with an external ip (but not the one we'll use).

You can continue at the next section (DB outside) or the one after that.

## DB on local (outside cluster)

For the situation that the database is running on the local machine and you want to reach it from Kubernetes, follow these steps.

(This will also start a database inside Kubernetes, because I did not want to make two versions of the files; you can ignore it).

* Start the 'mock database' in a separate shell:

      python3 mock_db.py "outside" localhost 3005

## DB in k8s

The database inside Kubernetes was already started by `kubectl apply` before. You can verify if that is the case with

    kubectl get pods
    
it should show `inside-db` as Running

    kubectl get services

it should show `mock-client-service` with an external ip (but not the one we'll use), and `inside-db-service` with only an internal ip (it is not exposed).

## Testing

To test, use

    minikube service mock-client-service

The url you get is the cluster ip (`minikube ip`) and the `LoadBalancer` port from `mock-services.yml`.

From the mock client (running inside Kubernetes), try to connect to the database you chose.

For a database **inside** Kubernetes (change the IP):

    http://1.2.3.4:30001/?host=inside-db-service&port=2006

* The first ip and port are from `minikube service mock-client-service`.
* The host to connect is the name of the inside database service, `inside-db-service`.
* The port is specified in `mock-services.yml` as 2006 (only reachable internally). Note that the database runs at 2005 in its container, but we have remapped it for demonstration purposes.

For a database **outside** Kubernetes, which we started on `localhost:3005` before, 

    http://1.2.3.4:30001/?host=outside-db-service&port=3006
    
* The first ip and port are again from `minikube service mock-client-service`.
* The host to connect to is the name of the outside database service, `outside-db-service`.
* The port is specified in `mock-services.yml` as 3006. It is different from the outside port (3005) for demonstration purposes - it can be the same.

## Hints

* To check connectivity, see [Host Access](https://minikube.sigs.k8s.io/docs/handbook/host-access/).
* How to make minikube ingress [info](https://kubernetes.io/docs/tasks/access-application-cluster/ingress-minikube/).

