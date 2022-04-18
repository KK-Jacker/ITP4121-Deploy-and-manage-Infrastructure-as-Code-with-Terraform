# ITP4121-Deploy-and-manage-Infrastructure-as-Code-with-Terraform
 create multiple public cloud infrastructure and Kubernetes deployment with Terraform or CDK-TF.
 This is Aure branch.

Before Deploy

Please make sure your system have installed azure-cli (install with Microsoft guide recommended), cdktf (v0.5.0 recommended), docker, jq and mysql client (v5.7 recommended).
(ref : https://docs.microsoft.com/en-us/cli/azure/install-azure-cli )
Please login to az cli and choose the subscription you want to deploy this project.
Please create an AAD by yourself ( since Azure requires us to prove we are not bot),
then create Face, Text Analytics and Computer Vision to review and acknowledge the terms.
(ref: https://docs.microsoft.com/en-us/azure/cognitive-services/cognitive-services-apis-create-account-cli?tabs=windows#prerequisites )

How to deploy?

run belows commands:
1. cdktf get
2. npm i
3. tsc
4. ./deploy.sh


How to import data to mysql in k8s :

1. kubectl port-forward service/mysql-service 30306:3306
2. ./insert_data_to_mysql.sh

How to destroy?

run this commands: cdktf destroy

