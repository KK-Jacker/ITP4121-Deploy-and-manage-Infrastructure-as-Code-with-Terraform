import {Construct} from "constructs";
import {ResourceGroup, VirtualNetwork, Subnet, PublicIp, ApplicationGateway, VirtualNetworkPeering} from "@cdktf/provider-azurerm";
interface VirtualNetworkConstructProps {
    resourceGroup: ResourceGroup;
}

export class VirtualNetworkConstruct extends Construct {
    public readonly aksvirtualNetwork: VirtualNetwork;
    public readonly akssubnet1: Subnet;
    public readonly akssubnet2: Subnet;
    public readonly appgwVirtualNetwork: VirtualNetwork;
    public readonly frontendSubnet: Subnet;
    public readonly backendSubnet: Subnet;
    public readonly publicIp: PublicIp;
    public readonly applicationGateway: ApplicationGateway;
    constructor(scope: Construct, name: string, props: VirtualNetworkConstructProps) {
        super(scope, name);

        const {resourceGroup} = props;

        this.aksvirtualNetwork = new VirtualNetwork(this, "ITP4121-Project lib Virtual Network for k8s", {
            name: "default_network",
            resourceGroupName: resourceGroup.name,
            location: resourceGroup.location,
            addressSpace: ['10.0.0.0/12'],
            tags: JSON.parse(process.env.AZURETAG!),
        });

        this.akssubnet1 = new Subnet(this, "ITP4121-Project lib Subnet 1 for k8s", {
            name: "akssubnet1",
            resourceGroupName: resourceGroup.name,
            virtualNetworkName: this.aksvirtualNetwork.name,
            addressPrefix: "10.1.0.0/16",
        });

        this.akssubnet2 = new Subnet(this, "ITP4121-Project lib Subnet 2 for k8s", {
            name: "akssubnet2",
            resourceGroupName: resourceGroup.name,
            virtualNetworkName: this.aksvirtualNetwork.name,
            addressPrefix: "10.2.0.0/16",
        });
        this.appgwVirtualNetwork = new VirtualNetwork(this, "ITP4121-Project lib Virtual Network for appgw", {
            name: "appgw_network",
            resourceGroupName: resourceGroup.name,
            location: resourceGroup.location,
            addressSpace: ['10.16.0.0/12'],
            tags: JSON.parse(process.env.AZURETAG!),
        });

        this.frontendSubnet = new Subnet(this, "ITP4121-Project lib Subnet 1 for appgw", {
            name: "frontend_subnet",
            resourceGroupName: resourceGroup.name,
            virtualNetworkName: this.appgwVirtualNetwork.name,
            addressPrefix: "10.17.0.0/16",
        });

        this.backendSubnet = new Subnet(this, "ITP4121-Project lib Subnet 2 for appgw", {
            name: "backend_subnet",
            resourceGroupName: resourceGroup.name,
            virtualNetworkName: this.appgwVirtualNetwork.name,
            addressPrefix: "10.18.0.0/16",
        });

        this.publicIp = new PublicIp(this, "ITP4121-Project lib Public IP for appgw", {
            name: "appgw_public_ip",
            resourceGroupName: resourceGroup.name,
            location: resourceGroup.location,
            allocationMethod: "Static",
            sku: "Standard",
        });

        const backend_address_pool_name = this.appgwVirtualNetwork.name + "-beap";
        const frontend_port_name = this.appgwVirtualNetwork.name + "-feport";
        const frontend_ip_configuration_name = this.appgwVirtualNetwork.name + "-feip";
        const http_setting_name = this.appgwVirtualNetwork.name + "-be-htst";
        const listener_name = this.appgwVirtualNetwork.name + "-httplstn";
        const request_routing_rule_name = this.appgwVirtualNetwork.name + "-rqrt";

        this.applicationGateway = new ApplicationGateway(this, "ITP4121-Project lib Application Gateway", {
            name: "itp4121-project-appgateway",
            resourceGroupName: resourceGroup.name,
            location: resourceGroup.location,
            sku: [{
                name: "Standard_v2",
                tier: "Standard_v2",
                capacity: 2,
            }],
            gatewayIpConfiguration: [
                {
                    name: "gateway-ip-configuration",
                    subnetId: this.frontendSubnet.id,
                },
            ],
            frontendPort: [
                {
                    name: frontend_port_name,
                    port: 80,
                },
            ],
            frontendIpConfiguration: [
                {
                    name: frontend_ip_configuration_name,
                    publicIpAddressId: this.publicIp.id,
                },
            ],
            backendAddressPool: [
                {
                    name: backend_address_pool_name,
                },
            ],
            backendHttpSettings: [
                {
                    name: http_setting_name,
                    port: 80,
                    protocol: "Http",
                    cookieBasedAffinity: "Disabled",
                    requestTimeout: 60,
                    path: "/",
                },
            ],
            httpListener: [
                {
                    name: listener_name,
                    frontendPortName: frontend_port_name,
                    frontendIpConfigurationName: frontend_ip_configuration_name,
                    protocol: "Http",
                },
            ],
            requestRoutingRule: [
                {
                    name: request_routing_rule_name,
                    ruleType: "Basic",
                    httpListenerName: listener_name,
                    backendAddressPoolName: backend_address_pool_name,
                    backendHttpSettingsName: http_setting_name,
                },
            ],
            dependsOn: [this.publicIp],
        });
        new VirtualNetworkPeering(this, "ITP4121-Project lib Virtual Network app gateway to aks Peering", {
            name: "appgw-aws-peer",
            resourceGroupName: resourceGroup.name,
            virtualNetworkName: this.appgwVirtualNetwork.name,
            remoteVirtualNetworkId: this.aksvirtualNetwork.id,
            dependsOn: [this.akssubnet1, this.akssubnet2,this.frontendSubnet, this.backendSubnet],
        });
        new VirtualNetworkPeering(this, "ITP4121-Project lib Virtual Network aks to app gatewayPeering", {
            name: "aws-appgw-peer",
            resourceGroupName: resourceGroup.name,
            virtualNetworkName: this.aksvirtualNetwork.name,
            remoteVirtualNetworkId: this.appgwVirtualNetwork.id,
            dependsOn: [this.akssubnet1, this.akssubnet2,this.frontendSubnet, this.backendSubnet],
        });
    }
}

