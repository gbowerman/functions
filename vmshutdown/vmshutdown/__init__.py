"""vmcleanup - tool to clean up resources at the specified time"""
import logging
import os
import datetime

import azure.functions as func
from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.resource import ResourceManagementClient


def shutdown_vm(compute_client, rg_name, vm_name):
    """Stop deallocate the named virtual machine"""
    logging.info(f"Deallocating virtual machine: {vm_name}")
    compute_client.virtual_machines.deallocate(rg_name, vm_name)


def shutdown_vms_in_rg(compute_client, rg_name):
    """Stop deallocate all the VMs in a resource group"""
    logging.info(f"Deallocating VMs in resource group: {rg_name}")
    for vm in compute_client.virtual_machines.list(rg_name):
        shutdown_vm(compute_client, rg_name, vm.name)


def shutdown_vms_in_sub(compute_client, resource_client):
    """Stop deallocate all the VMs in an Azure subscription"""
    logging.info(f"Deallocating all VMs in subscription")
    for resource_group in resource_client.resource_groups.list():
        shutdown_vms_in_rg(compute_client, resource_group.name)


def main(mytimer: func.TimerRequest) -> None:
    '''The main function triggered by the cron job'''
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('VM Shutdown timer is past due!')

    # shutdown VMs
    logging.info(f"VM shutdown routine triggered at {utc_timestamp}")

    # connect to Azure (note: only connecting if stop_time is triggered)
    subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]
    credentials = ServicePrincipalCredentials(
        client_id=os.environ["AZURE_CLIENT_ID"],
        secret=os.environ["AZURE_CLIENT_SECRET"],
        tenant=os.environ["AZURE_TENANT_ID"]
    )
    compute_client = ComputeManagementClient(credentials, subscription_id)

    # check if a resource group is specified, else shutdown all VMs in subscription
    if "RESOURCE_GROUP" in os.environ:
        shutdown_vms_in_rg(compute_client, os.environ["RESOURCE_GROUP"])
    else:
        resource_client = ResourceManagementClient(credentials, subscription_id)
        shutdown_vms_in_sub(compute_client, resource_client)

    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()
    logging.info(f"VM shutdown timer trigger function completed at {utc_timestamp}")
