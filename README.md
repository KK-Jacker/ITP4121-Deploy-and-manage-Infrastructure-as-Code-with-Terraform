# Clarify the project contribution
The FYP project is used A01 (from Hades Yiu Leung, Chan 200187164) which is based on Azure.
So the variable or environment in the code need to be modified by Hades Yiu Leung, Chan, so the code mostly is pushed to Github by Hades Yiu Leung Chan

the GCP code is created by Ka Kit,Leung  (200084821) (95% of the code),  Hades Yiu Leung, Chan (5% of the code)

the Kerbenetes code is created by Henry Pak Yan, Ho (200017034) (95% of the code), Hades Yiu Leung, Chan (5% of the code)

the Azure code is created by Hades Yiu Leung, Chan, 200187164 (70% of the code) and Hin Chun,Tam  (200241763)  (30% of the code)

code test, debug, report errors to creator and help to fix and optimize code by Hin Chun,Tam  (200241763) (100%)

the cloud environments are registered by Hin Chun,Tam 200241763 (100%)
#ITP4121-Deploy-and-manage-Infrastructure-as-Code-with-Terraform
Create multiple public cloud infrastructure and Kubernetes deployment with Terraform or CDK-TF. 

Before Deploy:

Please upload your domain private key and CA certificate to /Azure/pc_donation/ and modify web.sh in the same directory. If you do not want this project supports HTTPS, please modify the web.sh as well

Please modify /gcp/terraform.tfvars project-id to your google cloud project id

Please make sure your system have installed azure-cli (install with Microsoft guide recommended), cdktf (v0.5.0 recommended), terraform, gcloud-cli, docker, jq and mysql client (v5.7 recommended).
(ref : https://docs.microsoft.com/en-us/cli/azure/install-azure-cli )

Please login to az cli and choose the subscription you want to deploy this project.
Please create an AAD by yourself ( since Azure requires us to prove we are not bot),
then create Face, Text Analytics and Computer Vision to review and acknowledge the terms.
(ref: https://docs.microsoft.com/en-us/azure/cognitive-services/cognitive-services-apis-create-account-cli?tabs=windows#prerequisites )

Run ./deploy.sh to deploy the project.

Run ./destroy.sh to destroy the project.