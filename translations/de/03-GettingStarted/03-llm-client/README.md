<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "57f7b15640bb96ef2f6f09003eec935e",
  "translation_date": "2025-08-12T19:18:54+00:00",
  "source_file": "03-GettingStarted/03-llm-client/README.md",
  "language_code": "de"
}
-->
# Erstellen eines Clients mit LLM

Bisher haben Sie gelernt, wie man einen Server und einen Client erstellt. Der Client konnte den Server explizit aufrufen, um dessen Tools, Ressourcen und Eingabeaufforderungen aufzulisten. Dies ist jedoch keine besonders praktische Herangehensweise. Ihre Nutzer leben in einer agentischen Ära und erwarten, dass sie Eingabeaufforderungen verwenden und mit einem LLM kommunizieren können, um ihre Ziele zu erreichen. Für Ihre Nutzer ist es irrelevant, ob Sie MCP verwenden, um Ihre Fähigkeiten zu speichern – sie erwarten, auf natürliche Weise interagieren zu können. Wie lösen wir dieses Problem? Die Lösung besteht darin, ein LLM in den Client zu integrieren.

## Überblick

In dieser Lektion konzentrieren wir uns darauf, ein LLM in Ihren Client einzubinden und zu zeigen, wie dies die Benutzererfahrung erheblich verbessert.

## Lernziele

Am Ende dieser Lektion werden Sie in der Lage sein:

- Einen Client mit einem LLM zu erstellen.
- Nahtlos mit einem MCP-Server unter Verwendung eines LLM zu interagieren.
- Eine bessere Benutzererfahrung auf der Client-Seite bereitzustellen.

## Vorgehensweise

Lassen Sie uns die Herangehensweise verstehen, die wir verfolgen müssen. Ein LLM hinzuzufügen klingt einfach, aber wie setzen wir das tatsächlich um?

So wird der Client mit dem Server interagieren:

1. Verbindung mit dem Server herstellen.

1. Fähigkeiten, Eingabeaufforderungen, Ressourcen und Tools auflisten und deren Schema speichern.

1. Ein LLM hinzufügen und die gespeicherten Fähigkeiten und deren Schema in einem Format übergeben, das das LLM versteht.

1. Eine Benutzereingabe verarbeiten, indem sie zusammen mit den vom Client aufgelisteten Tools an das LLM übergeben wird.

Gut, jetzt verstehen wir auf hoher Ebene, wie wir vorgehen können. Lassen Sie uns dies in der folgenden Übung ausprobieren.

## Übung: Erstellen eines Clients mit einem LLM

In dieser Übung lernen wir, wie man ein LLM in den Client integriert.

### Authentifizierung mit einem GitHub Personal Access Token

Das Erstellen eines GitHub-Tokens ist ein einfacher Prozess. So geht's:

- Gehen Sie zu den GitHub-Einstellungen – Klicken Sie auf Ihr Profilbild oben rechts und wählen Sie „Settings“.
- Navigieren Sie zu den Entwicklereinstellungen – Scrollen Sie nach unten und klicken Sie auf „Developer Settings“.
- Wählen Sie „Personal Access Tokens“ – Klicken Sie auf „Personal access tokens“ und dann auf „Generate new token“.
- Konfigurieren Sie Ihr Token – Fügen Sie eine Notiz zur Referenz hinzu, legen Sie ein Ablaufdatum fest und wählen Sie die erforderlichen Berechtigungen (Scopes) aus.
- Token generieren und kopieren – Klicken Sie auf „Generate token“ und stellen Sie sicher, dass Sie es sofort kopieren, da Sie es später nicht mehr sehen können.

### -1- Verbindung zum Server herstellen

Erstellen wir zunächst unseren Client:

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

Im obigen Code haben wir:

- Die benötigten Bibliotheken importiert.
- Eine Klasse mit zwei Mitgliedern erstellt, `client` und `openai`, die uns helfen, einen Client zu verwalten und mit einem LLM zu interagieren.
- Unsere LLM-Instanz so konfiguriert, dass sie GitHub-Modelle verwendet, indem wir `baseUrl` auf die Inferenz-API setzen.

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

Im obigen Code haben wir:

- Die für MCP benötigten Bibliotheken importiert.
- Einen Client erstellt.

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

Zuerst müssen Sie die LangChain4j-Abhängigkeiten zu Ihrer `pom.xml`-Datei hinzufügen. Fügen Sie diese Abhängigkeiten hinzu, um MCP-Integration und GitHub-Modelle zu unterstützen:

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

Erstellen Sie dann Ihre Java-Client-Klasse:

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

Im obigen Code haben wir:

- **LangChain4j-Abhängigkeiten hinzugefügt**: Erforderlich für MCP-Integration, OpenAI-Client und GitHub-Modelle.
- **LangChain4j-Bibliotheken importiert**: Für MCP-Integration und OpenAI-Chat-Modell-Funktionalität.
- **Ein `ChatLanguageModel` erstellt**: Konfiguriert, um GitHub-Modelle mit Ihrem GitHub-Token zu verwenden.
- **HTTP-Transport eingerichtet**: Mit Server-Sent Events (SSE), um eine Verbindung zum MCP-Server herzustellen.
- **Einen MCP-Client erstellt**: Der die Kommunikation mit dem Server übernimmt.
- **LangChain4j's eingebaute MCP-Unterstützung verwendet**: Die die Integration zwischen LLMs und MCP-Servern vereinfacht.

#### Rust

Dieses Beispiel setzt voraus, dass Sie einen MCP-Server auf Rust-Basis betreiben. Falls nicht, schauen Sie sich die Lektion [01-first-server](../01-first-server/README.md) an, um den Server zu erstellen.

Sobald Sie Ihren Rust-MCP-Server haben, öffnen Sie ein Terminal, navigieren Sie in das gleiche Verzeichnis wie der Server und führen Sie den folgenden Befehl aus, um ein neues LLM-Client-Projekt zu erstellen:

```bash
mkdir calculator-llmclient
cd calculator-llmclient
cargo init
```

Fügen Sie die folgenden Abhängigkeiten zu Ihrer `Cargo.toml`-Datei hinzu:

```toml
[dependencies]
async-openai = { version = "0.29.0", features = ["byot"] }
rmcp = { version = "0.5.0", features = ["client", "transport-child-process"] }
serde_json = "1.0.141"
tokio = { version = "1.46.1", features = ["rt-multi-thread"] }
```

> [!NOTE]
> Es gibt keine offizielle Rust-Bibliothek für OpenAI, aber das `async-openai`-Crate ist eine [community-maintained library](https://platform.openai.com/docs/libraries/rust#rust), die häufig verwendet wird.

Öffnen Sie die Datei `src/main.rs` und ersetzen Sie deren Inhalt durch den folgenden Code:

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

Dieser Code richtet eine grundlegende Rust-Anwendung ein, die eine Verbindung zu einem MCP-Server und GitHub-Modellen für LLM-Interaktionen herstellt.

> [!IMPORTANT]
> Stellen Sie sicher, dass Sie die Umgebungsvariable `OPENAI_API_KEY` mit Ihrem GitHub-Token setzen, bevor Sie die Anwendung ausführen.

Gut, im nächsten Schritt listen wir die Fähigkeiten des Servers auf.

### -2- Serverfähigkeiten auflisten

Nun verbinden wir uns mit dem Server und fragen nach seinen Fähigkeiten:

#### TypeScript

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

Im obigen Code haben wir:

- Den Code für die Verbindung zum Server hinzugefügt, `connectToServer`.
- Eine `run`-Methode erstellt, die für den Ablauf unserer App verantwortlich ist. Bisher listet sie nur die Tools auf, aber wir werden bald mehr hinzufügen.

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

Hier haben wir hinzugefügt:

- Ressourcen und Tools aufgelistet und ausgegeben. Für Tools listen wir auch das `inputSchema` auf, das wir später verwenden.

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

Im obigen Code haben wir:

- Die auf dem MCP-Server verfügbaren Tools aufgelistet.
- Für jedes Tool den Namen, die Beschreibung und das Schema aufgelistet. Letzteres werden wir bald verwenden, um die Tools aufzurufen.

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

Im obigen Code haben wir:

- Einen `McpToolProvider` erstellt, der automatisch alle Tools vom MCP-Server erkennt und registriert.
- Der Tool-Provider übernimmt intern die Konvertierung zwischen MCP-Tool-Schemata und dem Tool-Format von LangChain4j.
- Dieser Ansatz abstrahiert den manuellen Prozess der Tool-Auflistung und -Konvertierung.

#### Rust

Das Abrufen von Tools vom MCP-Server erfolgt mit der Methode `list_tools`. Fügen Sie in Ihrer `main`-Funktion nach der Einrichtung des MCP-Clients den folgenden Code hinzu:

```rust
// Get MCP tool listing 
let tools = mcp_client.list_tools(Default::default()).await?;
```

### -3- Serverfähigkeiten in LLM-Tools umwandeln

Der nächste Schritt nach der Auflistung der Serverfähigkeiten besteht darin, diese in ein Format umzuwandeln, das das LLM versteht. Sobald wir das getan haben, können wir diese Fähigkeiten als Tools an unser LLM übergeben.

#### TypeScript

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

...
Wir werden mehrere Aufrufe an das LLM durchführen, daher definieren wir eine Funktion, die den LLM-Aufruf übernimmt. Fügen Sie die folgende Funktion zu Ihrer `main.rs` Datei hinzu:

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

Diese Funktion nimmt den LLM-Client, eine Liste von Nachrichten (einschließlich der Benutzeraufforderung), Tools vom MCP-Server und sendet eine Anfrage an das LLM, wobei die Antwort zurückgegeben wird.

Die Antwort des LLM enthält ein Array von `choices`. Wir müssen das Ergebnis verarbeiten, um festzustellen, ob `tool_calls` vorhanden sind. Dies zeigt uns, dass das LLM ein bestimmtes Tool mit Argumenten aufrufen möchte. Fügen Sie den folgenden Code am Ende Ihrer `main.rs` Datei hinzu, um eine Funktion zu definieren, die die LLM-Antwort verarbeitet:

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

Falls `tool_calls` vorhanden sind, extrahiert die Funktion die Tool-Informationen, ruft den MCP-Server mit der Tool-Anfrage auf und fügt die Ergebnisse den Konversationsnachrichten hinzu. Anschließend wird die Konversation mit dem LLM fortgesetzt, und die Nachrichten werden mit der Antwort des Assistenten und den Tool-Ergebnissen aktualisiert.

Um die Tool-Call-Informationen zu extrahieren, die das LLM für MCP-Aufrufe zurückgibt, fügen wir eine weitere Hilfsfunktion hinzu, die alles extrahiert, was für den Aufruf benötigt wird. Fügen Sie den folgenden Code am Ende Ihrer `main.rs` Datei hinzu:

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

Mit allen Bausteinen können wir nun die anfängliche Benutzeraufforderung verarbeiten und das LLM aufrufen. Aktualisieren Sie Ihre `main` Funktion, um den folgenden Code einzufügen:

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

Dies wird das LLM mit der anfänglichen Benutzeraufforderung abfragen, die nach der Summe von zwei Zahlen fragt, und die Antwort verarbeiten, um Tool-Aufrufe dynamisch zu handhaben.

Super, Sie haben es geschafft!

## Aufgabe

Nehmen Sie den Code aus der Übung und erweitern Sie den Server mit weiteren Tools. Erstellen Sie dann einen Client mit einem LLM, wie in der Übung, und testen Sie ihn mit verschiedenen Aufforderungen, um sicherzustellen, dass alle Ihre Server-Tools dynamisch aufgerufen werden. Diese Art, einen Client zu erstellen, sorgt für eine großartige Benutzererfahrung, da die Endbenutzer Aufforderungen verwenden können, anstatt genaue Client-Befehle, und sich keine Gedanken über einen MCP-Server machen müssen, der aufgerufen wird.

## Lösung

[Solution](/03-GettingStarted/03-llm-client/solution/README.md)

## Wichtige Erkenntnisse

- Das Hinzufügen eines LLM zu Ihrem Client bietet eine bessere Möglichkeit für Benutzer, mit MCP-Servern zu interagieren.
- Sie müssen die Antwort des MCP-Servers in ein Format umwandeln, das das LLM verstehen kann.

## Beispiele

- [Java Rechner](../samples/java/calculator/README.md)
- [.Net Rechner](../../../../03-GettingStarted/samples/csharp)
- [JavaScript Rechner](../samples/javascript/README.md)
- [TypeScript Rechner](../samples/typescript/README.md)
- [Python Rechner](../../../../03-GettingStarted/samples/python)
- [Rust Rechner](../../../../03-GettingStarted/samples/rust)

## Zusätzliche Ressourcen

## Was kommt als Nächstes

- Weiter: [Einen Server mit Visual Studio Code konsumieren](../04-vscode/README.md)

**Haftungsausschluss**:  
Dieses Dokument wurde mit dem KI-Übersetzungsdienst [Co-op Translator](https://github.com/Azure/co-op-translator) übersetzt. Obwohl wir uns um Genauigkeit bemühen, beachten Sie bitte, dass automatisierte Übersetzungen Fehler oder Ungenauigkeiten enthalten können. Das Originaldokument in seiner ursprünglichen Sprache sollte als maßgebliche Quelle betrachtet werden. Für kritische Informationen wird eine professionelle menschliche Übersetzung empfohlen. Wir übernehmen keine Haftung für Missverständnisse oder Fehlinterpretationen, die sich aus der Nutzung dieser Übersetzung ergeben.