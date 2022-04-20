import { Construct } from "constructs";
import { ResourceGroup } from "@cdktf/provider-azurerm";
interface CognitiveServiceConstructConstructProps {
    resourceGroup: ResourceGroup;
}
export declare class CognitiveServiceConstruct extends Construct {
    readonly cognitiveAccountComputerVisionKey: string;
    readonly cognitiveAccountComputerVisionEndpoint: string;
    readonly cognitiveAccountContentModeratorKey: string;
    readonly cognitiveAccountContentModeratorEndpoint: string;
    readonly cognitiveAccountTextAnalyticsKey: string;
    readonly cognitiveAccountTextAnalyticsEndpoint: string;
    readonly cognitiveAccountTextTranslationKey: string;
    readonly cognitiveAccountTextTranslationEndpoint: string;
    readonly cognitiveAccountFaceKey: string;
    readonly cognitiveAccountFaceEndpoint: string;
    readonly cognitiveAccountFormRecognizerKey: string;
    readonly cognitiveAccountFormRecognizerEndpoint: string;
    constructor(scope: Construct, name: string, props: CognitiveServiceConstructConstructProps);
}
export {};
