<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "ee93d6093964ea579dbdc20b4d643e9b",
  "translation_date": "2025-08-12T21:32:54+00:00",
  "source_file": "03-GettingStarted/01-first-server/README.md",
  "language_code": "hi"
}
-->
# MCP के साथ शुरुआत करें

Model Context Protocol (MCP) के साथ अपने पहले कदमों में आपका स्वागत है! चाहे आप MCP के लिए नए हों या अपनी समझ को गहरा करना चाहते हों, यह गाइड आपको आवश्यक सेटअप और विकास प्रक्रिया के माध्यम से मार्गदर्शन करेगा। आप जानेंगे कि MCP कैसे AI मॉडल और एप्लिकेशन के बीच सहज इंटीग्रेशन को सक्षम बनाता है और MCP-संचालित समाधान बनाने और परीक्षण करने के लिए अपने वातावरण को जल्दी से तैयार करने का तरीका सीखेंगे।

> संक्षेप में: यदि आप AI एप्लिकेशन बनाते हैं, तो आप जानते हैं कि आप LLM (large language model) में टूल्स और अन्य संसाधन जोड़ सकते हैं ताकि LLM अधिक ज्ञानवान बन सके। लेकिन यदि आप उन टूल्स और संसाधनों को सर्वर पर रखते हैं, तो एप्लिकेशन और सर्वर की क्षमताओं का उपयोग किसी भी क्लाइंट द्वारा LLM के साथ या बिना किया जा सकता है।

## अवलोकन

यह पाठ MCP वातावरण सेटअप और आपके पहले MCP एप्लिकेशन बनाने पर व्यावहारिक मार्गदर्शन प्रदान करता है। आप आवश्यक टूल्स और फ्रेमवर्क सेटअप करना, बेसिक MCP सर्वर बनाना, होस्ट एप्लिकेशन बनाना और अपनी इम्प्लीमेंटेशन का परीक्षण करना सीखेंगे।

Model Context Protocol (MCP) एक ओपन प्रोटोकॉल है जो एप्लिकेशन को LLMs को संदर्भ प्रदान करने का मानकीकृत तरीका प्रदान करता है। MCP को AI एप्लिकेशन के लिए USB-C पोर्ट की तरह सोचें - यह AI मॉडल को विभिन्न डेटा स्रोतों और टूल्स से कनेक्ट करने का मानकीकृत तरीका प्रदान करता है।

## सीखने के उद्देश्य

इस पाठ के अंत तक, आप सक्षम होंगे:

- C#, Java, Python, TypeScript, और Rust में MCP के लिए विकास वातावरण सेटअप करना
- कस्टम फीचर्स (संसाधन, प्रॉम्प्ट्स, और टूल्स) के साथ बेसिक MCP सर्वर बनाना और तैनात करना
- MCP सर्वर से कनेक्ट होने वाले होस्ट एप्लिकेशन बनाना
- MCP इम्प्लीमेंटेशन का परीक्षण और डिबग करना

## MCP वातावरण सेटअप करना

MCP के साथ काम शुरू करने से पहले, अपने विकास वातावरण को तैयार करना और बुनियादी वर्कफ़्लो को समझना महत्वपूर्ण है। यह अनुभाग आपको MCP के साथ एक सहज शुरुआत सुनिश्चित करने के लिए प्रारंभिक सेटअप चरणों के माध्यम से मार्गदर्शन करेगा।

### आवश्यकताएँ

MCP विकास में उतरने से पहले, सुनिश्चित करें कि आपके पास निम्नलिखित हैं:

- **विकास वातावरण**: आपके चुने हुए भाषा (C#, Java, Python, TypeScript, या Rust) के लिए
- **IDE/एडिटर**: Visual Studio, Visual Studio Code, IntelliJ, Eclipse, PyCharm, या कोई आधुनिक कोड एडिटर
- **पैकेज मैनेजर्स**: NuGet, Maven/Gradle, pip, npm/yarn, या Cargo
- **API कुंजियाँ**: उन AI सेवाओं के लिए जिन्हें आप अपने होस्ट एप्लिकेशन में उपयोग करने की योजना बना रहे हैं

## बेसिक MCP सर्वर संरचना

एक MCP सर्वर आमतौर पर निम्नलिखित शामिल करता है:

- **सर्वर कॉन्फ़िगरेशन**: पोर्ट, ऑथेंटिकेशन, और अन्य सेटिंग्स सेटअप करना
- **संसाधन**: LLMs को उपलब्ध कराए गए डेटा और संदर्भ
- **टूल्स**: मॉडल द्वारा उपयोग की जाने वाली कार्यक्षमता
- **प्रॉम्प्ट्स**: टेक्स्ट उत्पन्न करने या संरचना के लिए टेम्पलेट्स

TypeScript में एक सरल उदाहरण यहां दिया गया है:

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
  "file",
  // The 'list' parameter controls how the resource lists available files. Setting it to undefined disables listing for this resource.
  new ResourceTemplate("file://{path}", { list: undefined }),
  async (uri, { path }) => ({
    contents: [{
      uri: uri.href,
      text: `File, ${path}!`
    }]
// Add a file resource that reads the file contents
server.resource(
  "file",
  new ResourceTemplate("file://{path}", { list: undefined }),
  async (uri, { path }) => {
    let text;
    try {
      text = await fs.readFile(path, "utf8");
    } catch (err) {
      text = `Error reading file: ${err.message}`;
    }
    return {
      contents: [{
        uri: uri.href,
        text
      }]
    };
  }
);

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

// Start receiving messages on stdin and sending messages on stdout
const transport = new StdioServerTransport();
await server.connect(transport);
```

उपरोक्त कोड में हमने:

- MCP TypeScript SDK से आवश्यक क्लासेस को इम्पोर्ट किया।
- एक नया MCP सर्वर इंस्टेंस बनाया और कॉन्फ़िगर किया।
- एक कस्टम टूल (`calculator`) को हैंडलर फंक्शन के साथ रजिस्टर किया।
- MCP अनुरोधों के लिए सर्वर को सुनने के लिए शुरू किया।

## परीक्षण और डिबगिंग

अपने MCP सर्वर का परीक्षण शुरू करने से पहले, उपलब्ध टूल्स और डिबगिंग के लिए सर्वोत्तम प्रथाओं को समझना महत्वपूर्ण है। प्रभावी परीक्षण यह सुनिश्चित करता है कि आपका सर्वर अपेक्षित रूप से व्यवहार करता है और आपको समस्याओं की पहचान और समाधान जल्दी करने में मदद करता है। निम्नलिखित अनुभाग MCP इम्प्लीमेंटेशन को मान्य करने के लिए अनुशंसित दृष्टिकोणों को रेखांकित करता है।

MCP आपके सर्वर का परीक्षण और डिबग करने में मदद करने के लिए टूल्स प्रदान करता है:

- **Inspector टूल**, यह ग्राफिकल इंटरफ़ेस आपको अपने सर्वर से कनेक्ट करने और अपने टूल्स, प्रॉम्प्ट्स और संसाधनों का परीक्षण करने की अनुमति देता है।
- **curl**, आप कमांड लाइन टूल जैसे curl या अन्य क्लाइंट्स का उपयोग करके अपने सर्वर से कनेक्ट कर सकते हैं जो HTTP कमांड बना और चला सकते हैं।

### MCP Inspector का उपयोग करना

[MCP Inspector](https://github.com/modelcontextprotocol/inspector) एक विज़ुअल परीक्षण टूल है जो आपकी मदद करता है:

1. **सर्वर क्षमताओं की खोज करें**: उपलब्ध संसाधन, टूल्स, और प्रॉम्प्ट्स को स्वचालित रूप से पहचानें
2. **टूल निष्पादन का परीक्षण करें**: विभिन्न पैरामीटर आज़माएं और रियल-टाइम में प्रतिक्रियाएँ देखें
3. **सर्वर मेटाडेटा देखें**: सर्वर जानकारी, स्कीमास, और कॉन्फ़िगरेशन की जांच करें

```bash
# ex TypeScript, installing and running MCP Inspector
npx @modelcontextprotocol/inspector node build/index.js
```

जब आप उपरोक्त कमांड्स चलाते हैं, तो MCP Inspector आपके ब्राउज़र में एक स्थानीय वेब इंटरफ़ेस लॉन्च करेगा। आप एक डैशबोर्ड की उम्मीद कर सकते हैं जो आपके रजिस्टर्ड MCP सर्वर्स, उनके उपलब्ध टूल्स, संसाधन, और प्रॉम्प्ट्स को प्रदर्शित करता है। इंटरफ़ेस आपको इंटरैक्टिव रूप से टूल निष्पादन का परीक्षण करने, सर्वर मेटाडेटा का निरीक्षण करने, और रियल-टाइम प्रतिक्रियाएँ देखने की अनुमति देता है, जिससे आपके MCP सर्वर इम्प्लीमेंटेशन को मान्य और डिबग करना आसान हो जाता है।

यहां इसका स्क्रीनशॉट कैसा दिख सकता है:

![MCP Inspector सर्वर कनेक्शन](../../../../translated_images/connected.73d1e042c24075d386cacdd4ee7cd748c16364c277d814e646ff2f7b5eefde85.hi.png)

## सामान्य सेटअप समस्याएँ और समाधान

| समस्या | संभावित समाधान |
|-------|-------------------|
| कनेक्शन अस्वीकृत | जांचें कि सर्वर चल रहा है और पोर्ट सही है |
| टूल निष्पादन त्रुटियाँ | पैरामीटर मान्यता और त्रुटि हैंडलिंग की समीक्षा करें |
| ऑथेंटिकेशन विफलता | API कुंजियों और अनुमतियों को सत्यापित करें |
| स्कीमा मान्यता त्रुटियाँ | सुनिश्चित करें कि पैरामीटर परिभाषित स्कीमा से मेल खाते हैं |
| सर्वर शुरू नहीं हो रहा | पोर्ट संघर्ष या गायब निर्भरताओं की जांच करें |
| CORS त्रुटियाँ | क्रॉस-ओरिजिन अनुरोधों के लिए उचित CORS हेडर्स कॉन्फ़िगर करें |
| ऑथेंटिकेशन समस्याएँ | टोकन वैधता और अनुमतियों को सत्यापित करें |

## स्थानीय विकास

स्थानीय विकास और परीक्षण के लिए, आप MCP सर्वर्स को सीधे अपनी मशीन पर चला सकते हैं:

1. **सर्वर प्रक्रिया शुरू करें**: अपना MCP सर्वर एप्लिकेशन चलाएँ
2. **नेटवर्किंग कॉन्फ़िगर करें**: सुनिश्चित करें कि सर्वर अपेक्षित पोर्ट पर एक्सेस करने योग्य है
3. **क्लाइंट्स कनेक्ट करें**: स्थानीय कनेक्शन URLs जैसे `http://localhost:3000` का उपयोग करें

```bash
# Example: Running a TypeScript MCP server locally
npm run start
# Server running at http://localhost:3000
```

## अपना पहला MCP सर्वर बनाना

हमने पिछले पाठ में [Core concepts](/01-CoreConcepts/README.md) को कवर किया है, अब उस ज्ञान को काम में लाने का समय है।

### सर्वर क्या कर सकता है

कोड लिखना शुरू करने से पहले, चलिए याद कर लेते हैं कि सर्वर क्या कर सकता है:

एक MCP सर्वर उदाहरण के लिए:

- स्थानीय फाइल्स और डेटाबेस तक पहुंच सकता है
- रिमोट APIs से कनेक्ट कर सकता है
- गणनाएँ कर सकता है
- अन्य टूल्स और सेवाओं के साथ इंटीग्रेट कर सकता है
- इंटरैक्शन के लिए एक यूजर इंटरफ़ेस प्रदान कर सकता है

बहुत अच्छा, अब जब हमें पता है कि हम इसके लिए क्या कर सकते हैं, तो चलिए कोडिंग शुरू करते हैं।

## अभ्यास: सर्वर बनाना

सर्वर बनाने के लिए, आपको निम्नलिखित चरणों का पालन करना होगा:

- MCP SDK इंस्टॉल करें।
- एक प्रोजेक्ट बनाएं और प्रोजेक्ट संरचना सेट करें।
- सर्वर कोड लिखें।
- सर्वर का परीक्षण करें।

### -1- प्रोजेक्ट बनाएं

#### TypeScript

```sh
# Create project directory and initialize npm project
mkdir calculator-server
cd calculator-server
npm init -y
```

#### Python

```sh
# Create project dir
mkdir calculator-server
cd calculator-server
# Open the folder in Visual Studio Code - Skip this if you are using a different IDE
code .
```

#### .NET

```sh
dotnet new console -n McpCalculatorServer
cd McpCalculatorServer
```

#### Java

Java के लिए, एक Spring Boot प्रोजेक्ट बनाएं:

```bash
curl https://start.spring.io/starter.zip \
  -d dependencies=web \
  -d javaVersion=21 \
  -d type=maven-project \
  -d groupId=com.example \
  -d artifactId=calculator-server \
  -d name=McpServer \
  -d packageName=com.microsoft.mcp.sample.server \
  -o calculator-server.zip
```

Zip फ़ाइल को एक्सट्रैक्ट करें:

```bash
unzip calculator-server.zip -d calculator-server
cd calculator-server
# optional remove the unused test
rm -rf src/test/java
```

अपने *pom.xml* फ़ाइल में निम्नलिखित पूर्ण कॉन्फ़िगरेशन जोड़ें:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    
    <!-- Spring Boot parent for dependency management -->
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.5.0</version>
        <relativePath />
    </parent>

    <!-- Project coordinates -->
    <groupId>com.example</groupId>
    <artifactId>calculator-server</artifactId>
    <version>0.0.1-SNAPSHOT</version>
    <name>Calculator Server</name>
    <description>Basic calculator MCP service for beginners</description>

    <!-- Properties -->
    <properties>
        <java.version>21</java.version>
        <maven.compiler.source>21</maven.compiler.source>
        <maven.compiler.target>21</maven.compiler.target>
    </properties>

    <!-- Spring AI BOM for version management -->
    <dependencyManagement>
        <dependencies>
            <dependency>
                <groupId>org.springframework.ai</groupId>
                <artifactId>spring-ai-bom</artifactId>
                <version>1.0.0-SNAPSHOT</version>
                <type>pom</type>
                <scope>import</scope>
            </dependency>
        </dependencies>
    </dependencyManagement>

    <!-- Dependencies -->
    <dependencies>
        <dependency>
            <groupId>org.springframework.ai</groupId>
            <artifactId>spring-ai-starter-mcp-server-webflux</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-actuator</artifactId>
        </dependency>
        <dependency>
         <groupId>org.springframework.boot</groupId>
         <artifactId>spring-boot-starter-test</artifactId>
         <scope>test</scope>
      </dependency>
    </dependencies>

    <!-- Build configuration -->
    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <configuration>
                    <release>21</release>
                </configuration>
            </plugin>
        </plugins>
    </build>

    <!-- Repositories for Spring AI snapshots -->
    <repositories>
        <repository>
            <id>spring-milestones</id>
            <name>Spring Milestones</name>
            <url>https://repo.spring.io/milestone</url>
            <snapshots>
                <enabled>false</enabled>
            </snapshots>
        </repository>
        <repository>
            <id>spring-snapshots</id>
            <name>Spring Snapshots</name>
            <url>https://repo.spring.io/snapshot</url>
            <releases>
                <enabled>false</enabled>
            </releases>
        </repository>
    </repositories>
</project>
```

#### Rust

```sh
mkdir calculator-server
cd calculator-server
cargo init
```

### -2- निर्भरताएँ जोड़ें

अब जब आपने अपना प्रोजेक्ट बना लिया है, तो चलिए अगला निर्भरताएँ जोड़ते हैं:

#### TypeScript

```sh
# If not already installed, install TypeScript globally
npm install typescript -g

# Install the MCP SDK and Zod for schema validation
npm install @modelcontextprotocol/sdk zod
npm install -D @types/node typescript
```

#### Python

```sh
# Create a virtual env and install dependencies
python -m venv venv
venv\Scripts\activate
pip install "mcp[cli]"
```

#### Java

```bash
cd calculator-server
./mvnw clean install -DskipTests
```

#### Rust

```sh
cargo add rmcp --features server,transport-io
cargo add serde
cargo add tokio --features rt-multi-thread
```

### -3- प्रोजेक्ट फाइल्स बनाएं

#### TypeScript

*package.json* फ़ाइल खोलें और निम्नलिखित सामग्री के साथ इसे बदलें ताकि आप सर्वर को बना और चला सकें:

```json
{
  "name": "calculator-server",
  "version": "1.0.0",
  "main": "index.js",
  "type": "module",
  "scripts": {
    "start": "tsc && node ./build/index.js",
    "build": "tsc && node ./build/index.js"
  },
  "keywords": [],
  "author": "",
  "license": "ISC",
  "description": "A simple calculator server using Model Context Protocol",
  "dependencies": {
    "@modelcontextprotocol/sdk": "^1.16.0",
    "zod": "^3.25.76"
  },
  "devDependencies": {
    "@types/node": "^24.0.14",
    "typescript": "^5.8.3"
  }
}
```

*tsconfig.json* बनाएं और निम्नलिखित सामग्री जोड़ें:

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "Node16",
    "moduleResolution": "Node16",
    "outDir": "./build",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules"]
}
```

अपने सोर्स कोड के लिए एक डायरेक्टरी बनाएं:

```sh
mkdir src
touch src/index.ts
```

#### Python

*server.py* फ़ाइल बनाएं

```sh
touch server.py
```

#### .NET

आवश्यक NuGet पैकेज इंस्टॉल करें:

```sh
dotnet add package ModelContextProtocol --prerelease
dotnet add package Microsoft.Extensions.Hosting
```

#### Java

Java Spring Boot प्रोजेक्ट्स के लिए, प्रोजेक्ट संरचना स्वचालित रूप से बनाई जाती है।

#### Rust

Rust के लिए, जब आप `cargo init` चलाते हैं तो एक *src/main.rs* फ़ाइल डिफ़ॉल्ट रूप से बनाई जाती है। फ़ाइल खोलें और डिफ़ॉल्ट कोड हटा दें।

### -4- सर्वर कोड बनाएं

#### TypeScript

*index.ts* फ़ाइल बनाएं और निम्नलिखित कोड जोड़ें:

```typescript
import { McpServer, ResourceTemplate } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
 
// Create an MCP server
const server = new McpServer({
  name: "Calculator MCP Server",
  version: "1.0.0"
});
```

अब आपके पास एक सर्वर है, लेकिन यह ज्यादा कुछ नहीं करता, चलिए इसे ठीक करते हैं।

#### Python

```python
# server.py
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Demo")
```

#### .NET

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

// add features
```

#### Java

Java के लिए, मुख्य सर्वर घटकों को संशोधित करें। पहले, मुख्य एप्लिकेशन क्लास को संशोधित करें:

*src/main/java/com/microsoft/mcp/sample/server/McpServerApplication.java*:

```java
package com.microsoft.mcp.sample.server;

import org.springframework.ai.tool.ToolCallbackProvider;
import org.springframework.ai.tool.method.MethodToolCallbackProvider;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import com.microsoft.mcp.sample.server.service.CalculatorService;

@SpringBootApplication
public class McpServerApplication {

    public static void main(String[] args) {
        SpringApplication.run(McpServerApplication.class, args);
    }
    
    @Bean
    public ToolCallbackProvider calculatorTools(CalculatorService calculator) {
        return MethodToolCallbackProvider.builder().toolObjects(calculator).build();
    }
}
```

*src/main/java/com/microsoft/mcp/sample/server/service/CalculatorService.java* में कैलकुलेटर सेवा बनाएं:

```java
package com.microsoft.mcp.sample.server.service;

import org.springframework.ai.tool.annotation.Tool;
import org.springframework.stereotype.Service;

/**
 * Service for basic calculator operations.
 * This service provides simple calculator functionality through MCP.
 */
@Service
public class CalculatorService {

    /**
     * Add two numbers
     * @param a The first number
     * @param b The second number
     * @return The sum of the two numbers
     */
    @Tool(description = "Add two numbers together")
    public String add(double a, double b) {
        double result = a + b;
        return formatResult(a, "+", b, result);
    }

    /**
     * Subtract one number from another
     * @param a The number to subtract from
     * @param b The number to subtract
     * @return The result of the subtraction
     */
    @Tool(description = "Subtract the second number from the first number")
    public String subtract(double a, double b) {
        double result = a - b;
        return formatResult(a, "-", b, result);
    }

    /**
     * Multiply two numbers
     * @param a The first number
     * @param b The second number
     * @return The product of the two numbers
     */
    @Tool(description = "Multiply two numbers together")
    public String multiply(double a, double b) {
        double result = a * b;
        return formatResult(a, "*", b, result);
    }

    /**
     * Divide one number by another
     * @param a The numerator
     * @param b The denominator
     * @return The result of the division
     */
    @Tool(description = "Divide the first number by the second number")
    public String divide(double a, double b) {
        if (b == 0) {
            return "Error: Cannot divide by zero";
        }
        double result = a / b;
        return formatResult(a, "/", b, result);
    }

    /**
     * Calculate the power of a number
     * @param base The base number
     * @param exponent The exponent
     * @return The result of raising the base to the exponent
     */
    @Tool(description = "Calculate the power of a number (base raised to an exponent)")
    public String power(double base, double exponent) {
        double result = Math.pow(base, exponent);
        return formatResult(base, "^", exponent, result);
    }

    /**
     * Calculate the square root of a number
     * @param number The number to find the square root of
     * @return The square root of the number
     */
    @Tool(description = "Calculate the square root of a number")
    public String squareRoot(double number) {
        if (number < 0) {
            return "Error: Cannot calculate square root of a negative number";
        }
        double result = Math.sqrt(number);
        return String.format("√%.2f = %.2f", number, result);
    }

    /**
     * Calculate the modulus (remainder) of division
     * @param a The dividend
     * @param b The divisor
     * @return The remainder of the division
     */
    @Tool(description = "Calculate the remainder when one number is divided by another")
    public String modulus(double a, double b) {
        if (b == 0) {
            return "Error: Cannot divide by zero";
        }
        double result = a % b;
        return formatResult(a, "%", b, result);
    }

    /**
     * Calculate the absolute value of a number
     * @param number The number to find the absolute value of
     * @return The absolute value of the number
     */
    @Tool(description = "Calculate the absolute value of a number")
    public String absolute(double number) {
        double result = Math.abs(number);
        return String.format("|%.2f| = %.2f", number, result);
    }

    /**
     * Get help about available calculator operations
     * @return Information about available operations
     */
    @Tool(description = "Get help about available calculator operations")
    public String help() {
        return "Basic Calculator MCP Service\n\n" +
               "Available operations:\n" +
               "1. add(a, b) - Adds two numbers\n" +
               "2. subtract(a, b) - Subtracts the second number from the first\n" +
               "3. multiply(a, b) - Multiplies two numbers\n" +
               "4. divide(a, b) - Divides the first number by the second\n" +
               "5. power(base, exponent) - Raises a number to a power\n" +
               "6. squareRoot(number) - Calculates the square root\n" + 
               "7. modulus(a, b) - Calculates the remainder of division\n" +
               "8. absolute(number) - Calculates the absolute value\n\n" +
               "Example usage: add(5, 3) will return 5 + 3 = 8";
    }

    /**
     * Format the result of a calculation
     */
    private String formatResult(double a, String operator, double b, double result) {
        return String.format("%.2f %s %.2f = %.2f", a, operator, b, result);
    }
}
```

**उत्पादन-तैयार सेवा के लिए वैकल्पिक घटक:**

*src/main/java/com/microsoft/mcp/sample/server/config/StartupConfig.java* में स्टार्टअप कॉन्फ़िगरेशन बनाएं:

```java
package com.microsoft.mcp.sample.server.config;

import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class StartupConfig {
    
    @Bean
    public CommandLineRunner startupInfo() {
        return args -> {
            System.out.println("\n" + "=".repeat(60));
            System.out.println("Calculator MCP Server is starting...");
            System.out.println("SSE endpoint: http://localhost:8080/sse");
            System.out.println("Health check: http://localhost:8080/actuator/health");
            System.out.println("=".repeat(60) + "\n");
        };
    }
}
```

*src/main/java/com/microsoft/mcp/sample/server/controller/HealthController.java* में हेल्थ कंट्रोलर बनाएं:

```java
package com.microsoft.mcp.sample.server.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.Map;

@RestController
public class HealthController {
    
    @GetMapping("/health")
    public ResponseEntity<Map<String, Object>> healthCheck() {
        Map<String, Object> response = new HashMap<>();
        response.put("status", "UP");
        response.put("timestamp", LocalDateTime.now().toString());
        response.put("service", "Calculator MCP Server");
        return ResponseEntity.ok(response);
    }
}
```

*src/main/java/com/microsoft/mcp/sample/server/exception/GlobalExceptionHandler.java* में एक्सेप्शन हैंडलर बनाएं:

```java
package com.microsoft.mcp.sample.server.exception;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(IllegalArgumentException.class)
    public ResponseEntity<ErrorResponse> handleIllegalArgumentException(IllegalArgumentException ex) {
        ErrorResponse error = new ErrorResponse(
            "Invalid_Input", 
            "Invalid input parameter: " + ex.getMessage());
        return new ResponseEntity<>(error, HttpStatus.BAD_REQUEST);
    }

    public static class ErrorResponse {
        private String code;
        private String message;

        public ErrorResponse(String code, String message) {
            this.code = code;
            this.message = message;
        }

        // Getters
        public String getCode() { return code; }
        public String getMessage() { return message; }
    }
}
```

*src/main/resources/banner.txt* में कस्टम बैनर बनाएं:

```text
_____      _            _       _             
 / ____|    | |          | |     | |            
| |     __ _| | ___ _   _| | __ _| |_ ___  _ __ 
| |    / _` | |/ __| | | | |/ _` | __/ _ \| '__|
| |___| (_| | | (__| |_| | | (_| | || (_) | |   
 \_____\__,_|_|\___|\__,_|_|\__,_|\__\___/|_|   
                                                
Calculator MCP Server v1.0
Spring Boot MCP Application
```

#### Rust

*src/main.rs* फ़ाइल के शीर्ष पर निम्नलिखित कोड जोड़ें। यह आपके MCP सर्वर के लिए आवश्यक लाइब्रेरी और मॉड्यूल इम्पोर्ट करता है।

```rust
use rmcp::{
    handler::server::{router::tool::ToolRouter, tool::Parameters},
    model::{ServerCapabilities, ServerInfo},
    schemars, tool, tool_handler, tool_router,
    transport::stdio,
    ServerHandler, ServiceExt,
};
use std::error::Error;
```

कैलकुलेटर अनुरोध को दर्शाने के लिए एक स्ट्रक्चर बनाएं:

```rust
#[derive(Debug, serde::Deserialize, schemars::JsonSchema)]
pub struct CalculatorRequest {
    pub a: f64,
    pub b: f64,
}
```

कैलकुलेटर सर्वर को दर्शाने के लिए एक स्ट्रक्चर बनाएं। यह स्ट्रक्चर टूल राउटर को होल्ड करेगा, जिसका उपयोग टूल्स को रजिस्टर करने के लिए किया जाता है।

```rust
#[derive(Debug, Clone)]
pub struct Calculator {
    tool_router: ToolRouter<Self>,
}
```

अब, हम `Calculator` स्ट्रक्चर को इम्प्लीमेंट कर सकते हैं ताकि सर्वर की जानकारी प्रदान करने के लिए सर्वर हैंडलर को इम्प्लीमेंट किया जा सके।

```rust
#[tool_router]
impl Calculator {
    pub fn new() -> Self {
        Self {
            tool_router: Self::tool_router(),
        }
    }
}

#[tool_handler]
impl ServerHandler for Calculator {
    fn get_info(&self) -> ServerInfo {
        ServerInfo {
            instructions: Some("A simple calculator tool".into()),
            capabilities: ServerCapabilities::builder().enable_tools().build(),
            ..Default::default()
        }
    }
}
```

अंत में, हमें सर्वर शुरू करने के लिए मुख्य फ़ंक्शन को इम्प्लीमेंट करना होगा। यह फ़ंक्शन `Calculator` स्ट्रक्चर का एक इंस्टेंस बनाएगा और इसे स्टैंडर्ड इनपुट/आउटपुट पर सर्व करेगा।

```rust
#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    let service = Calculator::new().serve(stdio()).await?;
    service.waiting().await?;
    Ok(())
}
```

अब सर्वर बेसिक जानकारी प्रदान करने के लिए सेटअप हो गया है। अगला, हम जोड़ने की गणना करने के लिए एक टूल जोड़ेंगे।

### -5- टूल और संसाधन जोड़ना

एक टूल और संसाधन जोड़ें:

#### TypeScript

```typescript
server.tool(
  "add",
  { a: z.number(), b: z.number() },
  async ({ a, b }) => ({
    content: [{ type: "text", text: String(a + b) }]
  })
);

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
```

आपका टूल पैरामीटर `a` और `b` लेता है और एक फंक्शन चलाता है जो निम्नलिखित फॉर्म में प्रतिक्रिया उत्पन्न करता है:

```typescript
{
  contents: [{
    type: "text", content: "some content"
  }]
}
```

आपका संसाधन एक स्ट्रिंग "greeting" के माध्यम से एक्सेस किया जाता है और पैरामीटर `name` लेता है और टूल के समान प्रतिक्रिया उत्पन्न करता है:

```typescript
{
  uri: "<href>",
  text: "a text"
}
```

#### Python

```python
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

उपरोक्त कोड में हमने:

- एक टूल `add` परिभाषित किया जो पैरामीटर `a` और `p`, दोनों पूर्णांक लेता है।
- एक संसाधन `greeting` बनाया जो पैरामीटर `name` लेता है।

#### .NET

अपने Program.cs फ़ाइल में यह जोड़ें:

```csharp
[McpServerToolType]
public static class CalculatorTool
{
    [McpServerTool, Description("Adds two numbers")]
    public static string Add(int a, int b) => $"Sum {a + b}";
}
```

#### Java

पिछले चरण में टूल्स पहले ही बनाए जा चुके हैं।

#### Rust

`impl Calculator` ब्लॉक के अंदर एक नया टूल जोड़ें:

```rust
#[tool(description = "Adds a and b")]
async fn add(
    &self,
    Parameters(CalculatorRequest { a, b }): Parameters<CalculatorRequest>,
) -> String {
    (a + b).to_string()
}
```

### -6- अंतिम कोड

आइए वह अंतिम कोड जोड़ें जिसकी हमें आवश्यकता है ताकि सर्वर शुरू हो सके:

#### TypeScript

```typescript
// Start receiving messages on stdin and sending messages on stdout
const transport = new StdioServerTransport();
await server.connect(transport);
```

यहां पूरा कोड है:

```typescript
// index.ts
import { McpServer, ResourceTemplate } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

// Create an MCP server
const server = new McpServer({
  name: "Calculator MCP Server",
  version: "1.0.0"
});

// Add an addition tool
server.tool(
  "add",
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
const transport = new StdioServerTransport();
server.connect(transport);
```

#### Python

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

# Main execution block - this is required to run the server
if __name__ == "__main__":
    mcp.run()
```

#### .NET

एक Program.cs फ़ाइल बनाएं जिसमें निम्नलिखित सामग्री हो:

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

#### Java

आपका पूरा मुख्य एप्लिकेशन क्लास इस प्रकार दिखना चाहिए:

```java
// McpServerApplication.java
package com.microsoft.mcp.sample.server;

import org.springframework.ai.tool.ToolCallbackProvider;
import org.springframework.ai.tool.method.MethodToolCallbackProvider;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import com.microsoft.mcp.sample.server.service.CalculatorService;

@SpringBootApplication
public class McpServerApplication {

    public static void main(String[] args) {
        SpringApplication.run(McpServerApplication.class, args);
    }
    
    @Bean
    public ToolCallbackProvider calculatorTools(CalculatorService calculator) {
        return MethodToolCallbackProvider.builder().toolObjects(calculator).build();
    }
}
```

#### Rust

Rust सर्वर के लिए अंतिम कोड इस प्रकार दिखना चाहिए:

```rust
use rmcp::{
    ServerHandler, ServiceExt,
    handler::server::{router::tool::ToolRouter, tool::Parameters},
    model::{ServerCapabilities, ServerInfo},
    schemars, tool, tool_handler, tool_router,
    transport::stdio,
};
use std::error::Error;

#[derive(Debug, serde::Deserialize, schemars::JsonSchema)]
pub struct CalculatorRequest {
    pub a: f64,
    pub b: f64,
}

#[derive(Debug, Clone)]
pub struct Calculator {
    tool_router: ToolRouter<Self>,
}

#[tool_router]
impl Calculator {
    pub fn new() -> Self {
        Self {
            tool_router: Self::tool_router(),
        }
    }
    
    #[tool(description = "Adds a and b")]
    async fn add(
        &self,
        Parameters(CalculatorRequest { a, b }): Parameters<CalculatorRequest>,
    ) -> String {
        (a + b).to_string()
    }
}

#[tool_handler]
impl ServerHandler for Calculator {
    fn get_info(&self) -> ServerInfo {
        ServerInfo {
            instructions: Some("A simple calculator tool".into()),
            capabilities: ServerCapabilities::builder().enable_tools().build(),
            ..Default::default()
        }
    }
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    let service = Calculator::new().serve(stdio()).await?;
    service.waiting().await?;
    Ok(())
}
```

### -7- सर्वर का परीक्षण करें

निम्नलिखित कमांड के साथ सर्वर शुरू करें:

#### TypeScript

```sh
npm run build
```

#### Python

```sh
mcp run server.py
```

> MCP Inspector का उपयोग करने के लिए, `mcp dev server.py` का उपयोग करें जो स्वचालित रूप से Inspector लॉन्च करता है और आवश्यक प्रॉक्सी सेशन टोकन प्रदान करता है। यदि आप `mcp run server.py` का उपयोग कर रहे हैं, तो आपको मैन्युअल रूप से Inspector शुरू करना होगा और कनेक्शन कॉन्फ़िगर करना होगा।

#### .NET

सुनिश्चित करें कि आप अपने प्रोजेक्ट डायरेक्टरी में हैं:

```sh
cd McpCalculatorServer
dotnet run
```

#### Java

```bash
./mvnw clean install -DskipTests
java -jar target/calculator-server-0.0.1-SNAPSHOT.jar
```

#### Rust

सर्वर को प्रारूपित और चलाने के लिए निम्नलिखित कमांड चलाएँ:

```sh
cargo fmt
cargo run
```

### -8- Inspector का उपयोग करके चलाएँ

Inspector एक शानदार टूल है जो आपके सर्वर को शुरू कर सकता है और आपको इसके साथ इंटरैक्ट करने देता है ताकि आप परीक्षण कर सकें कि यह काम करता है। चलिए इसे शुरू करते हैं:

> [!NOTE]
> "command" फ़ील्ड में यह अलग दिख सकता है क्योंकि इसमें आपके विशिष्ट रनटाइम के साथ सर्वर चलाने के लिए कमांड होता है।

#### TypeScript

```sh
npx @modelcontextprotocol/inspector node build/index.js
```

या इसे अपने *package.json* में जोड़ें जैसे: `"inspector": "npx @modelcontextprotocol/inspector node build/index.js"` और फिर `npm run inspector` चलाएँ।

Python एक Node.js टूल को रैप करता है जिसे inspector कहा जाता है। इसे निम्नलिखित तरीके से कॉल करना संभव है:

```sh
mcp dev server.py
```

हालांकि, यह टूल पर उपलब्ध सभी विधियों को इम्प्लीमेंट नहीं करता है, इसलिए आपको नीचे दिए गए तरीके से सीधे Node.js टूल चलाने की सिफारिश की जाती है:

```sh
npx @modelcontextprotocol/inspector mcp run server.py
```

यदि आप किसी टूल या IDE का उपयोग कर रहे हैं जो स्क्रिप्ट चलाने के लिए कमांड और आर्गुमेंट्स को कॉन्फ़िगर करने की अनुमति देता है, 
सुनिश्चित करें कि `python` को `Command` फ़ील्ड में सेट करें और `server.py` को `Arguments` के रूप में। यह सुनिश्चित करता है कि स्क्रिप्ट सही ढंग से चलती है।

#### .NET

सुनिश्चित करें कि आप अपने प्रोजेक्ट डायरेक्टरी में हैं:

```sh
cd McpCalculatorServer
npx @modelcontextprotocol/inspector dotnet run
```

#### Java

सुनिश्चित करें कि आपका कैलकुलेटर सर्वर चल रहा है। फिर Inspector चलाएँ:

```cmd
npx @modelcontextprotocol/inspector
```

Inspector वेब इंटरफ़ेस में:

1. "SSE" को ट्रांसपोर्ट प्रकार के रूप में चुनें
2. URL सेट करें: `http://localhost:8080/sse`
3. "Connect" पर
![कनेक्ट करें](../../../../translated_images/tool.163d33e3ee307e209ef146d8f85060d2f7e83e9f59b3b1699a77204ae0454ad2.hi.png)

**अब आप सर्वर से कनेक्ट हो चुके हैं**  
**जावा सर्वर टेस्टिंग सेक्शन अब पूरा हो गया है**

अगला सेक्शन सर्वर के साथ इंटरैक्ट करने के बारे में है।

आपको निम्नलिखित यूजर इंटरफेस दिखाई देना चाहिए:

![कनेक्ट करें](../../../../translated_images/connect.141db0b2bd05f096fb1dd91273771fd8b2469d6507656c3b0c9df4b3c5473929.hi.png)

1. "कनेक्ट" बटन का चयन करके सर्वर से कनेक्ट करें।  
   सर्वर से कनेक्ट होने के बाद, आपको निम्नलिखित दिखाई देना चाहिए:

   ![कनेक्टेड](../../../../translated_images/connected.73d1e042c24075d386cacdd4ee7cd748c16364c277d814e646ff2f7b5eefde85.hi.png)

1. "टूल्स" और "listTools" का चयन करें। आपको "Add" दिखाई देगा। "Add" का चयन करें और पैरामीटर वैल्यू भरें।  

   आपको निम्नलिखित प्रतिक्रिया दिखाई देनी चाहिए, यानी "add" टूल का परिणाम:

   ![Add टूल चलाने का परिणाम](../../../../translated_images/ran-tool.a5a6ee878c1369ec1e379b81053395252a441799dbf23416c36ddf288faf8249.hi.png)

बधाई हो, आपने अपना पहला सर्वर बनाने और चलाने में सफलता प्राप्त की है!

#### रस्ट

MCP Inspector CLI के साथ रस्ट सर्वर चलाने के लिए, निम्नलिखित कमांड का उपयोग करें:

```sh
npx @modelcontextprotocol/inspector cargo run --cli --method tools/call --tool-name add --tool-arg a=1 b=2
```

### आधिकारिक SDKs

MCP कई भाषाओं के लिए आधिकारिक SDKs प्रदान करता है:

- [C# SDK](https://github.com/modelcontextprotocol/csharp-sdk) - Microsoft के सहयोग से बनाए रखा गया
- [Java SDK](https://github.com/modelcontextprotocol/java-sdk) - Spring AI के सहयोग से बनाए रखा गया
- [TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk) - आधिकारिक TypeScript कार्यान्वयन
- [Python SDK](https://github.com/modelcontextprotocol/python-sdk) - आधिकारिक Python कार्यान्वयन
- [Kotlin SDK](https://github.com/modelcontextprotocol/kotlin-sdk) - आधिकारिक Kotlin कार्यान्वयन
- [Swift SDK](https://github.com/modelcontextprotocol/swift-sdk) - Loopwork AI के सहयोग से बनाए रखा गया
- [Rust SDK](https://github.com/modelcontextprotocol/rust-sdk) - आधिकारिक Rust कार्यान्वयन

## मुख्य बातें

- MCP डेवलपमेंट एनवायरनमेंट सेटअप करना भाषा-विशिष्ट SDKs के साथ आसान है।  
- MCP सर्वर बनाना टूल्स को स्पष्ट स्कीमाओं के साथ क्रिएट और रजिस्टर करने पर आधारित है।  
- विश्वसनीय MCP कार्यान्वयन के लिए टेस्टिंग और डिबगिंग आवश्यक हैं।  

## नमूने

- [जावा कैलकुलेटर](../samples/java/calculator/README.md)  
- [.Net कैलकुलेटर](../../../../03-GettingStarted/samples/csharp)  
- [जावास्क्रिप्ट कैलकुलेटर](../samples/javascript/README.md)  
- [टाइपस्क्रिप्ट कैलकुलेटर](../samples/typescript/README.md)  
- [पायथन कैलकुलेटर](../../../../03-GettingStarted/samples/python)  
- [रस्ट कैलकुलेटर](../../../../03-GettingStarted/samples/rust)  

## असाइनमेंट

अपनी पसंद के टूल के साथ एक साधारण MCP सर्वर बनाएं:

1. अपनी पसंदीदा भाषा (.NET, Java, Python, TypeScript, या Rust) में टूल को लागू करें।  
2. इनपुट पैरामीटर और रिटर्न वैल्यू को परिभाषित करें।  
3. इंस्पेक्टर टूल चलाएं ताकि यह सुनिश्चित हो सके कि सर्वर सही तरीके से काम कर रहा है।  
4. विभिन्न इनपुट्स के साथ कार्यान्वयन का परीक्षण करें।  

## समाधान

[समाधान](./solution/README.md)

## अतिरिक्त संसाधन

- [Azure पर Model Context Protocol का उपयोग करके एजेंट बनाएं](https://learn.microsoft.com/azure/developer/ai/intro-agents-mcp)  
- [Azure Container Apps के साथ रिमोट MCP (Node.js/TypeScript/JavaScript)](https://learn.microsoft.com/samples/azure-samples/mcp-container-ts/mcp-container-ts/)  
- [.NET OpenAI MCP एजेंट](https://learn.microsoft.com/samples/azure-samples/openai-mcp-agent-dotnet/openai-mcp-agent-dotnet/)  

## आगे क्या

अगला: [MCP क्लाइंट्स के साथ शुरुआत करें](../02-client/README.md)  

**अस्वीकरण**:  
यह दस्तावेज़ AI अनुवाद सेवा [Co-op Translator](https://github.com/Azure/co-op-translator) का उपयोग करके अनुवादित किया गया है। जबकि हम सटीकता सुनिश्चित करने का प्रयास करते हैं, कृपया ध्यान दें कि स्वचालित अनुवाद में त्रुटियां या अशुद्धियां हो सकती हैं। मूल भाषा में उपलब्ध मूल दस्तावेज़ को प्रामाणिक स्रोत माना जाना चाहिए। महत्वपूर्ण जानकारी के लिए, पेशेवर मानव अनुवाद की सिफारिश की जाती है। इस अनुवाद के उपयोग से उत्पन्न किसी भी गलतफहमी या गलत व्याख्या के लिए हम उत्तरदायी नहीं हैं।