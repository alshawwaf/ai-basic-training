# CVE-2024-3094 — XZ Utils Backdoor

**CVSS:** 10.0 | **Severity:** Critical | **Disclosed:** 2024-03-29

## Summary
CVE-2024-3094 is a supply chain compromise of XZ Utils versions 5.6.0 and 5.6.1. A malicious maintainer ("Jia Tan") introduced obfuscated backdoor code into the liblzma build process over a period of two years. The backdoor targets the OpenSSH server (sshd) on systemd-based Linux distributions where sshd is patched to link against libsystemd, which in turn links liblzma. The injected code hooks the RSA public key verification routine, allowing the attacker to send a crafted SSH authentication payload that executes arbitrary commands before authentication completes.

## Affected Products
- XZ Utils 5.6.0 and 5.6.1 (source tarballs only; the backdoor code was not present in the git repository)
- Fedora 40 and Fedora Rawhide (shipped affected packages briefly)
- Debian Sid/Unstable (testing packages)
- openSUSE Tumbleweed and MicroOS (briefly affected)
- Kali Linux (rolling, briefly affected)
- Stable releases of Debian, Ubuntu LTS, RHEL, and SUSE Enterprise were NOT affected

## Attack Vector
The backdoor modifies liblzma at build time through a malicious `build-to-host.m4` script included only in release tarballs. At runtime, the compromised `liblzma.so` uses an IFUNC resolver to intercept the `RSA_public_decrypt` function in the OpenSSH process. When the attacker sends a specially crafted certificate during SSH key exchange, the backdoor extracts a payload from the certificate's CA signing key field, decrypts it with a hardcoded Ed448 key, and executes the result via `system()` as the root user before authentication.

## Detection
- Check installed XZ version: `xz --version` (affected: 5.6.0 or 5.6.1)
- Verify liblzma with Vegard Nossum's detection script: check for unexpected IFUNC symbols in `liblzma.so`
- Behavioral: sshd processes exhibiting unusual latency or unexpected child process spawning
- Compare the SHA-256 hash of installed `liblzma.so.5.6.0` or `liblzma.so.5.6.1` against known-compromised hashes published by distribution security teams

## Remediation
- **Patch:** Downgrade to XZ Utils 5.4.6 (last known-good release) or upgrade to 5.6.2+ once available with the backdoor removed
- **Workaround:** Rebuild XZ Utils from the git source (which did not contain the backdoor) rather than from release tarballs

## MITRE ATT&CK
- T1195.002 — Supply Chain Compromise: Compromise Software Supply Chain
- T1574.006 — Hijack Execution Flow: Dynamic Linker Hijacking
- T1556.004 — Modify Authentication Process: Network Device Authentication

## References
- https://nvd.nist.gov/vuln/detail/CVE-2024-3094
- https://www.openwall.com/lists/oss-security/2024/03/29/4
