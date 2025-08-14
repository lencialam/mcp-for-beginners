<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "57f7b15640bb96ef2f6f09003eec935e",
  "translation_date": "2025-08-12T19:16:57+00:00",
  "source_file": "03-GettingStarted/03-llm-client/README.md",
  "language_code": "es"
}
-->
# Creando un cliente con LLM

Hasta ahora, has visto cómo crear un servidor y un cliente. El cliente ha podido llamar explícitamente al servidor para listar sus herramientas, recursos y prompts. Sin embargo, no es un enfoque muy práctico. Tu usuario vive en la era de los agentes y espera usar prompts y comunicarse con un LLM para hacerlo. Para tu usuario, no importa si usas MCP o no para almacenar tus capacidades, pero sí espera interactuar usando lenguaje natural. Entonces, ¿cómo resolvemos esto? La solución consiste en agregar un LLM al cliente.

## Descripción general

En esta lección nos enfocamos en agregar un LLM a tu cliente y mostramos cómo esto proporciona una experiencia mucho mejor para tu usuario.

## Objetivos de aprendizaje

Al final de esta lección, serás capaz de:

- Crear un cliente con un LLM.
- Interactuar sin problemas con un servidor MCP usando un LLM.
- Proporcionar una mejor experiencia al usuario final en el lado del cliente.

## Enfoque

Intentemos entender el enfoque que necesitamos tomar. Agregar un LLM suena simple, pero ¿realmente lo haremos?

Así es como el cliente interactuará con el servidor:

1. Establecer conexión con el servidor.

1. Listar capacidades, prompts, recursos y herramientas, y guardar su esquema.

1. Agregar un LLM y pasar las capacidades guardadas y su esquema en un formato que el LLM entienda.

1. Manejar un prompt del usuario pasándolo al LLM junto con las herramientas listadas por el cliente.

Genial, ahora entendemos cómo podemos hacer esto a alto nivel, intentémoslo en el siguiente ejercicio.

## Ejercicio: Creando un cliente con un LLM

En este ejercicio, aprenderemos a agregar un LLM a nuestro cliente.

### Autenticación usando un token de acceso personal de GitHub

Crear un token de GitHub es un proceso sencillo. Aquí te explicamos cómo hacerlo:

- Ve a Configuración de GitHub – Haz clic en tu foto de perfil en la esquina superior derecha y selecciona Configuración.
- Navega a Configuración de desarrollador – Desplázate hacia abajo y haz clic en Configuración de desarrollador.
- Selecciona Tokens de acceso personal – Haz clic en Tokens de acceso personal y luego en Generar nuevo token.
- Configura tu token – Agrega una nota para referencia, establece una fecha de expiración y selecciona los alcances necesarios (permisos).
- Genera y copia el token – Haz clic en Generar token y asegúrate de copiarlo inmediatamente, ya que no podrás verlo nuevamente.

### -1- Conectar al servidor

Primero, creemos nuestro cliente:

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

En el código anterior hemos:

- Importado las bibliotecas necesarias.
- Creado una clase con dos miembros, `client` y `openai`, que nos ayudarán a gestionar un cliente e interactuar con un LLM respectivamente.
- Configurado nuestra instancia de LLM para usar GitHub Models estableciendo `baseUrl` para apuntar a la API de inferencia.

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

En el código anterior hemos:

- Importado las bibliotecas necesarias para MCP.
- Creado un cliente.

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

Primero, necesitarás agregar las dependencias de LangChain4j a tu archivo `pom.xml`. Agrega estas dependencias para habilitar la integración de MCP y el soporte para GitHub Models:

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

Luego, crea tu clase cliente en Java:

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

En el código anterior hemos:

- **Agregado dependencias de LangChain4j**: Necesarias para la integración de MCP, el cliente oficial de OpenAI y el soporte para GitHub Models.
- **Importado las bibliotecas de LangChain4j**: Para la integración de MCP y la funcionalidad del modelo de chat de OpenAI.
- **Creado un `ChatLanguageModel`**: Configurado para usar GitHub Models con tu token de GitHub.
- **Configurado transporte HTTP**: Usando eventos enviados por el servidor (SSE) para conectarse al servidor MCP.
- **Creado un cliente MCP**: Que manejará la comunicación con el servidor.
- **Usado el soporte MCP integrado de LangChain4j**: Que simplifica la integración entre LLMs y servidores MCP.

#### Rust

Este ejemplo asume que tienes un servidor MCP basado en Rust en ejecución. Si no tienes uno, consulta la lección [01-primer-servidor](../01-first-server/README.md) para crear el servidor.

Una vez que tengas tu servidor MCP en Rust, abre una terminal y navega al mismo directorio que el servidor. Luego ejecuta el siguiente comando para crear un nuevo proyecto de cliente LLM:

```bash
mkdir calculator-llmclient
cd calculator-llmclient
cargo init
```

Agrega las siguientes dependencias a tu archivo `Cargo.toml`:

```toml
[dependencies]
async-openai = { version = "0.29.0", features = ["byot"] }
rmcp = { version = "0.5.0", features = ["client", "transport-child-process"] }
serde_json = "1.0.141"
tokio = { version = "1.46.1", features = ["rt-multi-thread"] }
```

> [!NOTE]
> No existe una biblioteca oficial de Rust para OpenAI, sin embargo, el crate `async-openai` es una [biblioteca mantenida por la comunidad](https://platform.openai.com/docs/libraries/rust#rust) que se usa comúnmente.

Abre el archivo `src/main.rs` y reemplaza su contenido con el siguiente código:

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

Este código configura una aplicación básica en Rust que se conectará a un servidor MCP y GitHub Models para interacciones con LLM.

> [!IMPORTANT]
> Asegúrate de establecer la variable de entorno `OPENAI_API_KEY` con tu token de GitHub antes de ejecutar la aplicación.

Genial, para nuestro próximo paso, listemos las capacidades en el servidor.

### -2- Listar capacidades del servidor

Ahora nos conectaremos al servidor y pediremos sus capacidades:

#### TypeScript

En la misma clase, agrega los siguientes métodos:

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

En el código anterior hemos:

- Agregado código para conectarse al servidor, `connectToServer`.
- Creado un método `run` responsable de manejar el flujo de nuestra aplicación. Hasta ahora solo lista las herramientas, pero pronto agregaremos más.

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

Esto es lo que hemos agregado:

- Listado de recursos y herramientas y los hemos impreso. Para las herramientas también listamos `inputSchema`, que usaremos más adelante.

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

En el código anterior hemos:

- Listado las herramientas disponibles en el servidor MCP.
- Para cada herramienta, listado nombre, descripción y su esquema. Este último es algo que usaremos para llamar a las herramientas próximamente.

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

En el código anterior hemos:

- Creado un `McpToolProvider` que descubre y registra automáticamente todas las herramientas del servidor MCP.
- El proveedor de herramientas maneja la conversión entre esquemas de herramientas MCP y el formato de herramientas de LangChain4j internamente.
- Este enfoque abstrae el proceso manual de listado y conversión de herramientas.

#### Rust

Recuperar herramientas del servidor MCP se realiza usando el método `list_tools`. En tu función `main`, después de configurar el cliente MCP, agrega el siguiente código:

```rust
// Get MCP tool listing 
let tools = mcp_client.list_tools(Default::default()).await?;
```

### -3- Convertir capacidades del servidor a herramientas para LLM

El siguiente paso después de listar las capacidades del servidor es convertirlas en un formato que el LLM entienda. Una vez que hagamos eso, podemos proporcionar estas capacidades como herramientas a nuestro LLM.

#### TypeScript

1. Agrega el siguiente código para convertir la respuesta del servidor MCP a un formato de herramienta que el LLM pueda usar:

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

    El código anterior toma una respuesta del servidor MCP y la convierte en un formato de definición de herramienta que el LLM pueda entender.

1. Actualicemos el método `run` para listar las capacidades del servidor:

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

    En el código anterior, hemos actualizado el método `run` para recorrer el resultado y para cada entrada llamar a `openAiToolAdapter`.

#### Python

1. Primero, creemos la siguiente función de conversión:

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

    En la función anterior `convert_to_llm_tools` tomamos una respuesta de herramienta MCP y la convertimos a un formato que el LLM pueda entender.

1. Luego, actualicemos nuestro código de cliente para aprovechar esta función así:

    ```python
    for tool in tools.tools:
        print("Tool: ", tool.name)
        print("Tool", tool.inputSchema["properties"])
        functions.append(convert_to_llm_tool(tool))
    ```

    Aquí, estamos agregando una llamada a `convert_to_llm_tool` para convertir la respuesta de herramienta MCP en algo que podamos alimentar al LLM más adelante.

#### .NET

1. Agreguemos código para convertir la respuesta de herramienta MCP en algo que el LLM pueda entender:

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

En el código anterior hemos:

- Creado una función `ConvertFrom` que toma nombre, descripción y esquema de entrada.
- Definido funcionalidad que crea una FunctionDefinition que se pasa a un ChatCompletionsDefinition. Este último es algo que el LLM puede entender.

1. Veamos cómo podemos actualizar algo de código existente para aprovechar esta función anterior:

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

    En el código anterior hemos:

    - Actualizado la función para convertir la respuesta de herramienta MCP en una herramienta LLM. Destaquemos el código que agregamos:

        ```csharp
        JsonElement propertiesElement;
        tool.JsonSchema.TryGetProperty("properties", out propertiesElement);

        var def = ConvertFrom(tool.Name, tool.Description, propertiesElement);
        Console.WriteLine($"Tool definition: {def}");
        toolDefinitions.Add(def);
        ```

        El esquema de entrada es parte de la respuesta de herramienta pero en el atributo "properties", por lo que necesitamos extraerlo. Además, ahora llamamos a `ConvertFrom` con los detalles de la herramienta. Ahora que hemos hecho el trabajo pesado, veamos cómo todo se junta mientras manejamos un prompt del usuario a continuación.

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

En el código anterior hemos:

- Definido una interfaz simple `Bot` para interacciones en lenguaje natural.
- Usado los `AiServices` de LangChain4j para vincular automáticamente el LLM con el proveedor de herramientas MCP.
- El marco maneja automáticamente la conversión de esquemas de herramientas MCP y la llamada a funciones detrás de escena.
- Este enfoque elimina la conversión manual de herramientas: LangChain4j maneja toda la complejidad de convertir herramientas MCP a un formato compatible con LLM.

#### Rust

Para convertir la respuesta de herramienta MCP a un formato que el LLM pueda entender, agregaremos una función auxiliar que formatea el listado de herramientas. Agrega el siguiente código a tu archivo `main.rs` debajo de la función `main`. Esto se llamará al hacer solicitudes al LLM:

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

Genial, ahora estamos listos para manejar cualquier solicitud del usuario, así que abordemos eso a continuación.

### -4- Manejar solicitud de prompt del usuario

En esta parte del código, manejaremos las solicitudes del usuario.

#### TypeScript

1. Agrega un método que se usará para llamar a nuestro LLM:

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

    En el código anterior hemos:

    - Agregado un método `callTools`.
    - El método toma una respuesta del LLM y verifica qué herramientas se han llamado, si es que hay alguna:

        ```typescript
        for (const tool_call of tool_calls) {
        const toolName = tool_call.function.name;
        const args = tool_call.function.arguments;

        console.log(`Calling tool ${toolName} with args ${JSON.stringify(args)}`);

        // call tool
        }
        ```

    - Llama a una herramienta, si el LLM indica que debe ser llamada:

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

1. Actualiza el método `run` para incluir llamadas al LLM y llamar a `callTools`:

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

Genial, listemos el código completo:

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

1. Agreguemos algunas importaciones necesarias para llamar a un LLM:

    ```python
    # llm
    import os
    from azure.ai.inference import ChatCompletionsClient
    from azure.ai.inference.models import SystemMessage, UserMessage
    from azure.core.credentials import AzureKeyCredential
    import json
    ```

1. Luego, agreguemos la función que llamará al LLM:

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

    En el código anterior hemos:

    - Pasado nuestras funciones, que encontramos en el servidor MCP y convertimos, al LLM.
    - Luego llamamos al LLM con dichas funciones.
    - Luego, inspeccionamos el resultado para ver qué funciones debemos llamar, si es que hay alguna.
    - Finalmente, pasamos un array de funciones para llamar.

1. Último paso, actualicemos nuestro código principal:

    ```python
    prompt = "Add 2 to 20"

    # ask LLM what tools to all, if any
    functions_to_call = call_llm(prompt, functions)

    # call suggested functions
    for f in functions_to_call:
        result = await session.call_tool(f["name"], arguments=f["args"])
        print("TOOLS result: ", result.content)
    ```

    Ahí, ese fue el último paso, en el código anterior estamos:

    - Llamando a una herramienta MCP a través de `call_tool` usando una función que el LLM pensó que deberíamos llamar según nuestro prompt.
    - Imprimiendo el resultado de la llamada a la herramienta en el servidor MCP.

#### .NET

1. Mostremos algo de código para hacer una solicitud de prompt al LLM:

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

    En el código anterior hemos:

    - Recuperado herramientas del servidor MCP, `var tools = await GetMcpTools()`.
    - Definido un prompt del usuario `userMessage`.
    - Construido un objeto de opciones especificando el modelo y las herramientas.
    - Realizado una solicitud hacia el LLM.

1. Un último paso, veamos si el LLM piensa que debemos llamar a una función:

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

    En el código anterior hemos:

    - Recorrido una lista de llamadas a funciones.
    - Para cada llamada a herramienta, extraemos el nombre y los argumentos y llamamos a la herramienta en el servidor MCP usando el cliente MCP. Finalmente imprimimos los resultados.

Aquí está el código completo:

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

En el código anterior hemos:

- Usado prompts simples en lenguaje natural para interactuar con las herramientas del servidor MCP.
- El marco LangChain4j maneja automáticamente:
  - Convertir prompts del usuario en llamadas a herramientas cuando sea necesario.
  - Llamar a las herramientas MCP apropiadas según la decisión del LLM.
  - Gestionar el flujo de conversación entre el LLM y el servidor MCP.
- El método `bot.chat()` devuelve respuestas en lenguaje natural que pueden incluir resultados de ejecuciones de herramientas MCP.
- Este enfoque proporciona una experiencia de usuario fluida donde los usuarios no necesitan conocer la implementación subyacente de MCP.

Ejemplo completo de código:

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

Aquí es donde ocurre la mayor parte del trabajo. Llamaremos al LLM con el prompt inicial del usuario, luego procesaremos la respuesta para ver si se necesitan llamar herramientas. Si es así, llamaremos a esas herramientas y continuaremos la conversación con el LLM hasta que no se necesiten más llamadas a herramientas y tengamos una respuesta final.
Agreguemos una función que manejará las llamadas al LLM. Añade la siguiente función a tu archivo `main.rs`:

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

Esta función toma el cliente LLM, una lista de mensajes (incluyendo el mensaje del usuario), herramientas del servidor MCP, y envía una solicitud al LLM, devolviendo la respuesta.

La respuesta del LLM contendrá un arreglo de `choices`. Necesitaremos procesar el resultado para verificar si hay `tool_calls` presentes. Esto nos indica que el LLM está solicitando que se llame a una herramienta específica con argumentos. Añade el siguiente código al final de tu archivo `main.rs` para definir una función que maneje la respuesta del LLM:

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

Si hay `tool_calls` presentes, extrae la información de la herramienta, llama al servidor MCP con la solicitud de la herramienta y agrega los resultados a los mensajes de la conversación. Luego, continúa la conversación con el LLM y los mensajes se actualizan con la respuesta del asistente y los resultados de la llamada a la herramienta.

Para extraer la información de la llamada a la herramienta que el LLM devuelve para las llamadas MCP, añadiremos otra función auxiliar para extraer todo lo necesario para realizar la llamada. Añade el siguiente código al final de tu archivo `main.rs`:

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

Con todas las piezas en su lugar, ahora podemos manejar el mensaje inicial del usuario y llamar al LLM. Actualiza tu función `main` para incluir el siguiente código:

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

Esto consultará al LLM con el mensaje inicial del usuario pidiendo la suma de dos números, y procesará la respuesta para manejar dinámicamente las llamadas a herramientas.

¡Genial, lo lograste!

## Tarea

Toma el código del ejercicio y amplía el servidor con más herramientas. Luego, crea un cliente con un LLM, como en el ejercicio, y pruébalo con diferentes mensajes para asegurarte de que todas las herramientas de tu servidor se llamen dinámicamente. Este enfoque para construir un cliente significa que el usuario final tendrá una gran experiencia, ya que podrá usar mensajes en lugar de comandos exactos del cliente, sin darse cuenta de que se está llamando a un servidor MCP.

## Solución

[Solución](/03-GettingStarted/03-llm-client/solution/README.md)

## Puntos clave

- Agregar un LLM a tu cliente proporciona una mejor forma para que los usuarios interactúen con los servidores MCP.
- Necesitas convertir la respuesta del servidor MCP en algo que el LLM pueda entender.

## Ejemplos

- [Calculadora en Java](../samples/java/calculator/README.md)
- [Calculadora en .Net](../../../../03-GettingStarted/samples/csharp)
- [Calculadora en JavaScript](../samples/javascript/README.md)
- [Calculadora en TypeScript](../samples/typescript/README.md)
- [Calculadora en Python](../../../../03-GettingStarted/samples/python)
- [Calculadora en Rust](../../../../03-GettingStarted/samples/rust)

## Recursos adicionales

## ¿Qué sigue?

- Siguiente: [Consumir un servidor usando Visual Studio Code](../04-vscode/README.md)

**Descargo de responsabilidad**:  
Este documento ha sido traducido utilizando el servicio de traducción automática [Co-op Translator](https://github.com/Azure/co-op-translator). Aunque nos esforzamos por garantizar la precisión, tenga en cuenta que las traducciones automatizadas pueden contener errores o imprecisiones. El documento original en su idioma nativo debe considerarse como la fuente autorizada. Para información crítica, se recomienda una traducción profesional realizada por humanos. No nos hacemos responsables de malentendidos o interpretaciones erróneas que puedan surgir del uso de esta traducción.