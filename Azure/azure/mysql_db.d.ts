import { Construct } from "constructs";
import { MysqlDatabase, MysqlServer, ResourceGroup } from "@cdktf/provider-azurerm";
interface MySQLDatabaseConstructProps {
    resourceGroup: ResourceGroup;
    mysqlServer: MysqlServer;
}
export declare class MySQLDatabaseConstruct extends Construct {
    readonly mysqlDatabase: MysqlDatabase;
    constructor(scope: Construct, name: string, props: MySQLDatabaseConstructProps);
}
export {};
