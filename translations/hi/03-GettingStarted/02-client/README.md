<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "94c80ae71fb9971e9b57b51ab0912121",
  "translation_date": "2025-08-12T19:25:50+00:00",
  "source_file": "03-GettingStarted/02-client/README.md",
  "language_code": "hi"
}
-->
# क्लाइंट बनाना

क्लाइंट कस्टम एप्लिकेशन या स्क्रिप्ट होते हैं जो सीधे MCP सर्वर के साथ संवाद करते हैं ताकि संसाधन, टूल और प्रॉम्प्ट्स का अनुरोध किया जा सके। इंस्पेक्टर टूल का उपयोग करने के विपरीत, जो सर्वर के साथ इंटरैक्ट करने के लिए एक ग्राफिकल इंटरफ़ेस प्रदान करता है, अपना खुद का क्लाइंट लिखने से प्रोग्रामेटिक और स्वचालित इंटरैक्शन संभव हो जाता है। यह डेवलपर्स को MCP क्षमताओं को अपने वर्कफ़्लो में एकीकृत करने, कार्यों को स्वचालित करने और विशिष्ट आवश्यकताओं के अनुसार कस्टम समाधान बनाने की अनुमति देता है।

## परिचय

यह पाठ MCP (मॉडल कॉन्टेक्स्ट प्रोटोकॉल) इकोसिस्टम के भीतर क्लाइंट्स की अवधारणा को पेश करता है। आप सीखेंगे कि अपना खुद का क्लाइंट कैसे लिखें और इसे MCP सर्वर से कैसे कनेक्ट करें।

## सीखने के उद्देश्य

इस पाठ के अंत तक, आप सक्षम होंगे:

- समझें कि एक क्लाइंट क्या कर सकता है।
- अपना खुद का क्लाइंट लिखें।
- MCP सर्वर के साथ क्लाइंट को कनेक्ट और टेस्ट करें ताकि यह सुनिश्चित हो सके कि सर्वर अपेक्षा के अनुसार काम कर रहा है।

## क्लाइंट लिखने में क्या शामिल है?

क्लाइंट लिखने के लिए, आपको निम्नलिखित करना होगा:

- **सही लाइब्रेरीज़ इंपोर्ट करें**। आप वही लाइब्रेरी उपयोग करेंगे, बस अलग-अलग कॉन्स्ट्रक्ट्स के साथ।
- **क्लाइंट को इंस्टैंशिएट करें**। इसमें एक क्लाइंट इंस्टेंस बनाना और इसे चुने गए ट्रांसपोर्ट मेथड से कनेक्ट करना शामिल होगा।
- **तय करें कि कौन से संसाधनों को सूचीबद्ध करना है**। आपका MCP सर्वर संसाधनों, टूल्स और प्रॉम्प्ट्स के साथ आता है, आपको तय करना होगा कि इनमें से किसे सूचीबद्ध करना है।
- **क्लाइंट को होस्ट एप्लिकेशन में एकीकृत करें**। एक बार जब आप सर्वर की क्षमताओं को जान लेते हैं, तो आपको इसे अपने होस्ट एप्लिकेशन में एकीकृत करना होगा ताकि यदि कोई उपयोगकर्ता कोई प्रॉम्प्ट या अन्य कमांड टाइप करता है, तो संबंधित सर्वर फीचर सक्रिय हो जाए।

अब जब हमने उच्च स्तर पर समझ लिया है कि हम क्या करने जा रहे हैं, तो चलिए अगले उदाहरण पर नज़र डालते हैं।

### एक उदाहरण क्लाइंट

आइए इस उदाहरण क्लाइंट पर नज़र डालें:

### टाइपस्क्रिप्ट

```typescript
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";

const transport = new StdioClientTransport({
  command: "node",
  args: ["server.js"]
});

const client = new Client(
  {
    name: "example-client",
    version: "1.0.0"
  }
);

await client.connect(transport);

// List prompts
const prompts = await client.listPrompts();

// Get a prompt
const prompt = await client.getPrompt({
  name: "example-prompt",
  arguments: {
    arg1: "value"
  }
});

// List resources
const resources = await client.listResources();

// Read a resource
const resource = await client.readResource({
  uri: "file:///example.txt"
});

// Call a tool
const result = await client.callTool({
  name: "example-tool",
  arguments: {
    arg1: "value"
  }
});
```

ऊपर दिए गए कोड में हमने:

- लाइब्रेरीज़ इंपोर्ट कीं।
- एक क्लाइंट का इंस्टेंस बनाया और इसे ट्रांसपोर्ट के लिए `stdio` का उपयोग करके कनेक्ट किया।
- प्रॉम्प्ट्स, संसाधनों और टूल्स को सूचीबद्ध किया और उन सभी को सक्रिय किया।

यह रहा आपका एक क्लाइंट जो MCP सर्वर से बात कर सकता है।

आइए अगले अभ्यास खंड में प्रत्येक कोड स्निपेट को विस्तार से समझें और देखें कि इसमें क्या हो रहा है।

## अभ्यास: क्लाइंट लिखना

जैसा कि ऊपर कहा गया है, आइए कोड को विस्तार से समझें, और यदि आप चाहें तो कोड के साथ अभ्यास करें।

### -1- लाइब्रेरीज़ इंपोर्ट करें

आवश्यक लाइब्रेरीज़ इंपोर्ट करें। हमें क्लाइंट और हमारे चुने हुए ट्रांसपोर्ट प्रोटोकॉल, `stdio` का संदर्भ चाहिए। `stdio` उन चीज़ों के लिए एक प्रोटोकॉल है जो आपके लोकल मशीन पर चलने के लिए बनाई गई हैं। `SSE` एक और ट्रांसपोर्ट प्रोटोकॉल है जिसे हम भविष्य के अध्यायों में दिखाएंगे, लेकिन अभी के लिए, हम `stdio` के साथ जारी रखते हैं।

#### टाइपस्क्रिप्ट

```typescript
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";
```

#### पायथन

```python
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client
```

#### .NET

```csharp
using Microsoft.Extensions.AI;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Hosting;
using ModelContextProtocol.Client;
using ModelContextProtocol.Protocol.Transport;
```

#### जावा

जावा के लिए, आप पिछले अभ्यास से MCP सर्वर से कनेक्ट करने के लिए एक क्लाइंट बनाएंगे। [MCP सर्वर के साथ शुरुआत](../../../../03-GettingStarted/01-first-server/solution/java) से जावा स्प्रिंग बूट प्रोजेक्ट संरचना का उपयोग करते हुए, `src/main/java/com/microsoft/mcp/sample/client/` फोल्डर में `SDKClient` नामक एक नई जावा क्लास बनाएं और निम्नलिखित इंपोर्ट्स जोड़ें:

```java
import java.util.Map;
import org.springframework.web.reactive.function.client.WebClient;
import io.modelcontextprotocol.client.McpClient;
import io.modelcontextprotocol.client.transport.WebFluxSseClientTransport;
import io.modelcontextprotocol.spec.McpClientTransport;
import io.modelcontextprotocol.spec.McpSchema.CallToolRequest;
import io.modelcontextprotocol.spec.McpSchema.CallToolResult;
import io.modelcontextprotocol.spec.McpSchema.ListToolsResult;
```

#### रस्ट

आपको अपने `Cargo.toml` फाइल में निम्नलिखित डिपेंडेंसीज़ जोड़ने की आवश्यकता होगी।

```toml
[package]
name = "calculator-client"
version = "0.1.0"
edition = "2024"

[dependencies]
rmcp = { version = "0.5.0", features = ["client", "transport-child-process"] }
serde_json = "1.0.141"
tokio = { version = "1.46.1", features = ["rt-multi-thread"] }
```

इसके बाद, आप अपने क्लाइंट कोड में आवश्यक लाइब्रेरीज़ इंपोर्ट कर सकते हैं।

```rust
use rmcp::{
    RmcpError,
    model::CallToolRequestParam,
    service::ServiceExt,
    transport::{ConfigureCommandExt, TokioChildProcess},
};
use tokio::process::Command;
```

आइए इंस्टैंशिएशन पर आगे बढ़ें।

### -2- क्लाइंट और ट्रांसपोर्ट को इंस्टैंशिएट करना

हमें ट्रांसपोर्ट और क्लाइंट का एक इंस्टेंस बनाना होगा:

#### टाइपस्क्रिप्ट

```typescript
const transport = new StdioClientTransport({
  command: "node",
  args: ["server.js"]
});

const client = new Client(
  {
    name: "example-client",
    version: "1.0.0"
  }
);

await client.connect(transport);
```

ऊपर दिए गए कोड में हमने:

- `stdio` ट्रांसपोर्ट का एक इंस्टेंस बनाया। ध्यान दें कि यह सर्वर को ढूंढने और स्टार्ट करने के लिए कमांड और आर्ग्स को निर्दिष्ट करता है, क्योंकि यह कुछ ऐसा है जिसे हमें क्लाइंट बनाते समय करना होगा।

    ```typescript
    const transport = new StdioClientTransport({
        command: "node",
        args: ["server.js"]
    });
    ```

- एक क्लाइंट को नाम और संस्करण देकर इंस्टैंशिएट किया।

    ```typescript
    const client = new Client(
    {
        name: "example-client",
        version: "1.0.0"
    });
    ```

- क्लाइंट को चुने गए ट्रांसपोर्ट से कनेक्ट किया।

    ```typescript
    await client.connect(transport);
    ```

#### पायथन

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

- आवश्यक लाइब्रेरीज़ इंपोर्ट कीं।
- सर्वर पैरामीटर ऑब्जेक्ट को इंस्टैंशिएट किया, क्योंकि हम इसका उपयोग सर्वर को चलाने के लिए करेंगे ताकि हम अपने क्लाइंट के साथ कनेक्ट कर सकें।
- `run` नामक एक विधि परिभाषित की, जो `stdio_client` को कॉल करती है, जो एक क्लाइंट सत्र शुरू करता है।
- एक एंट्री पॉइंट बनाया जहां हम `run` विधि को `asyncio.run` में प्रदान करते हैं।

#### .NET

```dotnet
using Microsoft.Extensions.AI;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Hosting;
using ModelContextProtocol.Client;
using ModelContextProtocol.Protocol.Transport;

var builder = Host.CreateApplicationBuilder(args);

builder.Configuration
    .AddEnvironmentVariables()
    .AddUserSecrets<Program>();



var clientTransport = new StdioClientTransport(new()
{
    Name = "Demo Server",
    Command = "dotnet",
    Arguments = ["run", "--project", "path/to/file.csproj"],
});

await using var mcpClient = await McpClientFactory.CreateAsync(clientTransport);
```

ऊपर दिए गए कोड में हमने:

- आवश्यक लाइब्रेरीज़ इंपोर्ट कीं।
- `stdio` ट्रांसपोर्ट बनाया और एक क्लाइंट `mcpClient` बनाया। बाद वाले का उपयोग हम MCP सर्वर पर फीचर्स को सूचीबद्ध और सक्रिय करने के लिए करेंगे।

ध्यान दें, "Arguments" में, आप या तो *.csproj* या निष्पादन योग्य फ़ाइल की ओर इशारा कर सकते हैं।

#### जावा

```java
public class SDKClient {
    
    public static void main(String[] args) {
        var transport = new WebFluxSseClientTransport(WebClient.builder().baseUrl("http://localhost:8080"));
        new SDKClient(transport).run();
    }
    
    private final McpClientTransport transport;

    public SDKClient(McpClientTransport transport) {
        this.transport = transport;
    }

    public void run() {
        var client = McpClient.sync(this.transport).build();
        client.initialize();
        
        // Your client logic goes here
    }
}
```

ऊपर दिए गए कोड में हमने:

- एक मुख्य विधि बनाई जो `http://localhost:8080` पर चल रहे MCP सर्वर की ओर इशारा करते हुए SSE ट्रांसपोर्ट सेट करती है।
- एक क्लाइंट क्लास बनाई जो ट्रांसपोर्ट को कंस्ट्रक्टर पैरामीटर के रूप में लेती है।
- `run` विधि में, हमने ट्रांसपोर्ट का उपयोग करके एक सिंक्रोनस MCP क्लाइंट बनाया और कनेक्शन को इनिशियलाइज़ किया।
- SSE (सर्वर-सेंट इवेंट्स) ट्रांसपोर्ट का उपयोग किया, जो जावा स्प्रिंग बूट MCP सर्वर्स के साथ HTTP-आधारित संचार के लिए उपयुक्त है।

#### रस्ट

यह रस्ट क्लाइंट मानता है कि सर्वर उसी डायरेक्टरी में "calculator-server" नामक एक सिबलिंग प्रोजेक्ट है। नीचे दिया गया कोड सर्वर को शुरू करेगा और उससे कनेक्ट करेगा।

```rust
async fn main() -> Result<(), RmcpError> {
    // Assume the server is a sibling project named "calculator-server" in the same directory
    let server_dir = std::path::Path::new(env!("CARGO_MANIFEST_DIR"))
        .parent()
        .expect("failed to locate workspace root")
        .join("calculator-server");

    let client = ()
        .serve(
            TokioChildProcess::new(Command::new("cargo").configure(|cmd| {
                cmd.arg("run").current_dir(server_dir);
            }))
            .map_err(RmcpError::transport_creation::<TokioChildProcess>)?,
        )
        .await?;

    // TODO: Initialize

    // TODO: List tools

    // TODO: Call add tool with arguments = {"a": 3, "b": 2}

    client.cancel().await?;
    Ok(())
}
```

### -3- सर्वर फीचर्स को सूचीबद्ध करना

अब, हमारे पास एक क्लाइंट है जो प्रोग्राम चलाए जाने पर कनेक्ट कर सकता है। हालांकि, यह वास्तव में फीचर्स को सूचीबद्ध नहीं करता है, तो चलिए इसे अगला करते हैं:

#### टाइपस्क्रिप्ट

```typescript
// List prompts
const prompts = await client.listPrompts();

// List resources
const resources = await client.listResources();

// list tools
const tools = await client.listTools();
```

#### पायथन

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
```

यहां हमने उपलब्ध संसाधनों को `list_resources()` और टूल्स को `list_tools` के माध्यम से सूचीबद्ध किया और उन्हें प्रिंट किया।

#### .NET

```dotnet
foreach (var tool in await client.ListToolsAsync())
{
    Console.WriteLine($"{tool.Name} ({tool.Description})");
}
```

ऊपर एक उदाहरण है कि हम सर्वर पर टूल्स को कैसे सूचीबद्ध कर सकते हैं। प्रत्येक टूल के लिए, हमने उसका नाम प्रिंट किया।

#### जावा

```java
// List and demonstrate tools
ListToolsResult toolsList = client.listTools();
System.out.println("Available Tools = " + toolsList);

// You can also ping the server to verify connection
client.ping();
```

ऊपर दिए गए कोड में हमने:

- `listTools()` को कॉल किया ताकि MCP सर्वर से सभी उपलब्ध टूल्स प्राप्त किए जा सकें।
- `ping()` का उपयोग करके यह सत्यापित किया कि सर्वर से कनेक्शन काम कर रहा है।
- `ListToolsResult` में सभी टूल्स की जानकारी होती है, जिसमें उनके नाम, विवरण और इनपुट स्कीमा शामिल हैं।

बहुत बढ़िया, अब हमने सभी फीचर्स को कैप्चर कर लिया है। अब सवाल यह है कि हम उनका उपयोग कब करें? खैर, यह क्लाइंट काफी सरल है, सरल इस मायने में कि हमें फीचर्स को सक्रिय करने के लिए उन्हें स्पष्ट रूप से कॉल करना होगा। अगले अध्याय में, हम एक अधिक उन्नत क्लाइंट बनाएंगे जिसमें अपना बड़ा भाषा मॉडल (LLM) होगा। फिलहाल, चलिए देखते हैं कि हम सर्वर पर फीचर्स को कैसे सक्रिय कर सकते हैं:

#### रस्ट

मुख्य फ़ंक्शन में, क्लाइंट को इनिशियलाइज़ करने के बाद, हम सर्वर को इनिशियलाइज़ कर सकते हैं और उसके कुछ फीचर्स को सूचीबद्ध कर सकते हैं।

```rust
// Initialize
let server_info = client.peer_info();
println!("Server info: {:?}", server_info);

// List tools
let tools = client.list_tools(Default::default()).await?;
println!("Available tools: {:?}", tools);
```

### -4- फीचर्स को सक्रिय करना

फीचर्स को सक्रिय करने के लिए, हमें यह सुनिश्चित करना होगा कि हम सही आर्ग्युमेंट्स और कुछ मामलों में उस चीज़ का नाम निर्दिष्ट करें जिसे हम सक्रिय करना चाहते हैं।

#### टाइपस्क्रिप्ट

```typescript

// Read a resource
const resource = await client.readResource({
  uri: "file:///example.txt"
});

// Call a tool
const result = await client.callTool({
  name: "example-tool",
  arguments: {
    arg1: "value"
  }
});

// call prompt
const promptResult = await client.getPrompt({
    name: "review-code",
    arguments: {
        code: "console.log(\"Hello world\")"
    }
})
```

ऊपर दिए गए कोड में हमने:

- एक संसाधन पढ़ा, जिसे हमने `readResource()` को `uri` निर्दिष्ट करके कॉल किया। सर्वर साइड पर यह कुछ इस प्रकार दिखेगा:

    ```typescript
    server.resource(
        "readFile",
        new ResourceTemplate("file://{name}", { list: undefined }),
        async (uri, { name }) => ({
          contents: [{
            uri: uri.href,
            text: `Hello, ${name}!`
          }]
        })
    );
    ```

    हमारा `uri` मान `file://example.txt` सर्वर पर `file://{name}` से मेल खाता है। `example.txt` को `name` पर मैप किया जाएगा।

- एक टूल को कॉल किया, जिसे हमने इसके `name` और `arguments` निर्दिष्ट करके कॉल किया:

    ```typescript
    const result = await client.callTool({
        name: "example-tool",
        arguments: {
            arg1: "value"
        }
    });
    ```

- प्रॉम्प्ट प्राप्त किया, प्रॉम्प्ट प्राप्त करने के लिए, आप `getPrompt()` को `name` और `arguments` के साथ कॉल करते हैं। सर्वर कोड कुछ इस प्रकार दिखता है:

    ```typescript
    server.prompt(
        "review-code",
        { code: z.string() },
        ({ code }) => ({
            messages: [{
            role: "user",
            content: {
                type: "text",
                text: `Please review this code:\n\n${code}`
            }
            }]
        })
    );
    ```

    और आपका परिणामी क्लाइंट कोड सर्वर पर घोषित किए गए से मेल खाने के लिए इस प्रकार दिखता है:

    ```typescript
    const promptResult = await client.getPrompt({
        name: "review-code",
        arguments: {
            code: "console.log(\"Hello world\")"
        }
    })
    ```

#### पायथन

```python
# Read a resource
print("READING RESOURCE")
content, mime_type = await session.read_resource("greeting://hello")

# Call a tool
print("CALL TOOL")
result = await session.call_tool("add", arguments={"a": 1, "b": 7})
print(result.content)
```

ऊपर दिए गए कोड में हमने:

- `read_resource` का उपयोग करके `greeting` नामक एक संसाधन को कॉल किया।
- `call_tool` का उपयोग करके `add` नामक एक टूल को सक्रिय किया।

#### .NET

1. एक टूल को कॉल करने के लिए कुछ कोड जोड़ें:

  ```csharp
  var result = await mcpClient.CallToolAsync(
      "Add",
      new Dictionary<string, object?>() { ["a"] = 1, ["b"] = 3  },
      cancellationToken:CancellationToken.None);
  ```

1. परिणाम को प्रिंट करने के लिए, यहां कुछ कोड है:

  ```csharp
  Console.WriteLine(result.Content.First(c => c.Type == "text").Text);
  // Sum 4
  ```

#### जावा

```java
// Call various calculator tools
CallToolResult resultAdd = client.callTool(new CallToolRequest("add", Map.of("a", 5.0, "b", 3.0)));
System.out.println("Add Result = " + resultAdd);

CallToolResult resultSubtract = client.callTool(new CallToolRequest("subtract", Map.of("a", 10.0, "b", 4.0)));
System.out.println("Subtract Result = " + resultSubtract);

CallToolResult resultMultiply = client.callTool(new CallToolRequest("multiply", Map.of("a", 6.0, "b", 7.0)));
System.out.println("Multiply Result = " + resultMultiply);

CallToolResult resultDivide = client.callTool(new CallToolRequest("divide", Map.of("a", 20.0, "b", 4.0)));
System.out.println("Divide Result = " + resultDivide);

CallToolResult resultHelp = client.callTool(new CallToolRequest("help", Map.of()));
System.out.println("Help = " + resultHelp);
```

ऊपर दिए गए कोड में हमने:

- `callTool()` विधि का उपयोग करके कई कैलकुलेटर टूल्स को `CallToolRequest` ऑब्जेक्ट्स के साथ कॉल किया।
- प्रत्येक टूल कॉल में उस टूल का नाम और उस टूल द्वारा अपेक्षित आर्ग्युमेंट्स का `Map` निर्दिष्ट किया।
- सर्वर टूल्स विशिष्ट पैरामीटर नामों (जैसे "a", "b" गणितीय संचालन के लिए) की अपेक्षा करते हैं।
- परिणाम `CallToolResult` ऑब्जेक्ट्स के रूप में लौटाए जाते हैं, जिनमें सर्वर से प्रतिक्रिया होती है।

#### रस्ट

```rust
// Call add tool with arguments = {"a": 3, "b": 2}
let a = 3;
let b = 2;
let tool_result = client
    .call_tool(CallToolRequestParam {
        name: "add".into(),
        arguments: serde_json::json!({ "a": a, "b": b }).as_object().cloned(),
    })
    .await?;
println!("Result of {:?} + {:?}: {:?}", a, b, tool_result);
```

### -5- क्लाइंट चलाएं

क्लाइंट चलाने के लिए, टर्मिनल में निम्नलिखित कमांड टाइप करें:

#### टाइपस्क्रिप्ट

*package.json* में "scripts" सेक्शन में निम्नलिखित एंट्री जोड़ें:

```json
"client": "tsc && node build/client.js"
```

```sh
npm run client
```

#### पायथन

क्लाइंट को निम्नलिखित कमांड के साथ कॉल करें:

```sh
python client.py
```

#### .NET

```sh
dotnet run
```

#### जावा

पहले, सुनिश्चित करें कि आपका MCP सर्वर `http://localhost:8080` पर चल रहा है। फिर क्लाइंट चलाएं:

```bash
# Build you project
./mvnw clean compile

# Run the client
./mvnw exec:java -Dexec.mainClass="com.microsoft.mcp.sample.client.SDKClient"
```

वैकल्पिक रूप से, आप समाधान फोल्डर `03-GettingStarted\02-client\solution\java` में प्रदान किए गए पूर्ण क्लाइंट प्रोजेक्ट को चला सकते हैं:

```bash
# Navigate to the solution directory
cd 03-GettingStarted/02-client/solution/java

# Build and run the JAR
./mvnw clean package
java -jar target/calculator-client-0.0.1-SNAPSHOT.jar
```

#### रस्ट

```bash
cargo fmt
cargo run
```

## असाइनमेंट

इस असाइनमेंट में, आप जो आपने क्लाइंट बनाने में सीखा है उसका उपयोग करेंगे, लेकिन अपना खुद का क्लाइंट बनाएंगे।

यहां एक सर्वर है जिसे आपको अपने क्लाइंट कोड के माध्यम से कॉल करना है, देखें कि क्या आप सर्वर में और अधिक फीचर्स जोड़ सकते हैं ताकि यह और अधिक रोचक हो।

### टाइपस्क्रिप्ट

```typescript
import { McpServer, ResourceTemplate } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

// Create an MCP server
const server = new McpServer({
  name: "Demo",
  version: "1.0.0"
});

// Add an addition tool
server.tool("add",
  { a: z.number(), b: z.number() },
  async ({ a, b }) => ({
    content: [{ type: "text", text: String(a + b) }]
  })
);

// Add a dynamic greeting resource
server.resource(
  "greeting",
  new ResourceTemplate("greeting://{name}", { list: undefined }),
  async (uri, { name }) => ({
    contents: [{
      uri: uri.href,
      text: `Hello, ${name}!`
    }]
  })
);

// Start receiving messages on stdin and sending messages on stdout

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("MCPServer started on stdin/stdout");
}

main().catch((error) => {
  console.error("Fatal error: ", error);
  process.exit(1);
});
```

### पायथन

```python
# server.py
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Demo")


# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"

```

### .NET

```csharp
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;
using ModelContextProtocol.Server;
using System.ComponentModel;

var builder = Host.CreateApplicationBuilder(args);
builder.Logging.AddConsole(consoleLogOptions =>
{
    // Configure all logs to go to stderr
    consoleLogOptions.LogToStandardErrorThreshold = LogLevel.Trace;
});

builder.Services
    .AddMcpServer()
    .WithStdioServerTransport()
    .WithToolsFromAssembly();
await builder.Build().RunAsync();

[McpServerToolType]
public static class CalculatorTool
{
    [McpServerTool, Description("Adds two numbers")]
    public static string Add(int a, int b) => $"Sum {a + b}";
}
```

इस प्रोजेक्ट को देखें कि आप [प्रॉम्प्ट्स और संसाधन कैसे जोड़ सकते हैं](https://github.com/modelcontextprotocol/csharp-sdk/blob/main/samples/EverythingServer/Program.cs)।

साथ ही, इस लिंक को देखें कि [प्रॉम्प्ट्स और संसाधन कैसे सक्रिय करें](https://github.com/modelcontextprotocol/csharp-sdk/blob/main/src/ModelContextProtocol/Client/)।

### रस्ट

[पिछले सेक्शन](../../../../03-GettingStarted/01-first-server) में, आपने सीखा कि रस्ट के साथ एक साधारण MCP सर्वर कैसे बनाया जाए। आप उस पर निर्माण जारी रख सकते हैं या अधिक रस्ट-आधारित MCP सर्वर उदाहरणों के लिए इस लिंक को देख सकते हैं: [MCP Server Examples](https://github.com/modelcontextprotocol/rust-sdk/tree/main/examples/servers)

## समाधान

**सॉल्यूशन फोल्डर** में इस ट्यूटोरियल में शामिल सभी अवधारणाओं को प्रदर्शित करने वाले पूर्ण, तैयार-चलने वाले क्लाइंट इंप्लीमेंटेशन शामिल हैं। प्रत्येक समाधान में क्लाइंट और सर्वर कोड अलग-अलग, स्व-निहित प्रोजेक्ट्स में व्यवस्थित हैं।

### 📁 समाधान संरचना

सॉल्यूशन डायरेक्टरी प्रोग्रामिंग भाषा के अनुसार व्यवस्थित है:

```text
solution/
├── typescript/          # TypeScript client with npm/Node.js setup
│   ├── package.json     # Dependencies and scripts
│   ├── tsconfig.json    # TypeScript configuration
│   └── src/             # Source code
├── java/                # Java Spring Boot client project
│   ├── pom.xml          # Maven configuration
│   ├── src/             # Java source files
│   └── mvnw             # Maven wrapper
├── python/              # Python client implementation
│   ├── client.py        # Main client code
│   ├── server.py        # Compatible server
│   └── README.md        # Python-specific instructions
├── dotnet/              # .NET client project
│   ├── dotnet.csproj    # Project configuration
│   ├── Program.cs       # Main client code
│   └── dotnet.sln       # Solution file
├── rust/                # Rust client implementation
|  ├── Cargo.lock        # Cargo lock file
|  ├── Cargo.toml        # Project configuration and dependencies
|  ├── src               # Source code
|  │   └── main.rs       # Main client code
└── server/              # Additional .NET server implementation
    ├── Program.cs       # Server code
    └── server.csproj    # Server project file
```

### 🚀 प्रत्येक समाधान में क्या शामिल है

प्रत्येक भाषा-विशिष्ट समाधान प्रदान करता है:

- **पूर्ण क्लाइंट इंप्लीमेंटेशन** ट्यूटोरियल में शामिल सभी फीचर्स के साथ
- **कार्यशील प्रोजेक्ट संरचना** उचित डिपेंडेंसीज़ और कॉन्फ़िगरेशन के साथ
- **बिल्ड और रन स्क्रिप्ट्स** आसान सेटअप और निष्पादन के लिए
- **विस्तृत README** भाषा-विशिष्ट निर्देशों के साथ
- **त्रुटि हैंडलिंग** और परिणाम प्रोसेसिंग के उदाहरण

### 📖 समाधान का उपयोग करना

1. **अपनी पसंदीदा भाषा फोल्डर पर जाएं**:

   ```bash
   cd solution/typescript/    # For TypeScript
   cd solution/java/          # For Java
   cd solution/python/        # For Python
   cd solution/dotnet/        # For .NET
   ```

2. **प्रत्येक फोल्डर में README निर्देशों का पालन करें**:
   - डिपेंडेंसीज़ इंस्टॉल करना
   - प्रोजेक्ट बनाना
   - क्लाइंट चलाना

3. **उदाहरण आउटपुट** जो आपको देखना चाहिए:

   ```text
   Prompt: Please review this code: console.log("hello");
   Resource template: file
   Tool result: { content: [ { type: 'text', text: '9' } ] }
   ```

पूर्ण दस्तावेज़ और चरण-दर-चरण निर्देशों के लिए देखें: **[📖 समाधान दस्तावेज़](./solution/README.md)**

## 🎯 पूर्ण उदाहरण

हमने इस ट्यूटोरियल में शामिल सभी प्रोग्रामिंग भाषाओं के लिए पूर्ण, कार्यशील क्लाइंट इंप्लीमेंटेशन प्रदान किए हैं। ये उदाहरण ऊपर वर्णित सभी कार्यक्षमता का प्रदर्शन करते हैं और आपके अपने प्रोजेक्ट्स के लिए संदर्भ इंप्लीमेंटेशन या शुरुआती बिंदु के रूप में उपयोग किए जा सकते हैं।

### उपलब्ध पूर्ण उदाहरण

| भाषा | फ़ाइल | विवरण |
|----------|------|-------------|
| **जावा** | [`client_example_java.java`](../../../../03-GettingStarted/02-client/client_example_java.java) | SSE ट्रांसपोर्ट का उपयोग करने वाला पूर्ण जावा क्लाइंट, जिसमें व्यापक त्रुटि हैंडलिंग है |
| **C#** | [`client_example_csharp.cs`](../../../../03-GettingStarted/02-client/client_example_csharp.cs) | `stdio` ट्रांसपोर्ट का उपयोग करने वाला पूर्ण C# क्लाइंट, जिसमें स्वचालित सर्वर स्टार्टअप है |
| **टाइपस्क्रिप्ट** | [`client_example_typescript.ts`](../../../../03-GettingStarted/02-client/client_example_typescript.ts) | पूर्ण टाइपस्क्रिप्ट क्लाइंट, जिसमें MCP प्रोटोकॉल का पूरा समर्थन है |
| **पायथन** | [`client_example_python.py`](../../../../03-GettingStarted/02-client/client_example_python.py) | `async/await` पैटर्न का उपयोग करने वाला पूर्ण पायथन क्लाइंट |
| **रस्ट** | [`client_example_rust.rs`](../../../../03-GettingStarted/02-client/client_example_rust.rs) | असिंक्रोनस ऑपरेशंस के लिए टोकियो का उपयोग करने वाला पूर्ण रस्ट क्लाइंट |
प्रत्येक पूर्ण उदाहरण में शामिल हैं:

- ✅ **कनेक्शन स्थापित करना** और त्रुटि प्रबंधन
- ✅ **सर्वर खोज** (उपकरण, संसाधन, प्रॉम्प्ट जहां लागू हो)
- ✅ **कैलकुलेटर संचालन** (जोड़ना, घटाना, गुणा, भाग, सहायता)
- ✅ **परिणाम प्रसंस्करण** और स्वरूपित आउटपुट
- ✅ **व्यापक त्रुटि प्रबंधन**
- ✅ **साफ़, प्रलेखित कोड** चरण-दर-चरण टिप्पणियों के साथ

### पूर्ण उदाहरणों के साथ शुरुआत करना

1. **अपनी पसंदीदा भाषा चुनें** ऊपर दी गई तालिका से
2. **पूर्ण उदाहरण फ़ाइल की समीक्षा करें** ताकि पूरी कार्यान्वयन को समझा जा सके
3. **उदाहरण चलाएं** [`complete_examples.md`](./complete_examples.md) में दिए गए निर्देशों का पालन करते हुए
4. **अपने विशिष्ट उपयोग के मामले के लिए संशोधित और विस्तारित करें** उदाहरण

इन उदाहरणों को चलाने और अनुकूलित करने के बारे में विस्तृत दस्तावेज़ के लिए देखें: **[📖 पूर्ण उदाहरण दस्तावेज़](./complete_examples.md)**

### 💡 समाधान बनाम पूर्ण उदाहरण

| **समाधान फ़ोल्डर** | **पूर्ण उदाहरण** |
|--------------------|--------------------- |
| बिल्ड फ़ाइलों के साथ पूरी प्रोजेक्ट संरचना | सिंगल-फ़ाइल कार्यान्वयन |
| निर्भरताओं के साथ तैयार-से-चलाने वाला | केंद्रित कोड उदाहरण |
| उत्पादन-जैसा सेटअप | शैक्षिक संदर्भ |
| भाषा-विशिष्ट उपकरण | क्रॉस-भाषा तुलना |

दोनों दृष्टिकोण मूल्यवान हैं - **समाधान फ़ोल्डर** का उपयोग करें पूर्ण प्रोजेक्ट्स के लिए और **पूर्ण उदाहरणों** का उपयोग करें सीखने और संदर्भ के लिए।

## मुख्य बातें

इस अध्याय के लिए मुख्य बातें निम्नलिखित हैं, जो क्लाइंट्स के बारे में हैं:

- सर्वर पर सुविधाओं को खोजने और उन्हें लागू करने के लिए उपयोग किया जा सकता है।
- स्वयं शुरू होते समय सर्वर शुरू कर सकते हैं (जैसा कि इस अध्याय में है), लेकिन क्लाइंट्स चल रहे सर्वरों से भी कनेक्ट हो सकते हैं।
- सर्वर क्षमताओं का परीक्षण करने का एक शानदार तरीका है, जैसे कि पिछले अध्याय में वर्णित इंस्पेक्टर जैसे विकल्प।

## अतिरिक्त संसाधन

- [MCP में क्लाइंट्स बनाना](https://modelcontextprotocol.io/quickstart/client)

## नमूने

- [जावा कैलकुलेटर](../samples/java/calculator/README.md)
- [.नेट कैलकुलेटर](../../../../03-GettingStarted/samples/csharp)
- [जावास्क्रिप्ट कैलकुलेटर](../samples/javascript/README.md)
- [टाइपस्क्रिप्ट कैलकुलेटर](../samples/typescript/README.md)
- [पायथन कैलकुलेटर](../../../../03-GettingStarted/samples/python)
- [रस्ट कैलकुलेटर](../../../../03-GettingStarted/samples/rust)

## आगे क्या

- अगला: [LLM के साथ एक क्लाइंट बनाना](../03-llm-client/README.md)

**अस्वीकरण**:  
यह दस्तावेज़ AI अनुवाद सेवा [Co-op Translator](https://github.com/Azure/co-op-translator) का उपयोग करके अनुवादित किया गया है। जबकि हम सटीकता सुनिश्चित करने का प्रयास करते हैं, कृपया ध्यान दें कि स्वचालित अनुवाद में त्रुटियां या अशुद्धियां हो सकती हैं। मूल भाषा में उपलब्ध मूल दस्तावेज़ को प्रामाणिक स्रोत माना जाना चाहिए। महत्वपूर्ण जानकारी के लिए, पेशेवर मानव अनुवाद की सिफारिश की जाती है। इस अनुवाद के उपयोग से उत्पन्न किसी भी गलतफहमी या गलत व्याख्या के लिए हम जिम्मेदार नहीं हैं।