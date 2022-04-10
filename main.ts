import {Construct} from "constructs";
import {App, TerraformStack} from "cdktf";
import {AzurermProvider, ResourceGroup} from "@cdktf/provider-azurerm";
import {resolve} from "path";
import {config, parse} from "dotenv";
import * as fs from "fs";
import {VirtualNetworkConstruct} from "./azure/virtual_network";

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

        if (fs.existsSync(resolve(__dirname, `./secrets.env`))) {
            console.log("Overrides with secrets.env.template");
            const envConfig = parse(fs.readFileSync(resolve(__dirname, `./secrets.env`)))
            for (const k in envConfig) {
                process.env[k] = envConfig[k]
            }
        }

        new AzurermProvider(this, "Azure provider", {
            features: [{}],
            skipProviderRegistration: false,
        });

        const resourceGroup = new ResourceGroup(this, "Resource group", {
            name: process.env.RESOURCE_GROUP_NAME!,
            location: process.env.LOCATION!,
        });

        new VirtualNetworkConstruct(this, "Virtual Network", {
            resourceGroup,
        });

    }
}

const app = new App();
new MainStack(app, "ITP4121-Project", {env: "dev"});
app.synth();
