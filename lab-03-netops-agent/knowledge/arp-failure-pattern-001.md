# Historical Incident: ARP Update Process Failure

## Ticket Information

- **Ticket ID**: INC0011234
- **Date**: 2025-09-08
- **Priority**: P1 - Critical
- **Category**: Network Infrastructure
- **Subcategory**: Connectivity Issue

## Incident Summary

VM or Workload reachability failed on datacenter fabric leaf switch. Multiple VMs behind the switch became unreachable simultaneously.

## Affected Components

- **Switch**: fab1leaf2-dc01-prod (10.10.5.42)
- **VM IP Range**: 192.168.100.0/24
- **Number of affected VMs**: 15
- **Impact**: Complete connectivity loss to workloads

## Symptoms Observed

1. VM ping tests failing from external networks
2. ARP table not updating on the leaf switch
3. MAC address entries expiring from forwarding table
4. Traffic drops on workload-facing interfaces
5. No new ARP entries being learned

## Root Cause Analysis

The `arp_update` process on the SONiC switch stopped unexpectedly, causing:

- ARP cache management failure
- Inability to refresh existing ARP entries
- Automatic ARP table flush after timeout
- Loss of Layer 2 to Layer 3 mapping information

### Key Log Entries

```
2025-09-08 19:48:26.621561 fab1leaf2-dc01-prod NOTICE process_tracker: Alert [P1] [swss] arp_update is NOT running (status: STOPPED)
2025-09-08 19:48:26.622104 fab1leaf2-dc01-prod WARNING arp_mgr: ARP table cleanup initiated due to process failure
2025-09-08 19:48:27.105523 fab1leaf2-dc01-prod ERROR forwarding: Multiple ARP entries expired, traffic disruption expected
```

## Investigation Steps Taken

1. Checked switch management interface connectivity - OK
2. Verified routing protocols (BGP) status - Running normally
3. Examined interface status - All UP
4. Reviewed process status - Found `arp_update` STOPPED
5. Checked SYSLOG for process crashes - Confirmed process failure

## Resolution

Restarted the `arp_update` service on the affected switch using the command:

```bash
docker exec swss supervisorctl restart arp_update

```

### Post-Resolution Verification

```
2025-09-08 19:49:20.422628 fab1leaf2-dc01-prod NOTICE process_tracker: Alert [P1] [swss] arp_update restarted (PID changed: 283 → 331)
2025-09-08 19:49:21.105823 fab1leaf2-dc01-prod INFO arp_mgr: ARP table rebuild initiated
2025-09-08 19:49:35.442156 fab1leaf2-dc01-prod INFO arp_mgr: 47 ARP entries learned successfully
```

## Outcome

- Service restart successful
- ARP process resumed normal operation
- MAC/IP bindings relearned within 30 seconds
- VM connectivity fully restored
- No further incidents reported

## Resolution Time

- Detection to identification: 8 minutes
- Identification to resolution: 4 minutes
- Total resolution time: 12 minutes

## Prevention Recommendations

1. Enable process monitoring with automatic restart
2. Configure process health checks
3. Set up proactive alerting for process state changes
4. Review process logs for crash patterns
5. Consider implementing process redundancy

## Related Tickets

- INC0011235 - Similar ARP issue on different leaf switch (2025-09-15)
- INC0010876 - ARP timeout alerts (2025-08-20)

## Tags

`arp`, `process-failure`, `vm-connectivity`, `datacenter`, `sonic`, `leaf-switch`, `critical`
