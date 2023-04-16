# Deploying Stack 

## Prerequisites

To run this tutorial, you will need:

    Terraform installed locally
    AWS Cli is configured locally 
    kubeclt installed locally 
    helm installed locally 


## Create your EKS cluster

Create a new directory for your project.

    mkdir terraform_eks
    cd terraform_eks

Clone the EKS cluster tutorial repo.

    git clone https://github.com/hashicorp/learn-terraform-provision-eks-cluster

    cd learn-terraform-provision-eks-cluster

Run terraform init. 

    terraform init 

Apply the EKS cluster configuration. Respond yes at the prompt to confirm the operation.

    terraform apply

Copy the name of cluster from output 

    terraform show 

## Deploying Prerequisites For kubernetes

### nginx ingresss  

    helm upgrade --install ingress-nginx ingress-nginx \
  --repo https://kubernetes.github.io/ingress-nginx \
  --namespace ingress-nginx --create-namespace

### matrics server 

Add repository

    helm repo add metrics-server https://kubernetes-sigs.github.io/metrics-server/

Install chart

    helm install my-metrics-server metrics-server/metrics-server --version 3.10.0


### intsall helmfile 

    wget -O helmfile_linux_amd64 https://github.com/roboll/helmfile/releases/download/v0.135.0/helmfile_linux_amd64
    chmod +x helmfile_linux_amd64
    mv helmfile_linux_amd64 ~/.local/bin/helmfile


### deploying helm charts of applications

Export the .env

    export $(cat .env| xargs)

now run 

    helmfile sync 




