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
export DB_PASS=123qweASD && export DB_HOST=127.0.0.1 && export DB_PORT=30306 && export DB_USER="root" && export DB_NAME="default_schema"
cd inputsqldata
mysql -h 127.0.0.1 -P 30306 -u root --password=123qweASD -e "CREATE DATABASE IF NOT EXISTS default_schema;"
mysql -h 127.0.0.1 -P 30306 -u root --password=123qweASD default_schema < ./mysql.sql
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
python3 ./insert_init_data.py