<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "2e782fc6226cf5e2b5625b035d35e60a",
  "translation_date": "2025-08-11T10:36:18+00:00",
  "source_file": "02-Security/README.md",
  "language_code": "ko"
}
-->
# 보안 모범 사례

[![MCP 보안 모범 사례](../../../translated_images/03.175aed6dedae133f9d41e49cefd0f0a9a39c3317e1eaa7ef7182696af7534308.ko.png)](https://youtu.be/88No8pw706o)

_(위 이미지를 클릭하면 이 강의의 동영상을 볼 수 있습니다)_

보안은 매우 중요한 요소이기 때문에, 우리는 이를 두 번째 섹션으로 우선시합니다. 이는 Microsoft의 [Secure Future Initiative](https://www.microsoft.com/en-us/security/blog/2025/04/17/microsofts-secure-by-design-journey-one-year-of-success/)의 **Secure by design** 원칙에 부합합니다.

Model Context Protocol (MCP)을 채택하면 AI 기반 애플리케이션에 강력한 새로운 기능을 제공하지만, 기존 소프트웨어 위험을 넘어서는 독특한 보안 과제를 가져옵니다. 안전한 코딩, 최소 권한, 공급망 보안과 같은 기존의 우려 사항 외에도 MCP와 AI 워크로드는 프롬프트 주입, 도구 오염, 동적 도구 수정, 세션 탈취, 혼란스러운 대리 공격, 토큰 전달 취약점과 같은 새로운 위협에 직면합니다. 이러한 위험은 적절히 관리되지 않을 경우 데이터 유출, 개인정보 침해, 의도하지 않은 시스템 동작을 초래할 수 있습니다.

이 강의에서는 MCP와 관련된 가장 중요한 보안 위험—인증, 권한 부여, 과도한 권한, 간접 프롬프트 주입, 세션 보안, 혼란스러운 대리 문제, 토큰 전달 취약점, 공급망 취약점—을 탐구하고 이를 완화하기 위한 실행 가능한 통제 및 모범 사례를 제공합니다. 또한 Prompt Shields, Azure Content Safety, GitHub Advanced Security와 같은 Microsoft 솔루션을 활용하여 MCP 구현을 강화하는 방법을 배울 수 있습니다. 이러한 통제를 이해하고 적용함으로써 보안 침해 가능성을 크게 줄이고 AI 시스템이 강력하고 신뢰할 수 있도록 유지할 수 있습니다.

# 학습 목표

이 강의를 마치면 다음을 수행할 수 있습니다:

- Model Context Protocol (MCP)이 도입하는 독특한 보안 위험—프롬프트 주입, 도구 오염, 과도한 권한, 세션 탈취, 혼란스러운 대리 문제, 토큰 전달 취약점, 공급망 취약점—을 식별하고 설명할 수 있습니다.
- 강력한 인증, 최소 권한, 안전한 토큰 관리, 세션 보안 통제, 공급망 검증과 같은 MCP 보안 위험에 대한 효과적인 완화 통제를 설명하고 적용할 수 있습니다.
- MCP와 AI 워크로드를 보호하기 위해 Prompt Shields, Azure Content Safety, GitHub Advanced Security와 같은 Microsoft 솔루션을 이해하고 활용할 수 있습니다.
- 도구 메타데이터를 검증하고, 동적 변경 사항을 모니터링하며, 간접 프롬프트 주입 공격을 방어하고, 세션 탈취를 방지하는 중요성을 인식할 수 있습니다.
- 안전한 코딩, 서버 강화, 제로 트러스트 아키텍처와 같은 기존의 보안 모범 사례를 MCP 구현에 통합하여 보안 침해의 가능성과 영향을 줄일 수 있습니다.

# MCP 보안 통제

중요한 리소스에 접근할 수 있는 시스템은 암묵적으로 보안 과제를 포함합니다. 보안 과제는 일반적으로 기본적인 보안 통제와 개념을 올바르게 적용함으로써 해결할 수 있습니다. MCP는 새롭게 정의된 프로토콜로, 사양이 매우 빠르게 변화하고 있으며 프로토콜이 발전함에 따라 보안 통제도 성숙해질 것입니다. 이는 기업 및 기존 보안 아키텍처와 모범 사례와의 더 나은 통합을 가능하게 할 것입니다.

[Microsoft Digital Defense Report](https://aka.ms/mddr)에 발표된 연구에 따르면 보고된 침해의 98%는 강력한 보안 위생으로 예방할 수 있으며, 모든 종류의 침해에 대한 최고의 보호는 기본적인 보안 위생, 안전한 코딩 모범 사례, 공급망 보안을 올바르게 설정하는 것입니다. 우리가 이미 알고 있는 이러한 검증된 모범 사례는 보안 위험을 줄이는 데 가장 큰 영향을 미칩니다.

MCP를 채택할 때 보안 위험을 해결하기 시작할 수 있는 몇 가지 방법을 살펴보겠습니다.

> **Note:** 아래 정보는 **2025년 5월 29일** 기준으로 정확합니다. MCP 프로토콜은 지속적으로 발전하고 있으며, 향후 구현은 새로운 인증 패턴과 통제를 도입할 수 있습니다. 최신 업데이트와 지침은 항상 [MCP Specification](https://spec.modelcontextprotocol.io/) 및 공식 [MCP GitHub repository](https://github.com/modelcontextprotocol)와 [security best practice page](https://modelcontextprotocol.io/specification/draft/basic/security_best_practices)를 참조하세요.

### 문제 진술
초기 MCP 사양은 개발자가 자체 인증 서버를 작성할 것을 가정했습니다. 이는 OAuth 및 관련 보안 제약에 대한 지식을 요구했습니다. MCP 서버는 OAuth 2.0 인증 서버로 작동하며, 외부 서비스(예: Microsoft Entra ID)에 위임하지 않고 직접 사용자 인증을 관리했습니다. **2025년 4월 26일** 기준으로 MCP 사양 업데이트는 MCP 서버가 사용자 인증을 외부 서비스에 위임할 수 있도록 허용합니다.

### 위험
- MCP 서버의 잘못 구성된 권한 부여 로직은 민감한 데이터 노출 및 잘못된 접근 통제를 초래할 수 있습니다.
- 로컬 MCP 서버에서 OAuth 토큰이 도난당할 경우, 도난당한 토큰은 MCP 서버를 가장하여 해당 OAuth 토큰이 속한 서비스의 리소스와 데이터를 액세스하는 데 사용될 수 있습니다.

#### 토큰 전달
토큰 전달은 여러 보안 위험을 초래하기 때문에 인증 사양에서 명시적으로 금지됩니다. 이러한 위험에는 다음이 포함됩니다:

#### 보안 통제 우회
MCP 서버 또는 다운스트림 API는 토큰 대상 또는 기타 자격 증명 제약에 의존하는 속도 제한, 요청 검증, 트래픽 모니터링과 같은 중요한 보안 통제를 구현할 수 있습니다. 클라이언트가 MCP 서버가 토큰을 올바르게 검증하거나 토큰이 올바른 서비스에 대해 발급되었는지 확인하지 않고 다운스트림 API와 직접 토큰을 사용할 수 있다면 이러한 통제를 우회하게 됩니다.

#### 책임 및 감사 추적 문제
클라이언트가 상류에서 발급된 액세스 토큰을 사용하여 호출할 경우 MCP 서버는 MCP 클라이언트를 식별하거나 구분할 수 없습니다. 다운스트림 리소스 서버의 로그는 MCP 서버가 실제로 토큰을 전달하는 대신 다른 소스에서 온 것처럼 보이는 요청을 표시할 수 있습니다. 이러한 두 가지 요인은 사건 조사, 통제 및 감사 작업을 더 어렵게 만듭니다. MCP 서버가 역할, 권한 또는 대상과 같은 클레임이나 기타 메타데이터를 검증하지 않고 토큰을 전달하면 도난당한 토큰을 소유한 악의적인 행위자가 서버를 데이터 유출의 프록시로 사용할 수 있습니다.

#### 신뢰 경계 문제
다운스트림 리소스 서버는 특정 엔터티에 신뢰를 부여합니다. 이 신뢰는 출처 또는 클라이언트 행동 패턴에 대한 가정을 포함할 수 있습니다. 이 신뢰 경계를 깨뜨리면 예상치 못한 문제가 발생할 수 있습니다. 토큰이 적절한 검증 없이 여러 서비스에서 수락되면 한 서비스를 손상시킨 공격자가 해당 토큰을 사용하여 다른 연결된 서비스에 액세스할 수 있습니다.

#### 미래 호환성 위험
MCP 서버가 오늘날 "순수 프록시"로 시작하더라도 나중에 보안 통제를 추가해야 할 수 있습니다. 적절한 토큰 대상 분리를 시작하면 보안 모델을 발전시키기가 더 쉬워집니다.

### 완화 통제

**MCP 서버는 MCP 서버를 위해 명시적으로 발급되지 않은 토큰을 절대 수락해서는 안 됩니다**

- **권한 부여 로직 검토 및 강화:** MCP 서버의 권한 부여 구현을 신중히 감사하여 의도된 사용자와 클라이언트만 민감한 리소스에 액세스할 수 있도록 하세요. 실용적인 지침은 [Azure API Management Your Auth Gateway For MCP Servers | Microsoft Community Hub](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690) 및 [Using Microsoft Entra ID To Authenticate With MCP Servers Via Sessions - Den Delimarsky](https://den.dev/blog/mcp-server-auth-entra-id-session/)를 참조하세요.
- **안전한 토큰 관행 시행:** [Microsoft의 토큰 검증 및 수명에 대한 모범 사례](https://learn.microsoft.com/en-us/entra/identity-platform/access-tokens)를 따르세요. 이를 통해 액세스 토큰의 오용을 방지하고 토큰 재사용 또는 도난 위험을 줄일 수 있습니다.
- **토큰 저장소 보호:** 항상 토큰을 안전하게 저장하고, 휴지 상태 및 전송 중에 암호화를 사용하여 이를 보호하세요. 구현 팁은 [Use secure token storage and encrypt tokens](https://youtu.be/uRdX37EcCwg?si=6fSChs1G4glwXRy2)를 참조하세요.

# MCP 서버의 과도한 권한

### 문제 진술
MCP 서버가 액세스하는 서비스/리소스에 대해 과도한 권한을 부여받았을 수 있습니다. 예를 들어, AI 판매 애플리케이션의 일부인 MCP 서버가 기업 데이터 저장소에 연결되는 경우, 판매 데이터에 대한 액세스만 허용되어야 하며 저장소의 모든 파일에 액세스할 수 있어서는 안 됩니다. 가장 오래된 보안 원칙 중 하나인 최소 권한 원칙을 참고하면, 어떤 리소스도 의도된 작업을 실행하는 데 필요한 것 이상의 권한을 가져서는 안 됩니다. AI는 유연성을 가능하게 하기 위해 필요한 정확한 권한을 정의하는 것이 어려울 수 있어 이 영역에서 추가적인 도전을 제시합니다.

### 위험
- 과도한 권한을 부여하면 MCP 서버가 의도하지 않은 데이터에 액세스하거나 수정할 수 있어 데이터 유출 또는 수정이 발생할 수 있습니다. 이는 데이터가 개인 식별 가능 정보(PII)인 경우 개인정보 문제를 초래할 수도 있습니다.

### 완화 통제
- **최소 권한 원칙 적용:** MCP 서버에 필요한 작업을 수행하는 데 필요한 최소한의 권한만 부여하세요. 이러한 권한을 정기적으로 검토하고 업데이트하여 필요 이상으로 초과하지 않도록 하세요. 자세한 지침은 [Secure least-privileged access](https://learn.microsoft.com/entra/identity-platform/secure-least-privileged-access)를 참조하세요.
- **역할 기반 액세스 제어(RBAC) 사용:** MCP 서버에 특정 리소스와 작업에 엄격히 범위가 지정된 역할을 할당하여 광범위하거나 불필요한 권한을 피하세요.
- **권한 모니터링 및 감사:** 권한 사용을 지속적으로 모니터링하고 액세스 로그를 감사하여 과도하거나 사용되지 않는 권한을 신속히 탐지하고 수정하세요.

# 간접 프롬프트 주입 공격

### 문제 진술

악의적이거나 손상된 MCP 서버는 고객 데이터를 노출하거나 의도하지 않은 작업을 가능하게 함으로써 상당한 위험을 초래할 수 있습니다. 이러한 위험은 특히 AI 및 MCP 기반 워크로드에서 다음과 같은 경우에 관련이 있습니다:

- **프롬프트 주입 공격**: 공격자가 프롬프트나 외부 콘텐츠에 악의적인 지시를 삽입하여 AI 시스템이 의도하지 않은 작업을 수행하거나 민감한 데이터를 유출하도록 만듭니다. 자세히 알아보기: [Prompt Injection](https://simonwillison.net/2025/Apr/9/mcp-prompt-injection/)
- **도구 오염**: 공격자가 도구 메타데이터(예: 설명 또는 매개변수)를 조작하여 AI의 동작에 영향을 미치고 보안 통제를 우회하거나 데이터를 유출할 수 있습니다. 자세한 내용: [Tool Poisoning](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks)
- **크로스 도메인 프롬프트 주입**: 악의적인 지시가 문서, 웹 페이지 또는 이메일에 삽입되어 AI가 이를 처리할 때 데이터 유출 또는 조작이 발생합니다.
- **동적 도구 수정(러그 풀)**: 사용자 승인 후 도구 정의가 변경되어 사용자가 인식하지 못한 채 새로운 악의적 동작을 도입할 수 있습니다.

이러한 취약점은 MCP 서버와 도구를 환경에 통합할 때 강력한 검증, 모니터링 및 보안 통제가 필요함을 강조합니다. 위에 링크된 참조를 통해 자세히 알아보세요.

![prompt-injection-lg-2048x1034](../../../translated_images/prompt-injection.ed9fbfde297ca877c15bc6daa808681cd3c3dc7bf27bbbda342ef1ba5fc4f52d.ko.png)

**간접 프롬프트 주입**(크로스 도메인 프롬프트 주입 또는 XPIA로도 알려짐)은 Model Context Protocol (MCP)을 사용하는 생성 AI 시스템에서 중요한 취약점입니다. 이 공격에서는 악의적인 지시가 문서, 웹 페이지, 이메일과 같은 외부 콘텐츠에 숨겨집니다. AI 시스템이 이 콘텐츠를 처리할 때, 내장된 지시를 합법적인 사용자 명령으로 해석하여 데이터 유출, 유해한 콘텐츠 생성, 사용자 상호작용 조작과 같은 의도하지 않은 작업을 수행할 수 있습니다. 자세한 설명과 실제 사례는 [Prompt Injection](https://simonwillison.net/2025/Apr/9/mcp-prompt-injection/)을 참조하세요.

특히 위험한 형태의 공격은 **도구 오염**입니다. 여기서 공격자는 MCP 도구의 메타데이터(예: 도구 설명 또는 매개변수)에 악의적인 지시를 삽입합니다. 대규모 언어 모델(LLM)은 이 메타데이터를 사용하여 호출할 도구를 결정하기 때문에, 손상된 설명은 모델이 승인되지 않은 도구 호출을 실행하거나 보안 통제를 우회하도록 속일 수 있습니다. 이러한 조작은 최종 사용자에게는 보이지 않지만 AI 시스템에 의해 해석되고 실행될 수 있습니다. 이 위험은 호스팅된 MCP 서버 환경에서 더욱 높아지며, 여기서 도구 정의는 사용자 승인 후 업데이트될 수 있습니다—이러한 시나리오는 때때로 "[러그 풀](https://www.wiz.io/blog/mcp-security-research-briefing#remote-servers-22)"이라고도 불립니다. 이 경우 이전에 안전했던 도구가 나중에 데이터 유출 또는 시스템 동작 변경과 같은 악의적 작업을 수행하도록 수정될 수 있습니다. 이 공격 벡터에 대한 자세한 내용은 [Tool Poisoning](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks)을 참조하세요.

![tool-injection-lg-2048x1239 (1)](../../../translated_images/tool-injection.3b0b4a6b24de6befe7d3afdeae44138ef005881aebcfc84c6f61369ce31e3640.ko.png)

## 위험
의도하지 않은 AI 작업은 데이터 유출 및 개인정보 침해를 포함한 다양한 보안 위험을 초래합니다.

### 완화 통제
### 간접 프롬프트 주입 공격을 방어하기 위한 프롬프트 실드 사용
-----------------------------------------------------------------------------

**AI 프롬프트 실드**는 Microsoft가 직접 및 간접 프롬프트 주입 공격을 방어하기 위해 개발한 솔루션입니다. 이를 통해 다음을 수행합니다:

1.  **탐지 및 필터링**: 프롬프트 실드는 고급 머신 러닝 알고리즘과 자연어 처리를 사용하여 문서, 웹 페이지, 이메일과 같은 외부 콘텐츠에 삽입된 악의적인 지시를 탐지하고 필터링합니다.
    
2.  **스포트라이트**: 이 기술은 AI 시스템이 유효한 시스템 지시와 잠재적으로 신뢰할 수 없는 외부 입력을 구별할 수 있도록 돕습니다. 입력 텍스트를 모델에 더 적합하게 변환함으로써 스포트라이트는 AI가 악의적인 지시를 더 잘 식별하고 무시할 수 있도록 합니다.
    
3.  **구분자 및 데이터마킹**: 시스템 메시지에 구분자를 포함하여 입력 텍스트의 위치를 명시적으로 설명함으로써 AI 시스템이 사용자 입력과 잠재적으로 유해한 외부 콘텐츠를 인식하고 분리할 수 있도록 합니다. 데이터마킹은 신뢰할 수 있는 데이터와 신뢰할 수 없는 데이터의 경계를 강조하는 특별한 마커를 사용하여 이 개념을 확장합니다.
    
4.  **지속적인 모니터링 및 업데이트**: Microsoft는 새로운 위협과 진화하는 위협을 해결하기 위해 프롬프트 실드를 지속적으로 모니터링하고 업데이트합니다. 이러한 사전 예방적 접근 방식은 최신 공격 기술에 대해 방어가 효과적으로 유지되도록 보장합니다.
5. **Azure Content Safety와의 통합:** Prompt Shields는 Azure AI Content Safety 제품군의 일부로, AI 애플리케이션에서 탈옥 시도, 유해 콘텐츠 및 기타 보안 위험을 탐지하는 추가 도구를 제공합니다.

AI Prompt Shields에 대한 자세한 내용은 [Prompt Shields 문서](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)를 참조하세요.

![prompt-shield-lg-2048x1328](../../../translated_images/prompt-shield.ff5b95be76e9c78c6ec0888206a4a6a0a5ab4bb787832a9eceef7a62fe0138d1.ko.png)


# 혼란스러운 대리인 문제

### 문제 설명

혼란스러운 대리인 문제는 MCP 서버가 MCP 클라이언트와 제3자 API 간의 프록시 역할을 할 때 발생하는 보안 취약점입니다. 이 취약점은 MCP 서버가 동적 클라이언트 등록 지원이 없는 제3자 인증 서버와 인증하기 위해 정적 클라이언트 ID를 사용할 때 악용될 수 있습니다.

### 위험

- **쿠키 기반 동의 우회**: 사용자가 이전에 MCP 프록시 서버를 통해 인증한 경우, 제3자 인증 서버는 사용자의 브라우저에 동의 쿠키를 설정할 수 있습니다. 공격자는 이후 악의적으로 조작된 리디렉션 URI를 포함한 인증 요청 링크를 사용자에게 보내 이를 악용할 수 있습니다.
- **인증 코드 탈취**: 사용자가 악의적인 링크를 클릭하면, 기존 쿠키로 인해 제3자 인증 서버가 동의 화면을 건너뛸 수 있으며, 인증 코드는 공격자의 서버로 리디렉션될 수 있습니다.
- **무단 API 접근**: 공격자는 탈취한 인증 코드를 액세스 토큰으로 교환하여 사용자를 가장해 제3자 API에 명시적인 승인 없이 접근할 수 있습니다.

### 완화 방안

- **명시적 동의 요구**: 정적 클라이언트 ID를 사용하는 MCP 프록시 서버는 제3자 인증 서버로 전달하기 전에 각 동적으로 등록된 클라이언트에 대해 사용자 동의를 반드시 받아야 합니다.
- **적절한 OAuth 구현**: OAuth 2.1 보안 모범 사례를 따르고, 인증 요청에 대한 코드 챌린지(PKCE)를 사용하여 가로채기 공격을 방지하세요.
- **클라이언트 검증**: 악의적인 행위자가 악용하지 못하도록 리디렉션 URI와 클라이언트 식별자를 엄격히 검증하세요.


# 토큰 전달 취약점

### 문제 설명

"토큰 전달"은 MCP 서버가 MCP 클라이언트로부터 받은 토큰을 자체적으로 적절히 발급되었는지 검증하지 않고 다운스트림 API로 "전달"하는 반패턴입니다. 이 관행은 MCP 인증 사양을 명백히 위반하며 심각한 보안 위험을 초래합니다.

### 위험

- **보안 통제 우회**: 클라이언트가 적절한 검증 없이 다운스트림 API에서 직접 토큰을 사용할 수 있다면, 속도 제한, 요청 검증, 트래픽 모니터링과 같은 중요한 보안 통제를 우회할 수 있습니다.
- **책임 및 감사 추적 문제**: MCP 서버가 상위에서 발급된 액세스 토큰을 사용하는 클라이언트를 식별하거나 구분할 수 없게 되어 사고 조사와 감사가 어려워집니다.
- **데이터 유출**: 토큰 클레임 검증 없이 전달되면, 탈취된 토큰을 가진 악의적인 행위자가 서버를 데이터 유출의 프록시로 사용할 수 있습니다.
- **신뢰 경계 위반**: 다운스트림 리소스 서버는 특정 엔터티에 대해 기원 또는 행동 패턴에 대한 가정을 기반으로 신뢰를 부여할 수 있습니다. 이 신뢰 경계가 깨지면 예상치 못한 보안 문제가 발생할 수 있습니다.
- **다중 서비스 토큰 오용**: 여러 서비스가 적절한 검증 없이 토큰을 수락하면, 한 서비스를 손상시킨 공격자가 해당 토큰을 사용해 다른 연결된 서비스에 접근할 수 있습니다.

### 완화 방안

- **토큰 검증**: MCP 서버는 자신을 위해 명시적으로 발급되지 않은 토큰을 절대 수락해서는 안 됩니다.
- **대상 확인**: 토큰이 MCP 서버의 정체성과 일치하는 올바른 대상 클레임을 가지고 있는지 항상 확인하세요.
- **적절한 토큰 수명 관리**: 짧은 수명의 액세스 토큰과 적절한 토큰 회전 관행을 구현하여 토큰 탈취 및 오용 위험을 줄이세요.


# 세션 하이재킹

### 문제 설명

세션 하이재킹은 서버가 클라이언트에게 세션 ID를 제공하고, 권한이 없는 제3자가 동일한 세션 ID를 획득하여 원래 클라이언트를 가장해 무단 작업을 수행하는 공격 벡터입니다. 이는 MCP 요청을 처리하는 상태 저장 HTTP 서버에서 특히 우려됩니다.

### 위험

- **세션 하이재킹 프롬프트 주입**: 세션 ID를 획득한 공격자가 클라이언트가 연결된 서버와 세션 상태를 공유하는 서버에 악의적인 이벤트를 보낼 수 있으며, 이는 유해한 작업을 트리거하거나 민감한 데이터에 접근할 수 있습니다.
- **세션 하이재킹 가장**: 세션 ID를 탈취한 공격자가 MCP 서버에 직접 호출을 수행하여 인증을 우회하고 합법적인 사용자로 간주될 수 있습니다.
- **손상된 재개 가능한 스트림**: 서버가 재전송/재개 가능한 스트림을 지원하는 경우, 공격자가 요청을 조기에 종료하여 원래 클라이언트가 잠재적으로 악의적인 콘텐츠로 나중에 이를 재개하도록 유도할 수 있습니다.

### 완화 방안

- **인증 확인**: 인증을 구현하는 MCP 서버는 모든 수신 요청을 확인해야 하며, 세션을 인증에 사용해서는 안 됩니다.
- **보안 세션 ID**: MCP 서버는 보안 난수 생성기를 사용하여 생성된 보안적이고 비결정적인 세션 ID를 사용해야 합니다. 예측 가능하거나 순차적인 식별자는 피하세요.
- **사용자별 세션 바인딩**: MCP 서버는 세션 ID를 사용자별 정보에 바인딩해야 하며, `<user_id>:<session_id>`와 같은 형식을 사용하여 세션 ID를 승인된 사용자 고유 정보와 결합해야 합니다.
- **세션 만료**: 세션 ID가 손상되었을 경우 취약성 창을 제한하기 위해 적절한 세션 만료 및 회전을 구현하세요.
- **전송 보안**: 세션 ID 가로채기를 방지하기 위해 모든 통신에 HTTPS를 항상 사용하세요.


# 공급망 보안

공급망 보안은 AI 시대에서도 여전히 중요하며, 공급망의 범위가 확장되었습니다. 기존 코드 패키지 외에도, 이제는 기본 모델, 임베딩 서비스, 컨텍스트 제공자, 제3자 API 등 모든 AI 관련 구성 요소를 철저히 검증하고 모니터링해야 합니다. 이를 제대로 관리하지 않으면 취약점이나 위험이 발생할 수 있습니다.

**AI 및 MCP를 위한 주요 공급망 보안 관행:**
- **통합 전 모든 구성 요소 검증**: 오픈 소스 라이브러리뿐만 아니라 AI 모델, 데이터 소스, 외부 API도 포함됩니다. 항상 출처, 라이선스, 알려진 취약점을 확인하세요.
- **안전한 배포 파이프라인 유지**: 통합 보안 스캐닝이 포함된 자동화된 CI/CD 파이프라인을 사용하여 문제를 조기에 발견하세요. 신뢰할 수 있는 아티팩트만 프로덕션에 배포되도록 하세요.
- **지속적인 모니터링 및 감사**: 모델 및 데이터 서비스와 같은 모든 종속성을 지속적으로 모니터링하여 새로운 취약점이나 공급망 공격을 탐지하세요.
- **최소 권한 및 접근 제어 적용**: MCP 서버가 작동하는 데 필요한 모델, 데이터, 서비스에만 접근을 제한하세요.
- **위협에 신속히 대응**: 손상된 구성 요소를 패치하거나 교체하고, 침해가 감지되면 비밀 정보나 자격 증명을 회전하는 프로세스를 마련하세요.

[GitHub Advanced Security](https://github.com/security/advanced-security)는 비밀 스캐닝, 종속성 스캐닝, CodeQL 분석과 같은 기능을 제공합니다. 이러한 도구는 [Azure DevOps](https://azure.microsoft.com/en-us/products/devops) 및 [Azure Repos](https://azure.microsoft.com/en-us/products/devops/repos/)와 통합되어 팀이 코드 및 AI 공급망 구성 요소 전반에서 취약점을 식별하고 완화할 수 있도록 지원합니다.

Microsoft는 모든 제품에 대해 광범위한 공급망 보안 관행을 내부적으로 구현하고 있습니다. 자세한 내용은 [Microsoft의 소프트웨어 공급망 보안 여정](https://devblogs.microsoft.com/engineering-at-microsoft/the-journey-to-secure-the-software-supply-chain-at-microsoft/)을 참조하세요.


# MCP 구현의 보안 태세를 강화하는 기존 보안 모범 사례

MCP 구현은 이를 기반으로 구축된 조직 환경의 기존 보안 태세를 상속받으므로, MCP를 전체 AI 시스템의 구성 요소로 고려할 때 기존 보안 태세를 강화하는 것이 권장됩니다. 다음의 기존 보안 통제는 특히 중요합니다:

-   AI 애플리케이션에서의 안전한 코딩 모범 사례 - [OWASP Top 10](https://owasp.org/www-project-top-ten/), [OWASP Top 10 for LLMs](https://genai.owasp.org/download/43299/?tmstv=1731900559)에 대한 보호, 비밀 및 토큰을 위한 안전한 금고 사용, 모든 애플리케이션 구성 요소 간의 종단 간 안전한 통신 구현 등.
-   서버 강화 - 가능한 경우 MFA 사용, 최신 패치 유지, 액세스를 위한 제3자 ID 공급자와 서버 통합 등.
-   장치, 인프라 및 애플리케이션을 최신 패치로 유지
-   보안 모니터링 - AI 애플리케이션(MCP 클라이언트/서버 포함)의 로깅 및 모니터링 구현, 이상 활동 탐지를 위한 중앙 SIEM으로 로그 전송
-   제로 트러스트 아키텍처 - AI 애플리케이션이 손상된 경우 측면 이동을 최소화하기 위해 네트워크 및 ID 통제를 통해 구성 요소를 논리적으로 격리

# 주요 요점

- 보안 기본 사항은 여전히 중요합니다: 안전한 코딩, 최소 권한, 공급망 검증, 지속적인 모니터링은 MCP 및 AI 워크로드에 필수적입니다.
- MCP는 프롬프트 주입, 도구 중독, 세션 하이재킹, 혼란스러운 대리인 문제, 토큰 전달 취약점, 과도한 권한과 같은 새로운 위험을 도입하며, 전통적 및 AI 특화된 통제가 필요합니다.
- Microsoft Entra ID와 같은 외부 ID 공급자를 활용하여 강력한 인증, 권한 부여, 토큰 관리 관행을 사용하세요.
- 도구 메타데이터를 검증하고 동적 변경 사항을 모니터링하며 Microsoft Prompt Shields와 같은 솔루션을 사용하여 간접 프롬프트 주입 및 도구 중독을 방지하세요.
- 비결정적인 세션 ID를 사용하고 세션을 사용자 ID에 바인딩하며 세션을 인증에 사용하지 않음으로써 안전한 세션 관리를 구현하세요.
- 동적으로 등록된 각 클라이언트에 대해 명시적인 사용자 동의를 요구하고 적절한 OAuth 보안 관행을 구현하여 혼란스러운 대리인 공격을 방지하세요.
- MCP 서버가 자신을 위해 명시적으로 발급된 토큰만 수락하고 토큰 클레임을 적절히 검증하도록 하여 토큰 전달 취약점을 방지하세요.
- 모델, 임베딩, 컨텍스트 제공자를 포함한 AI 공급망의 모든 구성 요소를 코드 종속성과 동일한 엄격함으로 다루세요.
- 진화하는 MCP 사양을 최신 상태로 유지하고 커뮤니티에 기여하여 안전한 표준을 형성하는 데 도움을 주세요.

# 추가 자료

## 외부 자료
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

## 추가 보안 문서

더 자세한 보안 지침은 다음 문서를 참조하세요:

- [MCP Security Best Practices 2025](./mcp-security-best-practices-2025.md) - MCP 구현을 위한 포괄적인 보안 모범 사례 목록
- [Azure Content Safety Implementation](./azure-content-safety-implementation.md) - MCP 서버와 Azure Content Safety 통합을 위한 구현 예제
- [MCP Security Controls 2025](./mcp-security-controls-2025.md) - MCP 배포 보안을 위한 최신 보안 통제 및 기술
- [MCP Best Practices](./mcp-best-practices.md) - MCP 보안을 위한 빠른 참조 가이드

### 다음

다음: [3장: 시작하기](../03-GettingStarted/README.md)

**면책 조항**:  
이 문서는 AI 번역 서비스 [Co-op Translator](https://github.com/Azure/co-op-translator)를 사용하여 번역되었습니다. 정확성을 위해 최선을 다하고 있지만, 자동 번역에는 오류나 부정확성이 포함될 수 있습니다. 원본 문서의 원어 버전을 권위 있는 출처로 간주해야 합니다. 중요한 정보의 경우, 전문적인 인간 번역을 권장합니다. 이 번역 사용으로 인해 발생하는 오해나 잘못된 해석에 대해 책임을 지지 않습니다.