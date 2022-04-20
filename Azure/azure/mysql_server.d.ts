import { Construct } from "constructs";
import { MysqlServer, ResourceGroup } from "@cdktf/provider-azurerm";
interface MySQLServerConstructProps {
    resourceGroup: ResourceGroup;
}
export declare class MySQLServerConstruct extends Construct {
    readonly mysqlServer: MysqlServer;
    constructor(scope: Construct, name: string, props: MySQLServerConstructProps);
}
export {};
