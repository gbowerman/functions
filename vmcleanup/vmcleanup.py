"""vmcleanup - tool to clean up resources at the specified time"""
import datetime
import logging
import os

from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.resource import ResourceManagementClient
from dotenv import load_dotenv

# load Azure environment and start client connections
load_dotenv()
subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]
credentials = ServicePrincipalCredentials(
    client_id=os.environ["AZURE_CLIENT_ID"],
    secret=os.environ["AZURE_CLIENT_SECRET"],
    tenant=os.environ["AZURE_TENANT_ID"]
)
compute_client = ComputeManagementClient(credentials, subscription_id)
resource_client = ResourceManagementClient(credentials, subscription_id)


def shutdown_vm(rg_name, vm_name):
    """Stop deallocate the named virtual machine"""
    logging.info(f"Deallocating virtual machine: {vm_name}")
    compute_client.virtual_machines.deallocate(rg_name, vm_name)


def shutdown_vms_in_rg(rg_name):
    """Stop deallocate all the VMs in a resource group"""
    logging.info(f"Deallocating VMs in resource gorup: {rg_name}")
    for vm in compute_client.virtual_machines.list(rg_name):
        shutdown_vm(rg_name, vm.name)


def shutdown_vms_in_sub():
    """Stop deallocate all the VMs in an Azure subscription"""
    for resource_group in resource_client.resource_groups.list():
        logging.info(f"Deallocating all VMs in subscription")
        shutdown_vms_in_rg(resource_group.name)


def main():
    """main routine - start by checking parameters"""

    # check shutdown time
    if "SHUTDOWN_TIME" in os.environ:
        stop_time = os.environ["SHUTDOWN_TIME"]
    else:
        logging.error(f"SHUTDOWN_TIME not set")
        raise SystemExit("SHUTDOWN_TIME not set")

    # check current time
    date_time = datetime.datetime.now()
    time_str = date_time.strftime("%H:%M:%S")

    # shutdown VMs if current time later or equal to shutdown time
    if time_str >= stop_time:
        logging.info(f"Timer triggered at {time_str}")
        # check if a resource group is specified, else shutdown all VMs in subscription
        if "RESOURCE_GROUP" in os.environ:
            shutdown_vms_in_rg(os.environ["RESOURCE_GROUP"])
        else:
            shutdown_vms_in_sub()
    else: logging.info(f"Timer not triggered at {time_str}")

if __name__ == "__main__":
    main()
