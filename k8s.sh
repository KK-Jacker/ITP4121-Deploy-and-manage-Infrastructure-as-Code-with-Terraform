STACK_OUTPUT=../ITP4121-azure/stack_output.json && dev_env=../ITP4121-azure/dev.env && \
export VAULT_URL=$(cat $STACK_OUTPUT | jq -r .KeyVaultUri.value) && \
export AZURE_CLIENT_ID=$(cat $STACK_OUTPUT  | jq -r .ServicePrincipalAppId.valu\
e) && \
export AZURE_TENANT_ID=$(cat $STACK_OUTPUT  | jq -r .ServicePrincipalTenantId.v\
alue) && \
export AZURE_CLIENT_SECRET=$(cat $STACK_OUTPUT  | jq -r .ServicePrincipalPasswo\
rd.value) && \
export DB_HOST=$(cat $STACK_OUTPUT | jq -r .MySQLServerHostname.value) && \
export $(grep MYSQL_SERVER_ADMIN_USERNAME= $dev_env) && export DB_USER=${MYSQL_SERVER_ADMIN_USERNAME}@$(cat $STACK_OUTPUT | jq -r .ContainerRegistryAdminUsername.value) && \
export $(grep MYSQL_SERVER_ADMIN_PASSWORD= $dev_env) && export DB_PASS=${MYSQL_SERVER_ADMIN_PASSWORD}
export IMAGE=itp4121project2dev.azurecr.io/itp4121project2-azure:7346df5
export $(grep MYSQL_SCHEMA_NAME= $dev_env) && export DB_NAME=${MYSQL_SCHEMA_NAME}
gcloud container clusters get-credentials $(terraform output -raw kubernetes_cluster_name) --region $(terraform output -raw region)
kubectl create secret generic web-secret --from-literal='IMAGE=itp4121project2dev.azurecr.io/itp4121project2-azure:7346df5' --from-literal='port="3306"' --from-literal='username=${DB_USER}' --from-literal='password=${DB_PASS}' --from-literal='host=mysql-service' --from-literal='tablename=${DB_NAME}'
kubectl create secret docker-registry azurecr-secret --namespace default --docker-username=${AZURE_CLIENT_ID} --docker-password=${AZURE_CLIENT_SECRET} --docker-server=itp4121project2dev.azurecr.io
kubectl apply -f mysql-deployment.yaml,mysql-service.yaml
envsubst < web-deployment.yaml | kubectl apply -f -
kubectl apply -f web-service.yaml
sleep 15
echo k8s pod ip is $(kubectl get service -l app=web -o json | jq -r .items[].status.loadBalancer.ingress[].ip)