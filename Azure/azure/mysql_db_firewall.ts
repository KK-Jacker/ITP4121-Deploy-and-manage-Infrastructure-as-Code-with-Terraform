import {Construct} from "constructs";
import {MysqlFirewallRule, MysqlServer, ResourceGroup,} from "@cdktf/provider-azurerm";

interface MySQLFirewallConstructProps {
    resourceGroup: ResourceGroup;
    mysqlServer: MysqlServer;
}

export class MySQLFirewallConstruct extends Construct {
    public readonly mysqlFirewallRule: MysqlFirewallRule;

    constructor(scope: Construct, name: string, props: MySQLFirewallConstructProps) {
        super(scope, name);

        const {resourceGroup, mysqlServer} = props;

        // create application insights
        // https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/application_insights#attributes-reference
        this.mysqlFirewallRule = new MysqlFirewallRule(
            this,
            "itp4121project lib MySQL Server Firewall",
            {
                name: process.env.PROJECT_NAME! + process.env.ENV,
                resourceGroupName: resourceGroup.name,
                serverName: mysqlServer.name,
                startIpAddress: process.env.MYSQL_FIREWALL_START_IP!,
                endIpAddress: process.env.MYSQL_FIREWALL_END_IP!,
                dependsOn: [mysqlServer],
            }
        );
    }
}
