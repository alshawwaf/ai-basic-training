# CVE-2023-44487 — HTTP/2 Rapid Reset

**CVSS:** 7.5 | **Severity:** High | **Disclosed:** 2023-10-10

## Summary
HTTP/2 Rapid Reset is a denial-of-service vulnerability inherent in the HTTP/2 protocol specification. An attacker opens a large number of HTTP/2 streams and immediately sends RST_STREAM frames to cancel each one. The server allocates resources to begin processing each stream before the cancellation arrives, but the client-side cost of sending a reset is negligible. This asymmetry allows a single client to overwhelm a server, producing DDoS attacks exceeding 300 million requests per second as observed in the wild.

## Affected Products
- Nginx (prior to patched builds, Oct 2023)
- Apache HTTP Server with mod_http2 (prior to 2.4.58)
- Microsoft IIS with HTTP/2 enabled
- Envoy Proxy (prior to 1.27.1 / 1.26.5 / 1.25.10)
- Golang net/http2 (prior to Go 1.21.3)
- Node.js (prior to 18.18.2 / 20.8.1)
- All cloud load balancers and CDNs supporting HTTP/2

## Attack Vector
The attacker establishes a single TCP connection with HTTP/2 negotiated via ALPN. It then sends HEADERS frames to open streams in rapid succession, immediately followed by RST_STREAM frames for each. Because the server begins request processing (header parsing, routing, backend dispatch) before processing the reset, the server's work vastly exceeds the client's. The attacker does not need to wait for responses, enabling millions of pseudo-requests per second from a small number of connections.

## Detection
- Monitor for an abnormal ratio of RST_STREAM frames to completed HTTP/2 responses
- Alert on sudden spikes in HTTP/2 stream creation rates per connection
- Web server access logs may show a surge of incomplete requests with status 0 or no logged response
- Network sensors: high volume of HTTP/2 frames on a single connection with minimal data transfer

## Remediation
- **Patch:** Update to Nginx with the rapid-reset mitigation, Apache 2.4.58+, Go 1.21.3+, Node.js 18.18.2+ / 20.8.1+, or Envoy 1.27.1+
- **Workaround:** Configure HTTP/2 concurrent stream limits (`http2_max_concurrent_streams` in Nginx) and implement rate limiting on stream resets per connection

## MITRE ATT&CK
- T1498.001 — Network Denial of Service: Direct Network Flood
- T1499.002 — Endpoint Denial of Service: Service Exhaustion Flood

## References
- https://nvd.nist.gov/vuln/detail/CVE-2023-44487
- https://www.cisa.gov/news-events/alerts/2023/10/10/http2-rapid-reset-vulnerability-cve-2023-44487
