# Lab 3: netops-agent

**An intelligent network troubleshooting agent that orchestrates end-to-end incident resolution by integrating ServiceNow ticket management, Splunk log analysis.**

This lab demonstrates the power of multi-system orchestration with AI agents—going from ticket detection to root cause analysis to actionable recommendations, all guided by historical knowledge patterns.

---

## What You'll Learn

In this lab, you'll experience:

- **Multi-system orchestration**: Coordinating actions across ServiceNow and Splunk
- **Knowledge base integration**: Leveraging historical incident patterns via vector search
- **Systematic troubleshooting**: Following structured workflows for consistent results
- **Platform connectors**: Using NCP-managed integrations without custom code

---

## Prerequisites

**Environment Setup:**
Follow the [root README](../README.md) for Python environment setup, NCP SDK installation.

**Lab-Specific Requirements:**
This lab requires access to:
- ServiceNow connector (for ticket management)
- Splunk connector (for log analysis)

*(These are pre-configured for the workshop)*

---

## Project Structure

```
lab-03-netops-agent/
├── ncp.toml                          # Project configuration
├── requirements.txt                  # Python dependencies (none for this agent)
├── apt-requirements.txt              # System dependencies (none)
├── agents/
│   ├── __init__.py
│   └── main_agent.py                 # Agent definition with workflow instructions
├── tools/
│   └── __init__.py                   # No custom tools (uses connectors)
└── knowledge/                        # Historical incident patterns
    ├── arp-failure-pattern-001.md    # ARP process failure case from Sept 8
    ├── arp-failure-pattern-002.md    # Software upgrade ARP issue
    └── network-troubleshooting-guide.md  # General troubleshooting guide
```

**Key Features:**
- **No custom Python tools** - Everything uses platform connectors
- **Knowledge base** - Historical patterns automatically indexed for vector search
- **Comprehensive instructions** - 200+ lines guiding the agent through workflows

---

## Getting Started

Follow the root README for the complete deployment workflow. Quick reference:

```bash
# Navigate to this lab
cd lab-03-netops-agent

# Authenticate with platform
ncp authenticate

# Validate project
ncp validate .

# Package agent
ncp package -o netops-agent.ncp

# Deploy to platform
ncp deploy netops-agent.ncp

# Test interactively
ncp playground --agent netops-agent --show-tools
```

---

## Sample Questions

1. Fetch the incident details of `INC0010091`
2. Can you search for similar incidents in the past?


## Architecture

### Multi-System Integration

This agent integrates multiple systems without writing custom Python code:

**1. ServiceNow Connector** (`servicenow`)
- Fetch incident tickets
- Search historical tickets
- Add comments to tickets
- Update ticket status

**2. Splunk Connector** (`Splunk`)
- Search system logs (SYSLOGs)
- Filter by time range, hostname, patterns
- Identify error patterns and anomalies

**3. Knowledge Base** (`knowledge/` directory)
- Markdown files with historical incident patterns
- Automatically indexed by the platform
- Vector similarity search for pattern matching

### Agent Definition

```python
from ncp import Agent

agent = Agent(
    name="netops-troubleshooter-agent",
    description="Intelligent network troubleshooting assistant...",
    instructions="""
    # Comprehensive workflow instructions
    # Guides the agent through systematic troubleshooting
    # Specifies tool usage, workflow phases
    """,
    tools=[],  # No custom tools!
    connectors=["servicenow", "Splunk"],  # Platform-managed
)
```

**Key Design Decisions:**
- **Zero custom Python tools**: All functionality comes from platform connectors
- **Instruction-driven**: Comprehensive instructions guide agent behavior
- **Knowledge-enhanced**: Historical patterns inform current troubleshooting

---

## Experiment and Extend

Now that you understand how the agent works, try these modifications:

### 1. Modify Agent Behavior

**Change the instructions** in `agents/main_agent.py`:
- Add additional workflow phases
- Adjust the communication style
- Add more detailed explanations
- Modify safety constraints

**Example**: Add a "pre-remediation backup" phase that checks current configuration before making changes.

### 2. Expand the Knowledge Base

**Add new patterns** to the `knowledge/` directory:
- Create a new markdown file describing a different network issue (BGP flapping, interface errors, etc.)
- Include symptoms, root cause, resolution steps, log examples
- Redeploy the agent to index the new knowledge
- Test if the agent can find and use your new pattern

### 3. Test Different Scenarios

**Try different queries**:
- "Find tickets related to BGP issues"
- "Search logs for interface down events"
- "Analyze logs for network connectivity problems"

Observe how the agent adapts its workflow to different problem types.

### 4. Build Your Own Agent

Use this as a template to create agents for:
- **Security incident response**: Integrate with SIEM, firewall management
- **Configuration management**: Integrate with Git, validate config changes

---

## Key Takeaways

**No custom code needed** - Connectors + instructions = powerful automation
**Knowledge compounds** - Historical patterns make future troubleshooting faster
**Systematic workflows** - Structured phases ensure consistent, thorough results
**Multi-system orchestration** - AI agents excel at coordinating across platforms
**Instruction quality matters** - Well-written instructions drive agent effectiveness

---

## Next Steps

- **Deploy and test this agent** with the example workflow
- **Experiment with modifications** from the ideas above
- **Create your own knowledge base entries** for issues in your network
- **If you haven't completed Lab 1**, try the netbox-agent for data analytics experience
- **Build your own agent** for a use case in your environment