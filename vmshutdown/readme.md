# Azure VM Shutdown Function

The app takes a time of day, Azure subscription ID, and optionally an Azure resource group name as an app setting in the portal.

The app is set to run on a timer trigger, and each time it runs, if the specified time of day is past, it shuts down VMs in your subscription. 

If the Resource Group environment variable is set, it only shuts down VMs in the named resource group. If resource group is not set, it shuts down all VMs in the subscription.


### Required application variable settings
SHUTDOWN_TIME  HH:MM:SS  
AZURE_SUBSCRIPTION_ID  
AZURE_CLIENT_SECRET  
AZURE_TENANT_ID  

### Optional
RESOURCE_GROUP  

## Deployment
Set the crontab setting in function.json to the desired shutdown time in UTC. E.g. to shutdown at 5am UTC every day:

```
{
  "scriptFile": "__init__.py",
  "bindings": [
    {
      "name": "mytimer",
      "type": "timerTrigger",
      "direction": "in",
      "schedule": "0 0 5 * * *"
    }
  ]
}
```

### Publishing function after updating
```
py -3.6 -m venv .env
.env\scripts\activate
cd .\vmshutdown\
func azure functionapp publish azvmshutdown
```

## Usage

Required application variable settings:  
AZURE_SUBSCRIPTION_ID  
AZURE_CLIENT_SECRET  
AZURE_TENANT_ID 

Optional:  
RESOURCE_GROUP (only shutdown VMs in this resrouce group)  