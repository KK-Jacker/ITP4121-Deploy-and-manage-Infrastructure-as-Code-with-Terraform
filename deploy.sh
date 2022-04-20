cd Azure/
cdktf get
npm i
./deploy.sh
sleep 10
az aks get-credentials --resource-group itp4121project2dev --name itp4121project2dev --context aks --overwrite-existing
cd ../gcp
terraform init
./deploy.sh
echo will start deploy gcp in 10 seconds
sleep 10
gcloud container clusters get-credentials perceptive-map-347614-gke --region asia-east2 --project perceptive-map-347614
echo will start deploy consul in 10 seconds
cd ../consul
terraform init
sleep 5
terraform apply --auto-approve
echo Azure k8s pod ip is $(kubectl get service -l app=web --context aks -o json | jq -r .items[].status.loadBalancer.ingress[].ip)
echo GCP k8s pod ip is $(kubectl get service -l app=web -o json | jq -r .items[].status.loadBalancer.ingress[].ip)
