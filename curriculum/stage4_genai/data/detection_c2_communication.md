# Detection Guide: Command and Control Communication

## Overview

Command and control (C2) is the channel an attacker uses to remotely operate within a compromised environment. Modern C2 frameworks disguise their traffic inside legitimate protocols — DNS, HTTPS, and cloud services — making network-level detection essential. Identifying C2 early limits the attacker's ability to exfiltrate data, deploy ransomware, or deepen their foothold.

## Indicators

| Source | Indicator | Description |
|--------|-----------|-------------|
| DNS logs | Subdomain labels with Shannon entropy > 3.5 | DNS tunnelling encodes data in subdomain strings, producing high-entropy queries |
| DNS logs | Abnormal volume of TXT record queries to a single domain | TXT records carry larger payloads, favoured by tunnelling tools like `iodine` and `dnscat2` |
| Proxy/firewall logs | Consistent request intervals (e.g. every 60s +/- jitter) | Beacon-style callbacks characteristic of Cobalt Strike, Sliver, and Mythic |
| Proxy logs | `Host` header differs from SNI or resolved IP belongs to a CDN | Domain fronting routes C2 traffic through legitimate CDN edge servers |
| Proxy logs | Non-standard or rare User-Agent strings | Many C2 frameworks ship with default or randomly generated User-Agent headers |

## Detection Rules

**Rule 1 — DNS tunnelling (high-entropy subdomains)**
```
filter:
  log_source: dns
  query_name: regex match '[a-z0-9]{20,}\.\w+\.\w+'
condition:
  entropy(subdomain_label) > 3.5
  AND query_count > 50 per 10 minutes to same base domain
level: high
```

**Rule 2 — Beaconing interval detection**
```
filter:
  log_source: proxy
condition:
  group connections by (src_ip, dest_domain)
  calculate inter-request intervals
  flag if standard_deviation < 5% of mean interval
  AND count > 30 in 1 hour
level: medium
```

**Rule 3 — Domain fronting detection**
```
filter:
  log_source: proxy (TLS-inspecting)
condition:
  HTTP Host header != TLS SNI value
  OR resolved IP belongs to known CDN range
     AND domain is not in corporate whitelist
level: high
```

## MITRE ATT&CK Mapping

| Technique ID | Name |
|-------------|------|
| T1071.004 | Application Layer Protocol: DNS |
| T1071.001 | Application Layer Protocol: Web Protocols |
| T1572 | Protocol Tunneling |
| T1090.004 | Proxy: Domain Fronting |
| T1573 | Encrypted Channel |

## False Positive Considerations

- CDN-hosted SaaS applications (Slack, Teams, OneDrive) naturally show domain fronting-like patterns. Maintain a whitelist of sanctioned cloud services.
- Anti-virus and endpoint agents phone home at regular intervals, mimicking beaconing. Exclude known security product domains.
- DKIM and SPF validation can generate bursts of TXT record queries that resemble DNS tunnelling.

## Response Actions

1. Capture a full packet trace of the suspected C2 channel for protocol analysis.
2. Identify all internal hosts communicating with the suspected C2 destination.
3. Block the C2 domain/IP at the firewall and DNS sinkhole level.
4. Investigate the originating host for malware, persistence mechanisms, and credential theft.
5. If DNS tunnelling is confirmed, audit DNS resolver configurations and consider enforcing DNS-over-HTTPS to a controlled resolver.
