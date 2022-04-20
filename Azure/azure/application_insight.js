"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.ApplicationInsightsConstruct = void 0;
const constructs_1 = require("constructs");
const provider_azurerm_1 = require("@cdktf/provider-azurerm");
class ApplicationInsightsConstruct extends constructs_1.Construct {
    constructor(scope, name, props) {
        super(scope, name);
        const { resourceGroup } = props;
        // create application insights
        // https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/application_insights#attributes-reference
        this.applicationInsights = new provider_azurerm_1.ApplicationInsights(this, " ITP4121-Project lib application_insights", {
            name: process.env.PROJECT_NAME + process.env.ENV,
            applicationType: process.env.APPLICATION_INSIGHTS_TYPE,
            resourceGroupName: resourceGroup.name,
            location: resourceGroup.location,
            dependsOn: [resourceGroup],
            tags: JSON.parse(process.env.AZURETAG),
        });
    }
}
exports.ApplicationInsightsConstruct = ApplicationInsightsConstruct;
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiYXBwbGljYXRpb25faW5zaWdodC5qcyIsInNvdXJjZVJvb3QiOiIiLCJzb3VyY2VzIjpbImFwcGxpY2F0aW9uX2luc2lnaHQudHMiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6Ijs7O0FBQUEsMkNBQXFDO0FBQ3JDLDhEQUEyRTtBQU0zRSxNQUFhLDRCQUE2QixTQUFRLHNCQUFTO0lBR3ZELFlBQ0ksS0FBZ0IsRUFDaEIsSUFBWSxFQUNaLEtBQXdDO1FBRXhDLEtBQUssQ0FBQyxLQUFLLEVBQUUsSUFBSSxDQUFDLENBQUM7UUFFbkIsTUFBTSxFQUFDLGFBQWEsRUFBQyxHQUFHLEtBQUssQ0FBQztRQUU5Qiw4QkFBOEI7UUFDOUIsNEhBQTRIO1FBQzVILElBQUksQ0FBQyxtQkFBbUIsR0FBRyxJQUFJLHNDQUFtQixDQUM5QyxJQUFJLEVBQ0osMkNBQTJDLEVBQzNDO1lBQ0ksSUFBSSxFQUFFLE9BQU8sQ0FBQyxHQUFHLENBQUMsWUFBYSxHQUFHLE9BQU8sQ0FBQyxHQUFHLENBQUMsR0FBRztZQUNqRCxlQUFlLEVBQUUsT0FBTyxDQUFDLEdBQUcsQ0FBQyx5QkFBMEI7WUFDdkQsaUJBQWlCLEVBQUUsYUFBYSxDQUFDLElBQUk7WUFDckMsUUFBUSxFQUFFLGFBQWEsQ0FBQyxRQUFRO1lBQ2hDLFNBQVMsRUFBRSxDQUFDLGFBQWEsQ0FBQztZQUMxQixJQUFJLEVBQUUsSUFBSSxDQUFDLEtBQUssQ0FBQyxPQUFPLENBQUMsR0FBRyxDQUFDLFFBQVMsQ0FBQztTQUMxQyxDQUNKLENBQUM7SUFDTixDQUFDO0NBQ0o7QUEzQkQsb0VBMkJDIiwic291cmNlc0NvbnRlbnQiOlsiaW1wb3J0IHtDb25zdHJ1Y3R9IGZyb20gXCJjb25zdHJ1Y3RzXCI7XG5pbXBvcnQge0FwcGxpY2F0aW9uSW5zaWdodHMsIFJlc291cmNlR3JvdXB9IGZyb20gXCJAY2RrdGYvcHJvdmlkZXItYXp1cmVybVwiO1xuXG5pbnRlcmZhY2UgQXBwbGljYXRpb25JbnNpZ2h0c0NvbnN0cnVjdFByb3BzIHtcbiAgICByZXNvdXJjZUdyb3VwOiBSZXNvdXJjZUdyb3VwO1xufVxuXG5leHBvcnQgY2xhc3MgQXBwbGljYXRpb25JbnNpZ2h0c0NvbnN0cnVjdCBleHRlbmRzIENvbnN0cnVjdCB7XG4gICAgcHVibGljIHJlYWRvbmx5IGFwcGxpY2F0aW9uSW5zaWdodHM6IEFwcGxpY2F0aW9uSW5zaWdodHM7XG5cbiAgICBjb25zdHJ1Y3RvcihcbiAgICAgICAgc2NvcGU6IENvbnN0cnVjdCxcbiAgICAgICAgbmFtZTogc3RyaW5nLFxuICAgICAgICBwcm9wczogQXBwbGljYXRpb25JbnNpZ2h0c0NvbnN0cnVjdFByb3BzXG4gICAgKSB7XG4gICAgICAgIHN1cGVyKHNjb3BlLCBuYW1lKTtcblxuICAgICAgICBjb25zdCB7cmVzb3VyY2VHcm91cH0gPSBwcm9wcztcblxuICAgICAgICAvLyBjcmVhdGUgYXBwbGljYXRpb24gaW5zaWdodHNcbiAgICAgICAgLy8gaHR0cHM6Ly9yZWdpc3RyeS50ZXJyYWZvcm0uaW8vcHJvdmlkZXJzL2hhc2hpY29ycC9henVyZXJtL2xhdGVzdC9kb2NzL3Jlc291cmNlcy9hcHBsaWNhdGlvbl9pbnNpZ2h0cyNhdHRyaWJ1dGVzLXJlZmVyZW5jZVxuICAgICAgICB0aGlzLmFwcGxpY2F0aW9uSW5zaWdodHMgPSBuZXcgQXBwbGljYXRpb25JbnNpZ2h0cyhcbiAgICAgICAgICAgIHRoaXMsXG4gICAgICAgICAgICBcIiBJVFA0MTIxLVByb2plY3QgbGliIGFwcGxpY2F0aW9uX2luc2lnaHRzXCIsXG4gICAgICAgICAgICB7XG4gICAgICAgICAgICAgICAgbmFtZTogcHJvY2Vzcy5lbnYuUFJPSkVDVF9OQU1FISArIHByb2Nlc3MuZW52LkVOVixcbiAgICAgICAgICAgICAgICBhcHBsaWNhdGlvblR5cGU6IHByb2Nlc3MuZW52LkFQUExJQ0FUSU9OX0lOU0lHSFRTX1RZUEUhLFxuICAgICAgICAgICAgICAgIHJlc291cmNlR3JvdXBOYW1lOiByZXNvdXJjZUdyb3VwLm5hbWUsXG4gICAgICAgICAgICAgICAgbG9jYXRpb246IHJlc291cmNlR3JvdXAubG9jYXRpb24sXG4gICAgICAgICAgICAgICAgZGVwZW5kc09uOiBbcmVzb3VyY2VHcm91cF0sXG4gICAgICAgICAgICAgICAgdGFnczogSlNPTi5wYXJzZShwcm9jZXNzLmVudi5BWlVSRVRBRyEpLFxuICAgICAgICAgICAgfVxuICAgICAgICApO1xuICAgIH1cbn1cbiJdfQ==