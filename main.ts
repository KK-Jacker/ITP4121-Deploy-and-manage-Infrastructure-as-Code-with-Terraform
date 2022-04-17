import {Construct} from "constructs";
import {App, /*TerraformOutput,*/ TerraformStack} from "cdktf";
import {resolve} from "path";
import {config, parse} from "dotenv";
import * as fs from "fs";
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



    }
}

const app = new App();
new MainStack(app, "ITP4121-Project", {env: "dev"});
app.synth();
