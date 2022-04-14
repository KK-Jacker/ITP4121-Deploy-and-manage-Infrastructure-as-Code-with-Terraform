import {Construct} from "constructs";
import {
    DataAzurermClientConfig,
    KeyVault,
    KeyVaultSecret,
    ResourceGroup,
    StorageAccount
} from "@cdktf/provider-azurerm";
import {CognitiveServiceConstruct} from "./cognitive_service";

interface KeyVaultConstructProps {
    resourceGroup: ResourceGroup;
    storageAccount: StorageAccount;
    servicePrincipalObjectId: string;
    applicationInsightsKey: string;
    webChatBotSecret: string;
    cognitiveServiceConstruct: CognitiveServiceConstruct;
}

export class KeyVaultConstruct extends Construct {

    public readonly keyVault: KeyVault;

    constructor(scope: Construct, name: string, props: KeyVaultConstructProps) {
        super(scope, name);
        const dataAzureRmClientConfig = new DataAzurermClientConfig(this, "Client Config");
        const {resourceGroup, storageAccount, servicePrincipalObjectId} = props;

        this.keyVault = new KeyVault(this, "ITP4121-Project Key Vault", {
            name: process.env.PROJECT_NAME! + process.env.ENV,
            location: resourceGroup.location,
            resourceGroupName: resourceGroup.name,
            skuName: "standard",
            tenantId: dataAzureRmClientConfig.tenantId,
            accessPolicy: [{
                tenantId: dataAzureRmClientConfig.tenantId,
                objectId: dataAzureRmClientConfig.objectId, //the current user running deployment.
                secretPermissions: ["set", "get", "delete", "purge", "recover", "list"]
            }, {
                tenantId: dataAzureRmClientConfig.tenantId,
                objectId: servicePrincipalObjectId, //the current user running deployment.
                secretPermissions: ["set", "get", "delete", "purge", "recover", "list"]
            }
            ],
        });

        new KeyVaultSecret(this, "Storage Account Name", {
            keyVaultId: this.keyVault.id, name: "StorageAccountName", value: storageAccount.name
        });
        new KeyVaultSecret(this, "Storage Connection String", {
            keyVaultId: this.keyVault.id,
            name: "StorageConnectionString",
            value: storageAccount.primaryConnectionString
        });
        new KeyVaultSecret(this, "Storage Account Key", {
            keyVaultId: this.keyVault.id, name: "StorageAccountKey", value: storageAccount.primaryAccessKey
        });

        new KeyVaultSecret(this, "Application Insights Key", {
            keyVaultId: this.keyVault.id, name: "ApplicationInsightsKey", value: props.applicationInsightsKey
        });

        new KeyVaultSecret(this, "Google Map Key", {
            keyVaultId: this.keyVault.id, name: "GoogleMapKey", value: process.env.GOOGLE_MAP_KEY!
        });

        new KeyVaultSecret(this, "Recaptcha Secret Key", {
            keyVaultId: this.keyVault.id, name: "RecaptchaSecretKey", value: process.env.RECAPTCHA_SECRET_KEY!
        });

        new KeyVaultSecret(this, "Recaptcha Site Key", {
            keyVaultId: this.keyVault.id, name: "RecaptchaSiteKey", value: process.env.RECAPTCHA_SITE_KEY!
        });

        new KeyVaultSecret(this, "Cognitive Account Computer Vision Key", {
            keyVaultId: this.keyVault.id,
            name: "CognitiveAccountComputerVisionKey",
            value: props.cognitiveServiceConstruct.cognitiveAccountComputerVisionKey
        });

        new KeyVaultSecret(this, "Cognitive Account Computer Vision Endpoint", {
            keyVaultId: this.keyVault.id,
            name: "CognitiveAccountComputerVisionEndpoint",
            value: props.cognitiveServiceConstruct.cognitiveAccountComputerVisionEndpoint
        });

        new KeyVaultSecret(this, "Cognitive Account Content Moderator Key", {
            keyVaultId: this.keyVault.id,
            name: "CognitiveAccountContentModeratorKey",
            value: props.cognitiveServiceConstruct.cognitiveAccountContentModeratorKey
        });

        new KeyVaultSecret(this, "Cognitive Account Content Moderator Endpoint", {
            keyVaultId: this.keyVault.id,
            name: "CognitiveAccountContentModeratorEndpoint",
            value: props.cognitiveServiceConstruct.cognitiveAccountContentModeratorEndpoint
        });

        new KeyVaultSecret(this, "Cognitive Account Text Analytics Key", {
            keyVaultId: this.keyVault.id,
            name: "CognitiveAccountTextAnalyticsKey",
            value: props.cognitiveServiceConstruct.cognitiveAccountTextAnalyticsKey
        });
        new KeyVaultSecret(this, "Cognitive Account Text Analytics Endpoint", {
            keyVaultId: this.keyVault.id,
            name: "CognitiveAccountTextAnalyticsEndpoint",
            value: props.cognitiveServiceConstruct.cognitiveAccountTextAnalyticsEndpoint
        });

        new KeyVaultSecret(this, "Cognitive Account Text Translation Key", {
            keyVaultId: this.keyVault.id,
            name: "CognitiveAccountTextTranslationKey",
            value: props.cognitiveServiceConstruct.cognitiveAccountTextTranslationKey
        });

        new KeyVaultSecret(this, "Cognitive Account Text Translation Endpoint", {
            keyVaultId: this.keyVault.id,
            name: "CognitiveAccountTextTranslationEndpoint",
            value: props.cognitiveServiceConstruct.cognitiveAccountTextTranslationEndpoint
        });

        new KeyVaultSecret(this, "Cognitive Account Face Key", {
            keyVaultId: this.keyVault.id,
            name: "CognitiveAccountFaceKey",
            value: props.cognitiveServiceConstruct.cognitiveAccountFaceKey
        });
        new KeyVaultSecret(this, "Cognitive Account Face Endpoint", {
            keyVaultId: this.keyVault.id,
            name: "CognitiveAccountFaceEndpoint",
            value: props.cognitiveServiceConstruct.cognitiveAccountFaceEndpoint
        });
        new KeyVaultSecret(this, "Cognitive Account FormRecognizer Key", {
            keyVaultId: this.keyVault.id,
            name: "CognitiveAccountFormRecognizerKey",
            value: props.cognitiveServiceConstruct.cognitiveAccountFormRecognizerKey
        });
        new KeyVaultSecret(this, "Cognitive Account FormRecognizer Endpoint", {
            keyVaultId: this.keyVault.id,
            name: "CognitiveAccountFormRecognizerEndpoint",
            value: props.cognitiveServiceConstruct.cognitiveAccountFormRecognizerEndpoint
        });
        new KeyVaultSecret(this, "Web Chat Bot Secret", {
            keyVaultId: this.keyVault.id,
            name: "WebChatBotSecret",
            value: props.webChatBotSecret
        });

    }
}
