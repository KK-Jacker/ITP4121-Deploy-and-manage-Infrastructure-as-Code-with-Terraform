import {Construct} from "constructs";
import {MysqlDatabase, MysqlServer, ResourceGroup,} from "@cdktf/provider-azurerm";
import {Resource} from "@cdktf/provider-null";

interface MySQLDatabaseConstructProps {
    resourceGroup: ResourceGroup;
    mysqlServer: MysqlServer;
}

export class MySQLDatabaseConstruct extends Construct {
    public readonly mysqlDatabase: MysqlDatabase;

    constructor(scope: Construct, name: string, props: MySQLDatabaseConstructProps) {
        super(scope, name);
        const {resourceGroup, mysqlServer} = props;

        // create MySQL Database
        // https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/mysql_database
        this.mysqlDatabase = new MysqlDatabase(
            this,
            "itp4121project lib MySQL Server Firewall",
            {
                name: process.env.PROJECT_NAME! + process.env.ENV,
                resourceGroupName: resourceGroup.name,
                serverName: mysqlServer.name,
                charset: process.env.MYSQL_DATABASE_CHARSET!,
                collation: process.env.MYSQL_DATABASE_COLLATION!,
                dependsOn: [mysqlServer],
            }
        );
        const sqluploadtableNullResource = new Resource(this, "upload table", {
            triggers: {
            },
        });
        const serverentry = this.mysqlDatabase.serverName + ".mysql.database.azure.com"
        const username = process.env.MYSQL_SERVER_ADMIN_USERNAME + "@" + this.mysqlDatabase.serverName
        const password = process.env.MYSQL_SERVER_ADMIN_PASSWORD;
        const database = process.env.MYSQL_SCHEMA_NAME;
        sqluploadtableNullResource.addOverride(
            "provisioner.local-exec.command", `sleep 30 && mysql -h ${serverentry} -u ${username} --password=${password} --skip-ssl -e "CREATE DATABASE IF NOT EXISTS ${database}" && mysql -h ${serverentry} -u ${username} --password=${password} --skip-ssl --force ${database} < ../../../pc_donation/mysql.sql`
        );
    }
}
