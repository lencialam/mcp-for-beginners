<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "2e782fc6226cf5e2b5625b035d35e60a",
  "translation_date": "2025-08-11T10:45:42+00:00",
  "source_file": "02-Security/README.md",
  "language_code": "pt"
}
-->
# Melhores Práticas de Segurança

[![Melhores Práticas de Segurança do MCP](../../../translated_images/03.175aed6dedae133f9d41e49cefd0f0a9a39c3317e1eaa7ef7182696af7534308.pt.png)](https://youtu.be/88No8pw706o)

_(Clique na imagem acima para assistir ao vídeo desta lição)_

Como a segurança é um aspecto tão importante, damos prioridade a ela como nossa segunda seção. Isso está alinhado com o princípio **Seguro por Design** da [Iniciativa de Futuro Seguro](https://www.microsoft.com/en-us/security/blog/2025/04/17/microsofts-secure-by-design-journey-one-year-of-success/) da Microsoft.

A adoção do Model Context Protocol (MCP) traz novas capacidades poderosas para aplicações baseadas em IA, mas também introduz desafios de segurança únicos que vão além dos riscos tradicionais de software. Além de preocupações já conhecidas, como codificação segura, privilégio mínimo e segurança da cadeia de fornecimento, o MCP e as cargas de trabalho de IA enfrentam novas ameaças, como injeção de prompts, envenenamento de ferramentas, modificação dinâmica de ferramentas, sequestro de sessões, ataques de delegado confuso e vulnerabilidades de passagem de tokens. Esses riscos podem levar à exfiltração de dados, violações de privacidade e comportamentos inesperados do sistema, se não forem geridos adequadamente.

Esta lição explora os riscos de segurança mais relevantes associados ao MCP—including autenticação, autorização, permissões excessivas, injeção indireta de prompts, segurança de sessões, problemas de delegado confuso, vulnerabilidades de passagem de tokens e vulnerabilidades da cadeia de fornecimento—e fornece controles práticos e melhores práticas para mitigá-los. Você também aprenderá a aproveitar soluções da Microsoft, como Prompt Shields, Azure Content Safety e GitHub Advanced Security, para fortalecer sua implementação do MCP. Ao compreender e aplicar esses controles, você pode reduzir significativamente a probabilidade de uma violação de segurança e garantir que seus sistemas de IA permaneçam robustos e confiáveis.

# Objetivos de Aprendizagem

Ao final desta lição, você será capaz de:

- Identificar e explicar os riscos de segurança únicos introduzidos pelo Model Context Protocol (MCP), incluindo injeção de prompts, envenenamento de ferramentas, permissões excessivas, sequestro de sessões, problemas de delegado confuso, vulnerabilidades de passagem de tokens e vulnerabilidades da cadeia de fornecimento.
- Descrever e aplicar controles eficazes para mitigar os riscos de segurança do MCP, como autenticação robusta, privilégio mínimo, gestão segura de tokens, controles de segurança de sessões e verificação da cadeia de fornecimento.
- Compreender e utilizar soluções da Microsoft, como Prompt Shields, Azure Content Safety e GitHub Advanced Security, para proteger cargas de trabalho do MCP e de IA.
- Reconhecer a importância de validar metadados de ferramentas, monitorar mudanças dinâmicas, defender-se contra ataques de injeção indireta de prompts e prevenir o sequestro de sessões.
- Integrar melhores práticas de segurança estabelecidas—como codificação segura, fortalecimento de servidores e arquitetura de confiança zero—na sua implementação do MCP para reduzir a probabilidade e o impacto de violações de segurança.

# Controles de segurança do MCP

Qualquer sistema que tenha acesso a recursos importantes enfrenta desafios de segurança implícitos. Esses desafios geralmente podem ser resolvidos por meio da aplicação correta de controles e conceitos fundamentais de segurança. Como o MCP foi definido recentemente, sua especificação está evoluindo rapidamente. Eventualmente, os controles de segurança dentro dele amadurecerão, permitindo uma melhor integração com arquiteturas de segurança empresariais e melhores práticas estabelecidas.

Pesquisas publicadas no [Relatório de Defesa Digital da Microsoft](https://aka.ms/mddr) afirmam que 98% das violações relatadas poderiam ser evitadas com uma higiene de segurança robusta. A melhor proteção contra qualquer tipo de violação é garantir uma higiene de segurança básica, práticas de codificação segura e segurança da cadeia de fornecimento adequadas—essas práticas já testadas continuam sendo as mais impactantes na redução de riscos de segurança.

Vamos analisar algumas maneiras de começar a abordar os riscos de segurança ao adotar o MCP.

> **Nota:** As informações a seguir estão corretas até **29 de maio de 2025**. O protocolo MCP está em constante evolução, e implementações futuras podem introduzir novos padrões e controles de autenticação. Para as atualizações e orientações mais recentes, consulte sempre a [Especificação do MCP](https://spec.modelcontextprotocol.io/), o repositório oficial do [MCP no GitHub](https://github.com/modelcontextprotocol) e a [página de melhores práticas de segurança](https://modelcontextprotocol.io/specification/draft/basic/security_best_practices).

### Declaração do problema 
A especificação original do MCP assumia que os desenvolvedores criariam seu próprio servidor de autenticação. Isso exigia conhecimento de OAuth e restrições de segurança relacionadas. Os servidores MCP atuavam como Servidores de Autorização OAuth 2.0, gerenciando diretamente a autenticação do usuário necessária, em vez de delegá-la a um serviço externo, como o Microsoft Entra ID. A partir de **26 de abril de 2025**, uma atualização na especificação do MCP permite que os servidores MCP deleguem a autenticação do usuário a um serviço externo.

### Riscos
- A lógica de autorização mal configurada no servidor MCP pode levar à exposição de dados sensíveis e à aplicação incorreta de controles de acesso.
- Roubo de tokens OAuth no servidor MCP local. Se roubado, o token pode ser usado para se passar pelo servidor MCP e acessar recursos e dados do serviço para o qual o token OAuth foi emitido.

#### Passagem de Tokens
A passagem de tokens é explicitamente proibida na especificação de autorização, pois introduz vários riscos de segurança, incluindo:

#### Circunvenção de Controles de Segurança
O servidor MCP ou APIs a jusante podem implementar controles de segurança importantes, como limitação de taxa, validação de solicitações ou monitoramento de tráfego, que dependem do público do token ou de outras restrições de credenciais. Se os clientes puderem obter e usar tokens diretamente com as APIs a jusante sem que o servidor MCP os valide adequadamente ou garanta que os tokens foram emitidos para o serviço correto, esses controles são contornados.

#### Problemas de Responsabilidade e Trilhas de Auditoria
O servidor MCP não será capaz de identificar ou distinguir entre clientes MCP quando estes estiverem chamando com um token de acesso emitido a montante, que pode ser opaco para o servidor MCP.  
Os logs do servidor de recursos a jusante podem mostrar solicitações que parecem vir de uma fonte diferente, com uma identidade diferente, em vez do servidor MCP que está realmente encaminhando os tokens.  
Ambos os fatores dificultam a investigação de incidentes, os controles e a auditoria.  
Se o servidor MCP passar tokens sem validar suas declarações (por exemplo, funções, privilégios ou público) ou outros metadados, um ator malicioso em posse de um token roubado pode usar o servidor como um proxy para exfiltração de dados.

#### Problemas de Limites de Confiança
O servidor de recursos a jusante concede confiança a entidades específicas. Essa confiança pode incluir suposições sobre a origem ou padrões de comportamento do cliente. Romper esse limite de confiança pode levar a problemas inesperados.  
Se o token for aceito por vários serviços sem validação adequada, um invasor que comprometer um serviço pode usar o token para acessar outros serviços conectados.

#### Risco de Compatibilidade Futura
Mesmo que um servidor MCP comece como um "proxy puro" hoje, ele pode precisar adicionar controles de segurança mais tarde. Começar com uma separação adequada do público do token facilita a evolução do modelo de segurança.

### Controles de mitigação

**Servidores MCP NÃO DEVEM aceitar tokens que não tenham sido explicitamente emitidos para o servidor MCP**

- **Revisar e Fortalecer a Lógica de Autorização:** Audite cuidadosamente a implementação de autorização do servidor MCP para garantir que apenas usuários e clientes pretendidos possam acessar recursos sensíveis. Para orientações práticas, veja [Azure API Management Your Auth Gateway For MCP Servers | Microsoft Community Hub](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690) e [Using Microsoft Entra ID To Authenticate With MCP Servers Via Sessions - Den Delimarsky](https://den.dev/blog/mcp-server-auth-entra-id-session/).  
- **Aplicar Práticas Seguras de Tokens:** Siga as [melhores práticas da Microsoft para validação e duração de tokens](https://learn.microsoft.com/en-us/entra/identity-platform/access-tokens) para evitar o uso indevido de tokens de acesso e reduzir o risco de reprodução ou roubo de tokens.  
- **Proteger o Armazenamento de Tokens:** Sempre armazene tokens de forma segura e use criptografia para protegê-los em repouso e em trânsito. Para dicas de implementação, veja [Use secure token storage and encrypt tokens](https://youtu.be/uRdX37EcCwg?si=6fSChs1G4glwXRy2).

# Permissões excessivas para servidores MCP

### Declaração do problema
Servidores MCP podem ter recebido permissões excessivas para o serviço/recurso ao qual estão acessando. Por exemplo, um servidor MCP que faz parte de uma aplicação de vendas baseada em IA conectando-se a um repositório de dados empresarial deve ter acesso limitado aos dados de vendas e não deve ter permissão para acessar todos os arquivos do repositório. Referindo-se ao princípio do privilégio mínimo (um dos princípios de segurança mais antigos), nenhum recurso deve ter permissões além do necessário para executar as tarefas para as quais foi projetado. A IA apresenta um desafio adicional nesse espaço, pois, para permitir flexibilidade, pode ser difícil definir as permissões exatas necessárias.

### Riscos 
- Conceder permissões excessivas pode permitir a exfiltração ou modificação de dados que o servidor MCP não deveria acessar. Isso também pode ser um problema de privacidade se os dados forem informações pessoalmente identificáveis (PII).

### Controles de mitigação
- **Aplicar o Princípio do Privilégio Mínimo:** Conceda ao servidor MCP apenas as permissões mínimas necessárias para realizar suas tarefas. Revise e atualize essas permissões regularmente para garantir que não excedam o necessário. Para orientações detalhadas, veja [Secure least-privileged access](https://learn.microsoft.com/entra/identity-platform/secure-least-privileged-access).  
- **Usar Controle de Acesso Baseado em Funções (RBAC):** Atribua funções ao servidor MCP que sejam estritamente limitadas a recursos e ações específicas, evitando permissões amplas ou desnecessárias.  
- **Monitorar e Auditar Permissões:** Monitore continuamente o uso de permissões e audite os logs de acesso para detectar e corrigir privilégios excessivos ou não utilizados prontamente.

# Ataques de injeção indireta de prompts

### Declaração do problema

Servidores MCP maliciosos ou comprometidos podem introduzir riscos significativos ao expor dados de clientes ou permitir ações não intencionais. Esses riscos são especialmente relevantes em cargas de trabalho baseadas em IA e MCP, onde:

- **Ataques de Injeção de Prompts:** Atacantes inserem instruções maliciosas em prompts ou conteúdos externos, fazendo com que o sistema de IA execute ações não intencionais ou vaze dados sensíveis. Saiba mais: [Prompt Injection](https://simonwillison.net/2025/Apr/9/mcp-prompt-injection/)  
- **Envenenamento de Ferramentas:** Atacantes manipulam metadados de ferramentas (como descrições ou parâmetros) para influenciar o comportamento da IA, potencialmente contornando controles de segurança ou exfiltrando dados. Detalhes: [Tool Poisoning](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks)  
- **Injeção de Prompts entre Domínios:** Instruções maliciosas são inseridas em documentos, páginas web ou e-mails, que são então processados pela IA, levando a vazamentos de dados ou manipulação.  
- **Modificação Dinâmica de Ferramentas (Rug Pulls):** Definições de ferramentas podem ser alteradas após a aprovação do usuário, introduzindo novos comportamentos maliciosos sem o conhecimento do usuário.

Essas vulnerabilidades destacam a necessidade de validação robusta, monitoramento e controles de segurança ao integrar servidores MCP e ferramentas no seu ambiente. Para uma análise mais aprofundada, veja os links acima.

![prompt-injection-lg-2048x1034](../../../translated_images/prompt-injection.ed9fbfde297ca877c15bc6daa808681cd3c3dc7bf27bbbda342ef1ba5fc4f52d.pt.png)

**Injeção Indireta de Prompts** (também conhecida como injeção de prompts entre domínios ou XPIA) é uma vulnerabilidade crítica em sistemas de IA generativa, incluindo aqueles que utilizam o Model Context Protocol (MCP). Nesse ataque, instruções maliciosas são ocultadas em conteúdos externos—como documentos, páginas web ou e-mails. Quando o sistema de IA processa esse conteúdo, ele pode interpretar as instruções embutidas como comandos legítimos do usuário, resultando em ações não intencionais, como vazamento de dados, geração de conteúdo prejudicial ou manipulação de interações do usuário. Para uma explicação detalhada e exemplos do mundo real, veja [Prompt Injection](https://simonwillison.net/2025/Apr/9/mcp-prompt-injection/).

Uma forma particularmente perigosa desse ataque é o **Envenenamento de Ferramentas**. Aqui, os atacantes inserem instruções maliciosas nos metadados das ferramentas do MCP (como descrições ou parâmetros das ferramentas). Como os modelos de linguagem (LLMs) dependem desses metadados para decidir quais ferramentas invocar, descrições comprometidas podem enganar o modelo para executar chamadas de ferramentas não autorizadas ou contornar controles de segurança. Essas manipulações geralmente são invisíveis para os usuários finais, mas podem ser interpretadas e executadas pelo sistema de IA. Esse risco é ainda maior em ambientes de servidores MCP hospedados, onde as definições de ferramentas podem ser atualizadas após a aprovação do usuário—um cenário às vezes chamado de "[rug pull](https://www.wiz.io/blog/mcp-security-research-briefing#remote-servers-22)". Nesses casos, uma ferramenta que era anteriormente segura pode ser modificada posteriormente para realizar ações maliciosas, como exfiltrar dados ou alterar o comportamento do sistema, sem o conhecimento do usuário. Para mais informações sobre esse vetor de ataque, veja [Tool Poisoning](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks).

![tool-injection-lg-2048x1239 (1)](../../../translated_images/tool-injection.3b0b4a6b24de6befe7d3afdeae44138ef005881aebcfc84c6f61369ce31e3640.pt.png)

## Riscos
Ações não intencionais da IA apresentam uma variedade de riscos de segurança, incluindo exfiltração de dados e violações de privacidade.

### Controles de mitigação
### Usando Prompt Shields para proteger contra ataques de Injeção Indireta de Prompts
-----------------------------------------------------------------------------

**Prompt Shields de IA** são uma solução desenvolvida pela Microsoft para defender contra ataques de injeção de prompts, tanto diretos quanto indiretos. Eles ajudam por meio de:

1.  **Detecção e Filtragem:** Os Prompt Shields utilizam algoritmos avançados de machine learning e processamento de linguagem natural para detectar e filtrar instruções maliciosas embutidas em conteúdos externos, como documentos, páginas web ou e-mails.
    
2.  **Spotlighting:** Essa técnica ajuda o sistema de IA a distinguir entre instruções válidas do sistema e entradas externas potencialmente não confiáveis. Ao transformar o texto de entrada de uma forma que o torne mais relevante para o modelo, o Spotlighting garante que a IA possa identificar e ignorar melhor instruções maliciosas.
    
3.  **Delimitadores e Marcação de Dados:** A inclusão de delimitadores na mensagem do sistema delineia explicitamente a localização do texto de entrada, ajudando o sistema de IA a reconhecer e separar entradas do usuário de conteúdos externos potencialmente prejudiciais. A marcação de dados estende esse conceito ao usar marcadores especiais para destacar os limites entre dados confiáveis e não confiáveis.
    
4.  **Monitoramento Contínuo e Atualizações:** A Microsoft monitora e atualiza continuamente os Prompt Shields para lidar com ameaças novas e em evolução. Essa abordagem proativa garante que as defesas permaneçam eficazes contra as técnicas de ataque mais recentes.
5. **Integração com o Azure Content Safety:** Os Prompt Shields fazem parte do conjunto mais amplo do Azure AI Content Safety, que oferece ferramentas adicionais para detectar tentativas de jailbreak, conteúdos prejudiciais e outros riscos de segurança em aplicações de IA.

Pode ler mais sobre os Prompt Shields na [documentação de Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection).

![prompt-shield-lg-2048x1328](../../../translated_images/prompt-shield.ff5b95be76e9c78c6ec0888206a4a6a0a5ab4bb787832a9eceef7a62fe0138d1.pt.png)


# Problema do Confused Deputy

### Declaração do problema

O problema do confused deputy é uma vulnerabilidade de segurança que ocorre quando um servidor MCP atua como um proxy entre clientes MCP e APIs de terceiros. Esta vulnerabilidade pode ser explorada quando o servidor MCP utiliza um ID de cliente estático para autenticar-se com um servidor de autorização de terceiros que não suporta registo dinâmico de clientes.

### Riscos

- **Bypass de consentimento baseado em cookies**: Se um utilizador já tiver autenticado através do servidor proxy MCP, um servidor de autorização de terceiros pode definir um cookie de consentimento no navegador do utilizador. Um atacante pode explorar isso enviando ao utilizador um link malicioso com um pedido de autorização manipulado contendo um URI de redirecionamento malicioso.
- **Roubo de código de autorização**: Quando o utilizador clica no link malicioso, o servidor de autorização de terceiros pode ignorar o ecrã de consentimento devido ao cookie existente, e o código de autorização pode ser redirecionado para o servidor do atacante.
- **Acesso não autorizado à API**: O atacante pode trocar o código de autorização roubado por tokens de acesso e personificar o utilizador para aceder à API de terceiros sem aprovação explícita.

### Controles de mitigação

- **Requisitos de consentimento explícito**: Servidores proxy MCP que utilizam IDs de cliente estáticos **DEVEM** obter o consentimento do utilizador para cada cliente registado dinamicamente antes de encaminhar para servidores de autorização de terceiros.
- **Implementação adequada do OAuth**: Siga as melhores práticas de segurança do OAuth 2.1, incluindo o uso de desafios de código (PKCE) para pedidos de autorização, a fim de prevenir ataques de interceção.
- **Validação de clientes**: Implemente validações rigorosas de URIs de redirecionamento e identificadores de cliente para evitar exploração por atores maliciosos.


# Vulnerabilidades de Token Passthrough

### Declaração do problema

"Token passthrough" é um antipadrão onde um servidor MCP aceita tokens de um cliente MCP sem validar se os tokens foram devidamente emitidos para o próprio servidor MCP, e depois "os encaminha" para APIs downstream. Esta prática viola explicitamente a especificação de autorização do MCP e introduz sérios riscos de segurança.

### Riscos

- **Circunvenção de controles de segurança**: Clientes podem contornar controles de segurança importantes, como limitação de taxa, validação de pedidos ou monitorização de tráfego, se puderem usar tokens diretamente com APIs downstream sem validação adequada.
- **Problemas de responsabilidade e auditoria**: O servidor MCP não conseguirá identificar ou distinguir entre clientes MCP quando estes utilizam tokens de acesso emitidos upstream, dificultando investigações de incidentes e auditorias.
- **Exfiltração de dados**: Se os tokens forem encaminhados sem validação adequada de claims, um ator malicioso com um token roubado pode usar o servidor como proxy para exfiltração de dados.
- **Violações de limites de confiança**: Servidores de recursos downstream podem conceder confiança a entidades específicas com base em suposições sobre origem ou padrões de comportamento. Quebrar este limite de confiança pode levar a problemas de segurança inesperados.
- **Uso indevido de tokens em múltiplos serviços**: Se tokens forem aceites por múltiplos serviços sem validação adequada, um atacante que comprometer um serviço pode usar o token para aceder a outros serviços conectados.

### Controles de mitigação

- **Validação de tokens**: Servidores MCP **NÃO DEVEM** aceitar tokens que não tenham sido explicitamente emitidos para o próprio servidor MCP.
- **Verificação de audiência**: Valide sempre que os tokens tenham o claim de audiência correto que corresponda à identidade do servidor MCP.
- **Gestão adequada do ciclo de vida dos tokens**: Implemente tokens de acesso de curta duração e práticas adequadas de rotação de tokens para reduzir o risco de roubo e uso indevido de tokens.


# Sequestro de Sessão

### Declaração do problema

O sequestro de sessão é um vetor de ataque onde um cliente recebe um ID de sessão do servidor, e uma parte não autorizada obtém e utiliza esse mesmo ID de sessão para se fazer passar pelo cliente original e realizar ações não autorizadas em seu nome. Isto é particularmente preocupante em servidores HTTP com estado que lidam com pedidos MCP.

### Riscos

- **Injeção de prompts no sequestro de sessão**: Um atacante que obtenha um ID de sessão pode enviar eventos maliciosos para um servidor que partilha o estado da sessão com o servidor ao qual o cliente está conectado, potencialmente desencadeando ações prejudiciais ou acedendo a dados sensíveis.
- **Impersonação no sequestro de sessão**: Um atacante com um ID de sessão roubado pode fazer chamadas diretamente para o servidor MCP, contornando a autenticação e sendo tratado como o utilizador legítimo.
- **Streams recomeçáveis comprometidos**: Quando um servidor suporta redelivery/streams recomeçáveis, um atacante pode terminar um pedido prematuramente, levando a que seja retomado mais tarde pelo cliente original com conteúdo potencialmente malicioso.

### Controles de mitigação

- **Verificação de autorização**: Servidores MCP que implementam autorização **DEVEM** verificar todos os pedidos recebidos e **NÃO DEVEM** usar sessões para autenticação.
- **IDs de sessão seguros**: Servidores MCP **DEVEM** usar IDs de sessão seguros e não determinísticos gerados com geradores de números aleatórios seguros. Evite identificadores previsíveis ou sequenciais.
- **Vinculação de sessão ao utilizador**: Servidores MCP **DEVEM** vincular IDs de sessão a informações específicas do utilizador, combinando o ID de sessão com informações únicas do utilizador autorizado (como o seu ID interno) usando um formato como `<user_id>:<session_id>`.
- **Expiração de sessão**: Implemente expiração e rotação adequadas de sessões para limitar a janela de vulnerabilidade caso um ID de sessão seja comprometido.
- **Segurança no transporte**: Utilize sempre HTTPS para todas as comunicações para evitar a interceção de IDs de sessão.


# Segurança da Cadeia de Suprimentos

A segurança da cadeia de suprimentos continua a ser fundamental na era da IA, mas o âmbito do que constitui a sua cadeia de suprimentos expandiu-se. Para além dos pacotes de código tradicionais, deve agora verificar e monitorizar rigorosamente todos os componentes relacionados com IA, incluindo modelos base, serviços de embeddings, fornecedores de contexto e APIs de terceiros. Cada um destes pode introduzir vulnerabilidades ou riscos se não forem geridos adequadamente.

**Práticas-chave de segurança da cadeia de suprimentos para IA e MCP:**
- **Verifique todos os componentes antes da integração:** Isto inclui não apenas bibliotecas open-source, mas também modelos de IA, fontes de dados e APIs externas. Verifique sempre a proveniência, licenciamento e vulnerabilidades conhecidas.
- **Mantenha pipelines de implantação seguros:** Utilize pipelines CI/CD automatizados com varredura de segurança integrada para detetar problemas cedo. Certifique-se de que apenas artefatos confiáveis são implantados em produção.
- **Monitorize e audite continuamente:** Implemente monitorização contínua para todas as dependências, incluindo modelos e serviços de dados, para detetar novas vulnerabilidades ou ataques à cadeia de suprimentos.
- **Aplique o princípio do menor privilégio e controles de acesso:** Restrinja o acesso a modelos, dados e serviços apenas ao necessário para o funcionamento do servidor MCP.
- **Responda rapidamente a ameaças:** Tenha um processo em vigor para corrigir ou substituir componentes comprometidos e para rodar segredos ou credenciais caso seja detetada uma violação.

[GitHub Advanced Security](https://github.com/security/advanced-security) oferece recursos como varredura de segredos, varredura de dependências e análise CodeQL. Estas ferramentas integram-se com [Azure DevOps](https://azure.microsoft.com/en-us/products/devops) e [Azure Repos](https://azure.microsoft.com/en-us/products/devops/repos/) para ajudar as equipas a identificar e mitigar vulnerabilidades em componentes de código e da cadeia de suprimentos de IA.

A Microsoft também implementa práticas extensivas de segurança da cadeia de suprimentos internamente para todos os produtos. Saiba mais em [The Journey to Secure the Software Supply Chain at Microsoft](https://devblogs.microsoft.com/engineering-at-microsoft/the-journey-to-secure-the-software-supply-chain-at-microsoft/).


# Práticas de segurança estabelecidas que melhorarão a postura de segurança da sua implementação MCP

Qualquer implementação MCP herda a postura de segurança existente do ambiente da sua organização em que está construída, por isso, ao considerar a segurança do MCP como um componente dos seus sistemas de IA, recomenda-se que melhore a postura de segurança geral existente. Os seguintes controles de segurança estabelecidos são especialmente relevantes:

-   Melhores práticas de codificação segura na sua aplicação de IA - proteja contra [o OWASP Top 10](https://owasp.org/www-project-top-ten/), o [OWASP Top 10 para LLMs](https://genai.owasp.org/download/43299/?tmstv=1731900559), uso de cofres seguros para segredos e tokens, implementação de comunicações seguras de ponta a ponta entre todos os componentes da aplicação, etc.
-   Endurecimento do servidor - use MFA sempre que possível, mantenha os patches atualizados, integre o servidor com um fornecedor de identidade de terceiros para acesso, etc.
-   Mantenha dispositivos, infraestruturas e aplicações atualizados com patches
-   Monitorização de segurança - implemente registo e monitorização de uma aplicação de IA (incluindo os clientes/servidores MCP) e envie esses registos para um SIEM central para deteção de atividades anómalas
-   Arquitetura de confiança zero - isole componentes através de controles de rede e identidade de forma lógica para minimizar movimentos laterais caso uma aplicação de IA seja comprometida.

# Conclusões principais

- Os fundamentos de segurança continuam críticos: Codificação segura, menor privilégio, verificação da cadeia de suprimentos e monitorização contínua são essenciais para cargas de trabalho MCP e IA.
- MCP introduz novos riscos—como injeção de prompts, envenenamento de ferramentas, sequestro de sessão, problemas de confused deputy, vulnerabilidades de token passthrough e permissões excessivas—que requerem controles tradicionais e específicos para IA.
- Utilize práticas robustas de autenticação, autorização e gestão de tokens, aproveitando fornecedores de identidade externos como o Microsoft Entra ID sempre que possível.
- Proteja contra injeção indireta de prompts e envenenamento de ferramentas validando metadados de ferramentas, monitorizando alterações dinâmicas e utilizando soluções como o Microsoft Prompt Shields.
- Implemente gestão segura de sessões utilizando IDs de sessão não determinísticos, vinculando sessões a identidades de utilizadores e nunca utilizando sessões para autenticação.
- Previna ataques de confused deputy exigindo consentimento explícito do utilizador para cada cliente registado dinamicamente e implementando práticas adequadas de segurança OAuth.
- Evite vulnerabilidades de token passthrough garantindo que servidores MCP aceitam apenas tokens explicitamente emitidos para eles e validam adequadamente os claims dos tokens.
- Trate todos os componentes na sua cadeia de suprimentos de IA—including modelos, embeddings e fornecedores de contexto—com o mesmo rigor que dependências de código.
- Mantenha-se atualizado com as especificações MCP em evolução e contribua para a comunidade para ajudar a moldar padrões seguros.

# Recursos adicionais

## Recursos externos
- [Microsoft Digital Defense Report](https://aka.ms/mddr)
- [MCP Specification](https://spec.modelcontextprotocol.io/)
- [MCP Security Best Practices](https://modelcontextprotocol.io/specification/draft/basic/security_best_practices)
- [MCP Authorization Specification](https://modelcontextprotocol.io/specification/draft/basic/authorization)
- [OAuth 2.0 Security Best Practices (RFC 9700)](https://datatracker.ietf.org/doc/html/rfc9700)
- [Prompt Injection in MCP (Simon Willison)](https://simonwillison.net/2025/Apr/9/mcp-prompt-injection/)
- [Tool Poisoning Attacks (Invariant Labs)](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks)
- [Rug Pulls in MCP (Wiz Security)](https://www.wiz.io/blog/mcp-security-research-briefing#remote-servers-22)
- [Prompt Shields Documentation (Microsoft)](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP Top 10 for LLMs](https://genai.owasp.org/download/43299/?tmstv=1731900559)
- [GitHub Advanced Security](https://github.com/security/advanced-security)
- [Azure DevOps](https://azure.microsoft.com/products/devops)
- [Azure Repos](https://azure.microsoft.com/products/devops/repos/)
- [The Journey to Secure the Software Supply Chain at Microsoft](https://devblogs.microsoft.com/engineering-at-microsoft/the-journey-to-secure-the-software-supply-chain-at-microsoft/)
- [Secure Least-Privileged Access (Microsoft)](https://learn.microsoft.com/entra/identity-platform/secure-least-privileged-access)
- [Best Practices for Token Validation and Lifetime](https://learn.microsoft.com/entra/identity-platform/access-tokens)
- [Use Secure Token Storage and Encrypt Tokens (YouTube)](https://youtu.be/uRdX37EcCwg?si=6fSChs1G4glwXRy2)
- [Azure API Management as Auth Gateway for MCP](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690)
- [Using Microsoft Entra ID to Authenticate with MCP Servers](https://den.dev/blog/mcp-server-auth-entra-id-session/)

## Documentos adicionais de segurança

Para orientações de segurança mais detalhadas, consulte os seguintes documentos:

- [MCP Security Best Practices 2025](./mcp-security-best-practices-2025.md) - Lista abrangente de melhores práticas de segurança para implementações MCP
- [Azure Content Safety Implementation](./azure-content-safety-implementation.md) - Exemplos de implementação para integrar o Azure Content Safety com servidores MCP
- [MCP Security Controls 2025](./mcp-security-controls-2025.md) - Controles e técnicas de segurança mais recentes para proteger implementações MCP
- [MCP Best Practices](./mcp-best-practices.md) - Guia de referência rápida para segurança MCP

### Próximo

Próximo: [Capítulo 3: Primeiros Passos](../03-GettingStarted/README.md)

**Aviso Legal**:  
Este documento foi traduzido utilizando o serviço de tradução por IA [Co-op Translator](https://github.com/Azure/co-op-translator). Embora nos esforcemos para garantir a precisão, é importante notar que traduções automáticas podem conter erros ou imprecisões. O documento original na sua língua nativa deve ser considerado a fonte autoritária. Para informações críticas, recomenda-se a tradução profissional realizada por humanos. Não nos responsabilizamos por quaisquer mal-entendidos ou interpretações incorretas decorrentes do uso desta tradução.