from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client
from pydantic import AnyUrl

server_params = StdioServerParameters(command="mcp", args=["run", "server.py"], env=None)

async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            # List available resources
            resources = await session.list_resources()
            print("LISTING RESOURCES")
            for resource in resources:
                print("Resource: ", resource)

            # List available tools
            tools = await session.list_tools()
            print("LISTING TOOLS")
            for tool in tools.tools:
                print("Tool: ", tool.name)

            # Read a resource
            print("READING RESOURCE")
            content, mime_type = await session.read_resource(AnyUrl("greeting://friend"))
            print(f"From greeting://hello:\ncontent: {content}\nmime_type: {mime_type}")
            
            # Call a tool
            print("CALL TOOL")
            result = await session.call_tool("addition", arguments={"a": 1, "b": 7})
            print(f"Result: {result.content}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(run())