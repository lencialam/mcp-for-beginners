<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "2e782fc6226cf5e2b5625b035d35e60a",
  "translation_date": "2025-08-11T09:38:03+00:00",
  "source_file": "02-Security/README.md",
  "language_code": "zh"
}
-->
# 安全最佳实践

[![MCP 安全最佳实践](../../../translated_images/03.175aed6dedae133f9d41e49cefd0f0a9a39c3317e1eaa7ef7182696af7534308.zh.png)](https://youtu.be/88No8pw706o)

_（点击上方图片观看本课视频）_

由于安全性是一个至关重要的方面，我们将其作为第二部分重点讨论。这符合微软 [安全未来计划](https://www.microsoft.com/en-us/security/blog/2025/04/17/microsofts-secure-by-design-journey-one-year-of-success/)中的 **安全设计原则**。

采用模型上下文协议（MCP）为 AI 驱动的应用程序带来了强大的新功能，但也引入了超越传统软件风险的独特安全挑战。除了已知的安全编码、最小权限和供应链安全等问题外，MCP 和 AI 工作负载还面临新的威胁，例如提示注入、工具污染、动态工具修改、会话劫持、混淆代理攻击以及令牌传递漏洞。如果管理不当，这些风险可能导致数据泄露、隐私侵犯以及系统行为异常。

本课将探讨与 MCP 相关的最重要的安全风险，包括身份验证、授权、权限过多、间接提示注入、会话安全、混淆代理问题、令牌传递漏洞以及供应链漏洞，并提供可操作的控制措施和最佳实践来减轻这些风险。您还将学习如何利用微软解决方案，例如 Prompt Shields、Azure 内容安全和 GitHub 高级安全功能来加强 MCP 的实施。通过理解和应用这些控制措施，您可以显著降低安全漏洞的可能性，确保您的 AI 系统保持稳健和可信。

# 学习目标

完成本课后，您将能够：

- 识别并解释模型上下文协议（MCP）引入的独特安全风险，包括提示注入、工具污染、权限过多、会话劫持、混淆代理问题、令牌传递漏洞以及供应链漏洞。
- 描述并应用有效的 MCP 安全风险缓解控制措施，例如强大的身份验证、最小权限、安全令牌管理、会话安全控制以及供应链验证。
- 理解并利用微软解决方案，例如 Prompt Shields、Azure 内容安全和 GitHub 高级安全功能来保护 MCP 和 AI 工作负载。
- 认识到验证工具元数据、监控动态变化、防御间接提示注入攻击以及防止会话劫持的重要性。
- 将已建立的安全最佳实践（例如安全编码、服务器加固和零信任架构）集成到您的 MCP 实施中，以减少安全漏洞的可能性和影响。

# MCP 安全控制

任何访问重要资源的系统都隐含着安全挑战。通常可以通过正确应用基本的安全控制和概念来解决这些挑战。由于 MCP 是一个新定义的协议，其规范正在快速变化并随着协议的发展而演变。最终，协议中的安全控制将会成熟，从而更好地与企业和已建立的安全架构及最佳实践集成。

根据 [微软数字防御报告](https://aka.ms/mddr) 发布的研究，98% 的报告漏洞可以通过强大的安全卫生措施来预防。防止任何类型漏洞的最佳保护措施是确保您的基础安全卫生、正确的安全编码最佳实践以及供应链安全——这些我们已经知道的经过验证的实践仍然对降低安全风险最具影响力。

让我们来看看在采用 MCP 时可以开始解决安全风险的一些方法。

> **注意：** 以下信息截至 **2025 年 5 月 29 日** 是正确的。MCP 协议正在不断发展，未来的实施可能会引入新的身份验证模式和控制措施。有关最新更新和指导，请始终参考 [MCP 规范](https://spec.modelcontextprotocol.io/) 和官方 [MCP GitHub 仓库](https://github.com/modelcontextprotocol) 以及 [安全最佳实践页面](https://modelcontextprotocol.io/specification/draft/basic/security_best_practices)。

### 问题陈述
最初的 MCP 规范假设开发人员会编写自己的身份验证服务器。这需要了解 OAuth 和相关的安全约束。MCP 服务器充当 OAuth 2.0 授权服务器，直接管理所需的用户身份验证，而不是将其委托给外部服务，例如 Microsoft Entra ID。从 **2025 年 4 月 26 日** 起，MCP 规范的更新允许 MCP 服务器将用户身份验证委托给外部服务。

### 风险
- MCP 服务器中的授权逻辑配置错误可能导致敏感数据暴露和访问控制应用不当。
- 本地 MCP 服务器上的 OAuth 令牌被盗。如果被盗，令牌可以用来冒充 MCP 服务器并访问该令牌所对应服务的资源和数据。

#### 令牌传递
授权规范明确禁止令牌传递，因为它引入了许多安全风险，包括：

#### 安全控制规避
MCP 服务器或下游 API 可能实施了依赖令牌受众或其他凭证约束的重要安全控制，例如速率限制、请求验证或流量监控。如果客户端可以直接使用令牌与下游 API 通信，而无需 MCP 服务器正确验证或确保令牌是为正确的服务签发的，则会绕过这些控制。

#### 责任和审计问题
MCP 服务器无法识别或区分 MCP 客户端，因为客户端可能使用上游签发的访问令牌，而这些令牌对 MCP 服务器可能是不可见的。
下游资源服务器的日志可能显示来自不同来源的请求，而不是实际转发令牌的 MCP 服务器。
这两个因素使得事件调查、控制和审计更加困难。
如果 MCP 服务器在转发令牌时未验证其声明（例如角色、权限或受众）或其他元数据，持有被盗令牌的恶意行为者可以利用服务器作为数据泄露的代理。

#### 信任边界问题
下游资源服务器对特定实体授予信任。这种信任可能包括对来源或客户端行为模式的假设。打破这种信任边界可能导致意外问题。
如果令牌在没有适当验证的情况下被多个服务接受，则攻击者可以通过破坏一个服务来使用令牌访问其他连接的服务。

#### 未来兼容性风险
即使 MCP 服务器今天作为“纯代理”开始，它可能需要在以后添加安全控制。从一开始就实施正确的令牌受众分离可以更容易地演变安全模型。

### 缓解控制措施

**MCP 服务器不得接受任何未明确为 MCP 服务器签发的令牌**

- **审查并加强授权逻辑：** 仔细审计 MCP 服务器的授权实现，确保只有预期的用户和客户端可以访问敏感资源。有关实用指导，请参阅 [Azure API 管理：MCP 服务器的身份验证网关 | Microsoft 社区中心](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690) 和 [使用 Microsoft Entra ID 通过会话验证 MCP 服务器 - Den Delimarsky](https://den.dev/blog/mcp-server-auth-entra-id-session/)。
- **实施安全令牌实践：** 遵循 [微软的令牌验证和生命周期最佳实践](https://learn.microsoft.com/en-us/entra/identity-platform/access-tokens)，以防止访问令牌的滥用并降低令牌重放或盗窃的风险。
- **保护令牌存储：** 始终安全存储令牌，并使用加密保护其静态和传输中的安全性。有关实施技巧，请参阅 [使用安全令牌存储并加密令牌](https://youtu.be/uRdX37EcCwg?si=6fSChs1G4glwXRy2)。

# MCP 服务器权限过多

### 问题陈述
MCP 服务器可能被授予了对其访问的服务/资源的过多权限。例如，一个属于 AI 销售应用程序的 MCP 服务器连接到企业数据存储时，其访问范围应仅限于销售数据，而不应允许访问存储中的所有文件。回到最小权限原则（最古老的安全原则之一），任何资源的权限都不应超过其执行预期任务所需的权限。AI 在这一领域带来了更大的挑战，因为为了使其具有灵活性，定义确切的权限需求可能具有挑战性。

### 风险
- 授予过多权限可能允许 MCP 服务器访问或修改其不应访问的数据。这可能会成为隐私问题，尤其是当数据是个人身份信息（PII）时。

### 缓解控制措施
- **应用最小权限原则：** 仅授予 MCP 服务器执行其所需任务的最低权限。定期审查并更新这些权限，确保它们不会超过所需范围。有关详细指导，请参阅 [安全的最小权限访问](https://learn.microsoft.com/entra/identity-platform/secure-least-privileged-access)。
- **使用基于角色的访问控制（RBAC）：** 为 MCP 服务器分配严格限定到特定资源和操作的角色，避免广泛或不必要的权限。
- **监控和审计权限：** 持续监控权限使用情况并审计访问日志，及时检测和修复过多或未使用的权限。

# 间接提示注入攻击

### 问题陈述

恶意或被破坏的 MCP 服务器可能通过暴露客户数据或启用意外操作引入重大风险。这些风险在基于 AI 和 MCP 的工作负载中尤为相关，例如：

- **提示注入攻击：** 攻击者在提示或外部内容中嵌入恶意指令，导致 AI 系统执行意外操作或泄露敏感数据。了解更多：[提示注入](https://simonwillison.net/2025/Apr/9/mcp-prompt-injection/)
- **工具污染：** 攻击者操纵工具元数据（例如描述或参数），影响 AI 的行为，可能绕过安全控制或泄露数据。详情：[工具污染](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks)
- **跨域提示注入：** 恶意指令嵌入到文档、网页或电子邮件中，然后由 AI 处理，导致数据泄露或操纵。
- **动态工具修改（Rug Pulls）：** 工具定义在用户批准后可以被更改，引入新的恶意行为而用户无法察觉。

这些漏洞强调了在将 MCP 服务器和工具集成到您的环境中时需要进行强大的验证、监控和安全控制。有关更深入的探讨，请参阅上述链接参考。

![prompt-injection-lg-2048x1034](../../../translated_images/prompt-injection.ed9fbfde297ca877c15bc6daa808681cd3c3dc7bf27bbbda342ef1ba5fc4f52d.zh.png)

**间接提示注入**（也称为跨域提示注入或 XPIA）是生成式 AI 系统（包括使用模型上下文协议 MCP 的系统）中的一个关键漏洞。在这种攻击中，恶意指令隐藏在外部内容中，例如文档、网页或电子邮件。当 AI 系统处理这些内容时，它可能将嵌入的指令解释为合法的用户命令，从而导致意外操作，例如数据泄露、生成有害内容或操纵用户交互。有关详细解释和真实案例，请参阅 [提示注入](https://simonwillison.net/2025/Apr/9/mcp-prompt-injection/)。

一种特别危险的攻击形式是 **工具污染**。在这里，攻击者将恶意指令注入 MCP 工具的元数据（例如工具描述或参数）。由于大型语言模型（LLM）依赖这些元数据来决定调用哪些工具，被破坏的描述可以欺骗模型执行未经授权的工具调用或绕过安全控制。这些操作通常对最终用户是不可见的，但可以被 AI 系统解释并执行。这种风险在托管 MCP 服务器环境中尤为突出，在这种环境中，工具定义可以在用户批准后更新——这种场景有时被称为“[rug pull](https://www.wiz.io/blog/mcp-security-research-briefing#remote-servers-22)”。在这种情况下，之前安全的工具可能后来被修改为执行恶意操作，例如泄露数据或改变系统行为，而用户对此毫不知情。有关此攻击向量的更多信息，请参阅 [工具污染](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks)。

![tool-injection-lg-2048x1239 (1)](../../../translated_images/tool-injection.3b0b4a6b24de6befe7d3afdeae44138ef005881aebcfc84c6f61369ce31e3640.zh.png)

## 风险
意外的 AI 操作带来了多种安全风险，包括数据泄露和隐私侵犯。

### 缓解控制措施
### 使用 Prompt Shields 防御间接提示注入攻击
-----------------------------------------------------------------------------

**AI Prompt Shields** 是微软开发的一种解决方案，用于防御直接和间接提示注入攻击。它通过以下方式提供保护：

1. **检测和过滤：** Prompt Shields 使用先进的机器学习算法和自然语言处理技术，检测并过滤嵌入在外部内容（如文档、网页或电子邮件）中的恶意指令。
    
2. **聚焦技术：** 该技术帮助 AI 系统区分有效的系统指令和潜在的不可信外部输入。通过以更相关的方式转换输入文本，聚焦技术确保 AI 能更好地识别并忽略恶意指令。
    
3. **分隔符和数据标记：** 在系统消息中包含分隔符明确标示输入文本的位置，帮助 AI 系统识别并分离用户输入与潜在有害的外部内容。数据标记扩展了这一概念，通过使用特殊标记突出显示可信和不可信数据的边界。
    
4. **持续监控和更新：** 微软持续监控并更新 Prompt Shields，以应对新的和不断发展的威胁。这种主动方法确保防御措施始终有效应对最新的攻击技术。
5. **与 Azure 内容安全的集成：** Prompt Shields 是更广泛的 Azure AI 内容安全套件的一部分，该套件提供了额外的工具，用于检测越狱尝试、有害内容以及 AI 应用中的其他安全风险。

您可以在 [Prompt Shields 文档](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection) 中阅读更多关于 AI Prompt Shields 的信息。

![prompt-shield-lg-2048x1328](../../../translated_images/prompt-shield.ff5b95be76e9c78c6ec0888206a4a6a0a5ab4bb787832a9eceef7a62fe0138d1.zh.png)


# 混淆代理问题

### 问题描述

混淆代理问题是一种安全漏洞，当 MCP 服务器作为 MCP 客户端与第三方 API 之间的代理时可能发生。如果 MCP 服务器使用静态客户端 ID 来与不支持动态客户端注册的第三方授权服务器进行身份验证，则可能被利用。

### 风险

- **基于 Cookie 的同意绕过**：如果用户之前通过 MCP 代理服务器进行了身份验证，第三方授权服务器可能会在用户的浏览器中设置同意 Cookie。攻击者可以通过发送包含恶意重定向 URI 的授权请求链接来利用这一点。
- **授权码窃取**：当用户点击恶意链接时，第三方授权服务器可能会因为现有的 Cookie 而跳过同意屏幕，授权码可能会被重定向到攻击者的服务器。
- **未经授权的 API 访问**：攻击者可以用窃取的授权码交换访问令牌，冒充用户访问第三方 API，而无需明确批准。

### 缓解措施

- **明确的同意要求**：使用静态客户端 ID 的 MCP 代理服务器 **必须** 在转发到第三方授权服务器之前，为每个动态注册的客户端获取用户同意。
- **正确的 OAuth 实现**：遵循 OAuth 2.1 的安全最佳实践，包括在授权请求中使用代码挑战（PKCE）以防止拦截攻击。
- **客户端验证**：严格验证重定向 URI 和客户端标识符，以防止恶意行为者的利用。


# 令牌透传漏洞

### 问题描述

“令牌透传”是一种反模式，其中 MCP 服务器接受来自 MCP 客户端的令牌，而不验证这些令牌是否正确地为 MCP 服务器本身颁发，然后将其“透传”到下游 API。这种做法明确违反了 MCP 授权规范，并引入了严重的安全风险。

### 风险

- **安全控制规避**：如果客户端可以直接使用令牌与下游 API 交互而无需适当验证，则可能绕过重要的安全控制，例如速率限制、请求验证或流量监控。
- **问责和审计问题**：当客户端使用上游颁发的访问令牌时，MCP 服务器将无法识别或区分 MCP 客户端，从而使事件调查和审计更加困难。
- **数据泄露**：如果令牌在没有适当声明验证的情况下被透传，拥有被盗令牌的恶意行为者可能会利用服务器作为数据泄露的代理。
- **信任边界破坏**：下游资源服务器可能会基于来源或行为模式对特定实体授予信任。破坏这种信任边界可能导致意外的安全问题。
- **多服务令牌滥用**：如果多个服务在没有适当验证的情况下接受令牌，攻击者可能通过攻破一个服务来使用该令牌访问其他连接的服务。

### 缓解措施

- **令牌验证**：MCP 服务器 **不得** 接受任何未明确为其颁发的令牌。
- **受众验证**：始终验证令牌是否具有与 MCP 服务器身份匹配的正确受众声明。
- **正确的令牌生命周期管理**：实施短期访问令牌和适当的令牌轮换实践，以减少令牌被盗和滥用的风险。


# 会话劫持

### 问题描述

会话劫持是一种攻击方式，其中服务器向客户端提供会话 ID，而未经授权的一方获取并使用相同的会话 ID 冒充原始客户端，代表其执行未经授权的操作。这在处理 MCP 请求的有状态 HTTP 服务器中尤为令人担忧。

### 风险

- **会话劫持提示注入**：攻击者获取会话 ID 后，可能向与客户端连接的服务器共享会话状态的服务器发送恶意事件，从而触发有害操作或访问敏感数据。
- **会话劫持冒充**：拥有被盗会话 ID 的攻击者可以直接向 MCP 服务器发出调用，绕过身份验证并被视为合法用户。
- **受损的可恢复流**：当服务器支持重新传递/可恢复流时，攻击者可能会提前终止请求，导致原始客户端稍后恢复时可能包含恶意内容。

### 缓解措施

- **授权验证**：实现授权的 MCP 服务器 **必须** 验证所有入站请求，并且 **不得** 使用会话进行身份验证。
- **安全的会话 ID**：MCP 服务器 **必须** 使用安全的、非确定性的会话 ID，并通过安全随机数生成器生成。避免使用可预测或顺序的标识符。
- **用户特定的会话绑定**：MCP 服务器 **应** 将会话 ID 绑定到用户特定信息，将会话 ID 与授权用户的唯一信息（如其内部用户 ID）结合使用，例如 `<user_id>:<session_id>` 格式。
- **会话过期**：实施适当的会话过期和轮换，以限制会话 ID 被泄露后的漏洞窗口。
- **传输安全**：始终使用 HTTPS 进行所有通信，以防止会话 ID 被拦截。


# 供应链安全

在 AI 时代，供应链安全仍然至关重要，但供应链的范围已经扩大。除了传统的代码包外，您现在必须严格验证和监控所有与 AI 相关的组件，包括基础模型、嵌入服务、上下文提供者和第三方 API。如果管理不当，每个组件都可能引入漏洞或风险。

**AI 和 MCP 的关键供应链安全实践：**
- **在集成前验证所有组件**：这不仅包括开源库，还包括 AI 模型、数据源和外部 API。始终检查来源、许可和已知漏洞。
- **维护安全的部署管道**：使用集成安全扫描的自动化 CI/CD 管道，尽早发现问题。确保只有受信任的工件被部署到生产环境。
- **持续监控和审计**：对所有依赖项（包括模型和数据服务）实施持续监控，以检测新漏洞或供应链攻击。
- **应用最小权限和访问控制**：将对模型、数据和服务的访问限制为 MCP 服务器运行所需的最低权限。
- **快速响应威胁**：制定补丁或替换受损组件的流程，并在检测到漏洞时轮换密钥或凭据。

[GitHub Advanced Security](https://github.com/security/advanced-security) 提供了诸如密钥扫描、依赖项扫描和 CodeQL 分析等功能。这些工具与 [Azure DevOps](https://azure.microsoft.com/en-us/products/devops) 和 [Azure Repos](https://azure.microsoft.com/en-us/products/devops/repos/) 集成，帮助团队识别和缓解代码和 AI 供应链组件中的漏洞。

微软还在所有产品中实施了广泛的供应链安全实践。了解更多信息，请参阅 [微软软件供应链安全之旅](https://devblogs.microsoft.com/engineering-at-microsoft/the-journey-to-secure-the-software-supply-chain-at-microsoft/)。


# 提升 MCP 实现安全性的既定安全最佳实践

任何 MCP 实现都继承了其构建所在组织环境的现有安全态势，因此在考虑 MCP 作为整体 AI 系统组件的安全性时，建议提升整体现有的安全态势。以下既定的安全控制尤为重要：

-   AI 应用中的安全编码最佳实践 - 防范 [OWASP Top 10](https://owasp.org/www-project-top-ten/)、[OWASP LLMs Top 10](https://genai.owasp.org/download/43299/?tmstv=1731900559)，使用安全金库存储密钥和令牌，在所有应用组件之间实现端到端的安全通信等。
-   服务器加固 - 尽可能使用 MFA，保持补丁更新，将服务器与第三方身份提供者集成以进行访问控制等。
-   保持设备、基础设施和应用程序的补丁更新
-   安全监控 - 实现 AI 应用（包括 MCP 客户端/服务器）的日志记录和监控，并将这些日志发送到中央 SIEM 以检测异常活动
-   零信任架构 - 通过网络和身份控制以逻辑方式隔离组件，最小化 AI 应用被攻破后的横向移动。

# 关键要点

- 安全基础仍然至关重要：安全编码、最小权限、供应链验证和持续监控对于 MCP 和 AI 工作负载至关重要。
- MCP 引入了新的风险——如提示注入、工具投毒、会话劫持、混淆代理问题、令牌透传漏洞和过度权限——需要传统和 AI 特定的控制措施。
- 使用强大的身份验证、授权和令牌管理实践，尽可能利用外部身份提供者（如 Microsoft Entra ID）。
- 通过验证工具元数据、监控动态变化以及使用 Microsoft Prompt Shields 等解决方案，防范间接提示注入和工具投毒。
- 通过使用非确定性会话 ID、将会话绑定到用户身份以及绝不使用会话进行身份验证，实施安全的会话管理。
- 通过为每个动态注册的客户端要求明确的用户同意并实施正确的 OAuth 安全实践，防止混淆代理攻击。
- 避免令牌透传漏洞，确保 MCP 服务器仅接受明确为其颁发的令牌，并适当验证令牌声明。
- 将 AI 供应链中的所有组件（包括模型、嵌入和上下文提供者）视为代码依赖项一样严格。
- 紧跟不断发展的 MCP 规范，并为社区做出贡献以帮助制定安全标准。

# 其他资源

## 外部资源
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
- [微软软件供应链安全之旅](https://devblogs.microsoft.com/engineering-at-microsoft/the-journey-to-secure-the-software-supply-chain-at-microsoft/)
- [Secure Least-Privileged Access (Microsoft)](https://learn.microsoft.com/entra/identity-platform/secure-least-privileged-access)
- [Best Practices for Token Validation and Lifetime](https://learn.microsoft.com/entra/identity-platform/access-tokens)
- [Use Secure Token Storage and Encrypt Tokens (YouTube)](https://youtu.be/uRdX37EcCwg?si=6fSChs1G4glwXRy2)
- [Azure API Management as Auth Gateway for MCP](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690)
- [Using Microsoft Entra ID to Authenticate with MCP Servers](https://den.dev/blog/mcp-server-auth-entra-id-session/)

## 其他安全文档

有关更详细的安全指南，请参阅以下文档：

- [MCP 安全最佳实践 2025](./mcp-security-best-practices-2025.md) - MCP 实现的全面安全最佳实践列表
- [Azure 内容安全实施](./azure-content-safety-implementation.md) - 将 Azure 内容安全与 MCP 服务器集成的实施示例
- [MCP 安全控制 2025](./mcp-security-controls-2025.md) - 用于保护 MCP 部署的最新安全控制和技术
- [MCP 最佳实践](./mcp-best-practices.md) - MCP 安全的快速参考指南

### 下一步

下一步：[第 3 章：入门](../03-GettingStarted/README.md)

**免责声明**：  
本文档使用AI翻译服务 [Co-op Translator](https://github.com/Azure/co-op-translator) 进行翻译。尽管我们努力确保翻译的准确性，但请注意，自动翻译可能包含错误或不准确之处。原始语言的文档应被视为权威来源。对于重要信息，建议使用专业人工翻译。我们不对因使用此翻译而产生的任何误解或误读承担责任。