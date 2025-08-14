<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "2e782fc6226cf5e2b5625b035d35e60a",
  "translation_date": "2025-08-11T10:55:20+00:00",
  "source_file": "02-Security/README.md",
  "language_code": "es"
}
-->
# Mejores Prácticas de Seguridad

[![MCP Security Best Practices](../../../translated_images/03.175aed6dedae133f9d41e49cefd0f0a9a39c3317e1eaa7ef7182696af7534308.es.png)](https://youtu.be/88No8pw706o)

_(Haz clic en la imagen de arriba para ver el video de esta lección)_

Dado que la seguridad es un aspecto tan importante, la priorizamos como nuestra segunda sección. Esto está alineado con el principio de **Seguridad desde el diseño** de la [Iniciativa de Futuro Seguro](https://www.microsoft.com/en-us/security/blog/2025/04/17/microsofts-secure-by-design-journey-one-year-of-success/) de Microsoft.

Adoptar el Protocolo de Contexto de Modelo (MCP) aporta capacidades poderosas a las aplicaciones impulsadas por IA, pero también introduce desafíos de seguridad únicos que van más allá de los riesgos tradicionales del software. Además de preocupaciones ya conocidas como la codificación segura, el principio de privilegio mínimo y la seguridad en la cadena de suministro, MCP y las cargas de trabajo de IA enfrentan nuevas amenazas como inyección de prompts, envenenamiento de herramientas, modificación dinámica de herramientas, secuestro de sesiones, ataques de delegado confundido y vulnerabilidades de paso de tokens. Si no se gestionan adecuadamente, estos riesgos pueden llevar a la exfiltración de datos, violaciones de privacidad y comportamientos no deseados del sistema.

Esta lección explora los riesgos de seguridad más relevantes asociados con MCP, incluyendo autenticación, autorización, permisos excesivos, inyección indirecta de prompts, seguridad de sesiones, problemas de delegado confundido, vulnerabilidades de paso de tokens y vulnerabilidades en la cadena de suministro, y proporciona controles prácticos y mejores prácticas para mitigarlos. También aprenderás cómo aprovechar soluciones de Microsoft como Prompt Shields, Azure Content Safety y GitHub Advanced Security para fortalecer tu implementación de MCP. Al comprender y aplicar estos controles, puedes reducir significativamente la probabilidad de una brecha de seguridad y garantizar que tus sistemas de IA sean robustos y confiables.

# Objetivos de Aprendizaje

Al final de esta lección, podrás:

- Identificar y explicar los riesgos de seguridad únicos introducidos por el Protocolo de Contexto de Modelo (MCP), incluyendo inyección de prompts, envenenamiento de herramientas, permisos excesivos, secuestro de sesiones, problemas de delegado confundido, vulnerabilidades de paso de tokens y vulnerabilidades en la cadena de suministro.
- Describir y aplicar controles efectivos para mitigar los riesgos de seguridad de MCP, como autenticación robusta, privilegio mínimo, gestión segura de tokens, controles de seguridad de sesiones y verificación de la cadena de suministro.
- Comprender y aprovechar soluciones de Microsoft como Prompt Shields, Azure Content Safety y GitHub Advanced Security para proteger MCP y las cargas de trabajo de IA.
- Reconocer la importancia de validar metadatos de herramientas, monitorear cambios dinámicos, defenderse contra ataques de inyección indirecta de prompts y prevenir el secuestro de sesiones.
- Integrar mejores prácticas de seguridad establecidas, como codificación segura, endurecimiento de servidores y arquitectura de confianza cero, en tu implementación de MCP para reducir la probabilidad e impacto de brechas de seguridad.

# Controles de seguridad de MCP

Cualquier sistema que tenga acceso a recursos importantes implica desafíos de seguridad. Estos desafíos generalmente pueden abordarse mediante la aplicación correcta de controles y conceptos de seguridad fundamentales. Dado que MCP es una especificación recién definida, está evolucionando rápidamente y, a medida que el protocolo evoluciona, los controles de seguridad dentro de él madurarán, permitiendo una mejor integración con arquitecturas de seguridad empresariales y mejores prácticas ya establecidas.

Investigaciones publicadas en el [Informe de Defensa Digital de Microsoft](https://aka.ms/mddr) indican que el 98% de las brechas reportadas podrían prevenirse con una higiene de seguridad robusta, y la mejor protección contra cualquier tipo de brecha es establecer una base sólida de higiene de seguridad, mejores prácticas de codificación segura y seguridad en la cadena de suministro. Estas prácticas probadas y comprobadas siguen siendo las que más impacto tienen en la reducción del riesgo de seguridad.

Veamos algunas formas en las que puedes comenzar a abordar los riesgos de seguridad al adoptar MCP.

> **Nota:** La siguiente información es correcta al **29 de mayo de 2025**. El protocolo MCP está evolucionando continuamente, y las implementaciones futuras pueden introducir nuevos patrones y controles de autenticación. Para las actualizaciones y guías más recientes, consulta siempre la [Especificación de MCP](https://spec.modelcontextprotocol.io/), el [repositorio oficial de GitHub de MCP](https://github.com/modelcontextprotocol) y la [página de mejores prácticas de seguridad](https://modelcontextprotocol.io/specification/draft/basic/security_best_practices).

### Declaración del problema
La especificación original de MCP asumía que los desarrolladores escribirían su propio servidor de autenticación. Esto requería conocimiento de OAuth y restricciones de seguridad relacionadas. Los servidores MCP actuaban como Servidores de Autorización OAuth 2.0, gestionando la autenticación de usuarios directamente en lugar de delegarla a un servicio externo como Microsoft Entra ID. A partir del **26 de abril de 2025**, una actualización de la especificación de MCP permite que los servidores MCP deleguen la autenticación de usuarios a un servicio externo.

### Riesgos
- Una lógica de autorización mal configurada en el servidor MCP puede llevar a la exposición de datos sensibles y a la aplicación incorrecta de controles de acceso.
- Robo de tokens OAuth en el servidor MCP local. Si se roba, el token puede usarse para suplantar al servidor MCP y acceder a recursos y datos del servicio para el cual se emitió el token OAuth.

#### Paso de Tokens
El paso de tokens está explícitamente prohibido en la especificación de autorización, ya que introduce varios riesgos de seguridad, que incluyen:

#### Circunvención de Controles de Seguridad
El servidor MCP o las API descendentes podrían implementar controles de seguridad importantes como limitación de velocidad, validación de solicitudes o monitoreo de tráfico, que dependen de la audiencia del token u otras restricciones de credenciales. Si los clientes pueden obtener y usar tokens directamente con las API descendentes sin que el servidor MCP los valide adecuadamente o garantice que los tokens se emitan para el servicio correcto, se eluden estos controles.

#### Problemas de Responsabilidad y Auditoría
El servidor MCP no podrá identificar o distinguir entre clientes MCP cuando estos llamen con un token de acceso emitido por un servicio ascendente que puede ser opaco para el servidor MCP.  
Los registros del servidor de recursos descendente pueden mostrar solicitudes que parecen provenir de una fuente diferente con una identidad distinta, en lugar del servidor MCP que realmente está reenviando los tokens.  
Ambos factores dificultan la investigación de incidentes, los controles y la auditoría.  
Si el servidor MCP pasa tokens sin validar sus afirmaciones (por ejemplo, roles, privilegios o audiencia) u otros metadatos, un actor malicioso en posesión de un token robado puede usar el servidor como un proxy para la exfiltración de datos.

#### Problemas de Confianza
El servidor de recursos descendente otorga confianza a entidades específicas. Esta confianza podría incluir suposiciones sobre el origen o patrones de comportamiento del cliente. Romper este límite de confianza podría generar problemas inesperados.  
Si el token es aceptado por múltiples servicios sin una validación adecuada, un atacante que comprometa un servicio puede usar el token para acceder a otros servicios conectados.

#### Riesgo de Compatibilidad Futura
Incluso si un servidor MCP comienza como un "proxy puro" hoy, podría necesitar agregar controles de seguridad más adelante. Comenzar con una separación adecuada de la audiencia del token facilita la evolución del modelo de seguridad.

### Controles de mitigación

**Los servidores MCP NO DEBEN aceptar tokens que no hayan sido emitidos explícitamente para el servidor MCP**

- **Revisar y Fortalecer la Lógica de Autorización:** Audita cuidadosamente la implementación de autorización de tu servidor MCP para garantizar que solo los usuarios y clientes previstos puedan acceder a recursos sensibles. Para orientación práctica, consulta [Azure API Management Your Auth Gateway For MCP Servers | Microsoft Community Hub](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690) y [Using Microsoft Entra ID To Authenticate With MCP Servers Via Sessions - Den Delimarsky](https://den.dev/blog/mcp-server-auth-entra-id-session/).  
- **Aplicar Prácticas Seguras de Tokens:** Sigue las [mejores prácticas de Microsoft para la validación y duración de tokens](https://learn.microsoft.com/en-us/entra/identity-platform/access-tokens) para prevenir el mal uso de tokens de acceso y reducir el riesgo de reproducción o robo de tokens.  
- **Proteger el Almacenamiento de Tokens:** Siempre almacena los tokens de forma segura y utiliza cifrado para protegerlos tanto en reposo como en tránsito. Para consejos de implementación, consulta [Use secure token storage and encrypt tokens](https://youtu.be/uRdX37EcCwg?si=6fSChs1G4glwXRy2).

# Permisos excesivos para servidores MCP

### Declaración del problema
Los servidores MCP pueden haber recibido permisos excesivos para el servicio/recurso al que están accediendo. Por ejemplo, un servidor MCP que forma parte de una aplicación de ventas basada en IA que se conecta a un almacén de datos empresarial debería tener acceso limitado a los datos de ventas y no estar autorizado para acceder a todos los archivos del almacén. Siguiendo el principio de privilegio mínimo (uno de los principios de seguridad más antiguos), ningún recurso debería tener permisos que excedan lo necesario para ejecutar las tareas para las que fue diseñado. La IA presenta un desafío adicional en este ámbito porque, para permitir flexibilidad, puede ser difícil definir los permisos exactos requeridos.

### Riesgos
- Otorgar permisos excesivos puede permitir la exfiltración o modificación de datos que el servidor MCP no estaba destinado a acceder. Esto también podría ser un problema de privacidad si los datos son información personal identificable (PII).

### Controles de mitigación
- **Aplicar el Principio de Privilegio Mínimo:** Otorga al servidor MCP solo los permisos mínimos necesarios para realizar sus tareas requeridas. Revisa y actualiza regularmente estos permisos para garantizar que no excedan lo necesario. Para orientación detallada, consulta [Secure least-privileged access](https://learn.microsoft.com/entra/identity-platform/secure-least-privileged-access).  
- **Usar Control de Acceso Basado en Roles (RBAC):** Asigna roles al servidor MCP que estén estrictamente limitados a recursos y acciones específicas, evitando permisos amplios o innecesarios.  
- **Monitorear y Auditar Permisos:** Monitorea continuamente el uso de permisos y audita los registros de acceso para detectar y remediar privilegios excesivos o no utilizados de manera oportuna.

# Ataques de inyección indirecta de prompts

### Declaración del problema

Los servidores MCP maliciosos o comprometidos pueden introducir riesgos significativos al exponer datos de clientes o habilitar acciones no deseadas. Estos riesgos son especialmente relevantes en cargas de trabajo basadas en IA y MCP, donde:

- **Ataques de Inyección de Prompts:** Los atacantes incrustan instrucciones maliciosas en prompts o contenido externo, haciendo que el sistema de IA realice acciones no deseadas o filtre datos sensibles. Más información: [Prompt Injection](https://simonwillison.net/2025/Apr/9/mcp-prompt-injection/)  
- **Envenenamiento de Herramientas:** Los atacantes manipulan metadatos de herramientas (como descripciones o parámetros) para influir en el comportamiento de la IA, potencialmente eludiendo controles de seguridad o exfiltrando datos. Detalles: [Tool Poisoning](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks)  
- **Inyección de Prompts entre Dominios:** Instrucciones maliciosas se incrustan en documentos, páginas web o correos electrónicos, que luego son procesados por la IA, lo que lleva a filtraciones de datos o manipulaciones.  
- **Modificación Dinámica de Herramientas (Rug Pulls):** Las definiciones de herramientas pueden cambiarse después de la aprobación del usuario, introduciendo nuevos comportamientos maliciosos sin que el usuario lo sepa.

Estas vulnerabilidades destacan la necesidad de validación robusta, monitoreo y controles de seguridad al integrar servidores y herramientas MCP en tu entorno. Para un análisis más profundo, consulta las referencias vinculadas arriba.

![prompt-injection-lg-2048x1034](../../../translated_images/prompt-injection.ed9fbfde297ca877c15bc6daa808681cd3c3dc7bf27bbbda342ef1ba5fc4f52d.es.png)

**Inyección Indirecta de Prompts** (también conocida como inyección de prompts entre dominios o XPIA) es una vulnerabilidad crítica en sistemas de IA generativa, incluidos aquellos que usan el Protocolo de Contexto de Modelo (MCP). En este ataque, instrucciones maliciosas se ocultan dentro de contenido externo, como documentos, páginas web o correos electrónicos. Cuando el sistema de IA procesa este contenido, puede interpretar las instrucciones incrustadas como comandos legítimos del usuario, resultando en acciones no deseadas como filtración de datos, generación de contenido dañino o manipulación de interacciones del usuario. Para una explicación detallada y ejemplos del mundo real, consulta [Prompt Injection](https://simonwillison.net/2025/Apr/9/mcp-prompt-injection/).

Una forma particularmente peligrosa de este ataque es el **Envenenamiento de Herramientas**. Aquí, los atacantes inyectan instrucciones maliciosas en los metadatos de herramientas MCP (como descripciones o parámetros de herramientas). Dado que los modelos de lenguaje grande (LLMs) dependen de estos metadatos para decidir qué herramientas invocar, descripciones comprometidas pueden engañar al modelo para ejecutar llamadas de herramientas no autorizadas o eludir controles de seguridad. Estas manipulaciones suelen ser invisibles para los usuarios finales, pero pueden ser interpretadas y ejecutadas por el sistema de IA. Este riesgo se incrementa en entornos de servidores MCP alojados, donde las definiciones de herramientas pueden actualizarse después de la aprobación del usuario, un escenario a veces denominado "[rug pull](https://www.wiz.io/blog/mcp-security-research-briefing#remote-servers-22)". En tales casos, una herramienta que anteriormente era segura puede modificarse posteriormente para realizar acciones maliciosas, como exfiltrar datos o alterar el comportamiento del sistema, sin el conocimiento del usuario. Para más información sobre este vector de ataque, consulta [Tool Poisoning](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks).

![tool-injection-lg-2048x1239 (1)](../../../translated_images/tool-injection.3b0b4a6b24de6befe7d3afdeae44138ef005881aebcfc84c6f61369ce31e3640.es.png)

## Riesgos
Las acciones no deseadas de la IA presentan una variedad de riesgos de seguridad que incluyen exfiltración de datos y violaciones de privacidad.

### Controles de mitigación
### Uso de Prompt Shields para proteger contra ataques de inyección indirecta de prompts
-----------------------------------------------------------------------------

**AI Prompt Shields** es una solución desarrollada por Microsoft para defenderse tanto de ataques de inyección directa como indirecta de prompts. Ayudan mediante:

1.  **Detección y Filtrado:** Prompt Shields utiliza algoritmos avanzados de aprendizaje automático y procesamiento de lenguaje natural para detectar y filtrar instrucciones maliciosas incrustadas en contenido externo, como documentos, páginas web o correos electrónicos.
    
2.  **Spotlighting:** Esta técnica ayuda al sistema de IA a distinguir entre instrucciones válidas del sistema y entradas externas potencialmente no confiables. Al transformar el texto de entrada de una manera que lo haga más relevante para el modelo, Spotlighting asegura que la IA pueda identificar y ignorar mejor las instrucciones maliciosas.
    
3.  **Delimitadores y Marcado de Datos:** Incluir delimitadores en el mensaje del sistema describe explícitamente la ubicación del texto de entrada, ayudando al sistema de IA a reconocer y separar las entradas del usuario de contenido externo potencialmente dañino. El marcado de datos extiende este concepto utilizando marcadores especiales para resaltar los límites de datos confiables y no confiables.
    
4.  **Monitoreo y Actualizaciones Continuas:** Microsoft monitorea y actualiza continuamente Prompt Shields para abordar amenazas nuevas y en evolución. Este enfoque proactivo asegura que las defensas sigan siendo efectivas contra las técnicas de ataque más recientes.
5. **Integración con Azure Content Safety:** Prompt Shields son parte de la suite más amplia de Azure AI Content Safety, que proporciona herramientas adicionales para detectar intentos de jailbreak, contenido dañino y otros riesgos de seguridad en aplicaciones de IA.

Puedes leer más sobre los Prompt Shields en la [documentación de Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection).

![prompt-shield-lg-2048x1328](../../../translated_images/prompt-shield.ff5b95be76e9c78c6ec0888206a4a6a0a5ab4bb787832a9eceef7a62fe0138d1.es.png)


# Problema del Confused Deputy

### Declaración del problema

El problema del Confused Deputy es una vulnerabilidad de seguridad que ocurre cuando un servidor MCP actúa como proxy entre clientes MCP y APIs de terceros. Esta vulnerabilidad puede ser explotada cuando el servidor MCP utiliza un ID de cliente estático para autenticarse con un servidor de autorización de terceros que carece de soporte para registro dinámico de clientes.

### Riesgos

- **Elusión de consentimiento basado en cookies**: Si un usuario se ha autenticado previamente a través del servidor proxy MCP, un servidor de autorización de terceros puede establecer una cookie de consentimiento en el navegador del usuario. Un atacante puede explotar esto enviando al usuario un enlace malicioso con una solicitud de autorización manipulada que contiene un URI de redirección malicioso.
- **Robo de código de autorización**: Cuando el usuario hace clic en el enlace malicioso, el servidor de autorización de terceros puede omitir la pantalla de consentimiento debido a la cookie existente, y el código de autorización podría ser redirigido al servidor del atacante.
- **Acceso no autorizado a APIs**: El atacante puede intercambiar el código de autorización robado por tokens de acceso e impersonar al usuario para acceder a la API de terceros sin aprobación explícita.

### Controles de mitigación

- **Requisitos de consentimiento explícito**: Los servidores proxy MCP que utilizan IDs de cliente estáticos **DEBEN** obtener el consentimiento del usuario para cada cliente registrado dinámicamente antes de reenviar a servidores de autorización de terceros.
- **Implementación adecuada de OAuth**: Seguir las mejores prácticas de seguridad de OAuth 2.1, incluyendo el uso de desafíos de código (PKCE) para solicitudes de autorización para prevenir ataques de interceptación.
- **Validación de clientes**: Implementar una validación estricta de los URIs de redirección y los identificadores de cliente para prevenir la explotación por actores maliciosos.


# Vulnerabilidades de Token Passthrough

### Declaración del problema

El "Token Passthrough" es un patrón antiético donde un servidor MCP acepta tokens de un cliente MCP sin validar que los tokens fueron emitidos correctamente para el propio servidor MCP, y luego los "pasa" a APIs downstream. Esta práctica viola explícitamente la especificación de autorización de MCP e introduce graves riesgos de seguridad.

### Riesgos

- **Elusión de controles de seguridad**: Los clientes podrían eludir controles de seguridad importantes como limitación de tasa, validación de solicitudes o monitoreo de tráfico si pueden usar tokens directamente con APIs downstream sin una validación adecuada.
- **Problemas de responsabilidad y auditoría**: El servidor MCP no podrá identificar o distinguir entre clientes MCP cuando los clientes usen tokens de acceso emitidos upstream, dificultando la investigación de incidentes y la auditoría.
- **Exfiltración de datos**: Si los tokens se pasan sin una validación adecuada de las afirmaciones, un actor malicioso con un token robado podría usar el servidor como proxy para exfiltrar datos.
- **Violaciones de límites de confianza**: Los servidores de recursos downstream pueden otorgar confianza a entidades específicas con suposiciones sobre el origen o patrones de comportamiento. Romper este límite de confianza podría llevar a problemas de seguridad inesperados.
- **Uso indebido de tokens en múltiples servicios**: Si los tokens son aceptados por múltiples servicios sin una validación adecuada, un atacante que comprometa un servicio podría usar el token para acceder a otros servicios conectados.

### Controles de mitigación

- **Validación de tokens**: Los servidores MCP **NO DEBEN** aceptar ningún token que no haya sido emitido explícitamente para el propio servidor MCP.
- **Verificación de audiencia**: Siempre validar que los tokens tengan la afirmación de audiencia correcta que coincida con la identidad del servidor MCP.
- **Gestión adecuada del ciclo de vida de los tokens**: Implementar tokens de acceso de corta duración y prácticas adecuadas de rotación de tokens para reducir el riesgo de robo y uso indebido de tokens.


# Secuestro de sesión

### Declaración del problema

El secuestro de sesión es un vector de ataque donde un cliente recibe un ID de sesión del servidor, y una parte no autorizada obtiene y utiliza ese mismo ID de sesión para hacerse pasar por el cliente original y realizar acciones no autorizadas en su nombre. Esto es particularmente preocupante en servidores HTTP con estado que manejan solicitudes MCP.

### Riesgos

- **Inyección de eventos por secuestro de sesión**: Un atacante que obtenga un ID de sesión podría enviar eventos maliciosos a un servidor que comparte estado de sesión con el servidor al que está conectado el cliente, potencialmente desencadenando acciones dañinas o accediendo a datos sensibles.
- **Impersonación por secuestro de sesión**: Un atacante con un ID de sesión robado podría realizar llamadas directamente al servidor MCP, eludiendo la autenticación y siendo tratado como el usuario legítimo.
- **Streams reanudables comprometidos**: Cuando un servidor admite redelivery/streams reanudables, un atacante podría terminar una solicitud prematuramente, lo que llevaría a que se reanude más tarde por el cliente original con contenido potencialmente malicioso.

### Controles de mitigación

- **Verificación de autorización**: Los servidores MCP que implementen autorización **DEBEN** verificar todas las solicitudes entrantes y **NO DEBEN** usar sesiones para autenticación.
- **IDs de sesión seguros**: Los servidores MCP **DEBEN** usar IDs de sesión seguros y no determinísticos generados con generadores de números aleatorios seguros. Evitar identificadores predecibles o secuenciales.
- **Vinculación de sesión específica del usuario**: Los servidores MCP **DEBERÍAN** vincular los IDs de sesión a información específica del usuario, combinando el ID de sesión con información única del usuario autorizado (como su ID interno) usando un formato como `<user_id>:<session_id>`.
- **Expiración de sesión**: Implementar una expiración y rotación adecuada de sesiones para limitar la ventana de vulnerabilidad si un ID de sesión es comprometido.
- **Seguridad en el transporte**: Usar siempre HTTPS para todas las comunicaciones para prevenir la interceptación de IDs de sesión.


# Seguridad en la cadena de suministro

La seguridad en la cadena de suministro sigue siendo fundamental en la era de la IA, pero el alcance de lo que constituye tu cadena de suministro se ha ampliado. Además de los paquetes de código tradicionales, ahora debes verificar y monitorear rigurosamente todos los componentes relacionados con IA, incluidos modelos base, servicios de embeddings, proveedores de contexto y APIs de terceros. Cada uno de estos puede introducir vulnerabilidades o riesgos si no se gestionan adecuadamente.

**Prácticas clave de seguridad en la cadena de suministro para IA y MCP:**
- **Verificar todos los componentes antes de la integración:** Esto incluye no solo bibliotecas de código abierto, sino también modelos de IA, fuentes de datos y APIs externas. Siempre verifica la procedencia, licencias y vulnerabilidades conocidas.
- **Mantener pipelines de despliegue seguros:** Usar pipelines CI/CD automatizados con escaneo de seguridad integrado para detectar problemas temprano. Asegúrate de que solo artefactos confiables se desplieguen en producción.
- **Monitorear y auditar continuamente:** Implementar monitoreo continuo para todas las dependencias, incluidos modelos y servicios de datos, para detectar nuevas vulnerabilidades o ataques a la cadena de suministro.
- **Aplicar privilegios mínimos y controles de acceso:** Restringir el acceso a modelos, datos y servicios solo a lo necesario para que tu servidor MCP funcione.
- **Responder rápidamente a amenazas:** Tener un proceso en marcha para parchear o reemplazar componentes comprometidos, y para rotar secretos o credenciales si se detecta una brecha.

[GitHub Advanced Security](https://github.com/security/advanced-security) proporciona características como escaneo de secretos, escaneo de dependencias y análisis CodeQL. Estas herramientas se integran con [Azure DevOps](https://azure.microsoft.com/en-us/products/devops) y [Azure Repos](https://azure.microsoft.com/en-us/products/devops/repos/) para ayudar a los equipos a identificar y mitigar vulnerabilidades tanto en el código como en los componentes de la cadena de suministro de IA.

Microsoft también implementa prácticas extensivas de seguridad en la cadena de suministro internamente para todos los productos. Aprende más en [The Journey to Secure the Software Supply Chain at Microsoft](https://devblogs.microsoft.com/engineering-at-microsoft/the-journey-to-secure-the-software-supply-chain-at-microsoft/).


# Prácticas de seguridad establecidas que mejorarán la postura de seguridad de tu implementación MCP

Cualquier implementación MCP hereda la postura de seguridad existente del entorno de tu organización en el que se construye, por lo que al considerar la seguridad de MCP como un componente de tus sistemas de IA en general, se recomienda que mejores tu postura de seguridad existente. Los siguientes controles de seguridad establecidos son especialmente relevantes:

-   Mejores prácticas de codificación segura en tu aplicación de IA: proteger contra [el OWASP Top 10](https://owasp.org/www-project-top-ten/), el [OWASP Top 10 para LLMs](https://genai.owasp.org/download/43299/?tmstv=1731900559), uso de bóvedas seguras para secretos y tokens, implementación de comunicaciones seguras de extremo a extremo entre todos los componentes de la aplicación, etc.
-   Endurecimiento del servidor: usar MFA cuando sea posible, mantener los parches actualizados, integrar el servidor con un proveedor de identidad de terceros para el acceso, etc.
-   Mantener dispositivos, infraestructura y aplicaciones actualizados con parches.
-   Monitoreo de seguridad: implementar registro y monitoreo de una aplicación de IA (incluidos los clientes/servidores MCP) y enviar esos registros a un SIEM central para detectar actividades anómalas.
-   Arquitectura de confianza cero: aislar componentes mediante controles de red e identidad de manera lógica para minimizar el movimiento lateral si una aplicación de IA fuera comprometida.

# Puntos clave

- Los fundamentos de seguridad siguen siendo críticos: La codificación segura, el principio de privilegios mínimos, la verificación de la cadena de suministro y el monitoreo continuo son esenciales para las cargas de trabajo de MCP e IA.
- MCP introduce nuevos riesgos, como inyección de prompts, envenenamiento de herramientas, secuestro de sesión, problemas de Confused Deputy, vulnerabilidades de Token Passthrough y permisos excesivos, que requieren controles tanto tradicionales como específicos de IA.
- Utiliza prácticas robustas de autenticación, autorización y gestión de tokens, aprovechando proveedores de identidad externos como Microsoft Entra ID cuando sea posible.
- Protege contra la inyección indirecta de prompts y el envenenamiento de herramientas validando metadatos de herramientas, monitoreando cambios dinámicos y utilizando soluciones como Microsoft Prompt Shields.
- Implementa una gestión segura de sesiones utilizando IDs de sesión no determinísticos, vinculando sesiones a identidades de usuario y nunca utilizando sesiones para autenticación.
- Prevén ataques de Confused Deputy exigiendo consentimiento explícito del usuario para cada cliente registrado dinámicamente e implementando prácticas de seguridad adecuadas de OAuth.
- Evita vulnerabilidades de Token Passthrough asegurándote de que los servidores MCP solo acepten tokens emitidos explícitamente para ellos y validen las afirmaciones de los tokens de manera adecuada.
- Trata todos los componentes de tu cadena de suministro de IA, incluidos modelos, embeddings y proveedores de contexto, con el mismo rigor que las dependencias de código.
- Mantente al día con las especificaciones de MCP en evolución y contribuye a la comunidad para ayudar a establecer estándares seguros.

# Recursos adicionales

## Recursos externos
- [Microsoft Digital Defense Report](https://aka.ms/mddr)
- [Especificación MCP](https://spec.modelcontextprotocol.io/)
- [Prácticas de seguridad MCP](https://modelcontextprotocol.io/specification/draft/basic/security_best_practices)
- [Especificación de autorización MCP](https://modelcontextprotocol.io/specification/draft/basic/authorization)
- [Mejores prácticas de seguridad OAuth 2.0 (RFC 9700)](https://datatracker.ietf.org/doc/html/rfc9700)
- [Inyección de prompts en MCP (Simon Willison)](https://simonwillison.net/2025/Apr/9/mcp-prompt-injection/)
- [Ataques de envenenamiento de herramientas (Invariant Labs)](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks)
- [Rug Pulls en MCP (Wiz Security)](https://www.wiz.io/blog/mcp-security-research-briefing#remote-servers-22)
- [Documentación de Prompt Shields (Microsoft)](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP Top 10 para LLMs](https://genai.owasp.org/download/43299/?tmstv=1731900559)
- [GitHub Advanced Security](https://github.com/security/advanced-security)
- [Azure DevOps](https://azure.microsoft.com/products/devops)
- [Azure Repos](https://azure.microsoft.com/products/devops/repos/)
- [The Journey to Secure the Software Supply Chain at Microsoft](https://devblogs.microsoft.com/engineering-at-microsoft/the-journey-to-secure-the-software-supply-chain-at-microsoft/)
- [Acceso seguro con privilegios mínimos (Microsoft)](https://learn.microsoft.com/entra/identity-platform/secure-least-privileged-access)
- [Mejores prácticas para validación y duración de tokens](https://learn.microsoft.com/entra/identity-platform/access-tokens)
- [Uso de almacenamiento seguro de tokens y cifrado de tokens (YouTube)](https://youtu.be/uRdX37EcCwg?si=6fSChs1G4glwXRy2)
- [Azure API Management como puerta de autenticación para MCP](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690)
- [Uso de Microsoft Entra ID para autenticarse con servidores MCP](https://den.dev/blog/mcp-server-auth-entra-id-session/)

## Documentos adicionales de seguridad

Para obtener orientación más detallada sobre seguridad, consulta estos documentos:

- [Prácticas de seguridad MCP 2025](./mcp-security-best-practices-2025.md) - Lista completa de mejores prácticas de seguridad para implementaciones MCP
- [Implementación de Azure Content Safety](./azure-content-safety-implementation.md) - Ejemplos de implementación para integrar Azure Content Safety con servidores MCP
- [Controles de seguridad MCP 2025](./mcp-security-controls-2025.md) - Últimos controles y técnicas de seguridad para proteger despliegues MCP
- [Mejores prácticas MCP](./mcp-best-practices.md) - Guía de referencia rápida para la seguridad MCP

### Siguiente 

Siguiente: [Capítulo 3: Primeros pasos](../03-GettingStarted/README.md)

**Descargo de responsabilidad**:  
Este documento ha sido traducido utilizando el servicio de traducción automática [Co-op Translator](https://github.com/Azure/co-op-translator). Aunque nos esforzamos por garantizar la precisión, tenga en cuenta que las traducciones automatizadas pueden contener errores o imprecisiones. El documento original en su idioma nativo debe considerarse como la fuente autorizada. Para información crítica, se recomienda una traducción profesional realizada por humanos. No nos hacemos responsables de malentendidos o interpretaciones erróneas que puedan surgir del uso de esta traducción.