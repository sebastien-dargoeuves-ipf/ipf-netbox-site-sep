import os

from dotenv import load_dotenv, find_dotenv
import pynetbox
from ipfabric import IPFClient
from loguru import logger

def main():
    load_dotenv(find_dotenv(), override=True)
    ipf_url = os.getenv("IPF_URL", "https://ipfabric-instance.company.com")
    ipf_auth = os.getenv("IPF_TOKEN", "your_ipf_token")
    ipf_verify = eval(os.getenv("IPF_VERIFY", "False").title())
    netbox_url = os.getenv("NB_SERVER", "https://netbox.company.com")
    netbox_token = os.getenv("NB_TOKEN", "your_nb_token")
    netbox_site_mapper = os.getenv("NB_SITE_MAPPING", "site")
    logger.info(f"Import NetBox '{netbox_site_mapper}' to IP Fabric global attributes for site separation")
    
    logger.info(f"IP Fabric URL: {ipf_url}")
    ipf = IPFClient(base_url=ipf_url, auth=ipf_auth, verify=ipf_verify)

    logger.info(f"NetBox URL: {os.getenv('NB_SERVER')}")
    nbApi = pynetbox.api(url=netbox_url, token=netbox_token)
    nbApi.http_session.verify = False

    nb_devices = nbApi.dcim.devices.all()
    # Build the attributes dict based on the sn we have in NetBox and the location
    # you can replace 'site' by 'location' if you wish to use this field for the site name in IPF

    if new_attributes_sn_dict := {
        nb_dev.serial: {
            "sn": nb_dev.serial,
            "name": "siteName",
            "value": getattr(nb_dev, netbox_site_mapper).name if getattr(nb_dev, netbox_site_mapper) else "n/a",
        }
        for nb_dev in nb_devices
    }:
        push_sitename = input(f"Push the {len(new_attributes_sn_dict)} attributes to the Global Attributes of IP Fabric `{ipf_url}` (y/[n])? ")
        if push_sitename.lower() == "y":
            ipf.settings.global_attributes.set_attributes_by_sn(list(new_attributes_sn_dict.values()))
            logger.success("✅ Global Attributes updated!")
        else:
            logger.info("🚫 No action taken")

    # the above doesn't account for the SN in IP Fabric with constructed with a '/'
    # assumption: all children of a parent device belong to the same site
    ipf_devices = ipf.inventory.devices.all()
    if extra_attributes_list := [
        new_attributes_sn_dict[dev["sn"].split("/")[0]]
        for dev in ipf_devices
        if "/" in dev["sn"]
    ]:
        push_extra = input(f"{extra_attributes_list}\n🙋❔Push the extra attributes above to IP Fabric (y/[n])? ")
        if push_extra.lower() == "y":
            ipf.settings.global_attributes.set_attributes_by_sn(extra_attributes_list)
            logger.success("✅ Global Attributes updated!")
        else:
            logger.info("🚫 No action taken")

if __name__ == "__main__":
    main()
