<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "57f7b15640bb96ef2f6f09003eec935e",
  "translation_date": "2025-08-12T19:24:48+00:00",
  "source_file": "03-GettingStarted/03-llm-client/README.md",
  "language_code": "hi"
}
-->
# LLM के साथ क्लाइंट बनाना

अब तक, आपने देखा कि सर्वर और क्लाइंट कैसे बनाते हैं। क्लाइंट ने सर्वर को स्पष्ट रूप से कॉल करके उसके टूल्स, संसाधनों और प्रॉम्प्ट्स की सूची प्राप्त की है। हालांकि, यह बहुत व्यावहारिक तरीका नहीं है। आपका उपयोगकर्ता एजेंटिक युग में रहता है और उम्मीद करता है कि वह प्रॉम्प्ट्स का उपयोग करके और LLM के साथ संवाद करके काम करेगा। आपके उपयोगकर्ता को इस बात की परवाह नहीं है कि आप अपनी क्षमताओं को संग्रहीत करने के लिए MCP का उपयोग करते हैं या नहीं, लेकिन वे प्राकृतिक भाषा के माध्यम से बातचीत की उम्मीद करते हैं। तो हम इसे कैसे हल करें? समाधान है क्लाइंट में LLM जोड़ना।

## अवलोकन

इस पाठ में हम आपके क्लाइंट में LLM जोड़ने पर ध्यान केंद्रित करेंगे और दिखाएंगे कि यह आपके उपयोगकर्ता के लिए कितना बेहतर अनुभव प्रदान करता है।

## सीखने के उद्देश्य

इस पाठ के अंत तक, आप सक्षम होंगे:

- LLM के साथ एक क्लाइंट बनाना।
- MCP सर्वर के साथ LLM का उपयोग करके सहजता से बातचीत करना।
- क्लाइंट साइड पर बेहतर उपयोगकर्ता अनुभव प्रदान करना।

## दृष्टिकोण

आइए समझने की कोशिश करें कि हमें कौन सा दृष्टिकोण अपनाना चाहिए। LLM जोड़ना सरल लगता है, लेकिन क्या हम वास्तव में ऐसा करेंगे?

यहां बताया गया है कि क्लाइंट सर्वर के साथ कैसे बातचीत करेगा:

1. सर्वर के साथ कनेक्शन स्थापित करें।

1. क्षमताओं, प्रॉम्प्ट्स, संसाधनों और टूल्स की सूची बनाएं और उनकी स्कीमा को सहेजें।

1. एक LLM जोड़ें और सहेजी गई क्षमताओं और उनकी स्कीमा को एक ऐसे प्रारूप में पास करें जिसे LLM समझ सके।

1. उपयोगकर्ता प्रॉम्प्ट को संभालें और इसे LLM को पास करें, साथ ही क्लाइंट द्वारा सूचीबद्ध टूल्स को भी।

बहुत बढ़िया, अब हम समझ गए हैं कि इसे उच्च स्तर पर कैसे किया जा सकता है। आइए इसे नीचे दिए गए अभ्यास में आजमाएं।

## अभ्यास: LLM के साथ क्लाइंट बनाना

इस अभ्यास में, हम अपने क्लाइंट में LLM जोड़ना सीखेंगे।

### GitHub पर्सनल एक्सेस टोकन का उपयोग करके प्रमाणीकरण

GitHub टोकन बनाना एक सीधा प्रक्रिया है। इसे इस प्रकार करें:

- GitHub सेटिंग्स पर जाएं – ऊपर दाईं ओर अपनी प्रोफ़ाइल तस्वीर पर क्लिक करें और सेटिंग्स चुनें।
- डेवलपर सेटिंग्स पर जाएं – नीचे स्क्रॉल करें और डेवलपर सेटिंग्स पर क्लिक करें।
- पर्सनल एक्सेस टोकन चुनें – पर्सनल एक्सेस टोकन पर क्लिक करें और फिर नया टोकन जनरेट करें।
- अपने टोकन को कॉन्फ़िगर करें – संदर्भ के लिए एक नोट जोड़ें, समाप्ति तिथि सेट करें, और आवश्यक स्कोप (अनुमतियां) चुनें।
- टोकन जनरेट करें और कॉपी करें – टोकन जनरेट पर क्लिक करें और इसे तुरंत कॉपी करना सुनिश्चित करें, क्योंकि आप इसे फिर से नहीं देख पाएंगे।

### -1- सर्वर से कनेक्ट करें

आइए पहले अपना क्लाइंट बनाएं:

#### TypeScript

```typescript
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";
import { Transport } from "@modelcontextprotocol/sdk/shared/transport.js";
import OpenAI from "openai";
import { z } from "zod"; // Import zod for schema validation

class MCPClient {
    private openai: OpenAI;
    private client: Client;
    constructor(){
        this.openai = new OpenAI({
            baseURL: "https://models.inference.ai.azure.com", 
            apiKey: process.env.GITHUB_TOKEN,
        });

        this.client = new Client(
            {
                name: "example-client",
                version: "1.0.0"
            },
            {
                capabilities: {
                prompts: {},
                resources: {},
                tools: {}
                }
            }
            );    
    }
}
```

ऊपर दिए गए कोड में हमने:

- आवश्यक लाइब्रेरीज़ इंपोर्ट की हैं।
- एक क्लास बनाई है जिसमें दो मेंबर्स हैं, `client` और `openai`, जो हमें क्लाइंट को प्रबंधित करने और LLM के साथ बातचीत करने में मदद करेंगे।
- हमारे LLM इंस्टेंस को GitHub मॉडल्स का उपयोग करने के लिए कॉन्फ़िगर किया है, `baseUrl` को इन्फरेंस API की ओर इंगित करके।

#### Python

```python
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client

# Create server parameters for stdio connection
server_params = StdioServerParameters(
    command="mcp",  # Executable
    args=["run", "server.py"],  # Optional command line arguments
    env=None,  # Optional environment variables
)


async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(
            read, write
        ) as session:
            # Initialize the connection
            await session.initialize()


if __name__ == "__main__":
    import asyncio

    asyncio.run(run())

```

ऊपर दिए गए कोड में हमने:

- MCP के लिए आवश्यक लाइब्रेरीज़ इंपोर्ट की हैं।
- एक क्लाइंट बनाया है।

#### .NET

```csharp
using Azure;
using Azure.AI.Inference;
using Azure.Identity;
using System.Text.Json;
using ModelContextProtocol.Client;
using ModelContextProtocol.Protocol.Transport;
using System.Text.Json;

var clientTransport = new StdioClientTransport(new()
{
    Name = "Demo Server",
    Command = "/workspaces/mcp-for-beginners/03-GettingStarted/02-client/solution/server/bin/Debug/net8.0/server",
    Arguments = [],
});

await using var mcpClient = await McpClientFactory.CreateAsync(clientTransport);
```

#### Java

सबसे पहले, आपको अपने `pom.xml` फ़ाइल में LangChain4j डिपेंडेंसीज़ जोड़ने की आवश्यकता होगी। MCP इंटीग्रेशन और GitHub मॉडल्स सपोर्ट को सक्षम करने के लिए इन डिपेंडेंसीज़ को जोड़ें:

```xml
<properties>
    <langchain4j.version>1.0.0-beta3</langchain4j.version>
</properties>

<dependencies>
    <!-- LangChain4j MCP Integration -->
    <dependency>
        <groupId>dev.langchain4j</groupId>
        <artifactId>langchain4j-mcp</artifactId>
        <version>${langchain4j.version}</version>
    </dependency>
    
    <!-- OpenAI Official API Client -->
    <dependency>
        <groupId>dev.langchain4j</groupId>
        <artifactId>langchain4j-open-ai-official</artifactId>
        <version>${langchain4j.version}</version>
    </dependency>
    
    <!-- GitHub Models Support -->
    <dependency>
        <groupId>dev.langchain4j</groupId>
        <artifactId>langchain4j-github-models</artifactId>
        <version>${langchain4j.version}</version>
    </dependency>
    
    <!-- Spring Boot Starter (optional, for production apps) -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-actuator</artifactId>
    </dependency>
</dependencies>
```

फिर अपनी जावा क्लाइंट क्लास बनाएं:

```java
import dev.langchain4j.mcp.McpToolProvider;
import dev.langchain4j.mcp.client.DefaultMcpClient;
import dev.langchain4j.mcp.client.McpClient;
import dev.langchain4j.mcp.client.transport.McpTransport;
import dev.langchain4j.mcp.client.transport.http.HttpMcpTransport;
import dev.langchain4j.model.chat.ChatLanguageModel;
import dev.langchain4j.model.openaiofficial.OpenAiOfficialChatModel;
import dev.langchain4j.service.AiServices;
import dev.langchain4j.service.tool.ToolProvider;

import java.time.Duration;
import java.util.List;

public class LangChain4jClient {
    
    public static void main(String[] args) throws Exception {        // Configure the LLM to use GitHub Models
        ChatLanguageModel model = OpenAiOfficialChatModel.builder()
                .isGitHubModels(true)
                .apiKey(System.getenv("GITHUB_TOKEN"))
                .timeout(Duration.ofSeconds(60))
                .modelName("gpt-4.1-nano")
                .build();

        // Create MCP transport for connecting to server
        McpTransport transport = new HttpMcpTransport.Builder()
                .sseUrl("http://localhost:8080/sse")
                .timeout(Duration.ofSeconds(60))
                .logRequests(true)
                .logResponses(true)
                .build();

        // Create MCP client
        McpClient mcpClient = new DefaultMcpClient.Builder()
                .transport(transport)
                .build();
    }
}
```

ऊपर दिए गए कोड में हमने:

- **LangChain4j डिपेंडेंसीज़ जोड़ीं**: MCP इंटीग्रेशन, OpenAI आधिकारिक क्लाइंट, और GitHub मॉडल्स सपोर्ट के लिए आवश्यक।
- **LangChain4j लाइब्रेरीज़ इंपोर्ट कीं**: MCP इंटीग्रेशन और OpenAI चैट मॉडल कार्यक्षमता के लिए।
- **`ChatLanguageModel` बनाया**: GitHub मॉडल्स का उपयोग करने के लिए आपके GitHub टोकन के साथ कॉन्फ़िगर किया गया।
- **HTTP ट्रांसपोर्ट सेट किया**: MCP सर्वर से कनेक्ट करने के लिए Server-Sent Events (SSE) का उपयोग करके।
- **MCP क्लाइंट बनाया**: जो सर्वर के साथ संचार को संभालेगा।
- **LangChain4j का बिल्ट-इन MCP सपोर्ट उपयोग किया**: जो LLMs और MCP सर्वर के बीच इंटीग्रेशन को सरल बनाता है।

#### Rust

यह उदाहरण मानता है कि आपके पास एक Rust आधारित MCP सर्वर चल रहा है। यदि आपके पास ऐसा नहीं है, तो [01-first-server](../01-first-server/README.md) पाठ में वापस जाएं और सर्वर बनाएं।

एक बार जब आपके पास आपका Rust MCP सर्वर हो, तो एक टर्मिनल खोलें और सर्वर के समान डायरेक्टरी में नेविगेट करें। फिर एक नया LLM क्लाइंट प्रोजेक्ट बनाने के लिए निम्नलिखित कमांड चलाएं:

```bash
mkdir calculator-llmclient
cd calculator-llmclient
cargo init
```

अपने `Cargo.toml` फ़ाइल में निम्नलिखित डिपेंडेंसीज़ जोड़ें:

```toml
[dependencies]
async-openai = { version = "0.29.0", features = ["byot"] }
rmcp = { version = "0.5.0", features = ["client", "transport-child-process"] }
serde_json = "1.0.141"
tokio = { version = "1.46.1", features = ["rt-multi-thread"] }
```

> [!NOTE]
> OpenAI के लिए कोई आधिकारिक Rust लाइब्रेरी नहीं है, हालांकि, `async-openai` क्रेट एक [समुदाय द्वारा बनाए रखा गया लाइब्रेरी](https://platform.openai.com/docs/libraries/rust#rust) है जो आमतौर पर उपयोग किया जाता है।

`src/main.rs` फ़ाइल खोलें और इसकी सामग्री को निम्नलिखित कोड से बदलें:

```rust
use async_openai::{Client, config::OpenAIConfig};
use rmcp::{
    RmcpError,
    model::{CallToolRequestParam, ListToolsResult},
    service::{RoleClient, RunningService, ServiceExt},
    transport::{ConfigureCommandExt, TokioChildProcess},
};
use serde_json::{Value, json};
use std::error::Error;
use tokio::process::Command;

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    // Initial message
    let mut messages = vec![json!({"role": "user", "content": "What is the sum of 3 and 2?"})];

    // Setup OpenAI client
    let api_key = std::env::var("OPENAI_API_KEY")?;
    let openai_client = Client::with_config(
        OpenAIConfig::new()
            .with_api_base("https://models.github.ai/inference/chat")
            .with_api_key(api_key),
    );

    // Setup MCP client
    let server_dir = std::path::Path::new(env!("CARGO_MANIFEST_DIR"))
        .parent()
        .unwrap()
        .join("calculator-server");

    let mcp_client = ()
        .serve(
            TokioChildProcess::new(Command::new("cargo").configure(|cmd| {
                cmd.arg("run").current_dir(server_dir);
            }))
            .map_err(RmcpError::transport_creation::<TokioChildProcess>)?,
        )
        .await?;

    // TODO: Get MCP tool listing 

    // TODO: LLM conversation with tool calls

    Ok(())
}
```

यह कोड एक बेसिक Rust एप्लिकेशन सेट करता है जो MCP सर्वर और GitHub मॉडल्स के साथ LLM इंटरैक्शन के लिए कनेक्ट करेगा।

> [!IMPORTANT]
> एप्लिकेशन चलाने से पहले `OPENAI_API_KEY` पर्यावरण वेरिएबल को अपने GitHub टोकन के साथ सेट करना सुनिश्चित करें।

बहुत बढ़िया, अब अगले चरण में, आइए सर्वर की क्षमताओं को सूचीबद्ध करें।

### -2- सर्वर की क्षमताओं की सूची बनाएं

अब हम सर्वर से कनेक्ट करेंगे और उसकी क्षमताओं के बारे में पूछेंगे:

#### TypeScript

उसी क्लास में निम्नलिखित मेथड्स जोड़ें:

```typescript
async connectToServer(transport: Transport) {
     await this.client.connect(transport);
     this.run();
     console.error("MCPClient started on stdin/stdout");
}

async run() {
    console.log("Asking server for available tools");

    // listing tools
    const toolsResult = await this.client.listTools();
}
```

ऊपर दिए गए कोड में हमने:

- सर्वर से कनेक्ट करने के लिए कोड जोड़ा, `connectToServer`।
- एक `run` मेथड बनाया जो हमारे ऐप फ्लो को संभालने के लिए जिम्मेदार है। अभी तक यह केवल टूल्स की सूची बनाता है, लेकिन हम इसमें जल्द ही और जोड़ेंगे।

#### Python

```python
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
    print("Tool", tool.inputSchema["properties"])
```

यहां हमने जो जोड़ा है:

- संसाधनों और टूल्स की सूची बनाई और उन्हें प्रिंट किया। टूल्स के लिए हमने `inputSchema` भी सूचीबद्ध किया, जिसे हम बाद में उपयोग करेंगे।

#### .NET

```csharp
async Task<List<ChatCompletionsToolDefinition>> GetMcpTools()
{
    Console.WriteLine("Listing tools");
    var tools = await mcpClient.ListToolsAsync();

    List<ChatCompletionsToolDefinition> toolDefinitions = new List<ChatCompletionsToolDefinition>();

    foreach (var tool in tools)
    {
        Console.WriteLine($"Connected to server with tools: {tool.Name}");
        Console.WriteLine($"Tool description: {tool.Description}");
        Console.WriteLine($"Tool parameters: {tool.JsonSchema}");

        // TODO: convert tool definition from MCP tool to LLm tool     
    }

    return toolDefinitions;
}
```

ऊपर दिए गए कोड में हमने:

- MCP सर्वर पर उपलब्ध टूल्स की सूची बनाई।
- प्रत्येक टूल के लिए नाम, विवरण और उसकी स्कीमा सूचीबद्ध की। बाद वाला वह है जिसे हम जल्द ही टूल्स को कॉल करने के लिए उपयोग करेंगे।

#### Java

```java
// Create a tool provider that automatically discovers MCP tools
ToolProvider toolProvider = McpToolProvider.builder()
        .mcpClients(List.of(mcpClient))
        .build();

// The MCP tool provider automatically handles:
// - Listing available tools from the MCP server
// - Converting MCP tool schemas to LangChain4j format
// - Managing tool execution and responses
```

ऊपर दिए गए कोड में हमने:

- एक `McpToolProvider` बनाया जो MCP सर्वर से सभी टूल्स को स्वचालित रूप से खोजता और रजिस्टर करता है।
- टूल प्रोवाइडर आंतरिक रूप से MCP टूल स्कीमा और LangChain4j के टूल फॉर्मेट के बीच रूपांतरण को संभालता है।
- यह दृष्टिकोण मैनुअल टूल सूचीकरण और रूपांतरण प्रक्रिया को अमूर्त करता है।

#### Rust

MCP सर्वर से टूल्स प्राप्त करना `list_tools` मेथड का उपयोग करके किया जाता है। अपने `main` फ़ंक्शन में, MCP क्लाइंट सेटअप के बाद निम्नलिखित कोड जोड़ें:

```rust
// Get MCP tool listing 
let tools = mcp_client.list_tools(Default::default()).await?;
```

### -3- सर्वर क्षमताओं को LLM टूल्स में बदलें

सर्वर क्षमताओं को सूचीबद्ध करने के बाद अगला कदम उन्हें एक ऐसे प्रारूप में बदलना है जिसे LLM समझ सके। एक बार जब हम ऐसा कर लेते हैं, तो हम इन क्षमताओं को LLM को टूल्स के रूप में प्रदान कर सकते हैं।

#### TypeScript

1. MCP सर्वर से प्रतिक्रिया को LLM के लिए उपयोगी टूल फॉर्मेट में बदलने के लिए निम्नलिखित कोड जोड़ें:

    ```typescript
    openAiToolAdapter(tool: {
        name: string;
        description?: string;
        input_schema: any;
        }) {
        // Create a zod schema based on the input_schema
        const schema = z.object(tool.input_schema);
    
        return {
            type: "function" as const, // Explicitly set type to "function"
            function: {
            name: tool.name,
            description: tool.description,
            parameters: {
            type: "object",
            properties: tool.input_schema.properties,
            required: tool.input_schema.required,
            },
            },
        };
    }

    ```

    ऊपर दिया गया कोड MCP सर्वर से प्रतिक्रिया लेता है और उसे एक टूल परिभाषा प्रारूप में बदलता है जिसे LLM समझ सकता है।

1. इसके बाद, `run` मेथड को अपडेट करें ताकि सर्वर क्षमताओं की सूची बनाई जा सके:

    ```typescript
    async run() {
        console.log("Asking server for available tools");
        const toolsResult = await this.client.listTools();
        const tools = toolsResult.tools.map((tool) => {
            return this.openAiToolAdapter({
            name: tool.name,
            description: tool.description,
            input_schema: tool.inputSchema,
            });
        });
    }
    ```

    ऊपर दिए गए कोड में, हमने `run` मेथड को अपडेट किया है ताकि परिणाम के माध्यम से मैप किया जा सके और प्रत्येक प्रविष्टि के लिए `openAiToolAdapter` को कॉल किया जा सके।

#### Python

1. पहले, निम्नलिखित कन्वर्टर फ़ंक्शन बनाएं:

    ```python
    def convert_to_llm_tool(tool):
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
    ```

    ऊपर दिए गए `convert_to_llm_tools` फ़ंक्शन में हम MCP टूल प्रतिक्रिया लेते हैं और उसे एक प्रारूप में बदलते हैं जिसे LLM समझ सके।

1. इसके बाद, अपने क्लाइंट कोड को इस फ़ंक्शन का लाभ उठाने के लिए अपडेट करें:

    ```python
    for tool in tools.tools:
        print("Tool: ", tool.name)
        print("Tool", tool.inputSchema["properties"])
        functions.append(convert_to_llm_tool(tool))
    ```

    यहां, हम MCP टूल प्रतिक्रिया को LLM के लिए उपयोगी प्रारूप में बदलने के लिए `convert_to_llm_tool` को कॉल कर रहे हैं।

#### .NET

1. MCP टूल प्रतिक्रिया को LLM के लिए उपयोगी प्रारूप में बदलने के लिए कोड जोड़ें:

```csharp
ChatCompletionsToolDefinition ConvertFrom(string name, string description, JsonElement jsonElement)
{ 
    // convert the tool to a function definition
    FunctionDefinition functionDefinition = new FunctionDefinition(name)
    {
        Description = description,
        Parameters = BinaryData.FromObjectAsJson(new
        {
            Type = "object",
            Properties = jsonElement
        },
        new JsonSerializerOptions() { PropertyNamingPolicy = JsonNamingPolicy.CamelCase })
    };

    // create a tool definition
    ChatCompletionsToolDefinition toolDefinition = new ChatCompletionsToolDefinition(functionDefinition);
    return toolDefinition;
}
```

ऊपर दिए गए कोड में हमने:

- एक फ़ंक्शन `ConvertFrom` बनाया जो नाम, विवरण और इनपुट स्कीमा लेता है।
- एक FunctionDefinition बनाया जो ChatCompletionsDefinition को पास किया जाता है। बाद वाला वह है जिसे LLM समझ सकता है।

1. आइए देखें कि इस फ़ंक्शन का उपयोग करने के लिए मौजूदा कोड को कैसे अपडेट किया जा सकता है:

    ```csharp
    async Task<List<ChatCompletionsToolDefinition>> GetMcpTools()
    {
        Console.WriteLine("Listing tools");
        var tools = await mcpClient.ListToolsAsync();

        List<ChatCompletionsToolDefinition> toolDefinitions = new List<ChatCompletionsToolDefinition>();

        foreach (var tool in tools)
        {
            Console.WriteLine($"Connected to server with tools: {tool.Name}");
            Console.WriteLine($"Tool description: {tool.Description}");
            Console.WriteLine($"Tool parameters: {tool.JsonSchema}");

            JsonElement propertiesElement;
            tool.JsonSchema.TryGetProperty("properties", out propertiesElement);

            var def = ConvertFrom(tool.Name, tool.Description, propertiesElement);
            Console.WriteLine($"Tool definition: {def}");
            toolDefinitions.Add(def);

            Console.WriteLine($"Properties: {propertiesElement}");        
        }

        return toolDefinitions;
    }
    ```

    ऊपर दिए गए कोड में हमने:

    - MCP टूल प्रतिक्रिया को LLM टूल में बदलने के लिए फ़ंक्शन को अपडेट किया। आइए जोड़े गए कोड को हाइलाइट करें:

        ```csharp
        JsonElement propertiesElement;
        tool.JsonSchema.TryGetProperty("properties", out propertiesElement);

        var def = ConvertFrom(tool.Name, tool.Description, propertiesElement);
        Console.WriteLine($"Tool definition: {def}");
        toolDefinitions.Add(def);
        ```

        इनपुट स्कीमा टूल प्रतिक्रिया का हिस्सा है लेकिन "properties" एट्रिब्यूट पर है, इसलिए हमें इसे निकालने की आवश्यकता है। इसके अलावा, अब हम टूल विवरण के साथ `ConvertFrom` को कॉल करते हैं। अब हमने भारी काम कर लिया है, आइए देखें कि उपयोगकर्ता प्रॉम्प्ट को संभालते समय यह सब कैसे एक साथ आता है।

#### Java

```java
// Create a Bot interface for natural language interaction
public interface Bot {
    String chat(String prompt);
}

// Configure the AI service with LLM and MCP tools
Bot bot = AiServices.builder(Bot.class)
        .chatLanguageModel(model)
        .toolProvider(toolProvider)
        .build();
```

ऊपर दिए गए कोड में हमने:

- प्राकृतिक भाषा इंटरैक्शन के लिए एक सरल `Bot` इंटरफ़ेस परिभाषित किया।
- LangChain4j के `AiServices` का उपयोग करके LLM को MCP टूल प्रोवाइडर के साथ स्वचालित रूप से बाइंड किया।
- फ्रेमवर्क स्वचालित रूप से टूल स्कीमा रूपांतरण और फ़ंक्शन कॉलिंग को बैकग्राउंड में संभालता है।
- यह दृष्टिकोण मैनुअल टूल रूपांतरण को समाप्त करता है - LangChain4j MCP टूल्स को LLM-संगत प्रारूप में बदलने की सभी जटिलता को संभालता है।

#### Rust

MCP टूल प्रतिक्रिया को एक प्रारूप में बदलने के लिए जिसे LLM समझ सके, हम एक हेल्पर फ़ंक्शन जोड़ेंगे जो टूल्स सूची को फॉर्मेट करता है। अपने `main.rs` फ़ाइल में `main` फ़ंक्शन के नीचे निम्नलिखित कोड जोड़ें। इसे LLM को अनुरोध करते समय कॉल किया जाएगा:

```rust
async fn format_tools(tools: &ListToolsResult) -> Result<Vec<Value>, Box<dyn Error>> {
    let tools_json = serde_json::to_value(tools)?;
    let Some(tools_array) = tools_json.get("tools").and_then(|t| t.as_array()) else {
        return Ok(vec![]);
    };

    let formatted_tools = tools_array
        .iter()
        .filter_map(|tool| {
            let name = tool.get("name")?.as_str()?;
            let description = tool.get("description")?.as_str()?;
            let schema = tool.get("inputSchema")?;

            Some(json!({
                "type": "function",
                "function": {
                    "name": name,
                    "description": description,
                    "parameters": {
                        "type": "object",
                        "properties": schema.get("properties").unwrap_or(&json!({})),
                        "required": schema.get("required").unwrap_or(&json!([]))
                    }
                }
            }))
        })
        .collect();

    Ok(formatted_tools)
}
```

बहुत बढ़िया, अब हम किसी भी उपयोगकर्ता अनुरोध को संभालने के लिए तैयार हैं, तो आइए इसे अगले चरण में निपटाएं।

### -4- उपयोगकर्ता प्रॉम्प्ट अनुरोध को संभालें

इस कोड के इस भाग में, हम उपयोगकर्ता अनुरोधों को संभालेंगे।

#### TypeScript

1. एक मेथड जोड़ें जो हमारे LLM को कॉल करने के लिए उपयोग किया जाएगा:

    ```typescript
    async callTools(
        tool_calls: OpenAI.Chat.Completions.ChatCompletionMessageToolCall[],
        toolResults: any[]
    ) {
        for (const tool_call of tool_calls) {
        const toolName = tool_call.function.name;
        const args = tool_call.function.arguments;

        console.log(`Calling tool ${toolName} with args ${JSON.stringify(args)}`);


        // 2. Call the server's tool 
        const toolResult = await this.client.callTool({
            name: toolName,
            arguments: JSON.parse(args),
        });

        console.log("Tool result: ", toolResult);

        // 3. Do something with the result
        // TODO  

        }
    }
    ```

    ऊपर दिए गए कोड में हमने:

    - एक मेथड `callTools` जोड़ा।
    - यह मेथड LLM प्रतिक्रिया लेता है और जांचता है कि क्या कोई टूल्स कॉल किए गए हैं:

        ```typescript
        for (const tool_call of tool_calls) {
        const toolName = tool_call.function.name;
        const args = tool_call.function.arguments;

        console.log(`Calling tool ${toolName} with args ${JSON.stringify(args)}`);

        // call tool
        }
        ```

    - यदि LLM संकेत देता है, तो टूल को कॉल करता है:

        ```typescript
        // 2. Call the server's tool 
        const toolResult = await this.client.callTool({
            name: toolName,
            arguments: JSON.parse(args),
        });

        console.log("Tool result: ", toolResult);

        // 3. Do something with the result
        // TODO  
        ```

1. `run` मेथड को LLM और `callTools` को कॉल करने के लिए अपडेट करें:

    ```typescript

    // 1. Create messages that's input for the LLM
    const prompt = "What is the sum of 2 and 3?"

    const messages: OpenAI.Chat.Completions.ChatCompletionMessageParam[] = [
            {
                role: "user",
                content: prompt,
            },
        ];

    console.log("Querying LLM: ", messages[0].content);

    // 2. Calling the LLM
    let response = this.openai.chat.completions.create({
        model: "gpt-4o-mini",
        max_tokens: 1000,
        messages,
        tools: tools,
    });    

    let results: any[] = [];

    // 3. Go through the LLM response,for each choice, check if it has tool calls 
    (await response).choices.map(async (choice: { message: any; }) => {
        const message = choice.message;
        if (message.tool_calls) {
            console.log("Making tool call")
            await this.callTools(message.tool_calls, results);
        }
    });
    ```

बहुत बढ़िया, आइए कोड को पूरा देखें:

```typescript
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";
import { Transport } from "@modelcontextprotocol/sdk/shared/transport.js";
import OpenAI from "openai";
import { z } from "zod"; // Import zod for schema validation

class MyClient {
    private openai: OpenAI;
    private client: Client;
    constructor(){
        this.openai = new OpenAI({
            baseURL: "https://models.inference.ai.azure.com", // might need to change to this url in the future: https://models.github.ai/inference
            apiKey: process.env.GITHUB_TOKEN,
        });

        this.client = new Client(
            {
                name: "example-client",
                version: "1.0.0"
            },
            {
                capabilities: {
                prompts: {},
                resources: {},
                tools: {}
                }
            }
            );    
    }

    async connectToServer(transport: Transport) {
        await this.client.connect(transport);
        this.run();
        console.error("MCPClient started on stdin/stdout");
    }

    openAiToolAdapter(tool: {
        name: string;
        description?: string;
        input_schema: any;
          }) {
          // Create a zod schema based on the input_schema
          const schema = z.object(tool.input_schema);
      
          return {
            type: "function" as const, // Explicitly set type to "function"
            function: {
              name: tool.name,
              description: tool.description,
              parameters: {
              type: "object",
              properties: tool.input_schema.properties,
              required: tool.input_schema.required,
              },
            },
          };
    }
    
    async callTools(
        tool_calls: OpenAI.Chat.Completions.ChatCompletionMessageToolCall[],
        toolResults: any[]
      ) {
        for (const tool_call of tool_calls) {
          const toolName = tool_call.function.name;
          const args = tool_call.function.arguments;
    
          console.log(`Calling tool ${toolName} with args ${JSON.stringify(args)}`);
    
    
          // 2. Call the server's tool 
          const toolResult = await this.client.callTool({
            name: toolName,
            arguments: JSON.parse(args),
          });
    
          console.log("Tool result: ", toolResult);
    
          // 3. Do something with the result
          // TODO  
    
         }
    }

    async run() {
        console.log("Asking server for available tools");
        const toolsResult = await this.client.listTools();
        const tools = toolsResult.tools.map((tool) => {
            return this.openAiToolAdapter({
              name: tool.name,
              description: tool.description,
              input_schema: tool.inputSchema,
            });
        });

        const prompt = "What is the sum of 2 and 3?";
    
        const messages: OpenAI.Chat.Completions.ChatCompletionMessageParam[] = [
            {
                role: "user",
                content: prompt,
            },
        ];

        console.log("Querying LLM: ", messages[0].content);
        let response = this.openai.chat.completions.create({
            model: "gpt-4o-mini",
            max_tokens: 1000,
            messages,
            tools: tools,
        });    

        let results: any[] = [];
    
        // 1. Go through the LLM response,for each choice, check if it has tool calls 
        (await response).choices.map(async (choice: { message: any; }) => {
          const message = choice.message;
          if (message.tool_calls) {
              console.log("Making tool call")
              await this.callTools(message.tool_calls, results);
          }
        });
    }
    
}

let client = new MyClient();
 const transport = new StdioClientTransport({
            command: "node",
            args: ["./build/index.js"]
        });

client.connectToServer(transport);
```

#### Python

1. LLM को कॉल करने के लिए आवश्यक इंपोर्ट्स जोड़ें:

    ```python
    # llm
    import os
    from azure.ai.inference import ChatCompletionsClient
    from azure.ai.inference.models import SystemMessage, UserMessage
    from azure.core.credentials import AzureKeyCredential
    import json
    ```

1. इसके बाद, वह फ़ंक्शन जोड़ें जो LLM को कॉल करेगा:

    ```python
    # llm

    def call_llm(prompt, functions):
        token = os.environ["GITHUB_TOKEN"]
        endpoint = "https://models.inference.ai.azure.com"

        model_name = "gpt-4o"

        client = ChatCompletionsClient(
            endpoint=endpoint,
            credential=AzureKeyCredential(token),
        )

        print("CALLING LLM")
        response = client.complete(
            messages=[
                {
                "role": "system",
                "content": "You are a helpful assistant.",
                },
                {
                "role": "user",
                "content": prompt,
                },
            ],
            model=model_name,
            tools = functions,
            # Optional parameters
            temperature=1.,
            max_tokens=1000,
            top_p=1.    
        )

        response_message = response.choices[0].message
        
        functions_to_call = []

        if response_message.tool_calls:
            for tool_call in response_message.tool_calls:
                print("TOOL: ", tool_call)
                name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)
                functions_to_call.append({ "name": name, "args": args })

        return functions_to_call
    ```

    ऊपर दिए गए कोड में हमने:

    - हमारे फ़ंक्शंस, जिन्हें हमने MCP सर्वर पर पाया और रूपांतरित किया, LLM को पास किए।
    - फिर हमने LLM को इन फ़ंक्शंस के साथ कॉल किया।
    - फिर, हम परिणाम का निरीक्षण कर रहे हैं कि कौन से फ़ंक्शंस कॉल किए जाने चाहिए, यदि कोई हो।
    - अंत में, हम कॉल करने के लिए फ़ंक्शंस की एक सूची पास कर रहे हैं।

1. अंतिम चरण, हमारे मुख्य कोड को अपडेट करें:

    ```python
    prompt = "Add 2 to 20"

    # ask LLM what tools to all, if any
    functions_to_call = call_llm(prompt, functions)

    # call suggested functions
    for f in functions_to_call:
        result = await session.call_tool(f["name"], arguments=f["args"])
        print("TOOLS result: ", result.content)
    ```

    वहां, यह अंतिम चरण था। ऊपर दिए गए कोड में हम:

    - MCP सर्वर पर `call_tool` के माध्यम से MCP टूल को कॉल कर रहे हैं, एक फ़ंक्शन का उपयोग करके जिसे LLM ने हमारे प्रॉम्प्ट के आधार पर कॉल करने के लिए सोचा।
    - MCP सर्वर के टूल कॉल का परिणाम प्रिंट कर रहे हैं।

#### .NET

1. LLM प्रॉम्प्ट अनुरोध के लिए कोड दिखाएं:

    ```csharp
    var tools = await GetMcpTools();

    for (int i = 0; i < tools.Count; i++)
    {
        var tool = tools[i];
        Console.WriteLine($"MCP Tools def: {i}: {tool}");
    }

    // 0. Define the chat history and the user message
    var userMessage = "add 2 and 4";

    chatHistory.Add(new ChatRequestUserMessage(userMessage));

    // 1. Define tools
    ChatCompletionsToolDefinition def = CreateToolDefinition();


    // 2. Define options, including the tools
    var options = new ChatCompletionsOptions(chatHistory)
    {
        Model = "gpt-4o-mini",
        Tools = { tools[0] }
    };

    // 3. Call the model  

    ChatCompletions? response = await client.CompleteAsync(options);
    var content = response.Content;

    ```

    ऊपर दिए गए कोड में हमने:

    - MCP सर्वर से टूल्स प्राप्त किए, `var tools = await GetMcpTools()`।
    - एक उपयोगकर्ता प्रॉम्प्ट `userMessage` परिभाषित किया।
    - एक विकल्प ऑब्जेक्ट बनाया जिसमें मॉडल और टूल्स निर्दिष्ट किए गए।
    - LLM की ओर एक अनुरोध किया।

1. एक अंतिम चरण, देखें कि क्या LLM सोचता है कि हमें कोई फ़ंक्शन कॉल करना चाहिए:

    ```csharp
    // 4. Check if the response contains a function call
    ChatCompletionsToolCall? calls = response.ToolCalls.FirstOrDefault();
    for (int i = 0; i < response.ToolCalls.Count; i++)
    {
        var call = response.ToolCalls[i];
        Console.WriteLine($"Tool call {i}: {call.Name} with arguments {call.Arguments}");
        //Tool call 0: add with arguments {"a":2,"b":4}

        var dict = JsonSerializer.Deserialize<Dictionary<string, object>>(call.Arguments);
        var result = await mcpClient.CallToolAsync(
            call.Name,
            dict!,
            cancellationToken: CancellationToken.None
        );

        Console.WriteLine(result.Content.First(c => c.Type == "text").Text);

    }
    ```

    ऊपर दिए गए कोड में हमने:

    - फ़ंक्शन कॉल की सूची के माध्यम से लूप किया।
    - प्रत्येक टूल कॉल के लिए, नाम और तर्कों को पार्स किया और MCP क्लाइंट का उपयोग करके MCP सर्वर पर टूल को कॉल किया। अंत में हमने परिणाम प्रिंट किए।

यहां पूरा कोड है:

```csharp
using Azure;
using Azure.AI.Inference;
using Azure.Identity;
using System.Text.Json;
using ModelContextProtocol.Client;
using ModelContextProtocol.Protocol.Transport;
using System.Text.Json;

var endpoint = "https://models.inference.ai.azure.com";
var token = Environment.GetEnvironmentVariable("GITHUB_TOKEN"); // Your GitHub Access Token
var client = new ChatCompletionsClient(new Uri(endpoint), new AzureKeyCredential(token));
var chatHistory = new List<ChatRequestMessage>
{
    new ChatRequestSystemMessage("You are a helpful assistant that knows about AI")
};

var clientTransport = new StdioClientTransport(new()
{
    Name = "Demo Server",
    Command = "/workspaces/mcp-for-beginners/03-GettingStarted/02-client/solution/server/bin/Debug/net8.0/server",
    Arguments = [],
});

Console.WriteLine("Setting up stdio transport");

await using var mcpClient = await McpClientFactory.CreateAsync(clientTransport);

ChatCompletionsToolDefinition ConvertFrom(string name, string description, JsonElement jsonElement)
{ 
    // convert the tool to a function definition
    FunctionDefinition functionDefinition = new FunctionDefinition(name)
    {
        Description = description,
        Parameters = BinaryData.FromObjectAsJson(new
        {
            Type = "object",
            Properties = jsonElement
        },
        new JsonSerializerOptions() { PropertyNamingPolicy = JsonNamingPolicy.CamelCase })
    };

    // create a tool definition
    ChatCompletionsToolDefinition toolDefinition = new ChatCompletionsToolDefinition(functionDefinition);
    return toolDefinition;
}



async Task<List<ChatCompletionsToolDefinition>> GetMcpTools()
{
    Console.WriteLine("Listing tools");
    var tools = await mcpClient.ListToolsAsync();

    List<ChatCompletionsToolDefinition> toolDefinitions = new List<ChatCompletionsToolDefinition>();

    foreach (var tool in tools)
    {
        Console.WriteLine($"Connected to server with tools: {tool.Name}");
        Console.WriteLine($"Tool description: {tool.Description}");
        Console.WriteLine($"Tool parameters: {tool.JsonSchema}");

        JsonElement propertiesElement;
        tool.JsonSchema.TryGetProperty("properties", out propertiesElement);

        var def = ConvertFrom(tool.Name, tool.Description, propertiesElement);
        Console.WriteLine($"Tool definition: {def}");
        toolDefinitions.Add(def);

        Console.WriteLine($"Properties: {propertiesElement}");        
    }

    return toolDefinitions;
}

// 1. List tools on mcp server

var tools = await GetMcpTools();
for (int i = 0; i < tools.Count; i++)
{
    var tool = tools[i];
    Console.WriteLine($"MCP Tools def: {i}: {tool}");
}

// 2. Define the chat history and the user message
var userMessage = "add 2 and 4";

chatHistory.Add(new ChatRequestUserMessage(userMessage));


// 3. Define options, including the tools
var options = new ChatCompletionsOptions(chatHistory)
{
    Model = "gpt-4o-mini",
    Tools = { tools[0] }
};

// 4. Call the model  

ChatCompletions? response = await client.CompleteAsync(options);
var content = response.Content;

// 5. Check if the response contains a function call
ChatCompletionsToolCall? calls = response.ToolCalls.FirstOrDefault();
for (int i = 0; i < response.ToolCalls.Count; i++)
{
    var call = response.ToolCalls[i];
    Console.WriteLine($"Tool call {i}: {call.Name} with arguments {call.Arguments}");
    //Tool call 0: add with arguments {"a":2,"b":4}

    var dict = JsonSerializer.Deserialize<Dictionary<string, object>>(call.Arguments);
    var result = await mcpClient.CallToolAsync(
        call.Name,
        dict!,
        cancellationToken: CancellationToken.None
    );

    Console.WriteLine(result.Content.First(c => c.Type == "text").Text);

}

// 5. Print the generic response
Console.WriteLine($"Assistant response: {content}");
```

#### Java

```java
try {
    // Execute natural language requests that automatically use MCP tools
    String response = bot.chat("Calculate the sum of 24.5 and 17.3 using the calculator service");
    System.out.println(response);

    response = bot.chat("What's the square root of 144?");
    System.out.println(response);

    response = bot.chat("Show me the help for the calculator service");
    System.out.println(response);
} finally {
    mcpClient.close();
}
```

ऊपर दिए गए कोड में हमने:

- MCP सर्वर टूल्स के साथ बातचीत करने के लिए सरल प्राकृतिक भाषा प्रॉम्प्ट्स का उपयोग किया।
- LangChain4j फ्रेमवर्क स्वचालित रूप से संभालता है:
  - जब आवश्यक हो, तो उपयोगकर्ता प्रॉम्प्ट्स को टूल कॉल्स में बदलना।
  - LLM के निर्णय के आधार पर उपयुक्त MCP टूल्स को कॉल करना।
  - LLM और MCP सर्वर के बीच बातचीत प्रवाह का प्रबंधन।
- `bot.chat()` मेथड प्राकृतिक भाषा प्रतिक्रियाएं लौटाता है, जिनमें MCP टूल निष्पादन के परिणाम शामिल हो सकते हैं।
- यह दृष्टिकोण एक सहज उपयोगकर्ता अनुभव प्रदान करता है जहां उपयोगकर्ताओं को अंतर्निहित MCP कार्यान्वयन के बारे में जानने की आवश्यकता नहीं होती।

पूरा कोड उदाहरण:

```java
public class LangChain4jClient {
    
    public static void main(String[] args) throws Exception {        ChatLanguageModel model = OpenAiOfficialChatModel.builder()
                .isGitHubModels(true)
                .apiKey(System.getenv("GITHUB_TOKEN"))
                .timeout(Duration.ofSeconds(60))
                .modelName("gpt-4.1-nano")
                .timeout(Duration.ofSeconds(60))
                .build();

        McpTransport transport = new HttpMcpTransport.Builder()
                .sseUrl("http://localhost:8080/sse")
                .timeout(Duration.ofSeconds(60))
                .logRequests(true)
                .logResponses(true)
                .build();

        McpClient mcpClient = new DefaultMcpClient.Builder()
                .transport(transport)
                .build();

        ToolProvider toolProvider = McpToolProvider.builder()
                .mcpClients(List.of(mcpClient))
                .build();

        Bot bot = AiServices.builder(Bot.class)
                .chatLanguageModel(model)
                .toolProvider(toolProvider)
                .build();

        try {
            String response = bot.chat("Calculate the sum of 24.5 and 17.3 using the calculator service");
            System.out.println(response);

            response = bot.chat("What's the square root of 144?");
            System.out.println(response);

            response = bot.chat("Show me the help for the calculator service");
            System.out.println(response);
        } finally {
            mcpClient.close();
        }
    }
}
```

#### Rust

यहां अधिकांश काम होता है। हम प्रारंभिक उपयोगकर्ता प्रॉम्प्ट के साथ LLM को कॉल करेंगे, फिर प्रतिक्रिया को प्रोसेस करेंगे यह देखने के लिए कि क्या कोई टूल्स कॉल किए जाने की आवश्यकता है। यदि हां, तो हम उन टूल्स को कॉल करेंगे और LLM के साथ बातचीत जारी रखेंगे जब तक कि कोई और टूल कॉल की आवश्यकता न हो और हमारे पास अंतिम प्रतिक्रिया न हो।
हम LLM कॉल को संभालने के लिए एक फ़ंक्शन परिभाषित करेंगे। अपने `main.rs` फ़ाइल में निम्नलिखित फ़ंक्शन जोड़ें:

```rust
async fn call_llm(
    client: &Client<OpenAIConfig>,
    messages: &[Value],
    tools: &ListToolsResult,
) -> Result<Value, Box<dyn Error>> {
    let response = client
        .completions()
        .create_byot(json!({
            "messages": messages,
            "model": "openai/gpt-4.1",
            "tools": format_tools(tools).await?,
        }))
        .await?;
    Ok(response)
}
```

यह फ़ंक्शन LLM क्लाइंट, संदेशों की एक सूची (जिसमें उपयोगकर्ता का प्रॉम्प्ट शामिल है), MCP सर्वर से टूल्स लेता है, और LLM को एक अनुरोध भेजता है, जो प्रतिक्रिया लौटाता है।

LLM से प्रतिक्रिया में `choices` की एक सूची होगी। हमें परिणाम को प्रोसेस करना होगा यह देखने के लिए कि क्या कोई `tool_calls` मौजूद हैं। यह हमें बताता है कि LLM किसी विशेष टूल को तर्कों के साथ कॉल करने का अनुरोध कर रहा है। अपने `main.rs` फ़ाइल के अंत में निम्नलिखित कोड जोड़ें ताकि LLM प्रतिक्रिया को संभालने के लिए एक फ़ंक्शन परिभाषित किया जा सके:

```rust
async fn process_llm_response(
    llm_response: &Value,
    mcp_client: &RunningService<RoleClient, ()>,
    openai_client: &Client<OpenAIConfig>,
    mcp_tools: &ListToolsResult,
    messages: &mut Vec<Value>,
) -> Result<(), Box<dyn Error>> {
    let Some(message) = llm_response
        .get("choices")
        .and_then(|c| c.as_array())
        .and_then(|choices| choices.first())
        .and_then(|choice| choice.get("message"))
    else {
        return Ok(());
    };

    // Print content if available
    if let Some(content) = message.get("content").and_then(|c| c.as_str()) {
        println!("🤖 {}", content);
    }

    // Handle tool calls
    if let Some(tool_calls) = message.get("tool_calls").and_then(|tc| tc.as_array()) {
        messages.push(message.clone()); // Add assistant message

        // Execute each tool call
        for tool_call in tool_calls {
            let (tool_id, name, args) = extract_tool_call_info(tool_call)?;
            println!("⚡ Calling tool: {}", name);

            let result = mcp_client
                .call_tool(CallToolRequestParam {
                    name: name.into(),
                    arguments: serde_json::from_str::<Value>(&args)?.as_object().cloned(),
                })
                .await?;

            // Add tool result to messages
            messages.push(json!({
                "role": "tool",
                "tool_call_id": tool_id,
                "content": serde_json::to_string_pretty(&result)?
            }));
        }

        // Continue conversation with tool results
        let response = call_llm(openai_client, messages, mcp_tools).await?;
        Box::pin(process_llm_response(
            &response,
            mcp_client,
            openai_client,
            mcp_tools,
            messages,
        ))
        .await?;
    }
    Ok(())
}
```

यदि `tool_calls` मौजूद हैं, तो यह टूल की जानकारी निकालता है, MCP सर्वर को टूल अनुरोध के साथ कॉल करता है, और परिणामों को वार्तालाप संदेशों में जोड़ता है। फिर यह LLM के साथ वार्तालाप जारी रखता है और संदेशों को सहायक की प्रतिक्रिया और टूल कॉल परिणामों के साथ अपडेट करता है।

MCP कॉल के लिए LLM द्वारा लौटाई गई टूल कॉल जानकारी निकालने के लिए, हम एक और सहायक फ़ंक्शन जोड़ेंगे जो कॉल करने के लिए आवश्यक सब कुछ निकालता है। अपने `main.rs` फ़ाइल के अंत में निम्नलिखित कोड जोड़ें:

```rust
fn extract_tool_call_info(tool_call: &Value) -> Result<(String, String, String), Box<dyn Error>> {
    let tool_id = tool_call
        .get("id")
        .and_then(|id| id.as_str())
        .unwrap_or("")
        .to_string();
    let function = tool_call.get("function").ok_or("Missing function")?;
    let name = function
        .get("name")
        .and_then(|n| n.as_str())
        .unwrap_or("")
        .to_string();
    let args = function
        .get("arguments")
        .and_then(|a| a.as_str())
        .unwrap_or("{}")
        .to_string();
    Ok((tool_id, name, args))
}
```

सभी टुकड़े तैयार होने के बाद, अब हम प्रारंभिक उपयोगकर्ता प्रॉम्प्ट को संभाल सकते हैं और LLM को कॉल कर सकते हैं। अपने `main` फ़ंक्शन को निम्नलिखित कोड के साथ अपडेट करें:

```rust
// LLM conversation with tool calls
let response = call_llm(&openai_client, &messages, &tools).await?;
process_llm_response(
    &response,
    &mcp_client,
    &openai_client,
    &tools,
    &mut messages,
)
.await?;
```

यह प्रारंभिक उपयोगकर्ता प्रॉम्प्ट के साथ LLM से क्वेरी करेगा, जिसमें दो संख्याओं के योग के लिए पूछा जाएगा, और प्रतिक्रिया को प्रोसेस करेगा ताकि टूल कॉल को डायनामिक रूप से संभाला जा सके।

शानदार, आपने कर दिखाया!

## असाइनमेंट

अभ्यास से कोड लें और सर्वर को और अधिक टूल्स के साथ बनाएं। फिर अभ्यास की तरह एक LLM के साथ एक क्लाइंट बनाएं और इसे विभिन्न प्रॉम्प्ट्स के साथ टेस्ट करें ताकि यह सुनिश्चित हो सके कि आपके सभी सर्वर टूल्स डायनामिक रूप से कॉल हो रहे हैं। इस तरह से क्लाइंट बनाना उपयोगकर्ता को एक शानदार अनुभव प्रदान करता है क्योंकि वे प्रॉम्प्ट्स का उपयोग कर सकते हैं, सटीक क्लाइंट कमांड्स की आवश्यकता नहीं होती, और MCP सर्वर के कॉल होने से अनजान रहते हैं।

## समाधान

[Solution](/03-GettingStarted/03-llm-client/solution/README.md)

## मुख्य बातें

- अपने क्लाइंट में LLM जोड़ने से उपयोगकर्ताओं को MCP सर्वर्स के साथ इंटरैक्ट करने का एक बेहतर तरीका मिलता है।
- आपको MCP सर्वर प्रतिक्रिया को LLM के समझने योग्य प्रारूप में बदलने की आवश्यकता होती है।

## नमूने

- [Java Calculator](../samples/java/calculator/README.md)
- [.Net Calculator](../../../../03-GettingStarted/samples/csharp)
- [JavaScript Calculator](../samples/javascript/README.md)
- [TypeScript Calculator](../samples/typescript/README.md)
- [Python Calculator](../../../../03-GettingStarted/samples/python)
- [Rust Calculator](../../../../03-GettingStarted/samples/rust)

## अतिरिक्त संसाधन

## आगे क्या

- अगला: [Visual Studio Code का उपयोग करके सर्वर का उपभोग करना](../04-vscode/README.md)

**अस्वीकरण**:  
यह दस्तावेज़ AI अनुवाद सेवा [Co-op Translator](https://github.com/Azure/co-op-translator) का उपयोग करके अनुवादित किया गया है। जबकि हम सटीकता सुनिश्चित करने का प्रयास करते हैं, कृपया ध्यान दें कि स्वचालित अनुवाद में त्रुटियां या अशुद्धियां हो सकती हैं। मूल भाषा में उपलब्ध मूल दस्तावेज़ को प्रामाणिक स्रोत माना जाना चाहिए। महत्वपूर्ण जानकारी के लिए, पेशेवर मानव अनुवाद की सिफारिश की जाती है। इस अनुवाद के उपयोग से उत्पन्न किसी भी गलतफहमी या गलत व्याख्या के लिए हम उत्तरदायी नहीं हैं।