import { Construct } from "constructs";
import { ResourceGroup } from "@cdktf/provider-azurerm";
interface ChatBotConstructConstructProps {
    resourceGroup: ResourceGroup;
}
export declare class ChatBotConstruct extends Construct {
    readonly webChatBotSecret: string;
    constructor(scope: Construct, name: string, props: ChatBotConstructConstructProps);
}
export {};
