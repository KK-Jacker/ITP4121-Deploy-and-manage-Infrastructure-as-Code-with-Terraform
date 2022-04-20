import {Construct} from "constructs";
import {MysqlServer, ResourceGroup} from "@cdktf/provider-azurerm";

interface MySQLServerConstructProps {
    resourceGroup: ResourceGroup;
}

export class MySQLServerConstruct extends Construct {
    public readonly mysqlServer: MysqlServer;

    constructor(scope: Construct, name: string, props: MySQLServerConstructProps) {
        super(scope, name);

        const {resourceGroup} = props;

        // create MySQL Server
        // https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/mysql_server
        this.mysqlServer = new MysqlServer(this, "iShare lib MySQL Server", {
            name: process.env.PROJECT_NAME! + process.env.ENV,
            version: process.env.MYSQL_SERVER_VERSION!,
            skuName: process.env.MYSQL_SERVER_SKU_NAME!,
            storageMb: <number>(<unknown>process.env.MYSQL_SERVER_SKU_STORAGE_SIZE!),
            resourceGroupName: resourceGroup.name,
            location: resourceGroup.location,
            identity: [
                {
                    type: process.env.MYSQL_SERVER_IDENTITY_TYPE!,
                },
            ],
            administratorLogin: process.env.MYSQL_SERVER_ADMIN_USERNAME!,
            administratorLoginPassword: process.env.MYSQL_SERVER_ADMIN_PASSWORD!,
            publicNetworkAccessEnabled: true,
            sslEnforcementEnabled: false,
            geoRedundantBackupEnabled: true,
            dependsOn: [resourceGroup],
            tags: JSON.parse(process.env.AZURETAG!),
        });
    }
}
