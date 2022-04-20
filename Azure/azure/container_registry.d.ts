import { Construct } from "constructs";
import { ContainerRegistry, ResourceGroup } from "@cdktf/provider-azurerm";
import { Resource } from "@cdktf/provider-null";
import { AzureAdConstruct } from "./azure_ad";
interface ContainerRegistryConstructProps {
    resourceGroup: ResourceGroup;
    azureadConstruct: AzureAdConstruct;
}
export declare class ContainerRegistrySConstruct extends Construct {
    readonly containerRegistry: ContainerRegistry;
    readonly roleAssignment: Resource;
    readonly builddocker: Resource;
    constructor(scope: Construct, name: string, props: ContainerRegistryConstructProps);
}
export {};
