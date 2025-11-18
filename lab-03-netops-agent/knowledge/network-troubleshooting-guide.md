# Network Troubleshooting Guide

## Overview

This guide provides systematic troubleshooting approaches for common network issues in SONiC-based datacenter environments.

## Common Issue Patterns

### 1. VM/Workload Reachability Failures

#### Symptoms

- VM ping failures from external networks
- Partial or complete connectivity loss
- Intermittent packet loss
- ARP resolution failures

#### Common Root Causes

**A. ARP Process Issues**

- Process stopped/crashed
- Memory exhaustion
- Configuration errors
- Software bugs

**Investigation Steps:**

1. Check process status: `docker exec swss supervisorctl status arp_update`
2. Review SYSLOG for process_tracker alerts
3. Examine ARP table: `show arp`
4. Check interface status: `show interfaces status`

**B. Interface Issues**

- Physical link down
- Interface errors (CRC, drops)
- Speed/duplex mismatch
- Transceiver problems

**Investigation Steps:**

1. Check interface status: `show interfaces status`
2. Review interface counters: `show interfaces counters`
3. Check transceiver status: `show interfaces transceiver`

**C. Routing Issues**

- BGP session down
- Route missing
- Next-hop unreachable
- Routing loop

**Investigation Steps:**

1. Check BGP status: `show ip bgp summary`
2. Verify route table: `show ip route`
3. Test next-hop reachability: `ping <next-hop-ip>`

### 2. ARP Process Failure Troubleshooting

#### Detection

Look for these log patterns in Splunk:

```
"process_tracker" AND "arp_update" AND ("NOT running" OR "STOPPED" OR "crashed")
"arp_mgr" AND ("failure" OR "error" OR "cleanup")
"systemd" AND "arp_update.service" AND ("failed" OR "restart")
```

#### Diagnosis Steps

1. **Verify Process State**

   ```bash
   docker exec swss supervisorctl status arp_update
   ps aux | grep arp_update
   ```

2. **Check Recent Logs**
   Search Splunk for last 2 hours:

   ```
   index=network host="<switch-ip>" "arp_update" earliest=-2h
   ```

3. **Examine ARP Table**

   ```bash
   show arp
   show arp summary
   ```

4. **Check Memory and Resources**

   ```bash
   show system memory
   show processes cpu
   ```

#### Resolution Actions

**Standard Resolution:**

```bash
# Restart the ARP process
docker exec swss supervisorctl restart arp_update

# Verify restart successful
docker exec swss supervisorctl status arp_update

# Monitor for stability (wait 2-3 minutes)
tail -f /var/log/syslog | grep arp_update
```

**If Standard Restart Fails:**

```bash
# Force stop the process
docker exec swss supervisorctl stop arp_update
sudo pkill -9 arp_update

# Clear stale state
sudo rm -f /var/run/arp_update.pid

# Start fresh
docker exec swss supervisorctl start arp_update
```

#### Verification Steps

1. **Confirm Process Running**

   ```bash
    docker exec swss supervisorctl status arp_update
   ```

2. **Check Log Confirmation**
   Look for in Splunk:

   ```
   "arp_update restarted" OR "arp_update started"
   "PID changed" OR "running normally"
   ```

3. **Verify ARP Table Population**

   ```bash
   show arp | wc -l  # Should see entries being learned
   ```

4. **Test VM Connectivity**

   ```bash
   ping <vm-ip>
   ```

### 3. Log Analysis Patterns

#### Critical ARP Process Messages

**Process Stopped:**

```
Alert [P1] [swss] arp_update is NOT running (status: STOPPED)
```

→ **Action**: Restart service immediately

**Process Crashed:**

```
arp_update crashed (signal: SIGKILL)
process_tracker: arp_update terminated abnormally
```

→ **Action**: Check for memory issues, restart service

**Process Restarted Successfully:**

```
Alert [P1] [swss] arp_update restarted (PID changed: XXX → YYY)
process_tracker: arp_update running normally
```

→ **Confirmation**: Resolution successful

**Memory Issues:**

```
Memory allocation failed (OOM condition)
arp_update: Cannot allocate memory
```

→ **Action**: Check system memory, consider hotfix

#### Useful Splunk Queries

**Find ARP Process Issues:**

```
index=network sourcetype=syslog "process_tracker" "arp_update"
| eval status=case(
    like(_raw, "%NOT running%"), "stopped",
    like(_raw, "%crashed%"), "crashed",
    like(_raw, "%restarted%"), "restarted",
    like(_raw, "%running normally%"), "healthy"
  )
| stats count by host, status
```

**Correlate Issues with Connectivity:**

```
index=network (("arp_update" AND ("STOPPED" OR "crashed")) OR ("connectivity" AND "failure"))
| transaction host maxspan=10m
| table _time, host, _raw
```

**Timeline of Events:**

```
index=network host="<switch-ip>" (arp_update OR "connectivity failure" OR "VM reachability")
| sort _time
| table _time, severity, message
```

### 4. ServiceNow Integration

#### Ticket Update Format

**Root Cause Field:**

```
ARP update process failure on switch <switch-ip> (<hostname>).
Process stopped/crashed at <timestamp>, causing ARP table flush
and loss of MAC-to-IP mappings for connected workloads.
```

**Action Taken Field:**

```
1. Identified process failure via Splunk log analysis
2. Verified process state
3. Restarted arp_update service via Sonic MCP server
4. Monitored process stability for 5 minutes
5. Verified ARP table repopulation
6. Confirmed VM connectivity restoration
```

**Resolution Field:**

```
Service restarted successfully at <timestamp>.
ARP process running normally (PID: <new-pid>).
ARP table repopulated with <count> entries.
VM connectivity verified and restored.
No further action required.
```

#### Closure Codes

- **Resolved - Service Restart**: For standard ARP process restarts
- **Resolved - Hotfix Applied**: For issues requiring vendor patches
- **Resolved - Configuration Change**: For config-related issues

### 5. Decision Trees

#### VM Reachability Failure Decision Tree

```
VM Reachability Failed
│
├─ Check Switch Management Reachability
│  ├─ Unreachable → Check physical connectivity / management network
│  └─ Reachable → Continue
│
├─ Check Process Status (arp_update)
│  ├─ Stopped/Crashed → RESTART SERVICE → Verify → Resolve
│  ├─ Running → Continue
│  └─ Unknown → Check logs
│
├─ Check Interface Status
│  ├─ Down → Check physical layer / transceivers
│  └─ Up → Continue
│
├─ Check ARP Table
│  ├─ Empty → Possible arp_update issue → Check logs
│  └─ Populated → Check routing
│
└─ Check Routing (BGP)
   ├─ Session Down → Investigate BGP issue
   └─ Routes Missing → Investigate routing protocols
```

### 6. Best Practices

#### Before Making Changes

1. Always ask user for confirmation
2. Document current state (logs, config)
3. Have rollback plan ready
4. Verify backup connectivity paths if available

#### During Troubleshooting

1. Follow systematic approach (don't skip steps)
2. Document findings as you go
3. Correlate events with timelines
4. Keep user informed of progress

#### After Resolution

1. Verify solution thoroughly
2. Monitor for stability (5-10 minutes)
3. Update documentation
4. Close ticket with detailed notes

## Quick Reference

### SONiC Commands for ARP Troubleshooting

```bash
# Check process status
docker exec swss supervisorctl status arp_update
show processes | grep arp

# View ARP table
show arp
show arp summary
show arp <ip-address>

# Interface checks
show interfaces status
show interfaces counters
show ip interface

# System health
show system health
show system memory
show processes cpu

# Logs
show logging | grep arp
tail -f /var/log/syslog
```

### Splunk Search Templates

```
# Last 1 hour ARP issues
index=network "arp_update" earliest=-1h

# Specific switch logs
index=network host="10.1.1.10"

# Critical process errors
index=network severity=critical "process_tracker"

# Time correlation
ndex=network earliest="09/08/2025:19:45:00" latest="09/08/2025:19:50:00"
```

### Common Time Ranges for Investigation

- **Incident correlation**: ±15 minutes around reported issue
- **Process stability**: 5-10 minutes after restart
- **Pattern analysis**: Last 7 days
- **Trend analysis**: Last 30 days

## Related Documentation

- SONiC Process Management Guide
- ARP Protocol RFC 826
- Data Center Network Design Best Practices
- Incident Response Procedures
