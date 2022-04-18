echo to insert data to k8s sql, you have to open new terminal and run below commands to port-forward, because port-forward command does not return
echo kubectl port-forward service/mysql-service 30306:3306
sleep 10
STACK_OUTPUT=../ITP4121-azure/stack_output.json && dev_env=../ITP4121-azure/dev.env && \
export VAULT_URL=$(cat $STACK_OUTPUT | jq -r .KeyVaultUri.value) && \
export AZURE_CLIENT_ID=$(cat $STACK_OUTPUT  | jq -r .ServicePrincipalAppId.valu\
e) && \
export AZURE_TENANT_ID=$(cat $STACK_OUTPUT  | jq -r .ServicePrincipalTenantId.v\
alue) && \
export AZURE_CLIENT_SECRET=$(cat $STACK_OUTPUT  | jq -r .ServicePrincipalPasswo\
rd.value) && \
export DB_HOST=$(cat $STACK_OUTPUT | jq -r .MySQLServerHostname.value) && \
export $(grep MYSQL_SERVER_ADMIN_USERNAME= $dev_env)&& \
export $(grep MYSQL_SERVER_ADMIN_PASSWORD= $dev_env) && export DB_PASS=${MYSQL_SERVER_ADMIN_PASSWORD}
export $(grep MYSQL_SCHEMA_NAME= $dev_env) && export DB_NAME=${MYSQL_SCHEMA_NAME}
export DB_HOST=127.0.0.1 && export DB_PORT=30306 && export DB_USER="root"
cd pc_donation
mysql -h 127.0.0.1 -P 30306 -u ${DB_USER} --password=${DB_PASS} -e "CREATE DATABASE IF NOT EXISTS ${DB_NAME};"
mysql -h 127.0.0.1 -P 30306 -u ${DB_USER} --password=${DB_PASS} ${DB_NAME} < ./mysql.sql
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
python3 ./insert_init_data.py