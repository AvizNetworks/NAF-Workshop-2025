# Historical Incident: ARP Process Crash After Software Upgrade

## Ticket Information

- **Ticket ID**: INC0011567
- **Date**: 2025-09-15
- **Priority**: P1 - Critical
- **Category**: Network Infrastructure
- **Subcategory**: Service Disruption

## Incident Summary

Intermittent VM reachability issues following SONiC software upgrade on spine switch. VMs experiencing packet loss and connection timeouts.

## Affected Components

- **Switch**: fab1spine1-dc02-prod (10.10.6.10)
- **SONiC Version**: 202305 (recently upgraded from 202211)
- **Affected Workloads**: 8 VM clusters behind leaf switches
- **Impact**: Intermittent connectivity, 20-40% packet loss

## Symptoms Observed

1. Periodic ARP resolution failures
2. Ping packet loss (20-40%)
3. TCP connection establishment delays
4. ARP process showing high CPU usage before crash
5. Multiple restart attempts visible in logs

## Root Cause Analysis

The `arp_update` process encountered a compatibility issue with the new SONiC version, causing:

- Memory leak in ARP process
- Process crash after reaching memory threshold
- Automatic restart by systemd (but recurring crashes)
- Incomplete ARP table population between crashes

### Key Log Entries

```
2025-09-15 14:23:41.881234 fab1spine1-dc02-prod ERROR arp_update: Memory allocation failed (OOM condition)
2025-09-15 14:23:41.882019 fab1spine1-dc02-prod CRITICAL process_tracker: arp_update crashed (signal: SIGKILL)
2025-09-15 14:23:42.105432 fab1spine1-dc02-prod NOTICE systemd: arp_update.service: Service hold-off time over, scheduling restart
2025-09-15 14:23:42.556789 fab1spine1-dc02-prod WARNING systemd: arp_update.service: Start request repeated too quickly
2025-09-15 14:23:45.002341 fab1spine1-dc02-prod NOTICE process_tracker: arp_update started (PID: 1247)
```

## Investigation Steps Taken

1. Verified software upgrade completion - Successful
2. Checked process crash logs - Found memory issues
3. Reviewed known issues for SONiC 202305 - Found matching bug report
4. Analyzed memory utilization - ARP process consuming 85% before crash
5. Checked vendor release notes - Hotfix available

## Resolution

Applied a two-step resolution:

1. **Immediate Fix**: Restarted service with increased memory limits

   ```bash
   sudo docker exec swss supervisorctl restart arp_update
   ```

2. **Permanent Fix**: Applied vendor hotfix patch

   ```bash
   sudo sonic-installer install sonic-hotfix-202305.1.bin
   sudo reboot
   ```

### Post-Resolution Verification

```
2025-09-15 15:45:12.334567 fab1spine1-dc02-prod NOTICE process_tracker: arp_update running normally (PID: 2341, uptime: 1h 20m)
2025-09-15 15:45:15.123456 fab1spine1-dc02-prod INFO arp_mgr: ARP table stable, 156 entries maintained
2025-09-15 15:45:20.445566 fab1spine1-dc02-prod INFO monitoring: Memory usage normal (arp_update: 12% of allocated)
```

## Outcome

- Hotfix successfully applied
- Memory leak resolved
- ARP process stable (no crashes in 48-hour monitoring period)
- Packet loss eliminated
- VM connectivity fully restored

## Resolution Time

- Detection to identification: 25 minutes
- Identification to temporary fix: 5 minutes
- Temporary fix to permanent fix: 45 minutes (including reboot)
- Total resolution time: 75 minutes

## Prevention Recommendations

1. Review vendor release notes before upgrades
2. Test upgrades in staging environment first
3. Monitor process memory usage post-upgrade
4. Subscribe to vendor security and hotfix alerts
5. Implement automated rollback procedures for failed upgrades

## Lessons Learned

- Always check for known issues after software upgrades
- Monitor process health metrics for 48 hours post-upgrade
- Keep vendor support channels updated with deployment plans
- Document software versions across all devices
- Maintain a hotfix repository for quick deployment

## Related Tickets

- INC0011234 - Earlier ARP process failure (different root cause)
- INC0011598 - Similar issue on spine2 (same fix applied)
- CHG0009845 - Change request for SONiC upgrade

## Vendor Reference

- **Bug ID**: SONIC-12345
- **Hotfix Version**: 202305.1
- **KB Article**: KB-SONIC-ARP-MEM-001

## Tags

`arp`, `software-upgrade`, `memory-leak`, `hotfix`, `sonic`, `spine-switch`, `critical`
