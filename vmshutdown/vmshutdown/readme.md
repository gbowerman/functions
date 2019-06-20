# VM Shutdown Azure Function

This app takes a time of day, Azure subscription ID, and optionally an Azure resource group name as an app setting in the portal.

The app is set to run on a timer trigger, and each time it runs, if the specified time of day is past, it shuts down VMs in your subscription. 

If the RESOURCE_GRUOP environment variable is set, it only shuts down VMs in the named resource group. If resource group is not set, it shuts down all VMs in the subscription.

### Required application variable settings
SHUTDOWN_TIME  HH:MM:SS  
AZURE_SUBSCRIPTION_ID  
AZURE_CLIENT_SECRET  
AZURE_TENANT_ID  

### Optional
RESOURCE_GROUP  

