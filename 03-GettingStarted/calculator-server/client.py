from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client
from pydantic import AnyUrl
# llm
import os
from dotenv import load_dotenv
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential
import json

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
            functions = []
            print("LISTING TOOLS")
            for tool in tools.tools:
                print(f"Tool name: {tool.name}")
                print(f"Tool schema: {tool.inputSchema["properties"]}")
                functions.append(convert_to_llm_tool(tool))

            # Read a resource
            print("READING RESOURCE")
            content, mime_type = await session.read_resource(AnyUrl("greeting://friend"))
            print(f"From greeting://hello:\ncontent: {content}\nmime_type: {mime_type}")
            
            # Call a tool
            print("CALL TOOL")
            result = await session.call_tool("addition", arguments={"a": 1, "b": 7})
            print(f"Result: {result.content}")

            # Call tools with LLM
            prompt = "Add 2 to 20"
            print(f"Prompt is: {prompt}")
            # ask LLM what tools to call, if any
            functions_to_call = call_llm(prompt, functions)
            # call suggested functions
            for f in functions_to_call:
                result = await session.call_tool(f["name"], arguments=f["args"])
                print("Call tool with LLM result: ", result.content)

def convert_to_llm_tool(tool: types.Tool):
    tool_schema = {
        "type": "function",
        "function": {
            "name": tool.name,
            "description": tool.description,
            "type": "function",
            "parameters": {
                "type": "object",
                "properties": tool.inputSchema["properties"]
            }
        }
    }
    return tool_schema

def call_llm(prompt: str, functions):
    load_dotenv()
    token = os.environ["GITHUB_TOKEN"]
    endpoint = "https://models.inference.ai.azure.com"

    model_name = "gpt-4o"

    client = ChatCompletionsClient(
        endpoint = endpoint,
        credential = AzureKeyCredential(token)
    )

    print("CALLING LLM")
    response = client.complete(
        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        model = model_name,
        tools = functions,
        # Optional params
        temperature = 1.,
        max_tokens = 1000,
        top_p = 1.,
    )

    response_message = response.choices[0].message

    functions_to_call = []
    if response_message.tool_calls:
        for tool_call in response_message.tool_calls:
            print("TOOL: ", tool_call)
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            functions_to_call.append({
                "name": name,
                "args": args
            })
    return functions_to_call

if __name__ == "__main__":
    import asyncio

    asyncio.run(run())