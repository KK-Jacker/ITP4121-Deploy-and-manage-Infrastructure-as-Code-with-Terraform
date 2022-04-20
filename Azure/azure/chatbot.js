"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.ChatBotConstruct = void 0;
const constructs_1 = require("constructs");
const provider_azurerm_1 = require("@cdktf/provider-azurerm");
const application_1 = require("../.gen/providers/azuread/application");
const provider_null_1 = require("@cdktf/provider-null");
const data_local_file_1 = require("../.gen/providers/local/data-local-file");
class ChatBotConstruct extends constructs_1.Construct {
    constructor(scope, name, props) {
        super(scope, name);
        const { resourceGroup } = props;
        const resourceGroupName = resourceGroup.name;
        const dataAzureRmClientConfig = new provider_azurerm_1.DataAzurermClientConfig(this, "Client Config");
        const application = new application_1.Application(this, "ITP4121-Project Bot Application", {
            displayName: process.env.PROJECT_NAME + process.env.ENV + "BotWebAppApplication",
            owners: [dataAzureRmClientConfig.objectId],
        });
        const botChannelsRegistration = new provider_azurerm_1.BotChannelsRegistration(this, "ITP4121-Project BotChannelsRegistration", {
            microsoftAppId: application.objectId,
            name: process.env.STORAGE_ACCOUNT_NAME + process.env.ENV + "BotWebApp",
            resourceGroupName,
            location: "global",
            sku: process.env.BOTWEBAPP_SKU
        });
        const botName = botChannelsRegistration.name;
        const botChannelWebChat = new provider_azurerm_1.BotChannelWebChat(this, "ITP4121-Project BotChannelWebChat", {
            botName,
            resourceGroupName,
            location: "global",
            siteNames: ["donor", "volunteer", "student", "teacher", "anonymous"]
        });
        const webchatSecretsNullResource = new provider_null_1.Resource(this, "Bot Channel WebChat Keys", {
            triggers: {
                dummy: new Date().getMilliseconds().toString()
            },
            dependsOn: [botChannelWebChat],
        });
        webchatSecretsNullResource.addOverride("provisioner.local-exec.command", `az bot webchat show --name ${botName} --resource-group ${resourceGroupName} --with-secrets \
            | jq '.resource.properties.sites| map({(.siteName) : .key}) | add' \
            > ../../../webchat_secrets.json`);
        const webChatBotSecretLocalFile = new data_local_file_1.DataLocalFile(this, "Webchat Secrets DataLocalFile", {
            filename: "../../../webchat_secrets.json",
            dependsOn: [webchatSecretsNullResource]
        });
        this.webChatBotSecret = webChatBotSecretLocalFile.content;
    }
}
exports.ChatBotConstruct = ChatBotConstruct;
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiY2hhdGJvdC5qcyIsInNvdXJjZVJvb3QiOiIiLCJzb3VyY2VzIjpbImNoYXRib3QudHMiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6Ijs7O0FBQUEsMkNBQXFDO0FBQ3JDLDhEQUtpQztBQUNqQyx1RUFBa0U7QUFDbEUsd0RBQThDO0FBQzlDLDZFQUFzRTtBQU90RSxNQUFhLGdCQUFpQixTQUFRLHNCQUFTO0lBRzNDLFlBQ0ksS0FBZ0IsRUFDaEIsSUFBWSxFQUNaLEtBQXFDO1FBRXJDLEtBQUssQ0FBQyxLQUFLLEVBQUUsSUFBSSxDQUFDLENBQUM7UUFFbkIsTUFBTSxFQUFDLGFBQWEsRUFBQyxHQUFHLEtBQUssQ0FBQztRQUM5QixNQUFNLGlCQUFpQixHQUFHLGFBQWEsQ0FBQyxJQUFJLENBQUM7UUFFN0MsTUFBTSx1QkFBdUIsR0FBRyxJQUFJLDBDQUF1QixDQUFDLElBQUksRUFBRSxlQUFlLENBQUMsQ0FBQztRQUNuRixNQUFNLFdBQVcsR0FBRyxJQUFJLHlCQUFXLENBQUMsSUFBSSxFQUFFLGlDQUFpQyxFQUFFO1lBQ3pFLFdBQVcsRUFBRSxPQUFPLENBQUMsR0FBRyxDQUFDLFlBQWEsR0FBRyxPQUFPLENBQUMsR0FBRyxDQUFDLEdBQUcsR0FBRyxzQkFBc0I7WUFDakYsTUFBTSxFQUFFLENBQUMsdUJBQXVCLENBQUMsUUFBUSxDQUFDO1NBQzdDLENBQUMsQ0FBQztRQUVILE1BQU0sdUJBQXVCLEdBQUcsSUFBSSwwQ0FBdUIsQ0FBQyxJQUFJLEVBQUUseUNBQXlDLEVBQUU7WUFDekcsY0FBYyxFQUFFLFdBQVcsQ0FBQyxRQUFRO1lBQ3BDLElBQUksRUFBRSxPQUFPLENBQUMsR0FBRyxDQUFDLG9CQUFxQixHQUFHLE9BQU8sQ0FBQyxHQUFHLENBQUMsR0FBRyxHQUFHLFdBQVc7WUFDdkUsaUJBQWlCO1lBQ2pCLFFBQVEsRUFBRSxRQUFRO1lBQ2xCLEdBQUcsRUFBRSxPQUFPLENBQUMsR0FBRyxDQUFDLGFBQWM7U0FDbEMsQ0FBQyxDQUFDO1FBRUgsTUFBTSxPQUFPLEdBQUcsdUJBQXVCLENBQUMsSUFBSSxDQUFDO1FBQzdDLE1BQU0saUJBQWlCLEdBQUcsSUFBSSxvQ0FBaUIsQ0FBQyxJQUFJLEVBQUUsbUNBQW1DLEVBQUU7WUFDdkYsT0FBTztZQUNQLGlCQUFpQjtZQUNqQixRQUFRLEVBQUUsUUFBUTtZQUNsQixTQUFTLEVBQUUsQ0FBQyxPQUFPLEVBQUUsV0FBVyxFQUFFLFNBQVMsRUFBRSxTQUFTLEVBQUUsV0FBVyxDQUFDO1NBQ3ZFLENBQUMsQ0FBQztRQUVILE1BQU0sMEJBQTBCLEdBQUcsSUFBSSx3QkFBUSxDQUFDLElBQUksRUFBRSwwQkFBMEIsRUFBRTtZQUM5RSxRQUFRLEVBQUU7Z0JBQ04sS0FBSyxFQUFFLElBQUksSUFBSSxFQUFFLENBQUMsZUFBZSxFQUFFLENBQUMsUUFBUSxFQUFFO2FBQ2pEO1lBQ0QsU0FBUyxFQUFFLENBQUMsaUJBQWlCLENBQUM7U0FDakMsQ0FBQyxDQUFDO1FBQ0gsMEJBQTBCLENBQUMsV0FBVyxDQUNsQyxnQ0FBZ0MsRUFBRSw4QkFBOEIsT0FBTyxxQkFBcUIsaUJBQWlCOzs0Q0FFN0UsQ0FDbkMsQ0FBQztRQUVGLE1BQU0seUJBQXlCLEdBQUcsSUFBSSwrQkFBYSxDQUFDLElBQUksRUFBRSwrQkFBK0IsRUFBRTtZQUN2RixRQUFRLEVBQUUsK0JBQStCO1lBQ3pDLFNBQVMsRUFBRSxDQUFDLDBCQUEwQixDQUFDO1NBQzFDLENBQUMsQ0FBQztRQUNILElBQUksQ0FBQyxnQkFBZ0IsR0FBRyx5QkFBeUIsQ0FBQyxPQUFPLENBQUM7SUFDOUQsQ0FBQztDQUNKO0FBckRELDRDQXFEQyIsInNvdXJjZXNDb250ZW50IjpbImltcG9ydCB7Q29uc3RydWN0fSBmcm9tIFwiY29uc3RydWN0c1wiO1xuaW1wb3J0IHtcbiAgICBCb3RDaGFubmVsc1JlZ2lzdHJhdGlvbixcbiAgICBCb3RDaGFubmVsV2ViQ2hhdCxcbiAgICBEYXRhQXp1cmVybUNsaWVudENvbmZpZyxcbiAgICBSZXNvdXJjZUdyb3VwLFxufSBmcm9tIFwiQGNka3RmL3Byb3ZpZGVyLWF6dXJlcm1cIjtcbmltcG9ydCB7QXBwbGljYXRpb259IGZyb20gXCIuLi8uZ2VuL3Byb3ZpZGVycy9henVyZWFkL2FwcGxpY2F0aW9uXCI7XG5pbXBvcnQge1Jlc291cmNlfSBmcm9tIFwiQGNka3RmL3Byb3ZpZGVyLW51bGxcIjtcbmltcG9ydCB7RGF0YUxvY2FsRmlsZX0gZnJvbSBcIi4uLy5nZW4vcHJvdmlkZXJzL2xvY2FsL2RhdGEtbG9jYWwtZmlsZVwiO1xuXG5cbmludGVyZmFjZSBDaGF0Qm90Q29uc3RydWN0Q29uc3RydWN0UHJvcHMge1xuICAgIHJlc291cmNlR3JvdXA6IFJlc291cmNlR3JvdXA7XG59XG5cbmV4cG9ydCBjbGFzcyBDaGF0Qm90Q29uc3RydWN0IGV4dGVuZHMgQ29uc3RydWN0IHtcbiAgICBwdWJsaWMgcmVhZG9ubHkgd2ViQ2hhdEJvdFNlY3JldDogc3RyaW5nO1xuXG4gICAgY29uc3RydWN0b3IoXG4gICAgICAgIHNjb3BlOiBDb25zdHJ1Y3QsXG4gICAgICAgIG5hbWU6IHN0cmluZyxcbiAgICAgICAgcHJvcHM6IENoYXRCb3RDb25zdHJ1Y3RDb25zdHJ1Y3RQcm9wc1xuICAgICkge1xuICAgICAgICBzdXBlcihzY29wZSwgbmFtZSk7XG5cbiAgICAgICAgY29uc3Qge3Jlc291cmNlR3JvdXB9ID0gcHJvcHM7XG4gICAgICAgIGNvbnN0IHJlc291cmNlR3JvdXBOYW1lID0gcmVzb3VyY2VHcm91cC5uYW1lO1xuXG4gICAgICAgIGNvbnN0IGRhdGFBenVyZVJtQ2xpZW50Q29uZmlnID0gbmV3IERhdGFBenVyZXJtQ2xpZW50Q29uZmlnKHRoaXMsIFwiQ2xpZW50IENvbmZpZ1wiKTtcbiAgICAgICAgY29uc3QgYXBwbGljYXRpb24gPSBuZXcgQXBwbGljYXRpb24odGhpcywgXCJJVFA0MTIxLVByb2plY3QgQm90IEFwcGxpY2F0aW9uXCIsIHtcbiAgICAgICAgICAgIGRpc3BsYXlOYW1lOiBwcm9jZXNzLmVudi5QUk9KRUNUX05BTUUhICsgcHJvY2Vzcy5lbnYuRU5WICsgXCJCb3RXZWJBcHBBcHBsaWNhdGlvblwiLFxuICAgICAgICAgICAgb3duZXJzOiBbZGF0YUF6dXJlUm1DbGllbnRDb25maWcub2JqZWN0SWRdLFxuICAgICAgICB9KTtcblxuICAgICAgICBjb25zdCBib3RDaGFubmVsc1JlZ2lzdHJhdGlvbiA9IG5ldyBCb3RDaGFubmVsc1JlZ2lzdHJhdGlvbih0aGlzLCBcIklUUDQxMjEtUHJvamVjdCBCb3RDaGFubmVsc1JlZ2lzdHJhdGlvblwiLCB7XG4gICAgICAgICAgICBtaWNyb3NvZnRBcHBJZDogYXBwbGljYXRpb24ub2JqZWN0SWQsXG4gICAgICAgICAgICBuYW1lOiBwcm9jZXNzLmVudi5TVE9SQUdFX0FDQ09VTlRfTkFNRSEgKyBwcm9jZXNzLmVudi5FTlYgKyBcIkJvdFdlYkFwcFwiLFxuICAgICAgICAgICAgcmVzb3VyY2VHcm91cE5hbWUsXG4gICAgICAgICAgICBsb2NhdGlvbjogXCJnbG9iYWxcIixcbiAgICAgICAgICAgIHNrdTogcHJvY2Vzcy5lbnYuQk9UV0VCQVBQX1NLVSFcbiAgICAgICAgfSk7XG5cbiAgICAgICAgY29uc3QgYm90TmFtZSA9IGJvdENoYW5uZWxzUmVnaXN0cmF0aW9uLm5hbWU7XG4gICAgICAgIGNvbnN0IGJvdENoYW5uZWxXZWJDaGF0ID0gbmV3IEJvdENoYW5uZWxXZWJDaGF0KHRoaXMsIFwiSVRQNDEyMS1Qcm9qZWN0IEJvdENoYW5uZWxXZWJDaGF0XCIsIHtcbiAgICAgICAgICAgIGJvdE5hbWUsXG4gICAgICAgICAgICByZXNvdXJjZUdyb3VwTmFtZSxcbiAgICAgICAgICAgIGxvY2F0aW9uOiBcImdsb2JhbFwiLFxuICAgICAgICAgICAgc2l0ZU5hbWVzOiBbXCJkb25vclwiLCBcInZvbHVudGVlclwiLCBcInN0dWRlbnRcIiwgXCJ0ZWFjaGVyXCIsIFwiYW5vbnltb3VzXCJdXG4gICAgICAgIH0pO1xuXG4gICAgICAgIGNvbnN0IHdlYmNoYXRTZWNyZXRzTnVsbFJlc291cmNlID0gbmV3IFJlc291cmNlKHRoaXMsIFwiQm90IENoYW5uZWwgV2ViQ2hhdCBLZXlzXCIsIHtcbiAgICAgICAgICAgIHRyaWdnZXJzOiB7XG4gICAgICAgICAgICAgICAgZHVtbXk6IG5ldyBEYXRlKCkuZ2V0TWlsbGlzZWNvbmRzKCkudG9TdHJpbmcoKVxuICAgICAgICAgICAgfSxcbiAgICAgICAgICAgIGRlcGVuZHNPbjogW2JvdENoYW5uZWxXZWJDaGF0XSxcbiAgICAgICAgfSk7XG4gICAgICAgIHdlYmNoYXRTZWNyZXRzTnVsbFJlc291cmNlLmFkZE92ZXJyaWRlKFxuICAgICAgICAgICAgXCJwcm92aXNpb25lci5sb2NhbC1leGVjLmNvbW1hbmRcIiwgYGF6IGJvdCB3ZWJjaGF0IHNob3cgLS1uYW1lICR7Ym90TmFtZX0gLS1yZXNvdXJjZS1ncm91cCAke3Jlc291cmNlR3JvdXBOYW1lfSAtLXdpdGgtc2VjcmV0cyBcXFxuICAgICAgICAgICAgfCBqcSAnLnJlc291cmNlLnByb3BlcnRpZXMuc2l0ZXN8IG1hcCh7KC5zaXRlTmFtZSkgOiAua2V5fSkgfCBhZGQnIFxcXG4gICAgICAgICAgICA+IC4uLy4uLy4uL3dlYmNoYXRfc2VjcmV0cy5qc29uYFxuICAgICAgICApO1xuXG4gICAgICAgIGNvbnN0IHdlYkNoYXRCb3RTZWNyZXRMb2NhbEZpbGUgPSBuZXcgRGF0YUxvY2FsRmlsZSh0aGlzLCBcIldlYmNoYXQgU2VjcmV0cyBEYXRhTG9jYWxGaWxlXCIsIHtcbiAgICAgICAgICAgIGZpbGVuYW1lOiBcIi4uLy4uLy4uL3dlYmNoYXRfc2VjcmV0cy5qc29uXCIsXG4gICAgICAgICAgICBkZXBlbmRzT246IFt3ZWJjaGF0U2VjcmV0c051bGxSZXNvdXJjZV1cbiAgICAgICAgfSk7XG4gICAgICAgIHRoaXMud2ViQ2hhdEJvdFNlY3JldCA9IHdlYkNoYXRCb3RTZWNyZXRMb2NhbEZpbGUuY29udGVudDtcbiAgICB9XG59XG4iXX0=