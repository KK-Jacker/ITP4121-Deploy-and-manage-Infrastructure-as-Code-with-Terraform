import { Construct } from "constructs";
import { KubernetesCluster, ResourceGroup } from "@cdktf/provider-azurerm";
import { AzureAdConstruct } from "./azure_ad";
import { VirtualNetworkConstruct } from "./virtual_network";
import { ContainerRegistrySConstruct } from "./container_registry";
import { KeyVaultConstruct } from "./key_vault";
import { Resource } from "@cdktf/provider-null";
import { MySQLServerConstruct } from "./mysql_server";
interface KubernetesClusterSConstructProps {
    resourceGroup: ResourceGroup;
    virtualNetwork: VirtualNetworkConstruct;
    azureAdConstruct: AzureAdConstruct;
    containerRegistry: ContainerRegistrySConstruct;
    keyVaultConstruct: KeyVaultConstruct;
    mysqlServerConstruct: MySQLServerConstruct;
}
export declare class KubernetesClusterSConstruct extends Construct {
    readonly kubernetesCluster: KubernetesCluster;
    readonly kubectl: Resource;
    constructor(scope: Construct, name: string, props: KubernetesClusterSConstructProps);
}
export {};
