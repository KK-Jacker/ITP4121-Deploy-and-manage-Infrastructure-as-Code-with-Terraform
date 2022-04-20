import { Construct } from "constructs";
import { TerraformStack } from "cdktf";
interface MainStackProps {
    env: string;
}
export declare class MainStack extends TerraformStack {
    constructor(scope: Construct, name: string, props: MainStackProps);
}
export {};
