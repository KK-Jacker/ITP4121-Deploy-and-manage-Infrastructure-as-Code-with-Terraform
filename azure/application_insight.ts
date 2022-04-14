import {Construct} from "constructs";
import {ApplicationInsights, ResourceGroup} from "@cdktf/provider-azurerm";

interface ApplicationInsightsConstructProps {
    resourceGroup: ResourceGroup;
}

export class ApplicationInsightsConstruct extends Construct {
    public readonly applicationInsights: ApplicationInsights;

    constructor(
        scope: Construct,
        name: string,
        props: ApplicationInsightsConstructProps
    ) {
        super(scope, name);

        const {resourceGroup} = props;

        // create application insights
        // https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/application_insights#attributes-reference
        this.applicationInsights = new ApplicationInsights(
            this,
            " ITP4121-Project lib application_insights",
            {
                name: process.env.PROJECT_NAME! + process.env.ENV,
                applicationType: process.env.APPLICATION_INSIGHTS_TYPE!,
                resourceGroupName: resourceGroup.name,
                location: resourceGroup.location,
                dependsOn: [resourceGroup],
                tags: JSON.parse(process.env.AZURETAG!),
            }
        );
    }
}
