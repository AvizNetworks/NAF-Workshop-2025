"""Main agent definition."""

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
    """
    # Note: When creating chart URLs, always use 'naflab2.aviznetworks.com' in place of '10.20.1.69'—the rest of the URL should remain unchanged.
    # """

    tools=[],
    connectors=["Netbox"],
    # mcp_servers=[
    #     MCPConfig(transport_type="sse", url="http://10.20.1.69:1122/sse")
    # ],
)
