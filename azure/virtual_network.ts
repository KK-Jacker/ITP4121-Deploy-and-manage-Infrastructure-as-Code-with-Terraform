import {Construct} from "constructs";
import {ResourceGroup, VirtualNetwork} from "@cdktf/provider-azurerm";
interface VirtualNetworkConstructProps {
    resourceGroup: ResourceGroup;
}

export class VirtualNetworkConstruct extends Construct {
    public readonly virtualNetwork: VirtualNetwork;
    constructor(scope: Construct, name: string, props: VirtualNetworkConstructProps) {
        super(scope, name);

        const {resourceGroup} = props;

        this.virtualNetwork = new VirtualNetwork(this, "virtualNetwork", {
            name: "default_network",
            resourceGroupName: resourceGroup.name,
            location: resourceGroup.location,
            addressSpace: ['10.0.0.0/16'],
            subnet: [{
                name: 'subnet1',
                addressPrefix: "10.0.1.0/24"
            },
            {
                name: 'subnet2',
                addressPrefix: '10.0.2.0/24',
            }
            ],
            tags: JSON.parse(process.env.TAG!),
        });



    }
}
