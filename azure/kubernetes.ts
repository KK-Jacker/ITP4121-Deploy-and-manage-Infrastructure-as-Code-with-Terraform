import {Construct} from "constructs";
import {KubernetesCluster, ResourceGroup} from "@cdktf/provider-azurerm";
import {AzureAdConstruct} from "./azure_ad";
import {VirtualNetworkConstruct} from "./virtual_network"
import {ContainerRegistrySConstruct} from "./container_registry"
import {Resource} from "@cdktf/provider-null";
import {DataLocalFile} from "../.gen/providers/local/data-local-file";

interface KubernetesClusterSConstructProps {
    resourceGroup: ResourceGroup;
    virtualNetwork: VirtualNetworkConstruct;
    azureAdConstruct: AzureAdConstruct;
    containerRegistry: ContainerRegistrySConstruct;
}

export class KubernetesClusterSConstruct extends Construct {
    public readonly kubernetesCluster: KubernetesCluster;
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
                addonProfile: [{
                    ingressApplicationGateway: [{
                        enabled: true,
                        gatewayId: virtualNetwork.applicationGateway.id,
                    }]
                }],
                defaultNodePool: [{
                    name: "np01",
                    nodeCount: 1,
                    vmSize: "Standard_D2s_v3",
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
        const kubectl = new Resource(this, "kubectl", {
            triggers: {
            },
            dependsOn: [this.kubernetesCluster, get_image_var],
        });

        const db_user = process.env.MYSQL_SERVER_ADMIN_USERNAME!.toLowerCase() //+ "@" + process.env.PROJECT_NAME! + process.env.ENV
        const db_pass = process.env.MYSQL_SERVER_ADMIN_PASSWORD!.toLowerCase()
        const db_host = "mysql-service"
        const db_name = process.env.MYSQL_SCHEMA_NAME;
        const image= process.env.PROJECT_NAME! + process.env.ENV + ".azurecr.io/" + process.env.PROJECT_NAME! + "-" + branch_content.content + ":" + hash_content.content ;
        const vault_url = "https://" + process.env.PROJECT_NAME! + process.env.ENV + ".vault.azure.net/"
        const azure_client_id = props.azureAdConstruct.servicePrincipalAppId;
        const azure_client_secret = props.azureAdConstruct.servicePrincipalPassword;
        const azure_tenant_id = props.azureAdConstruct.servicePrincipalTenantId;
        const resource_group_name = resourceGroup.name;
        const kubernetes_name = this.kubernetesCluster.name;
        const azurecr_loginserver = props.containerRegistry.containerRegistry.loginServer;
        kubectl.addOverride(
            "provisioner.local-exec.command", `az aks get-credentials --resource-group ${resource_group_name} --name ${kubernetes_name} --overwrite-existing && \
            cd ../../../pc_donation/ && export DB_USER=${db_user} && export DB_PASS=${db_pass} && export DB_HOST=${db_host} && export DB_NAME=${db_name} && export DB_PORT=3306 export IMAGE=${image} \
             export VAULT_URL=${vault_url} && export AZURE_CLIENT_ID=${azure_client_id} && export AZURE_CLIENT_SECRET=${azure_client_secret} && export AZURE_TENANT_ID=${azure_tenant_id} && \
             kubectl create secret generic web-secret --from-literal='IMAGE=${image}' --from-literal='DB_PORT=3306' --from-literal='DB_USER=${db_user}' --from-literal='DB_PASS=${db_pass}' --from-literal='DB_HOST=${db_host}' --from-literal='DB_NAME=${db_name}' && \
             kubectl create secret docker-registry azurecr-secret --namespace default --docker-server=${azurecr_loginserver} --docker-username=${azure_client_id} --docker-password=${azure_client_secret} --
             envsubst < web-deployment.yaml | kubectl apply -f - && kubectl apply -f web-service.yaml,web-ingress.yaml,mysql-deployment.yaml,mysql-service.yaml
             `
        );
    }
}
