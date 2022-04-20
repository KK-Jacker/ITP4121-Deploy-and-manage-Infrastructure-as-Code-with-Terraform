import { Construct } from "constructs";
import { ResourceGroup, StorageAccount, StorageContainer } from "@cdktf/provider-azurerm";
interface BlobStorageConstructProps {
    resourceGroup: ResourceGroup;
}
export declare class BlobStorageConstruct extends Construct {
    readonly storageAccount: StorageAccount;
    readonly tempContainer: StorageContainer;
    readonly pictureContainer: StorageContainer;
    constructor(scope: Construct, name: string, props: BlobStorageConstructProps);
}
export {};
