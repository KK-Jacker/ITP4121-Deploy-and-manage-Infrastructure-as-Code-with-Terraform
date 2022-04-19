import {Construct} from "constructs";
import {
    BotChannelsRegistration,
    BotChannelWebChat,
    DataAzurermClientConfig,
    ResourceGroup,
} from "@cdktf/provider-azurerm";
import {Application} from "../.gen/providers/azuread/application";
import {Resource} from "@cdktf/provider-null";
import {DataLocalFile} from "../.gen/providers/local/data-local-file";


interface ChatBotConstructConstructProps {
    resourceGroup: ResourceGroup;
}

export class ChatBotConstruct extends Construct {
    public readonly webChatBotSecret: string;

    constructor(
        scope: Construct,
        name: string,
        props: ChatBotConstructConstructProps
    ) {
        super(scope, name);

        const {resourceGroup} = props;
        const resourceGroupName = resourceGroup.name;

        const dataAzureRmClientConfig = new DataAzurermClientConfig(this, "Client Config");
        const application = new Application(this, "ITP4121-Project Bot Application", {
            displayName: process.env.PROJECT_NAME! + process.env.ENV + "BotWebAppApplication",
            owners: [dataAzureRmClientConfig.objectId],
        });

        const botChannelsRegistration = new BotChannelsRegistration(this, "ITP4121-Project BotChannelsRegistration", {
            microsoftAppId: application.objectId,
            name: process.env.STORAGE_ACCOUNT_NAME! + process.env.ENV + "BotWebApp",
            resourceGroupName,
            location: "global",
            sku: process.env.BOTWEBAPP_SKU!
        });

        const botName = botChannelsRegistration.name;
        const botChannelWebChat = new BotChannelWebChat(this, "ITP4121-Project BotChannelWebChat", {
            botName,
            resourceGroupName,
            location: "global",
            siteNames: ["donor", "volunteer", "student", "teacher", "anonymous"]
        });

        const webchatSecretsNullResource = new Resource(this, "Bot Channel WebChat Keys", {
            triggers: {
                dummy: new Date().getMilliseconds().toString()
            },
            dependsOn: [botChannelWebChat],
        });
        webchatSecretsNullResource.addOverride(
            "provisioner.local-exec.command", `az bot webchat show --name ${botName} --resource-group ${resourceGroupName} --with-secrets \
            | jq '.resource.properties.sites| map({(.siteName) : .key}) | add' \
            > ../../../webchat_secrets.json`
        );

        const webChatBotSecretLocalFile = new DataLocalFile(this, "Webchat Secrets DataLocalFile", {
            filename: "../../../webchat_secrets.json",
            dependsOn: [webchatSecretsNullResource]
        });
        this.webChatBotSecret = webChatBotSecretLocalFile.content;
    }
}
