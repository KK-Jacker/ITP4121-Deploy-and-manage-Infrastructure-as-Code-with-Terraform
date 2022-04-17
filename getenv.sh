STACK_OUTPUT=stack_output.json && \
export VAULT_URL=$(cat $STACK_OUTPUT | jq -r .KeyVaultUri.value) && \
export AZURE_CLIENT_ID=$(cat $STACK_OUTPUT  | jq -r .ServicePrincipalAppId.valu\
e) && \
export AZURE_TENANT_ID=$(cat $STACK_OUTPUT  | jq -r .ServicePrincipalTenantId.v\
alue) && \
export AZURE_CLIENT_SECRET=$(cat $STACK_OUTPUT  | jq -r .ServicePrincipalPasswo\
rd.value) && \
export DB_HOST=$(cat $STACK_OUTPUT | jq -r .MySQLServerHostname.value) && \
export $(grep MYSQL_SERVER_ADMIN_USERNAME= dev.env) && export DB_USER=${MYSQL_SERVER_ADMIN_USERNAME}@$(cat $STACK_OUTPUT | jq -r .ContainerRegistryAdminUsername.value) && \
export $(grep MYSQL_SERVER_ADMIN_PASSWORD= dev.env) && export DB_PASS=${MYSQL_SERVER_ADMIN_PASSWORD} && \
export $(grep MYSQL_SCHEMA_NAME= dev.env) && export DB_NAME=${MYSQL_SCHEMA_NAME} &&\ export DB_PORT=3306