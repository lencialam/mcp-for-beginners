<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "0df1ee78a6dd8300f3a040ca5b411c2e",
  "translation_date": "2025-08-12T07:55:10+00:00",
  "source_file": "00-Introduction/README.md",
  "language_code": "pt"
}
-->
# Introdução ao Protocolo de Contexto de Modelo (MCP): Por Que Ele É Importante para Aplicações de IA Escaláveis

[![Introdução ao Protocolo de Contexto de Modelo](../../../translated_images/01.a467036d886b5fb5b9cf7b39bac0e743b6ca0a4a18a492de90061daaf0cc55f0.pt.png)](https://youtu.be/agBbdiOPLQA)

_(Clique na imagem acima para assistir ao vídeo desta lição)_

As aplicações de IA generativa representam um grande avanço, pois frequentemente permitem que o utilizador interaja com a aplicação através de prompts em linguagem natural. No entanto, à medida que mais tempo e recursos são investidos nessas aplicações, é importante garantir que seja fácil integrar funcionalidades e recursos de forma a permitir extensões, que a aplicação suporte mais de um modelo e consiga lidar com as diversas particularidades dos modelos. Em resumo, construir aplicações de IA generativa é simples no início, mas, à medida que crescem e se tornam mais complexas, é necessário começar a definir uma arquitetura e, provavelmente, recorrer a um padrão para garantir que as aplicações sejam desenvolvidas de forma consistente. É aqui que o MCP entra em cena para organizar as coisas e fornecer um padrão.

---

## **🔍 O Que É o Protocolo de Contexto de Modelo (MCP)?**

O **Protocolo de Contexto de Modelo (MCP)** é uma **interface aberta e padronizada** que permite que Modelos de Linguagem de Grande Escala (LLMs) interajam de forma fluida com ferramentas externas, APIs e fontes de dados. Ele fornece uma arquitetura consistente para ampliar as funcionalidades dos modelos de IA além dos seus dados de treino, permitindo sistemas de IA mais inteligentes, escaláveis e responsivos.

---

## **🎯 Por Que a Padronização em IA É Importante**

À medida que as aplicações de IA generativa se tornam mais complexas, é essencial adotar padrões que garantam **escalabilidade, extensibilidade, manutenção** e **evitem dependência de fornecedores**. O MCP aborda essas necessidades ao:

- Unificar as integrações entre modelos e ferramentas
- Reduzir soluções personalizadas frágeis e pontuais
- Permitir que múltiplos modelos de diferentes fornecedores coexistam em um único ecossistema

**Nota:** Embora o MCP se apresente como um padrão aberto, não há planos para padronizá-lo através de organismos de padronização existentes, como IEEE, IETF, W3C, ISO ou outros.

---

## **📚 Objetivos de Aprendizagem**

Ao final deste artigo, será capaz de:

- Definir o **Protocolo de Contexto de Modelo (MCP)** e os seus casos de uso
- Compreender como o MCP padroniza a comunicação entre modelos e ferramentas
- Identificar os componentes principais da arquitetura do MCP
- Explorar aplicações reais do MCP em contextos empresariais e de desenvolvimento

---

## **💡 Por Que o Protocolo de Contexto de Modelo (MCP) É Revolucionário**

### **🔗 O MCP Resolve a Fragmentação nas Interações de IA**

Antes do MCP, integrar modelos com ferramentas exigia:

- Código personalizado para cada par ferramenta-modelo
- APIs não padronizadas para cada fornecedor
- Quebras frequentes devido a atualizações
- Escalabilidade limitada com mais ferramentas

### **✅ Benefícios da Padronização do MCP**

| **Benefício**              | **Descrição**                                                                |
|----------------------------|------------------------------------------------------------------------------|
| Interoperabilidade         | LLMs funcionam perfeitamente com ferramentas de diferentes fornecedores      |
| Consistência               | Comportamento uniforme em plataformas e ferramentas                          |
| Reutilização               | Ferramentas desenvolvidas uma vez podem ser usadas em vários projetos        |
| Desenvolvimento Acelerado  | Redução do tempo de desenvolvimento com interfaces padronizadas e plug-and-play |

---

## **🧱 Visão Geral da Arquitetura de Alto Nível do MCP**

O MCP segue um modelo **cliente-servidor**, onde:

- **Hosts MCP** executam os modelos de IA
- **Clientes MCP** iniciam pedidos
- **Servidores MCP** fornecem contexto, ferramentas e capacidades

### **Componentes Principais:**

- **Recursos** – Dados estáticos ou dinâmicos para os modelos  
- **Prompts** – Fluxos de trabalho predefinidos para geração orientada  
- **Ferramentas** – Funções executáveis, como pesquisa, cálculos  
- **Amostragem** – Comportamento agente através de interações recursivas  

---

## Como Funcionam os Servidores MCP

Os servidores MCP operam da seguinte forma:

- **Fluxo de Pedido**:
    1. Um pedido é iniciado por um utilizador final ou software que age em seu nome.
    2. O **Cliente MCP** envia o pedido para um **Host MCP**, que gere o runtime do Modelo de IA.
    3. O **Modelo de IA** recebe o prompt do utilizador e pode solicitar acesso a ferramentas ou dados externos através de uma ou mais chamadas de ferramentas.
    4. O **Host MCP**, e não o modelo diretamente, comunica-se com o(s) **Servidor(es) MCP** apropriado(s) usando o protocolo padronizado.
- **Funcionalidade do Host MCP**:
    - **Registo de Ferramentas**: Mantém um catálogo de ferramentas disponíveis e suas capacidades.
    - **Autenticação**: Verifica permissões para acesso às ferramentas.
    - **Gestor de Pedidos**: Processa pedidos de ferramentas recebidos do modelo.
    - **Formatador de Respostas**: Estrutura as saídas das ferramentas num formato compreensível pelo modelo.
- **Execução do Servidor MCP**:
    - O **Host MCP** encaminha chamadas de ferramentas para um ou mais **Servidores MCP**, cada um expondo funções especializadas (por exemplo, pesquisa, cálculos, consultas a bases de dados).
    - Os **Servidores MCP** realizam as suas operações e devolvem os resultados ao **Host MCP** num formato consistente.
    - O **Host MCP** formata e retransmite esses resultados para o **Modelo de IA**.
- **Conclusão da Resposta**:
    - O **Modelo de IA** incorpora as saídas das ferramentas numa resposta final.
    - O **Host MCP** envia esta resposta de volta ao **Cliente MCP**, que a entrega ao utilizador final ou software chamador.

```mermaid
---
title: MCP Architecture and Component Interactions
description: A diagram showing the flows of the components in MCP.
---
graph TD
    Client[MCP Client/Application] -->|Sends Request| H[MCP Host]
    H -->|Invokes| A[AI Model]
    A -->|Tool Call Request| H
    H -->|MCP Protocol| T1[MCP Server Tool 01: Web Search]
    H -->|MCP Protocol| T2[MCP Server Tool 02: Calculator tool]
    H -->|MCP Protocol| T3[MCP Server Tool 03: Database Access tool]
    H -->|MCP Protocol| T4[MCP Server Tool 04: File System tool]
    H -->|Sends Response| Client

    subgraph "MCP Host Components"
        H
        G[Tool Registry]
        I[Authentication]
        J[Request Handler]
        K[Response Formatter]
    end

    H <--> G
    H <--> I
    H <--> J
    H <--> K

    style A fill:#f9d5e5,stroke:#333,stroke-width:2px
    style H fill:#eeeeee,stroke:#333,stroke-width:2px
    style Client fill:#d5e8f9,stroke:#333,stroke-width:2px
    style G fill:#fffbe6,stroke:#333,stroke-width:1px
    style I fill:#fffbe6,stroke:#333,stroke-width:1px
    style J fill:#fffbe6,stroke:#333,stroke-width:1px
    style K fill:#fffbe6,stroke:#333,stroke-width:1px
    style T1 fill:#c2f0c2,stroke:#333,stroke-width:1px
    style T2 fill:#c2f0c2,stroke:#333,stroke-width:1px
    style T3 fill:#c2f0c2,stroke:#333,stroke-width:1px
    style T4 fill:#c2f0c2,stroke:#333,stroke-width:1px
```

## 👨‍💻 Como Construir um Servidor MCP (Com Exemplos)

Os servidores MCP permitem estender as capacidades dos LLMs fornecendo dados e funcionalidades.

Pronto para experimentar? Aqui estão SDKs específicos para linguagens e/ou stacks com exemplos de criação de servidores MCP simples em diferentes linguagens/stacks:

- **Python SDK**: https://github.com/modelcontextprotocol/python-sdk

- **TypeScript SDK**: https://github.com/modelcontextprotocol/typescript-sdk

- **Java SDK**: https://github.com/modelcontextprotocol/java-sdk

- **C#/.NET SDK**: https://github.com/modelcontextprotocol/csharp-sdk

---

## 🌍 Casos de Uso Reais para o MCP

O MCP possibilita uma ampla gama de aplicações ao estender as capacidades da IA:

| **Aplicação**               | **Descrição**                                                                |
|-----------------------------|------------------------------------------------------------------------------|
| Integração de Dados Empresariais | Conectar LLMs a bases de dados, CRMs ou ferramentas internas               |
| Sistemas de IA Agentes      | Permitir agentes autónomos com acesso a ferramentas e fluxos de decisão      |
| Aplicações Multimodais      | Combinar ferramentas de texto, imagem e áudio numa única aplicação de IA     |
| Integração de Dados em Tempo Real | Incorporar dados ao vivo nas interações de IA para resultados mais precisos e atuais |

---

### 🧠 MCP = Padrão Universal para Interações de IA

O Protocolo de Contexto de Modelo (MCP) atua como um padrão universal para interações de IA, assim como o USB-C padronizou conexões físicas para dispositivos. No mundo da IA, o MCP fornece uma interface consistente, permitindo que modelos (clientes) integrem-se perfeitamente com ferramentas externas e fornecedores de dados (servidores). Isso elimina a necessidade de protocolos personalizados e diversos para cada API ou fonte de dados.

Sob o MCP, uma ferramenta compatível com MCP (referida como servidor MCP) segue um padrão unificado. Esses servidores podem listar as ferramentas ou ações que oferecem e executar essas ações quando solicitados por um agente de IA. Plataformas de agentes de IA que suportam MCP são capazes de descobrir ferramentas disponíveis nos servidores e invocá-las através deste protocolo padrão.

---

### 💡 Facilita o acesso ao conhecimento

Além de oferecer ferramentas, o MCP também facilita o acesso ao conhecimento. Ele permite que aplicações forneçam contexto a modelos de linguagem de grande escala (LLMs) ao conectá-los a várias fontes de dados. Por exemplo, um servidor MCP pode representar o repositório de documentos de uma empresa, permitindo que agentes recuperem informações relevantes sob demanda. Outro servidor pode lidar com ações específicas, como enviar e-mails ou atualizar registos. Do ponto de vista do agente, estas são simplesmente ferramentas que ele pode usar—algumas ferramentas retornam dados (contexto de conhecimento), enquanto outras executam ações. O MCP gere ambos de forma eficiente.

Um agente que se conecta a um servidor MCP aprende automaticamente as capacidades disponíveis e os dados acessíveis do servidor através de um formato padrão. Essa padronização permite a disponibilidade dinâmica de ferramentas. Por exemplo, adicionar um novo servidor MCP ao sistema de um agente torna as suas funções imediatamente utilizáveis, sem necessidade de personalização adicional das instruções do agente.

Essa integração simplificada alinha-se com o fluxo representado no diagrama a seguir, onde os servidores fornecem tanto ferramentas quanto conhecimento, garantindo colaboração fluida entre sistemas.

---

### 👉 Exemplo: Solução de Agente Escalável

```mermaid
---
title: Scalable Agent Solution with MCP
description: A diagram illustrating how a user interacts with an LLM that connects to multiple MCP servers, with each server providing both knowledge and tools, creating a scalable AI system architecture
---
graph TD
    User -->|Prompt| LLM
    LLM -->|Response| User
    LLM -->|MCP| ServerA
    LLM -->|MCP| ServerB
    ServerA -->|Universal connector| ServerB
    ServerA --> KnowledgeA
    ServerA --> ToolsA
    ServerB --> KnowledgeB
    ServerB --> ToolsB

    subgraph Server A
        KnowledgeA[Knowledge]
        ToolsA[Tools]
    end

    subgraph Server B
        KnowledgeB[Knowledge]
        ToolsB[Tools]
    end
```

---

### 🔄 Cenários Avançados de MCP com Integração de LLM no Lado do Cliente

Além da arquitetura básica do MCP, existem cenários avançados onde tanto o cliente quanto o servidor contêm LLMs, permitindo interações mais sofisticadas. No diagrama a seguir, a **Aplicação Cliente** pode ser um IDE com várias ferramentas MCP disponíveis para uso pelo LLM:

```mermaid
---
title: Advanced MCP Scenarios with Client-Server LLM Integration
description: A sequence diagram showing the detailed interaction flow between user, client application, client LLM, multiple MCP servers, and server LLM, illustrating tool discovery, user interaction, direct tool calling, and feature negotiation phases
---
sequenceDiagram
    autonumber
    actor User as 👤 User
    participant ClientApp as 🖥️ Client App
    participant ClientLLM as 🧠 Client LLM
    participant Server1 as 🔧 MCP Server 1
    participant Server2 as 📚 MCP Server 2
    participant ServerLLM as 🤖 Server LLM
    
    %% Discovery Phase
    rect rgb(220, 240, 255)
        Note over ClientApp, Server2: TOOL DISCOVERY PHASE
        ClientApp->>+Server1: Request available tools/resources
        Server1-->>-ClientApp: Return tool list (JSON)
        ClientApp->>+Server2: Request available tools/resources
        Server2-->>-ClientApp: Return tool list (JSON)
        Note right of ClientApp: Store combined tool<br/>catalog locally
    end
    
    %% User Interaction
    rect rgb(255, 240, 220)
        Note over User, ClientLLM: USER INTERACTION PHASE
        User->>+ClientApp: Enter natural language prompt
        ClientApp->>+ClientLLM: Forward prompt + tool catalog
        ClientLLM->>-ClientLLM: Analyze prompt & select tools
    end
    
    %% Scenario A: Direct Tool Calling
    alt Direct Tool Calling
        rect rgb(220, 255, 220)
            Note over ClientApp, Server1: SCENARIO A: DIRECT TOOL CALLING
            ClientLLM->>+ClientApp: Request tool execution
            ClientApp->>+Server1: Execute specific tool
            Server1-->>-ClientApp: Return results
            ClientApp->>+ClientLLM: Process results
            ClientLLM-->>-ClientApp: Generate response
            ClientApp-->>-User: Display final answer
        end
    
    %% Scenario B: Feature Negotiation (VS Code style)
    else Feature Negotiation (VS Code style)
        rect rgb(255, 220, 220)
            Note over ClientApp, ServerLLM: SCENARIO B: FEATURE NEGOTIATION
            ClientLLM->>+ClientApp: Identify needed capabilities
            ClientApp->>+Server2: Negotiate features/capabilities
            Server2->>+ServerLLM: Request additional context
            ServerLLM-->>-Server2: Provide context
            Server2-->>-ClientApp: Return available features
            ClientApp->>+Server2: Call negotiated tools
            Server2-->>-ClientApp: Return results
            ClientApp->>+ClientLLM: Process results
            ClientLLM-->>-ClientApp: Generate response
            ClientApp-->>-User: Display final answer
        end
    end
```

---

## 🔐 Benefícios Práticos do MCP

Aqui estão os benefícios práticos de usar o MCP:

- **Atualidade**: Os modelos podem acessar informações atualizadas além dos seus dados de treino
- **Extensão de Capacidades**: Os modelos podem utilizar ferramentas especializadas para tarefas para as quais não foram treinados
- **Redução de Alucinações**: Fontes de dados externas fornecem uma base factual
- **Privacidade**: Dados sensíveis podem permanecer em ambientes seguros em vez de serem incorporados em prompts

---

## 📌 Principais Conclusões

As seguintes são as principais conclusões sobre o uso do MCP:

- O **MCP** padroniza como os modelos de IA interagem com ferramentas e dados
- Promove **extensibilidade, consistência e interoperabilidade**
- O MCP ajuda a **reduzir o tempo de desenvolvimento, melhorar a fiabilidade e ampliar as capacidades dos modelos**
- A arquitetura cliente-servidor **permite aplicações de IA flexíveis e extensíveis**

---

## 🧠 Exercício

Pense numa aplicação de IA que gostaria de construir.

- Quais **ferramentas ou dados externos** poderiam melhorar as suas capacidades?
- Como o MCP poderia tornar a integração **mais simples e fiável**?

---

## Recursos Adicionais

- [Repositório GitHub do MCP](https://github.com/modelcontextprotocol)

---

## O Que Vem a Seguir

Próximo: [Capítulo 1: Conceitos Fundamentais](../01-CoreConcepts/README.md)

**Aviso Legal**:  
Este documento foi traduzido utilizando o serviço de tradução por IA [Co-op Translator](https://github.com/Azure/co-op-translator). Embora nos esforcemos para garantir a precisão, esteja ciente de que traduções automáticas podem conter erros ou imprecisões. O documento original na sua língua nativa deve ser considerado a fonte oficial. Para informações críticas, recomenda-se uma tradução profissional realizada por humanos. Não nos responsabilizamos por quaisquer mal-entendidos ou interpretações incorretas resultantes do uso desta tradução.