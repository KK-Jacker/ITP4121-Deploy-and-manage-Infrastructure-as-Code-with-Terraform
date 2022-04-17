import {Construct} from "constructs";
import {Vpc, Subnet} from "@cdktf/provider-aws";

export class VirtualNetworkConstruct extends Construct {
    public readonly aksvirtualNetwork: Vpc;
    public readonly akssubnet1: Subnet;
    public readonly akssubnet2: Subnet;
    constructor(scope: Construct, name: string, ) {
        super(scope, name);

        this.aksvirtualNetwork = new Vpc(this, 'aksvirtualNetwork', {
            cidrBlock: '10.0.0.0/16',
            tags: JSON.parse(process.env.AWSTAG!)
        });

        this.akssubnet1 =new Subnet(this, 'akssubnet1', {
            vpcId: this.aksvirtualNetwork.id,
            cidrBlock: '10.0.0.0/17',
            tags: JSON.parse(process.env.AWSTAG!),
            dependsOn: [this.aksvirtualNetwork]
        });

        this.akssubnet2 = new Subnet(this, 'akssubnet2', {
            vpcId: this.aksvirtualNetwork.id,
            cidrBlock: '10.0.128.0/17',
            tags: JSON.parse(process.env.AWSTAG!),
            dependsOn: [this.aksvirtualNetwork]
        });
    }
}

