import {Construct} from "constructs";
import {ResourceGroup, StorageAccount, StorageContainer,} from "@cdktf/provider-azurerm";

interface BlobStorageConstructProps {
    resourceGroup: ResourceGroup;
}

export class BlobStorageConstruct extends Construct {
    public readonly storageAccount: StorageAccount;
    public readonly tempContainer: StorageContainer;
    public readonly pictureContainer: StorageContainer;

    constructor(scope: Construct, name: string, props: BlobStorageConstructProps) {
        super(scope, name);

        const {resourceGroup} = props;

        // create storage account
        // https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/storage_account
        this.storageAccount = new StorageAccount(
            this,
            "ITP4121-Project lib storage account",
            {
                name: process.env.STORAGE_ACCOUNT_NAME! + process.env.ENV,
                resourceGroupName: resourceGroup.name,
                location: resourceGroup.location,
                accountTier: process.env.STORAGE_ACCOUNT_TIER!,
                accountReplicationType: process.env.STORAGE_ACCOUNT_REPLICATION_TYPE!,
            }
        );

        // create container
        // https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/storage_blob
        this.tempContainer = new StorageContainer(
            this,
            "ITP4121-Project lib temp container",
            {
                name: process.env.STORAGE_CONTAINER_TEMP_NAME!,
                containerAccessType: process.env.STORAGE_CONTAINER_ACCESS_TYPE!,
                storageAccountName: this.storageAccount.name,
            }
        );

        this.pictureContainer = new StorageContainer(
            this,
            "ITP4121-Project lib picture container",
            {
                name: process.env.STORAGE_CONTAINER_PERMANENT_NAME!,
                containerAccessType: process.env.STORAGE_CONTAINER_ACCESS_TYPE!,
                storageAccountName: this.storageAccount.name,
            }
        );

        // create lifecycle policy
        // https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/storage_management_policy
    }
}
