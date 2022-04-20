import { Construct } from "constructs";
import { KeyVault, ResourceGroup, StorageAccount } from "@cdktf/provider-azurerm";
import { CognitiveServiceConstruct } from "./cognitive_service";
interface KeyVaultConstructProps {
    resourceGroup: ResourceGroup;
    storageAccount: StorageAccount;
    servicePrincipalObjectId: string;
    applicationInsightsKey: string;
    webChatBotSecret: string;
    cognitiveServiceConstruct: CognitiveServiceConstruct;
}
export declare class KeyVaultConstruct extends Construct {
    readonly keyVault: KeyVault;
    constructor(scope: Construct, name: string, props: KeyVaultConstructProps);
}
export {};
