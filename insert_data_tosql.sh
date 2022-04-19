STACK_OUTPUT=stack_output.json && \
export VAULT_URL=$(cat $STACK_OUTPUT | jq -r .KeyVaultUri.value) && \
export AZURE_CLIENT_ID=$(cat $STACK_OUTPUT  | jq -r .ServicePrincipalAppId.value) && \
export AZURE_TENANT_ID=$(cat $STACK_OUTPUT  | jq -r .ServicePrincipalTenantId.value) && \
export AZURE_CLIENT_SECRET=$(cat $STACK_OUTPUT  | jq -r .ServicePrincipalPassword.value) && \
export DB_HOST=$(cat $STACK_OUTPUT  | jq -r .MySQLServerHostname.value) && \
export $(grep MYSQL_SCHEMA_NAME= ./dev.env) && export DB_NAME=${MYSQL_SCHEMA_NAME} && \
export $(grep MYSQL_SERVER_ADMIN_PASSWORD= ./dev.env) && export DB_PASS=${MYSQL_SERVER_ADMIN_PASSWORD} && \
export $(grep MYSQL_SERVER_ADMIN_USERNAME= ./dev.env)&& export $(grep PROJECT_NAME= ./dev.env)  && export export DB_USER=${MYSQL_SERVER_ADMIN_USERNAME}@${PROJECT_NAME}dev && export DB_PORT=3306
cd pc_donation
mysql -h ${DB_HOST} -u ${DB_USER} --password=${DB_PASS} -e "CREATE DATABASE IF NOT EXISTS ${DB_NAME};"
mysql -h ${DB_HOST} -u ${DB_USER} --password=${DB_PASS} ${DB_NAME} < ./mysql.sql
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
python3 ./insert_init_data.py