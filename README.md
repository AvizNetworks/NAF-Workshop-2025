# NAF Workshop 2025 - Build Your Own AI Ops Workflows with an Agentic Private AI Platform

Welcome to the **Network Automation Forum (NAF) 2025 Workshop**! In this hands-on workshop, you'll learn to build intelligent AI agents for network operations using the **NCP SDK** (Network Copilot Software Development Kit).

---

## Prerequisites

Before starting the workshop, ensure you have:

- ✅ **Python 3.9+** installed on your system
- ✅ **Git** installed
- ✅ **Code editor** (VS Code recommended, or your preferred editor)
- ✅ **NCP platform account** (pre-configured for workshop attendees)

---

## Getting Started

### 1. Clone the Workshop Repository

```bash
git clone https://github.com/AvizNetworks/NAF-Workshop-2025
cd NAF-Workshop-2025
```

### 2. Set Up Python Virtual Environment

Create and activate a virtual environment to isolate workshop dependencies:

**On Linux/macOS:**

```bash
python -m venv .venv
source .venv/bin/activate
```

**On Windows:**

```bash
python -m venv .venv
.venv\Scripts\activate
```

You should see `(.venv)` prefix in your terminal prompt, indicating the virtual environment is active.

### 3. Install NCP SDK

Install the NCP SDK package from PyPI:

```bash
pip install ncp-sdk
```

### 4. Verify Installation

Check that the NCP SDK is installed correctly:

```bash
ncp --help
```

You should see the NCP CLI help output with available commands.

---

## NCP SDK Developer Workflow

The NCP SDK provides a streamlined workflow for developing, testing, and deploying AI agents. Here's the standard development cycle:

### Step 1: Initialize a New Agent Project

Create a new agent project using the NCP SDK:

```bash
ncp init weather-agent
cd weather-agent
```

This creates the standard NCP SDK project structure with all necessary files.

### Step 2: Authenticate with Platform

Authenticate with the NCP platform (run this from inside your agent directory):

```bash
ncp authenticate
```

You'll be prompted for:

- **Platform URL**: Provided by workshop instructor
- **Username**: Your registered email address
- **Password**: `NAF@2025`

Your authentication credentials are stored locally and used for subsequent deployments.

### Step 3: Validate Your Agent

Before deploying, validate that your agent is properly configured:

```bash
ncp validate .
```

This checks:

- Project structure (agents/, tools/, ncp.toml)
- Configuration file syntax
- Entry point exists and is valid
- Dependencies are specified correctly

**Expected output:**

```
✓ Project structure validated
✓ Configuration file valid
✓ Entry point found: agents.main_agent:agent
✓ Validation passed!
```

### Step 4: Package Your Agent

Package your agent into a `.ncp` file for deployment:

```bash
ncp package
```

This creates a `.ncp` archive containing:

- All Python code (agents/, tools/)
- Configuration (ncp.toml)
- Dependencies (requirements.txt, apt-requirements.txt)
- Knowledge base files (if present)

### Step 5: Deploy to Platform

Deploy your packaged agent to the NCP platform:

```bash
ncp deploy <agent-name>.ncp
```

Example:
```bash
ncp deploy weather-agent.ncp
```

**First-time deployment:** This command registers your agent on the platform.

**Updating an existing agent:**

```bash
ncp deploy <agent-name>.ncp --update
```

### Step 6: Test with CLI Playground

Test your deployed agent interactively using the CLI playground:

**Basic interactive mode:**

```bash
ncp playground --agent weather-agent
```

**With tool call visibility:**

```bash
ncp playground --agent weather-agent --show-tools
```

The `--show-tools` flag shows:

- Which tools the LLM is calling
- Tool parameters
- Tool results
- Agent reasoning process

This is invaluable for debugging and understanding how your agent works.

---

## Workshop Labs

### Lab 1: netbox-agent

**Focus**: Network inventory analytics with natural language and visualizations

Build an AI-powered analytics agent that transforms NetBox inventory data into actionable insights through conversational queries and automated chart generation using the Charts MCP Server.

**See `lab-01-netbox-agent/README.md` for detailed instructions and example queries.**

### Lab 2: netops-agent

**Focus**: End-to-end network troubleshooting workflow with multi-system orchestration

Build an intelligent agent that orchestrates network incident resolution by integrating ServiceNow for ticket management, Splunk for log analysis, and SONiC MCP for device remediation. Includes knowledge base integration for historical pattern matching.

**See `lab-02-netops-agent/README.md` for detailed instructions and use case walkthrough.**

### Lab 3: fabric-agent

**Focus**: Network fabric automation and multi-tenancy management

Build an AI-powered fabric management agent that automates network operations across entire fabrics or individual devices. Manage interfaces, VLANs, host allocation, and multi-tenancy through natural language commands using a specialized Fabric Management MCP server.

**See `lab-03-fabric-agent/README.md` for detailed instructions and example commands.**

---

## Common Commands Reference

| Command | Description |
|---------|-------------|
| `ncp --help` | Show all available commands and options |
| `ncp authenticate` | Authenticate with the NCP platform |
| `ncp validate .` | Validate current project structure and configuration |
| `ncp package .` | Create a `.ncp` deployment package |
| `ncp deploy <file>.ncp` | Deploy agent to platform (first time) |
| `ncp deploy <file>.ncp --update` | Update an existing deployed agent |
| `ncp playground --agent <name>` | Interactive testing with your agent |
| `ncp playground --agent <name> --show-tools` | Show LLM tool calls during testing |
| `ncp list agents` | List all your deployed agents |
| `ncp remove --agent <name>` | Remove a deployed agent |

---

## Project Structure

Each lab follows the standard NCP SDK project structure:

```
lab-name/
├── ncp.toml                 # Project configuration and metadata
├── requirements.txt         # Python dependencies
├── apt-requirements.txt     # System dependencies (optional)
├── agents/
│   ├── __init__.py
│   └── main_agent.py        # Main agent definition
├── tools/
│   ├── __init__.py
│   └── *.py                 # Custom tool implementations
└── knowledge/               # Knowledge base files (optional)
    └── *.md
```

**Key files:**

- `ncp.toml`: Defines project metadata, Python version, entry point
- `agents/main_agent.py`: Where you define your agent's behavior, instructions, and capabilities
- `tools/*.py`: Custom Python functions decorated with `@tool` that your agent can call
- `knowledge/*.md`: Markdown files for vector search (automatically indexed)

---

## Troubleshooting

### Virtual Environment Not Activated

**Symptom:** `ncp: command not found` or wrong Python version

**Solution:**

```bash
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
```

### NCP SDK Installation Issues

**Symptom:** `pip install ncp-sdk` fails

**Solutions:**

- Ensure Python 3.9+ is installed: `python --version`
- Update pip: `pip install --upgrade pip`
- Check internet connectivity

### Authentication Failures

**Symptom:** "Authentication failed" when running `ncp authenticate`

**Solutions:**

- Verify you're in a lab directory (e.g., `cd lab-01-netbox-agent`)
- Check platform URL in `ncp.toml` or as provided by instructor
- Verify username is correct
- Ensure password is exactly: `NAF@2025`
- Check network connectivity to platform

### Validation Errors

**Symptom:** `ncp validate .` reports errors

**Solutions:**

- Ensure you're in the correct lab directory
- Check that `ncp.toml` exists
- Verify `agents/main_agent.py` exists
- Check that entry point in `ncp.toml` matches actual file structure

### Deployment Problems

**Symptom:** `ncp deploy` fails

**Solutions:**

- Run `ncp validate .` first to check for configuration issues
- Ensure you're authenticated: run `ncp authenticate` again
- For updates, use `--update` flag: `ncp deploy <file>.ncp --update`
- Check platform connectivity

### Playground Not Working

**Symptom:** `ncp playground` doesn't start or agent not found

**Solutions:**

- Ensure agent is deployed: `ncp list agents`
- Check agent name matches deployment
- Verify platform authentication is valid

---

## Development Tips

### Best Practices

1. **Always validate before deploying**: Run `ncp validate .` to catch issues early
2. **Use the playground for testing**: Test your agent with `--show-tools` to debug
3. **Read lab READMEs carefully**: Each lab has specific instructions and learning objectives
4. **Experiment**: Modify agents, try different instructions, add new tools
5. **Ask questions**: Workshop instructors are here to help

### Iterative Development Cycle

1. Make changes to your agent code
2. Validate: `ncp validate .`
3. Package: `ncp package`
4. Deploy: `ncp deploy <agent-name>.ncp --update`
5. Test: `ncp playground --agent <name> --show-tools`
6. Iterate based on results

---

## Next Steps

Ready to start? Head to **Lab 1**:

```bash
cd lab-01-netbox-agent
cat README.md  # Read the lab instructions
```

Follow the lab README for detailed use case walkthrough, deployment instructions, and learning objectives.

**Happy building! 🚀**
