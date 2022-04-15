import {Construct} from "constructs";
import {ResourceGroup, VirtualNetwork, Subnet} from "@cdktf/provider-azurerm";
interface VirtualNetworkConstructProps {
    resourceGroup: ResourceGroup;
}

export class VirtualNetworkConstruct extends Construct {
    public readonly aksvirtualNetwork: VirtualNetwork;
    public readonly akssubnet1: Subnet;
    public readonly akssubnet2: Subnet;
    constructor(scope: Construct, name: string, props: VirtualNetworkConstructProps) {
        super(scope, name);

        const {resourceGroup} = props;

        this.aksvirtualNetwork = new VirtualNetwork(this, "ITP4121-Project lib Virtual Network for k8s", {
            name: "default_network",
            resourceGroupName: resourceGroup.name,
            location: resourceGroup.location,
            addressSpace: ['10.0.0.0/8'],
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
    }
}

