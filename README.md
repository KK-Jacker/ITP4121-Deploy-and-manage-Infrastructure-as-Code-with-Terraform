# ITP4121-Deploy-and-manage-Infrastructure-as-Code-with-Terraform
create multiple public cloud infrastructure and Kubernetes deployment with Terraform or CDK-TF.

This is GCP branch.

Before deploy please make sure your system have installed following software:

gcloud-cli, mysql client (v5.7 recommanded), terraform, jq

How to deploy:

1. terraform init
2. ./deploy.sh

How to import data to mysql in k8s :

1. kubectl port-forward service/mysql-service 30306:3306
2. ./insert_data_to_mysql.sh

