import { Construct } from "constructs";
import { MysqlFirewallRule, MysqlServer, ResourceGroup } from "@cdktf/provider-azurerm";
interface MySQLFirewallConstructProps {
    resourceGroup: ResourceGroup;
    mysqlServer: MysqlServer;
}
export declare class MySQLFirewallConstruct extends Construct {
    readonly mysqlFirewallRule: MysqlFirewallRule;
    constructor(scope: Construct, name: string, props: MySQLFirewallConstructProps);
}
export {};
