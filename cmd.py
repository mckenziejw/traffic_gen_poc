sites = mist.orgs.sites.listOrgSites(session, org_id=org_id).data
site = filter_assets(sites, filter={'name':'Durham'})
devices = mist.orgs.inventory.getOrgInventory(session, org_id=org_id, type='gateway').data
device = filter_assets(devices, filter={'name':'SSR-1'})
tshoot_edge = mist.orgs.troubleshoot.troubleshootOrg(session, org_id=org_id, site_id=site['id'], mac=device['mac'], type='wan').data
tshoot_edge
org_alarms = mist.orgs.alarms.searchOrgAlarms(session, org_id=org_id).data
org_alarm_df = pd.DataFrame(org_alarms['results'])
org_alarm_df
site_alarms = mist.sites.alarms.searchSiteAlarms(session, site_id=site['id']).data
site_alarms_df = pd.DataFrame(site_alarms['results'])
site_alarms_df