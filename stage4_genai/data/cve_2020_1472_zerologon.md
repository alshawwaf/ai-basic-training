# CVE-2020-1472 — Zerologon

**CVSS:** 10.0 | **Severity:** Critical | **Disclosed:** 2020-08-11

## Summary
Zerologon is a privilege escalation vulnerability in the Microsoft Netlogon Remote Protocol (MS-NRPC). A flaw in the AES-CFB8 implementation of the Netlogon authentication handshake allows an unauthenticated attacker with network access to a domain controller to establish a Netlogon secure channel using an all-zero client credential. This lets the attacker reset the domain controller's machine account password, leading to full domain compromise. Exploitation takes approximately three seconds.

## Affected Products
- Windows Server 2008 R2 SP1
- Windows Server 2012 and 2012 R2
- Windows Server 2016
- Windows Server 2019
- Windows Server version 1903, 1909, 2004
- All Active Directory domain controller roles on affected Windows Server versions

## Attack Vector
The attacker sends Netlogon authentication requests (NetrServerReqChallenge / NetrServerAuthenticate3) to the domain controller over TCP port 135 / dynamic RPC ports. The Netlogon protocol uses AES-CFB8 with a client challenge as the initialization vector. By setting the client challenge to all zeros, the attacker can brute-force a valid session key in roughly 256 attempts (statistically ~1 in 256 chance per attempt), because AES-CFB8 with a zero IV produces a zero ciphertext for certain keys. Once authenticated, the attacker calls `NetrServerPasswordSet2` to set the DC machine account password to an empty string, then uses secretsdump or DCSync to extract all domain credentials including the `krbtgt` hash.

## Detection
- Windows Event ID 4742: "A computer account was changed" — look for the domain controller's own machine account password being reset
- Event ID 5805: "A machine account failed to authenticate" — repeated Netlogon authentication failures from a single source
- Network: high volume of RPC traffic to the domain controller's Netlogon service from a non-DC source within a short time window
- EDR / SIEM: detect tools such as Mimikatz (`lsadump::zerologon`), Impacket's `zerologon_tester.py`, or SharpZeroLogon

## Remediation
- **Patch:** Install the August 2020 security update (KB4571702 for Server 2019, KB4571703 for Server 2016) and enable enforcement mode via the `FullSecureChannelProtection` registry key
- **Workaround:** No effective workaround exists; patching is required. Monitor and restrict network access to domain controllers using firewall rules to limit RPC access to trusted hosts only

## MITRE ATT&CK
- T1068 — Exploitation for Privilege Escalation
- T1003.006 — OS Credential Dumping: DCSync
- T1098 — Account Manipulation

## References
- https://nvd.nist.gov/vuln/detail/CVE-2020-1472
- https://msrc.microsoft.com/update-guide/vulnerability/CVE-2020-1472
