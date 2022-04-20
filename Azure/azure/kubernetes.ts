import {Construct} from "constructs";
import {KubernetesCluster, ResourceGroup} from "@cdktf/provider-azurerm";
import {AzureAdConstruct} from "./azure_ad";
import {VirtualNetworkConstruct} from "./virtual_network"
import {ContainerRegistrySConstruct} from "./container_registry"
import {KeyVaultConstruct} from "./key_vault"
import {Resource} from "@cdktf/provider-null";
import {MySQLServerConstruct} from "./mysql_server"
import {DataLocalFile} from "../.gen/providers/local/data-local-file";

interface KubernetesClusterSConstructProps {
    resourceGroup: ResourceGroup;
    virtualNetwork: VirtualNetworkConstruct;
    azureAdConstruct: AzureAdConstruct;
    containerRegistry: ContainerRegistrySConstruct;
    keyVaultConstruct: KeyVaultConstruct;
    mysqlServerConstruct: MySQLServerConstruct;
}

export class KubernetesClusterSConstruct extends Construct {
    public readonly kubernetesCluster: KubernetesCluster;
    public readonly kubectl: Resource;
    constructor(
        scope: Construct,
        name: string,
        props: KubernetesClusterSConstructProps
    ) {
        super(scope, name);

        const {resourceGroup, virtualNetwork} = props;


        // create container registry
        this.kubernetesCluster = new KubernetesCluster(
            this,
            "ITP4121-Project kubernetes Cluster",
            {
                name: process.env.PROJECT_NAME! + process.env.ENV,
                resourceGroupName: resourceGroup.name,
                location: resourceGroup.location,
                dnsPrefix: process.env.PROJECT_NAME! + process.env.ENV + "-dns",
                defaultNodePool: [{
                    name: "np01",
                    nodeCount: 1,
                    vmSize: "Standard_D4s_v3",
                    availabilityZones: ["1","2","3"],
                    enableAutoScaling: true,
                    minCount: 1,
                    maxCount: 3,
                    vnetSubnetId: virtualNetwork.akssubnet1.id,
                    osDiskSizeGb: 30,
                }],
                servicePrincipal: [{
                    clientId: props.azureAdConstruct.servicePrincipalAppId,
                    clientSecret: props.azureAdConstruct.servicePrincipalPassword,
                }],
                networkProfile: [{
                    networkPlugin: "azure"
                }],

                tags: JSON.parse(process.env.AZURETAG!),
                dependsOn: [ virtualNetwork.akssubnet1]
            }
        );
        const get_image_var = new Resource(this, "kubectlDownload", {
            triggers: {
            },
            dependsOn: [this.kubernetesCluster],
        });
        get_image_var.addOverride("provisioner.local-exec.command",
            `echo -n $(git symbolic-ref --short HEAD) > branch.txt && echo -n $(git rev-parse --short HEAD) > hash.txt`
        );

        const hash_content = new DataLocalFile(this, "hash_content", {
            filename: "hash.txt",
            dependsOn: [get_image_var],
        });
        const branch_content = new DataLocalFile(this, "branch_content", {
            filename: "branch.txt",
            dependsOn: [get_image_var],
        });
        this.kubectl = new Resource(this, "kubectl", {
            triggers: {
            },
            dependsOn: [this.kubernetesCluster, get_image_var, props.keyVaultConstruct.keyVault, props.containerRegistry.builddocker],
        });

        const db_user = props.mysqlServerConstruct.mysqlServer.administratorLogin + "@" + props.mysqlServerConstruct.mysqlServer.name // add + "@" + props.mysqlServerConstruct.mysqlServer.name for cloud mysql
        const db_pass = props.mysqlServerConstruct.mysqlServer.administratorLoginPassword // same but k8s sql must use process.env.MYSQL_SERVER_ADMIN_PASSWORD
        const db_host = props.mysqlServerConstruct.mysqlServer.fqdn  //props.mysqlServerConstruct.mysqlServer.fqdn for azure cloud mysql // mysql-service for k8s mysql
        const db_name = process.env.MYSQL_SCHEMA_NAME;
        const image= props.containerRegistry.containerRegistry.loginServer + "/" + process.env.PROJECT_NAME! + "-" + branch_content.content + ":" + hash_content.content ;
        const vault_url = props.keyVaultConstruct.keyVault.vaultUri
        const azure_client_id = props.azureAdConstruct.servicePrincipalAppId;
        const azure_client_secret = props.azureAdConstruct.servicePrincipalPassword;
        const azure_tenant_id = props.azureAdConstruct.servicePrincipalTenantId;
        const resource_group_name = resourceGroup.name;
        const kubernetes_name = this.kubernetesCluster.name;
        const azurecr_loginserver = props.containerRegistry.containerRegistry.loginServer;
        this.kubectl.addOverride(
            "provisioner.local-exec.command", `az aks get-credentials --resource-group ${resource_group_name} --name ${kubernetes_name} --overwrite-existing && \
            cd ../../../pc_donation/ && export DB_USER=${db_user} && export DB_PASS=${db_pass} && export DB_HOST=${db_host} && export DB_NAME=${db_name} && export DB_PORT=3306 export IMAGE=${image} \
             export VAULT_URL=${vault_url} && export AZURE_CLIENT_ID=${azure_client_id} && export AZURE_CLIENT_SECRET=${azure_client_secret} && export AZURE_TENANT_ID=${azure_tenant_id} && \
             kubectl create secret generic web-secret --from-literal='IMAGE=${image}' --from-literal='port="3306"' --from-literal='username=${db_user}' --from-literal='password=${db_pass}' --from-literal='host=${db_host}' --from-literal='tablename=${db_name}' && \
             kubectl create secret docker-registry azurecr-secret --namespace default --docker-server=${azurecr_loginserver} --docker-username=${azure_client_id} --docker-password=${azure_client_secret} --
             kubectl apply -f mysql-deployment.yaml,mysql-service.yaml && \ 
             envsubst < web-deployment.yaml | kubectl apply -f - && kubectl apply -f web-service.yaml
             `
            // envsubst < web-deployment.yaml | kubectl apply -f - && kubectl apply -f web-service.yaml
            // kubectl apply -f mysql-deployment.yaml,mysql-service.yaml for k8s mysql, if use cloud mysql just delete it
        );
    }
}
