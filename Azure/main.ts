import {Construct} from "constructs";
import {App, TerraformOutput, TerraformStack} from "cdktf";
import {AzurermProvider, ResourceGroup} from "@cdktf/provider-azurerm";
import {AzureAdConstruct} from "./azure/azure_ad";
import {ApplicationInsightsConstruct} from "./azure/application_insight";
import {MySQLServerConstruct} from "./azure/mysql_server";
import {MySQLDatabaseConstruct} from "./azure/mysql_db";
import {MySQLFirewallConstruct} from "./azure/mysql_db_firewall";
import {BlobStorageConstruct} from "./azure/blob";
import {ChatBotConstruct} from "./azure/chatbot";
import {ContainerRegistrySConstruct} from "./azure/container_registry";
import {CognitiveServiceConstruct} from "./azure/cognitive_service";
import {KeyVaultConstruct} from "./azure/key_vault";
import {VirtualNetworkConstruct} from "./azure/virtual_network";
import {KubernetesClusterSConstruct} from "./azure/kubernetes";
import {resolve} from "path";
import {config, parse} from "dotenv";
import * as fs from "fs";
import {Resource} from "@cdktf/provider-null";
import {DataLocalFile} from "./.gen/providers/local";



interface MainStackProps {
    env: string;
}

export class MainStack extends TerraformStack {
    constructor(scope: Construct, name: string, props: MainStackProps) {
        super(scope, name);

        config({path: resolve(__dirname, `./${props.env}.env`)});
        process.env.ENV = props.env;
        process.env.RESOURCE_GROUP_NAME = process.env.RESOURCE_GROUP_NAME + props.env;
        console.log("Resource Group:" + process.env.RESOURCE_GROUP_NAME);

        if (fs.existsSync(resolve(__dirname, `./secrets.env`))) {
            console.log("Overrides with secrets.env.template");
            const envConfig = parse(fs.readFileSync(resolve(__dirname, `./secrets.env`)))
            for (const k in envConfig) {
                process.env[k] = envConfig[k]
            }
        }

        new AzurermProvider(this, "Azure provider", {
            features: [{}],
            skipProviderRegistration: false,
        });


        const resourceGroup = new ResourceGroup(this, "Resource group", {
            name: process.env.RESOURCE_GROUP_NAME!,
            location: process.env.LOCATION!,
        });

        const azureAdConstruct = new AzureAdConstruct(this, "Azure AD");

        const blobStorageConstruct = new BlobStorageConstruct(this, "Blob", {resourceGroup});

        const mySQLServerConstruct = new MySQLServerConstruct(this, "MySQL server", {resourceGroup});

        new MySQLDatabaseConstruct(this, "MySQL database", {
            resourceGroup,
            mysqlServer: mySQLServerConstruct.mysqlServer,
        });

        new MySQLFirewallConstruct(this, "MySQL firewall", {
            resourceGroup,
            mysqlServer: mySQLServerConstruct.mysqlServer,
        });

        const virtualNetworkConstruct = new VirtualNetworkConstruct(this, "Virtual Network", {
            resourceGroup,
        });



        const containerRegistrySConstruct = new ContainerRegistrySConstruct(this, "container registry", {
            resourceGroup,
            azureadConstruct: azureAdConstruct,
        });

        const applicationInsightsConstruct = new ApplicationInsightsConstruct(this, "Application insights", {
            resourceGroup,
        });

        const cognitiveServiceConstruct = new CognitiveServiceConstruct(this, "Cognitive Service", {
            resourceGroup
        });

        const chatBotConstruct = new ChatBotConstruct(this, "Chat Bot", {
            resourceGroup
        });

        const keyVaultConstruct = new KeyVaultConstruct(this, "KeyVault", {
            resourceGroup,
            storageAccount: blobStorageConstruct.storageAccount,
            servicePrincipalObjectId: azureAdConstruct.servicePrincipalObjectId,
            applicationInsightsKey: applicationInsightsConstruct.applicationInsights.instrumentationKey,
            webChatBotSecret: chatBotConstruct.webChatBotSecret,
            cognitiveServiceConstruct
        });

        const kubernetesClusterSConstruct = new KubernetesClusterSConstruct(this, "Kubernetes", {
            resourceGroup,
            virtualNetwork: virtualNetworkConstruct,
            azureAdConstruct: azureAdConstruct,
            containerRegistry: containerRegistrySConstruct,
            keyVaultConstruct: keyVaultConstruct,
            mysqlServerConstruct: mySQLServerConstruct,
        });

        const get_k8s_exposed_ip = new Resource(this, "get kubectl exposed ip", {
            triggers: {
            },
            dependsOn: [kubernetesClusterSConstruct.kubectl],
        });
        get_k8s_exposed_ip.addOverride("provisioner.local-exec.command",
            `sleep 30 && kubectl get service -l app=web -o json | jq -r .items[].status.loadBalancer.ingress[].ip > k8sexposedip.txt`
        );

        const k8sip = new DataLocalFile(this, "hash_content", {
            filename: "k8sexposedip.txt",
            dependsOn: [get_k8s_exposed_ip],
        });

        const k8sipcontent = k8sip.content

        new TerraformOutput(
            this,
            "Service Principal App Id",
            {value: azureAdConstruct.servicePrincipalAppId, sensitive: true}
        );

        new TerraformOutput(
            this,
            "Service Principal Password",
            {value: azureAdConstruct.servicePrincipalPassword, sensitive: true}
        );
        new TerraformOutput(
            this,
            "Service Principal Tenant Id",
            {value: azureAdConstruct.servicePrincipalTenantId, sensitive: true}
        );

        new TerraformOutput(
            this,
            "Container Registry Admin Username",
            {value: containerRegistrySConstruct.containerRegistry.adminUsername, sensitive: true}
        );

        new TerraformOutput(
            this,
            "Container Registry Admin Password",
            {value: containerRegistrySConstruct.containerRegistry.adminPassword, sensitive: true}
        );

        new TerraformOutput(
            this,
            "Container Registry Identity",
            {value: containerRegistrySConstruct.containerRegistry.identity, sensitive: true}
        );

        new TerraformOutput(
            this,
            "Key Vault Uri",
            {value: keyVaultConstruct.keyVault.vaultUri, sensitive: true}
        );

        new TerraformOutput(
            this,
            "K8s LoadBalancer IP",
            {value: k8sipcontent, sensitive: true}
        );

        new TerraformOutput(
            this,
            "MySQL Server Hostname",
            {value: mySQLServerConstruct.mysqlServer.fqdn, sensitive: true}
        );
        new TerraformOutput(
            this,
            "MySQL Server Identity",
            {value: mySQLServerConstruct.mysqlServer.identity, sensitive: true}
        );

        new TerraformOutput(
            this,
            "MySQL Server Username",
            {value: mySQLServerConstruct.mysqlServer.administratorLogin, sensitive: true}
        );

        new TerraformOutput(
            this,
            "MySQL Server Password",
            {value: mySQLServerConstruct.mysqlServer.administratorLoginPassword, sensitive: true}
        );
        const get_image_var = new Resource(this, "get docker image name", {
            triggers: {
            },
            dependsOn: [kubernetesClusterSConstruct.kubernetesCluster],
        });
        get_image_var.addOverride("provisioner.local-exec.command",
            `echo -n $(git symbolic-ref --short HEAD) > branch.txt && echo -n $(git rev-parse --short HEAD) > hash.txt`
        );

        const hash_content = new DataLocalFile(this, "hash_content_main", {
            filename: "hash.txt",
            dependsOn: [get_image_var],
        });
        const branch_content = new DataLocalFile(this, "branch_content_main", {
            filename: "branch.txt",
            dependsOn: [get_image_var],
        });
        const dockerimagename = containerRegistrySConstruct.containerRegistry.loginServer + "/" + process.env.PROJECT_NAME! + "-" + branch_content.content + ":" +  hash_content.content ;

        new TerraformOutput(
            this,
            "Docker Image Name",
            {value: dockerimagename, sensitive: true}
        );

        new TerraformOutput(
            this,
            "resource group name",
            {value: resourceGroup.name, sensitive: true}
        );

        new TerraformOutput(
            this,
            "kubernetes cluster name",
            {value: kubernetesClusterSConstruct.kubernetesCluster.name, sensitive: true}
        );


    }
}

const app = new App();
new MainStack(app, "ITP4121-Project", {env: "dev"});
app.synth();
