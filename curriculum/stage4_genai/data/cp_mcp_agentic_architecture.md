# Check Point MCP and Agentic AI Architecture

## Overview

Check Point provides a set of MCP (Model Context Protocol) servers that enable AI agents to orchestrate security operations programmatically. MCP is an open standard that defines how AI agents discover, authenticate to, and invoke tools exposed by external systems. By publishing MCP servers, Check Point allows autonomous agents and LLM-powered copilots to interact with firewalls, threat intelligence, SASE infrastructure, and management APIs through a standardised protocol.

## What Is MCP

The Model Context Protocol is an open standard for AI agent tool access. It defines a structured interface through which an AI agent can:

1. **Discover** available tools and their parameters
2. **Authenticate** using scoped credentials with defined permissions
3. **Invoke** tools by passing structured input and receiving structured output
4. **Chain** multiple tool calls to accomplish multi-step workflows

MCP replaces ad hoc API integrations with a consistent protocol that supports capability discovery, input validation, and access control — critical requirements when autonomous agents are executing security-sensitive operations.

## Check Point MCP Servers

Check Point publishes 13 MCP servers covering the major product areas:

| Server Category | Coverage |
|----------------|----------|
| Management | Policy management, rule creation, object configuration, session handling |
| Threat Prevention | Threat intelligence lookups, reputation checks, IOC queries, sandbox submission |
| Quantum Gateways | Firewall status, interface monitoring, VPN tunnel management, routing tables |
| Harmony SASE | SASE policy configuration, user access monitoring, SDP gateway management |
| Diagnostics | Log queries, health checks, performance metrics, troubleshooting commands |

## Available Tools (Examples)

Representative tools exposed via MCP include: `list_firewalls`, `get_policy`, `add_rule`, `check_reputation`, `query_logs`, `submit_for_sandboxing`, `get_threat_indicators`, `list_vpn_tunnels`, `get_gateway_status`, and `run_diagnostic`.

## Security Considerations

Granting an AI agent access to security infrastructure demands rigorous controls:

- **Least-privilege tool access:** Each agent receives only the MCP tool bindings required for its specific task — a reporting agent should not have `add_rule` access
- **Invocation monitoring:** Every MCP call is logged with full context — agent identity, tool name, parameters, timestamp, and response summary
- **Data flow controls:** Sensitive data returned by tools (credentials, internal IPs, policy details) is tracked to prevent exfiltration through the agent's output channel
- **Scoped authentication:** MCP credentials are scoped per agent and per server, with automatic rotation and revocation capabilities
