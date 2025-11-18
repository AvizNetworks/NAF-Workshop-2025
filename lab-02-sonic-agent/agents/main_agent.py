"""Main agent definition."""

from ncp import Agent, MCPConfig


agent = Agent(
    name="sonic-agent",
    description="SONiC Switch Agent",
    instructions="""
    You are a helpful SONiC switch agent. Your goal is to assist users with network switch operations.

    Be:
    - Concise and clear in your responses
    - Helpful and friendly
    - Professional

    Use the available tools to accomplish tasks when appropriate.
    """,
    tools=[],
    mcp_servers=[
        MCPConfig(transport_type="sse", url="http://10.4.6.11:4321/sse")
    ],
)
