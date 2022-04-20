import { Construct } from "constructs";
export declare class AzureAdConstruct extends Construct {
    readonly servicePrincipalObjectId: string;
    readonly servicePrincipalAppId: string;
    readonly servicePrincipalTenantId: string;
    readonly servicePrincipalPassword: string;
    constructor(scope: Construct, name: string);
}
