import { Construct } from "constructs";
import { ResourceGroup, VirtualNetwork, Subnet } from "@cdktf/provider-azurerm";
interface VirtualNetworkConstructProps {
    resourceGroup: ResourceGroup;
}
export declare class VirtualNetworkConstruct extends Construct {
    readonly aksvirtualNetwork: VirtualNetwork;
    readonly akssubnet1: Subnet;
    readonly akssubnet2: Subnet;
    constructor(scope: Construct, name: string, props: VirtualNetworkConstructProps);
}
export {};
