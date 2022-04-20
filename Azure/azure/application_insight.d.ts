import { Construct } from "constructs";
import { ApplicationInsights, ResourceGroup } from "@cdktf/provider-azurerm";
interface ApplicationInsightsConstructProps {
    resourceGroup: ResourceGroup;
}
export declare class ApplicationInsightsConstruct extends Construct {
    readonly applicationInsights: ApplicationInsights;
    constructor(scope: Construct, name: string, props: ApplicationInsightsConstructProps);
}
export {};
