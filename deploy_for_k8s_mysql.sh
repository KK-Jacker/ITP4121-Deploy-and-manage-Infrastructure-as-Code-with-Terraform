terraform apply --auto-approve
terraform output -state=terraform.ITP4121-Project.tfstate -json > stack_output.json
STACK_OUTPUT=../ITP4121-azure/stack_output.json && \
export VAULT_URL=$(cat $STACK_OUTPUT | jq -r .KeyVaultUri.value) && \
export AZURE_CLIENT_ID=$(cat $STACK_OUTPUT  | jq -r .ServicePrincipalAppId.value) && \
export AZURE_TENANT_ID=$(cat $STACK_OUTPUT  | jq -r .ServicePrincipalTenantId.value) && \
export AZURE_CLIENT_SECRET=$(cat $STACK_OUTPUT  | jq -r .ServicePrincipalPassword.value) && \
export IMAGE=$(cat $STACK_OUTPUT  | jq -r .DockerImageName.value)
gcloud container clusters get-credentials $(terraform output -raw kubernetes_cluster_name) --region $(terraform output -raw region)
kubectl create secret generic web-secret --from-literal='port=3306' --from-literal='username=itp4121project' --from-literal='password=123qweASD' --from-literal='host=mysql-service' --from-literal='tablename=default_schema'
kubectl create secret docker-registry azurecr-secret --namespace default --docker-username=${AZURE_CLIENT_ID} --docker-password=${AZURE_CLIENT_SECRET} --docker-server=itp4121project2dev.azurecr.io
kubectl apply -f mysql-deployment.yaml,mysql-service.yaml
envsubst < web-deployment.yaml | kubectl apply -f -
kubectl apply -f web-service.yaml
sleep 60
echo k8s pod ip is $(kubectl get service -l app=web -o json | jq -r .items[].status.loadBalancer.ingress[].ip)