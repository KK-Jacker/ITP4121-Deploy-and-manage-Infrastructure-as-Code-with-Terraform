echo to insert data to k8s sql, you have to open new terminal and run kubectl port-forward service/mysql-deployment 30306:3306, because this command does not return
sleep 5
STACK_OUTPUT=stack_output.json
export VAULT_URL=$(cat $STACK_OUTPUT | jq -r .KeyVaultUri.value)
export AZURE_CLIENT_ID=$(cat $STACK_OUTPUT  | jq -r .ServicePrincipalAppId.value)
export AZURE_TENANT_ID=$(cat $STACK_OUTPUT  | jq -r .ServicePrincipalTenantId.value)
export AZURE_CLIENT_SECRET=$(cat $STACK_OUTPUT  | jq -r .ServicePrincipalPassword.value)
export $(grep MYSQL_SERVER_ADMIN_USERNAME= dev.env) && export DB_USER=${MYSQL_SERVER_ADMIN_USERNAME}
export $(grep MYSQL_SERVER_ADMIN_PASSWORD= dev.env) && export DB_PASS=${MYSQL_SERVER_ADMIN_PASSWORD}
export $(grep MYSQL_SCHEMA_NAME= dev.env) && export DB_NAME=${MYSQL_SCHEMA_NAME}
export DB_HOST=127.0.0.1 && export DB_PORT=30306 && export DB_USER=itp4121admin && DB_PASS=123qweasd
cd pc_donation
mysql -h 127.0.0.1 -P 30306 -u itp4121admin --password=123qweasd  default_schema < ./mysql.sql
chmod 777 -R venv/bin/
. venv/bin/activate
pip install -r requirements.txt
python3 ./insert_init_data.py