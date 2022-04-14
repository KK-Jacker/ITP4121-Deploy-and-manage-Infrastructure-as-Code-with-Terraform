import {Construct} from "constructs";
import {CognitiveAccount, ResourceGroup} from "@cdktf/provider-azurerm";

interface CognitiveServiceConstructConstructProps {
    resourceGroup: ResourceGroup;
}

export class CognitiveServiceConstruct extends Construct {
    public readonly cognitiveAccountComputerVisionKey: string;
    public readonly cognitiveAccountComputerVisionEndpoint: string;
    public readonly cognitiveAccountContentModeratorKey: string;
    public readonly cognitiveAccountContentModeratorEndpoint: string;
    public readonly cognitiveAccountTextAnalyticsKey: string;
    public readonly cognitiveAccountTextAnalyticsEndpoint: string;
    public readonly cognitiveAccountTextTranslationKey: string;
    public readonly cognitiveAccountTextTranslationEndpoint: string;
    public readonly cognitiveAccountFaceKey: string;
    public readonly cognitiveAccountFaceEndpoint: string;
    public readonly cognitiveAccountFormRecognizerKey: string;
    public readonly cognitiveAccountFormRecognizerEndpoint: string;

    constructor(
        scope: Construct,
        name: string,
        props: CognitiveServiceConstructConstructProps
    ) {
        super(scope, name);

        const {resourceGroup} = props;

        const cognitiveAccountComputerVision = new CognitiveAccount(this, "Computer Vision Cognitive Account", {
            name: process.env.STORAGE_ACCOUNT_NAME! + process.env.ENV + "ComputerVision",
            resourceGroupName: resourceGroup.name,
            location: resourceGroup.location,
            kind: "ComputerVision", skuName: process.env.COGNITIVE_ACCOUNT_SKU_NAME_COMPUTER_VISION!
        });
        this.cognitiveAccountComputerVisionKey = cognitiveAccountComputerVision.primaryAccessKey;
        this.cognitiveAccountComputerVisionEndpoint = cognitiveAccountComputerVision.endpoint;

        const cognitiveAccountContentModerator = new CognitiveAccount(this, "Content Moderator Cognitive Account", {
            name: process.env.STORAGE_ACCOUNT_NAME! + process.env.ENV + "ContentModerator",
            resourceGroupName: resourceGroup.name,
            location: resourceGroup.location,
            kind: "ContentModerator", skuName: process.env.COGNITIVE_ACCOUNT_SKU_NAME!
        });
        this.cognitiveAccountContentModeratorKey = cognitiveAccountContentModerator.primaryAccessKey;
        this.cognitiveAccountContentModeratorEndpoint = cognitiveAccountContentModerator.endpoint;

        const cognitiveAccountTextAnalytics = new CognitiveAccount(this, "Text Analytics Cognitive Account", {
            name: process.env.STORAGE_ACCOUNT_NAME! + process.env.ENV + "TextAnalytics",
            resourceGroupName: resourceGroup.name,
            location: resourceGroup.location,
            kind: "TextAnalytics", skuName: process.env.COGNITIVE_ACCOUNT_SKU_NAME_TEXTANALYTICS!
        });
        this.cognitiveAccountTextAnalyticsKey = cognitiveAccountTextAnalytics.primaryAccessKey;
        this.cognitiveAccountTextAnalyticsEndpoint = cognitiveAccountTextAnalytics.endpoint;

        const cognitiveAccountTextTranslation = new CognitiveAccount(this, "Text Translation Cognitive Account", {
            name: process.env.STORAGE_ACCOUNT_NAME! + process.env.ENV + "TextTranslation",
            resourceGroupName: resourceGroup.name,
            location: resourceGroup.location,
            kind: "TextTranslation", skuName: process.env.COGNITIVE_ACCOUNT_SKU_NAME_TEXTTRANSLATION!
        });
        this.cognitiveAccountTextTranslationKey = cognitiveAccountTextTranslation.primaryAccessKey;
        this.cognitiveAccountTextTranslationEndpoint = cognitiveAccountTextTranslation.endpoint;

        const cognitiveAccountFace = new CognitiveAccount(this, "Face Cognitive Account", {
            name: process.env.STORAGE_ACCOUNT_NAME! + process.env.ENV + "Face",
            resourceGroupName: resourceGroup.name,
            location: resourceGroup.location,
            kind: "Face", skuName: process.env.COGNITIVE_ACCOUNT_SKU_NAME!
        });
        this.cognitiveAccountFaceKey = cognitiveAccountFace.primaryAccessKey;
        this.cognitiveAccountFaceEndpoint = cognitiveAccountFace.endpoint;

        const cognitiveAccountFormRecognizer = new CognitiveAccount(this, "FormRecognizer Cognitive Account", {
            name: process.env.STORAGE_ACCOUNT_NAME! + process.env.ENV + "FormRecognizer",
            resourceGroupName: resourceGroup.name,
            location: resourceGroup.location,
            kind: "FormRecognizer", skuName: process.env.COGNITIVE_ACCOUNT_SKU_NAME!
        });
        this.cognitiveAccountFormRecognizerKey = cognitiveAccountFormRecognizer.primaryAccessKey;
        this.cognitiveAccountFormRecognizerEndpoint = cognitiveAccountFormRecognizer.endpoint;

    }
}
