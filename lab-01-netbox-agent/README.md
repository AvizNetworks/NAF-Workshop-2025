# Lab 1: netbox-agent

**An AI-powered network inventory analytics agent that transforms NetBox data into actionable insights through natural language queries and automated visualizations.**

This lab demonstrates the power of data-driven AI agents—turning complex inventory queries into simple conversations, complete with charts and analytics, all without writing SQL or custom scripts.

---

## What You'll Learn

In this lab, you'll experience:

- **Platform connector integration**: Using NCP-managed NetBox connector for inventory access
- **Data analytics with AI**: Transforming natural language into queries and insights
- **Multi-category analysis**: Exploring inventory from multiple angles (counts, status, hardware, OS, gaps)
- **MCP server for visualization**: Integrating Charts MCP Server to auto-generate charts
- **Zero-code analytics**: Building powerful analytics without writing Python tools

---

## Prerequisites

**Environment Setup:**
Follow the [root README](../README.md) for Python environment setup and NCP SDK installation.

**Lab-Specific Requirements:**
This lab requires access to:
- NetBox connector (for inventory data access)
- Charts MCP server (for visualization generation) - *added in Phase 2*

*(These are pre-configured for the workshop)*

---

## Project Structure

```
lab-01-netbox-agent/
├── ncp.toml                 # Project configuration
├── requirements.txt         # Python dependencies (none for this agent)
├── apt-requirements.txt     # System dependencies (none)
├── agents/
│   ├── __init__.py
│   └── main_agent.py        # Agent definition
└── tools/
    └── __init__.py          # No custom tools (uses connector + MCP)
```

**Key Features:**
- **No custom Python tools** - Everything uses NetBox connector and Charts MCP server
- **Natural language interface** - Ask questions in plain English
- **Progressive learning** - Start with data, add visualizations later

---

## Getting Started - Phase 1: NetBox Connector Only

We'll start by deploying the agent with just the NetBox connector to focus on data analysis.

```bash
# Navigate to this lab
cd lab-01-netbox-agent

# Authenticate with platform
# platform url: https://naflab2.aviznetworks.com:9001
# username: Your registered email address
# password: NAF@2025
ncp authenticate

# Validate project
ncp validate .

# Package agent
ncp package

# Deploy to platform
ncp deploy netbox-agent.ncp

# Test interactively
ncp playground --agent netbox-agent --show-tools
```

---

## Phase 1: Data Analysis with NetBox Connector

In this phase, explore NetBox inventory data through natural language queries. The agent will retrieve and analyze data without visualizations.

### 1. Basic Counts and Inventory

Get quick inventory counts and breakdowns:

- **"How many total devices do we have in NetBox?"**
- **"Show device count breakdown by manufacturer"**
- **"What's our inventory size per location via NetBox?"**
- **"List all devices and their basic information"**
- **"How many devices are at each site?"**

### 2. Status and Health Analysis

Monitor operational status across your network:

- **"What percentage of our inventory is currently online vs offline?"**
- **"Show me which sites have the most offline devices"**
- **"List all devices by their operational status (active/offline/planned)"**
- **"Which locations have devices in offline status?"**
- **"Show devices grouped by status for each site"**

### 3. Device Roles and Functions

Understand how your network is composed by function:

- **"Break down inventory by device role (router/switch/firewall/etc)"**
- **"Which device roles are most common in our network?"**
- **"How many devices of each role type do we have?"**
- **"List devices by role for each location"**

### 4. Hardware Analysis

Analyze hardware diversity and vendor concentration:

- **"Show the most common device models in our inventory"**
- **"What are the top 15 device models by count?"**
- **"List devices grouped by hardware manufacturer"**
- **"Are we over-concentrated on specific models?"**
- **"Show hardware diversity across manufacturers"**

### 5. Operating System Analysis

Track operating system versions and platforms:

- **"Display devices grouped by operating system version"**
- **"How many devices are running each OS type?"**
- **"List all operating systems in use across our network"**
- **"Show devices by OS platform (Cisco IOS/NX-OS, Arista EOS, etc)"**
- **"Which OS versions are most common?"**

### 6. Inventory Gaps and Data Quality

Identify incomplete or missing data:

- **"Show devices with missing data - which fields are commonly missing?"**
- **"Display incomplete device records (without location, role, or contact)"**
- **"Which devices are missing critical information?"**
- **"List devices that don't have an assigned role"**
- **"Find devices without location information"**

---

## Next Step: Enable Visualizations

Once you're comfortable with data analysis, enhance your agent with visualization capabilities by adding the Charts MCP Server.

### How to Enable Charts

**1. Edit the agent configuration:**

Open `agents/main_agent.py` and add or comment out the MCP server configuration and update the system prompt:

```python
from ncp import Agent, MCPConfig

agent = Agent(
    name="netbox-agent",
    description="Netbox Agent",
    instructions="""
    You are a helpful netbox agent. Your goal is to assist users with their tasks.

    Be:
    - Concise and clear in your responses
    - Helpful and friendly
    - Professional

    Use the available tools to accomplish tasks when appropriate.
    """,
    tools=[],
    connectors=["Netbox"],
    mcp_servers=[
        MCPConfig(
            transport_type="sse",
            url="http://10.20.1.69:1122/sse"
        ),  # Charts MCP Server
    ],
)
```

**2. Re-package and deploy:**

```bash
# Package the updated agent
ncp package

# Deploy with update flag
ncp deploy netbox-agent.ncp --update

# Test with new visualization capabilities
ncp playground --agent netbox-agent --show-tools
```

---

## Phase 2: Visual Analytics with Charts

Now that the Charts MCP Server is enabled, you can ask the same questions but request visualizations!

### 1. Device Distribution Visualizations

Create visual breakdowns of your inventory:

- **"Create a chart showing device distribution by site"**
- **"Show device count breakdown by manufacturer as a pie chart"**
- **"Chart device distribution across locations as a bar graph"**
- **"Create a visual breakdown of total devices grouped by device type"**

### 2. Status and Health Charts

Visualize operational status:

- **"Display devices by status across each site as a stacked bar chart"**
- **"Chart all devices by their operational status (active/offline/planned)"**
- **"Create a pie chart showing percentage of online vs offline devices"**
- **"Show a stacked bar chart of device status per location"**

### 3. Device Role Visualizations

Visual analysis of network composition:

- **"Show count of devices per role with a pie chart"**
- **"Chart device role distribution per location"**
- **"Create a bar chart of inventory breakdown by device role"**
- **"Visualize which device roles are most common in our network"**

### 4. Hardware Distribution Charts

Visual hardware analysis:

- **"Create a pie chart of device distribution by hardware manufacturer"**
- **"Chart device models by count - which models dominate our network?"**
- **"Show top 15 most common device models as a bar chart"**
- **"Visualize hardware diversity across vendors"**

### 5. Operating System Charts

OS distribution visualizations:

- **"Create a chart showing OS distribution across all devices"**
- **"Chart devices by OS platform (Cisco IOS/NX-OS, Arista EOS, etc)"**
- **"Show a pie chart of operating system version distribution"**
- **"Visualize which OS versions need attention (end-of-support)"**

### 6. Data Quality Visualizations

Visual representation of inventory gaps:

- **"Create a chart showing missing data: devices without location, role, or contact"**
- **"Visualize incomplete device records - what fields are commonly missing?"**
- **"Show a breakdown chart of data completeness across inventory"**

---

## Architecture

### Two-Phase Integration Approach

This lab demonstrates progressive enhancement of agent capabilities:

**Phase 1: NetBox Connector Only**
```python
agent = Agent(
    name="netbox-agent",
    connectors=["Netbox"],  # Platform-managed connector
    mcp_servers=[],         # No MCP servers yet
)
```
- Focus on data retrieval and analysis
- Natural language queries return text-based insights
- Learn how platform connectors work

**Phase 2: Adding Charts MCP Server**
```python
agent = Agent(
    name="netbox-agent",
    connectors=["Netbox"],
    mcp_servers=[
        MCPConfig(transport_type="sse", url="http://10.20.1.69:1122/sse")
    ],
)
```
- Adds visualization capabilities
- Same queries can now generate charts
- Demonstrates MCP server integration

### Integration Details

**1. NetBox Connector** (`Netbox`)
- Configured by platform administrator
- Handles authentication and API communication
- Provides access to inventory data

**2. Charts MCP Server** (SSE transport at `http://10.20.1.69:1122/sse`)
- Generate various chart types (bar, pie, line, stacked, etc.)
- Automatically creates visualizations from data
- Added in Phase 2 of the lab

### Design Philosophy

**Key Design Decisions:**
- **Zero custom Python tools**: All functionality comes from connector and MCP server
- **Natural language driven**: LLM interprets queries and generates appropriate API calls
- **Progressive enhancement**: Start simple (data), add complexity (charts)
- **Auto-visualization**: Charts MCP automatically generates visualizations from data
- **Ad-hoc analytics**: No pre-defined reports—ask anything about your inventory

---

## Experiment and Extend

### Try These Modifications

**1. Combine Multiple Dimensions**
- "Show device count by manufacturer AND location in a stacked chart"
- "Create a chart comparing device roles across different sites"

**2. Complex Queries**
- "Which site has the most diversity in hardware vendors?"
- "Show correlation between device role and operational status"

**3. Custom Visualizations**
- Request specific chart types (scatter, line, area)
- Ask for color coding based on status

### Build Your Own Agent

Use this as a template to create agents for:
- **Configuration database analytics**: Integrate with your CMDB
- **Asset management**: Track warranty, EOL, support contracts
- **Security posture**: Identify devices with outdated OS, missing patches

---

## Key Takeaways

**Natural language = universal interface** - No need to learn APIs or query languages

**Progressive enhancement** - Start simple, add capabilities incrementally

**Visualization is automatic** - LLM + MCP server = instant charts

**Zero custom code** - Connector + MCP + instructions = powerful analytics

**Data accessibility** - Enable non-technical stakeholders to access inventory insights

**Ad-hoc analysis** - Ask any question without pre-building reports

**Composable architecture** - Mix and match connectors and MCP servers for new capabilities

---

## Next Steps

- **Complete Phase 1** - Deploy and test data analysis queries
- **Enable Phase 2** - Add Charts MCP server and explore visualizations
- **Experiment with complex queries** combining multiple dimensions
- **Try different chart types** (pie, bar, stacked, line, scatter)
- **Build your own analytics agent** for another data source in your environment

---

**Ready to turn data into insights with AI? Deploy the agent and start asking questions!** 🚀
