"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.VirtualNetworkConstruct = void 0;
const constructs_1 = require("constructs");
const provider_azurerm_1 = require("@cdktf/provider-azurerm");
class VirtualNetworkConstruct extends constructs_1.Construct {
    constructor(scope, name, props) {
        super(scope, name);
        const { resourceGroup } = props;
        this.aksvirtualNetwork = new provider_azurerm_1.VirtualNetwork(this, "ITP4121-Project lib Virtual Network for k8s", {
            name: "default_network",
            resourceGroupName: resourceGroup.name,
            location: resourceGroup.location,
            addressSpace: ['10.0.0.0/8'],
            tags: JSON.parse(process.env.AZURETAG),
        });
        this.akssubnet1 = new provider_azurerm_1.Subnet(this, "ITP4121-Project lib Subnet 1 for k8s", {
            name: "akssubnet1",
            resourceGroupName: resourceGroup.name,
            virtualNetworkName: this.aksvirtualNetwork.name,
            addressPrefix: "10.1.0.0/16",
        });
        this.akssubnet2 = new provider_azurerm_1.Subnet(this, "ITP4121-Project lib Subnet 2 for k8s", {
            name: "akssubnet2",
            resourceGroupName: resourceGroup.name,
            virtualNetworkName: this.aksvirtualNetwork.name,
            addressPrefix: "10.2.0.0/16",
        });
    }
}
exports.VirtualNetworkConstruct = VirtualNetworkConstruct;
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoidmlydHVhbF9uZXR3b3JrLmpzIiwic291cmNlUm9vdCI6IiIsInNvdXJjZXMiOlsidmlydHVhbF9uZXR3b3JrLnRzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiI7OztBQUFBLDJDQUFxQztBQUNyQyw4REFBOEU7QUFLOUUsTUFBYSx1QkFBd0IsU0FBUSxzQkFBUztJQUlsRCxZQUFZLEtBQWdCLEVBQUUsSUFBWSxFQUFFLEtBQW1DO1FBQzNFLEtBQUssQ0FBQyxLQUFLLEVBQUUsSUFBSSxDQUFDLENBQUM7UUFFbkIsTUFBTSxFQUFDLGFBQWEsRUFBQyxHQUFHLEtBQUssQ0FBQztRQUU5QixJQUFJLENBQUMsaUJBQWlCLEdBQUcsSUFBSSxpQ0FBYyxDQUFDLElBQUksRUFBRSw2Q0FBNkMsRUFBRTtZQUM3RixJQUFJLEVBQUUsaUJBQWlCO1lBQ3ZCLGlCQUFpQixFQUFFLGFBQWEsQ0FBQyxJQUFJO1lBQ3JDLFFBQVEsRUFBRSxhQUFhLENBQUMsUUFBUTtZQUNoQyxZQUFZLEVBQUUsQ0FBQyxZQUFZLENBQUM7WUFDNUIsSUFBSSxFQUFFLElBQUksQ0FBQyxLQUFLLENBQUMsT0FBTyxDQUFDLEdBQUcsQ0FBQyxRQUFTLENBQUM7U0FDMUMsQ0FBQyxDQUFDO1FBRUgsSUFBSSxDQUFDLFVBQVUsR0FBRyxJQUFJLHlCQUFNLENBQUMsSUFBSSxFQUFFLHNDQUFzQyxFQUFFO1lBQ3ZFLElBQUksRUFBRSxZQUFZO1lBQ2xCLGlCQUFpQixFQUFFLGFBQWEsQ0FBQyxJQUFJO1lBQ3JDLGtCQUFrQixFQUFFLElBQUksQ0FBQyxpQkFBaUIsQ0FBQyxJQUFJO1lBQy9DLGFBQWEsRUFBRSxhQUFhO1NBQy9CLENBQUMsQ0FBQztRQUVILElBQUksQ0FBQyxVQUFVLEdBQUcsSUFBSSx5QkFBTSxDQUFDLElBQUksRUFBRSxzQ0FBc0MsRUFBRTtZQUN2RSxJQUFJLEVBQUUsWUFBWTtZQUNsQixpQkFBaUIsRUFBRSxhQUFhLENBQUMsSUFBSTtZQUNyQyxrQkFBa0IsRUFBRSxJQUFJLENBQUMsaUJBQWlCLENBQUMsSUFBSTtZQUMvQyxhQUFhLEVBQUUsYUFBYTtTQUMvQixDQUFDLENBQUM7SUFDUCxDQUFDO0NBQ0o7QUEvQkQsMERBK0JDIiwic291cmNlc0NvbnRlbnQiOlsiaW1wb3J0IHtDb25zdHJ1Y3R9IGZyb20gXCJjb25zdHJ1Y3RzXCI7XG5pbXBvcnQge1Jlc291cmNlR3JvdXAsIFZpcnR1YWxOZXR3b3JrLCBTdWJuZXR9IGZyb20gXCJAY2RrdGYvcHJvdmlkZXItYXp1cmVybVwiO1xuaW50ZXJmYWNlIFZpcnR1YWxOZXR3b3JrQ29uc3RydWN0UHJvcHMge1xuICAgIHJlc291cmNlR3JvdXA6IFJlc291cmNlR3JvdXA7XG59XG5cbmV4cG9ydCBjbGFzcyBWaXJ0dWFsTmV0d29ya0NvbnN0cnVjdCBleHRlbmRzIENvbnN0cnVjdCB7XG4gICAgcHVibGljIHJlYWRvbmx5IGFrc3ZpcnR1YWxOZXR3b3JrOiBWaXJ0dWFsTmV0d29yaztcbiAgICBwdWJsaWMgcmVhZG9ubHkgYWtzc3VibmV0MTogU3VibmV0O1xuICAgIHB1YmxpYyByZWFkb25seSBha3NzdWJuZXQyOiBTdWJuZXQ7XG4gICAgY29uc3RydWN0b3Ioc2NvcGU6IENvbnN0cnVjdCwgbmFtZTogc3RyaW5nLCBwcm9wczogVmlydHVhbE5ldHdvcmtDb25zdHJ1Y3RQcm9wcykge1xuICAgICAgICBzdXBlcihzY29wZSwgbmFtZSk7XG5cbiAgICAgICAgY29uc3Qge3Jlc291cmNlR3JvdXB9ID0gcHJvcHM7XG5cbiAgICAgICAgdGhpcy5ha3N2aXJ0dWFsTmV0d29yayA9IG5ldyBWaXJ0dWFsTmV0d29yayh0aGlzLCBcIklUUDQxMjEtUHJvamVjdCBsaWIgVmlydHVhbCBOZXR3b3JrIGZvciBrOHNcIiwge1xuICAgICAgICAgICAgbmFtZTogXCJkZWZhdWx0X25ldHdvcmtcIixcbiAgICAgICAgICAgIHJlc291cmNlR3JvdXBOYW1lOiByZXNvdXJjZUdyb3VwLm5hbWUsXG4gICAgICAgICAgICBsb2NhdGlvbjogcmVzb3VyY2VHcm91cC5sb2NhdGlvbixcbiAgICAgICAgICAgIGFkZHJlc3NTcGFjZTogWycxMC4wLjAuMC84J10sXG4gICAgICAgICAgICB0YWdzOiBKU09OLnBhcnNlKHByb2Nlc3MuZW52LkFaVVJFVEFHISksXG4gICAgICAgIH0pO1xuXG4gICAgICAgIHRoaXMuYWtzc3VibmV0MSA9IG5ldyBTdWJuZXQodGhpcywgXCJJVFA0MTIxLVByb2plY3QgbGliIFN1Ym5ldCAxIGZvciBrOHNcIiwge1xuICAgICAgICAgICAgbmFtZTogXCJha3NzdWJuZXQxXCIsXG4gICAgICAgICAgICByZXNvdXJjZUdyb3VwTmFtZTogcmVzb3VyY2VHcm91cC5uYW1lLFxuICAgICAgICAgICAgdmlydHVhbE5ldHdvcmtOYW1lOiB0aGlzLmFrc3ZpcnR1YWxOZXR3b3JrLm5hbWUsXG4gICAgICAgICAgICBhZGRyZXNzUHJlZml4OiBcIjEwLjEuMC4wLzE2XCIsXG4gICAgICAgIH0pO1xuXG4gICAgICAgIHRoaXMuYWtzc3VibmV0MiA9IG5ldyBTdWJuZXQodGhpcywgXCJJVFA0MTIxLVByb2plY3QgbGliIFN1Ym5ldCAyIGZvciBrOHNcIiwge1xuICAgICAgICAgICAgbmFtZTogXCJha3NzdWJuZXQyXCIsXG4gICAgICAgICAgICByZXNvdXJjZUdyb3VwTmFtZTogcmVzb3VyY2VHcm91cC5uYW1lLFxuICAgICAgICAgICAgdmlydHVhbE5ldHdvcmtOYW1lOiB0aGlzLmFrc3ZpcnR1YWxOZXR3b3JrLm5hbWUsXG4gICAgICAgICAgICBhZGRyZXNzUHJlZml4OiBcIjEwLjIuMC4wLzE2XCIsXG4gICAgICAgIH0pO1xuICAgIH1cbn1cblxuIl19