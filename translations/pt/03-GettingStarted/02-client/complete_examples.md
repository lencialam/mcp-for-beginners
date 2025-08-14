<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "8358c13b5b6877e475674697cdc1a904",
  "translation_date": "2025-08-11T10:51:16+00:00",
  "source_file": "03-GettingStarted/02-client/complete_examples.md",
  "language_code": "pt"
}
-->
# Exemplos Completos de Clientes MCP

Este diretório contém exemplos completos e funcionais de clientes MCP em diferentes linguagens de programação. Cada cliente demonstra toda a funcionalidade descrita no tutorial principal README.md.

## Clientes Disponíveis

### 1. Cliente Java (`client_example_java.java`)

- **Transporte**: SSE (Server-Sent Events) via HTTP
- **Servidor Alvo**: `http://localhost:8080`
- **Funcionalidades**:
  - Estabelecimento de conexão e ping
  - Listagem de ferramentas
  - Operações de calculadora (somar, subtrair, multiplicar, dividir, ajuda)
  - Tratamento de erros e extração de resultados

**Para executar:**

```bash
# Ensure your MCP server is running on localhost:8080
javac client_example_java.java
java client_example_java
```

### 2. Cliente C# (`client_example_csharp.cs`)

- **Transporte**: Stdio (Entrada/Saída Padrão)
- **Servidor Alvo**: Servidor MCP local .NET via dotnet run
- **Funcionalidades**:
  - Inicialização automática do servidor via transporte stdio
  - Listagem de ferramentas e recursos
  - Operações de calculadora
  - Análise de resultados em JSON
  - Tratamento de erros abrangente

**Para executar:**

```bash
dotnet run
```

### 3. Cliente TypeScript (`client_example_typescript.ts`)

- **Transporte**: Stdio (Entrada/Saída Padrão)
- **Servidor Alvo**: Servidor MCP local Node.js
- **Funcionalidades**:
  - Suporte completo ao protocolo MCP
  - Operações com ferramentas, recursos e prompts
  - Operações de calculadora
  - Leitura de recursos e execução de prompts
  - Tratamento robusto de erros

**Para executar:**

```bash
# First compile TypeScript (if needed)
npm run build

# Then run the client
npm run client
# or
node client_example_typescript.js
```

### 4. Cliente Python (`client_example_python.py`)

- **Transporte**: Stdio (Entrada/Saída Padrão)  
- **Servidor Alvo**: Servidor MCP local Python
- **Funcionalidades**:
  - Padrão async/await para operações
  - Descoberta de ferramentas e recursos
  - Teste de operações de calculadora
  - Leitura de conteúdo de recursos
  - Organização baseada em classes

**Para executar:**

```bash
python client_example_python.py
```

## Funcionalidades Comuns Entre Todos os Clientes

Cada implementação de cliente demonstra:

1. **Gestão de Conexão**
   - Estabelecimento de conexão com o servidor MCP
   - Tratamento de erros de conexão
   - Limpeza adequada e gestão de recursos

2. **Descoberta do Servidor**
   - Listagem de ferramentas disponíveis
   - Listagem de recursos disponíveis (quando suportado)
   - Listagem de prompts disponíveis (quando suportado)

3. **Invocação de Ferramentas**
   - Operações básicas de calculadora (somar, subtrair, multiplicar, dividir)
   - Comando de ajuda para informações do servidor
   - Passagem adequada de argumentos e tratamento de resultados

4. **Tratamento de Erros**
   - Erros de conexão
   - Erros na execução de ferramentas
   - Falhas controladas e feedback ao utilizador

5. **Processamento de Resultados**
   - Extração de conteúdo textual das respostas
   - Formatação de saída para melhor legibilidade
   - Tratamento de diferentes formatos de resposta

## Pré-requisitos

Antes de executar estes clientes, certifique-se de que:

1. **O servidor MCP correspondente está em execução** (a partir de `../01-first-server/`)
2. **As dependências necessárias estão instaladas** para a linguagem escolhida
3. **A conectividade de rede está adequada** (para transportes baseados em HTTP)

## Diferenças Principais Entre Implementações

| Linguagem   | Transporte | Inicialização do Servidor | Modelo Assíncrono | Bibliotecas Principais |
|-------------|------------|---------------------------|--------------------|-------------------------|
| Java        | SSE/HTTP   | Externo                  | Sincrono           | WebFlux, MCP SDK        |
| C#          | Stdio      | Automática               | Async/Await        | .NET MCP SDK            |
| TypeScript  | Stdio      | Automática               | Async/Await        | Node MCP SDK            |
| Python      | Stdio      | Automática               | AsyncIO            | Python MCP SDK          |
| Rust        | Stdio      | Automática               | Async/Await        | Rust MCP SDK, Tokio     |

## Próximos Passos

Após explorar estes exemplos de clientes:

1. **Modifique os clientes** para adicionar novas funcionalidades ou operações
2. **Crie o seu próprio servidor** e teste-o com estes clientes
3. **Experimente diferentes transportes** (SSE vs. Stdio)
4. **Construa uma aplicação mais complexa** que integre a funcionalidade MCP

## Resolução de Problemas

### Problemas Comuns

1. **Conexão recusada**: Certifique-se de que o servidor MCP está em execução na porta/caminho esperado
2. **Módulo não encontrado**: Instale o MCP SDK necessário para a sua linguagem
3. **Permissão negada**: Verifique as permissões de ficheiros para o transporte stdio
4. **Ferramenta não encontrada**: Confirme que o servidor implementa as ferramentas esperadas

### Dicas de Depuração

1. **Ative o registo detalhado** no seu MCP SDK
2. **Verifique os registos do servidor** para mensagens de erro
3. **Confirme os nomes e assinaturas das ferramentas** entre cliente e servidor
4. **Teste primeiro com o MCP Inspector** para validar a funcionalidade do servidor

## Documentação Relacionada

- [Tutorial Principal de Cliente](./README.md)
- [Exemplos de Servidor MCP](../../../../03-GettingStarted/01-first-server)
- [MCP com Integração LLM](../../../../03-GettingStarted/03-llm-client)
- [Documentação Oficial MCP](https://modelcontextprotocol.io/)

**Aviso Legal**:  
Este documento foi traduzido utilizando o serviço de tradução por IA [Co-op Translator](https://github.com/Azure/co-op-translator). Embora nos esforcemos para garantir a precisão, esteja ciente de que traduções automáticas podem conter erros ou imprecisões. O documento original no seu idioma nativo deve ser considerado a fonte oficial. Para informações críticas, recomenda-se uma tradução profissional realizada por humanos. Não nos responsabilizamos por quaisquer mal-entendidos ou interpretações incorretas resultantes do uso desta tradução.