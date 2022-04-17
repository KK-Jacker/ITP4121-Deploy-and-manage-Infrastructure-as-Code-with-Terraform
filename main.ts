import {Construct} from "constructs";
import {App, /*TerraformOutput,*/ TerraformStack} from "cdktf";
import {AwsProvider} from "@cdktf/provider-aws";
import {resolve} from "path";
import {config} from "dotenv";
import {VirtualNetworkConstruct} from "./aws/aws_vpc";
interface MainStackProps {
    env: string;
}

export class MainStack extends TerraformStack {
    constructor(scope: Construct, name: string, props: MainStackProps) {
        super(scope, name);

        config({path: resolve(__dirname, `./${props.env}.env`)});
        process.env.ENV = props.env;
        process.env.RESOURCE_GROUP_NAME = process.env.RESOURCE_GROUP_NAME + props.env;
        console.log("Resource Group:" + process.env.RESOURCE_GROUP_NAME);

        new AwsProvider(this, "AWS Provider", {
            region: "ap-east-1",
            sharedCredentialsFile: "~/.aws/credentials",
        })

         new VirtualNetworkConstruct(this, "Virtual Network ");


    }
}

const app = new App();
new MainStack(app, "ITP4121-Project", {env: "dev"});
app.synth();
