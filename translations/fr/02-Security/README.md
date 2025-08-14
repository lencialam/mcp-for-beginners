<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "2e782fc6226cf5e2b5625b035d35e60a",
  "translation_date": "2025-08-11T10:10:11+00:00",
  "source_file": "02-Security/README.md",
  "language_code": "fr"
}
-->
# Meilleures pratiques en matière de sécurité

[![Meilleures pratiques de sécurité MCP](../../../translated_images/03.175aed6dedae133f9d41e49cefd0f0a9a39c3317e1eaa7ef7182696af7534308.fr.png)](https://youtu.be/88No8pw706o)

_(Cliquez sur l'image ci-dessus pour visionner la vidéo de cette leçon)_

Parce que la sécurité est un aspect si important, nous la plaçons en priorité dans notre deuxième section. Cela s'inscrit dans le principe **Sécurisé par conception** de l'initiative [Secure Future Initiative](https://www.microsoft.com/en-us/security/blog/2025/04/17/microsofts-secure-by-design-journey-one-year-of-success/) de Microsoft.

L'adoption du Model Context Protocol (MCP) apporte de nouvelles capacités puissantes aux applications pilotées par l'IA, mais introduit également des défis de sécurité uniques qui vont au-delà des risques logiciels traditionnels. En plus des préoccupations établies comme le codage sécurisé, le principe du moindre privilège et la sécurité de la chaîne d'approvisionnement, MCP et les charges de travail IA font face à de nouvelles menaces telles que l'injection de prompts, l'empoisonnement d'outils, la modification dynamique d'outils, le détournement de session, les attaques de type "confused deputy" et les vulnérabilités de transmission de jetons. Ces risques peuvent entraîner une exfiltration de données, des atteintes à la vie privée et des comportements système non intentionnels s'ils ne sont pas correctement gérés.

Cette leçon explore les risques de sécurité les plus pertinents associés à MCP, notamment l'authentification, l'autorisation, les permissions excessives, l'injection indirecte de prompts, la sécurité des sessions, les problèmes de "confused deputy", les vulnérabilités de transmission de jetons et les vulnérabilités de la chaîne d'approvisionnement. Elle fournit également des contrôles concrets et des meilleures pratiques pour les atténuer. Vous apprendrez également à utiliser des solutions Microsoft comme Prompt Shields, Azure Content Safety et GitHub Advanced Security pour renforcer votre implémentation MCP. En comprenant et en appliquant ces contrôles, vous pouvez réduire considérablement la probabilité d'une violation de sécurité et garantir que vos systèmes IA restent robustes et fiables.

# Objectifs d'apprentissage

À la fin de cette leçon, vous serez capable de :

- Identifier et expliquer les risques de sécurité uniques introduits par le Model Context Protocol (MCP), y compris l'injection de prompts, l'empoisonnement d'outils, les permissions excessives, le détournement de session, les problèmes de "confused deputy", les vulnérabilités de transmission de jetons et les vulnérabilités de la chaîne d'approvisionnement.
- Décrire et appliquer des contrôles d'atténuation efficaces pour les risques de sécurité MCP, tels qu'une authentification robuste, le principe du moindre privilège, une gestion sécurisée des jetons, des contrôles de sécurité des sessions et la vérification de la chaîne d'approvisionnement.
- Comprendre et utiliser des solutions Microsoft comme Prompt Shields, Azure Content Safety et GitHub Advanced Security pour protéger les charges de travail MCP et IA.
- Reconnaître l'importance de valider les métadonnées des outils, de surveiller les changements dynamiques, de se défendre contre les attaques d'injection indirecte de prompts et de prévenir le détournement de session.
- Intégrer les meilleures pratiques de sécurité établies, telles que le codage sécurisé, le renforcement des serveurs et l'architecture Zero Trust, dans votre implémentation MCP pour réduire la probabilité et l'impact des violations de sécurité.

# Contrôles de sécurité MCP

Tout système ayant accès à des ressources importantes présente des défis de sécurité implicites. Ces défis peuvent généralement être relevés grâce à une application correcte des contrôles et concepts fondamentaux de sécurité. Comme MCP est une spécification nouvellement définie, elle évolue très rapidement. À mesure que le protocole évolue, les contrôles de sécurité qu'il contient mûriront, permettant une meilleure intégration avec les architectures de sécurité d'entreprise et les meilleures pratiques établies.

Des recherches publiées dans le [Microsoft Digital Defense Report](https://aka.ms/mddr) indiquent que 98 % des violations signalées pourraient être évitées grâce à une hygiène de sécurité robuste. La meilleure protection contre tout type de violation consiste à établir une hygiène de sécurité de base, à appliquer les meilleures pratiques de codage sécurisé et à sécuriser la chaîne d'approvisionnement. Ces pratiques éprouvées restent les plus efficaces pour réduire les risques de sécurité.

Examinons certaines des façons dont vous pouvez commencer à aborder les risques de sécurité lors de l'adoption de MCP.

> **Note :** Les informations suivantes sont correctes au **29 mai 2025**. Le protocole MCP évolue continuellement, et les implémentations futures peuvent introduire de nouveaux modèles d'authentification et contrôles. Pour les dernières mises à jour et recommandations, consultez toujours la [spécification MCP](https://spec.modelcontextprotocol.io/), le [dépôt GitHub officiel MCP](https://github.com/modelcontextprotocol) et la [page des meilleures pratiques de sécurité](https://modelcontextprotocol.io/specification/draft/basic/security_best_practices).

### Énoncé du problème
La spécification originale de MCP supposait que les développeurs écriraient leur propre serveur d'authentification. Cela nécessitait une connaissance d'OAuth et des contraintes de sécurité associées. Les serveurs MCP agissaient comme des serveurs d'autorisation OAuth 2.0, gérant directement l'authentification des utilisateurs plutôt que de la déléguer à un service externe tel que Microsoft Entra ID. Depuis le **26 avril 2025**, une mise à jour de la spécification MCP permet aux serveurs MCP de déléguer l'authentification des utilisateurs à un service externe.

### Risques
- Une logique d'autorisation mal configurée dans le serveur MCP peut entraîner une exposition de données sensibles et des contrôles d'accès mal appliqués.
- Vol de jetons OAuth sur le serveur MCP local. Si volé, le jeton peut être utilisé pour usurper l'identité du serveur MCP et accéder aux ressources et données du service pour lequel le jeton OAuth est destiné.

#### Transmission de jetons
La transmission de jetons est explicitement interdite dans la spécification d'autorisation, car elle introduit plusieurs risques de sécurité, notamment :

#### Contournement des contrôles de sécurité
Le serveur MCP ou les API en aval peuvent implémenter des contrôles de sécurité importants comme la limitation de débit, la validation des requêtes ou la surveillance du trafic, qui dépendent de l'audience du jeton ou d'autres contraintes d'identification. Si les clients peuvent obtenir et utiliser directement des jetons avec les API en aval sans que le serveur MCP les valide correctement ou s'assure que les jetons sont émis pour le bon service, ils contournent ces contrôles.

#### Problèmes de responsabilité et de traçabilité
Le serveur MCP ne pourra pas identifier ou distinguer les clients MCP lorsque ceux-ci appellent avec un jeton d'accès émis en amont, qui peut être opaque pour le serveur MCP.  
Les journaux du serveur de ressources en aval peuvent montrer des requêtes provenant d'une source différente avec une identité différente, plutôt que du serveur MCP qui transmet réellement les jetons.  
Ces deux facteurs compliquent les enquêtes sur les incidents, les contrôles et les audits.  
Si le serveur MCP transmet des jetons sans valider leurs revendications (par exemple, rôles, privilèges ou audience) ou d'autres métadonnées, un acteur malveillant en possession d'un jeton volé peut utiliser le serveur comme proxy pour exfiltrer des données.

#### Problèmes de frontière de confiance
Le serveur de ressources en aval accorde sa confiance à des entités spécifiques. Cette confiance peut inclure des hypothèses sur l'origine ou les comportements des clients. Briser cette frontière de confiance pourrait entraîner des problèmes inattendus.  
Si le jeton est accepté par plusieurs services sans validation appropriée, un attaquant compromettant un service peut utiliser le jeton pour accéder à d'autres services connectés.

#### Risque de compatibilité future
Même si un serveur MCP commence comme un "proxy pur" aujourd'hui, il pourrait avoir besoin d'ajouter des contrôles de sécurité plus tard. Commencer avec une séparation appropriée des audiences des jetons facilite l'évolution du modèle de sécurité.

### Contrôles d'atténuation

**Les serveurs MCP NE DOIVENT PAS accepter de jetons qui n'ont pas été explicitement émis pour le serveur MCP**

- **Revoir et renforcer la logique d'autorisation :** Auditez soigneusement l'implémentation de l'autorisation de votre serveur MCP pour garantir que seuls les utilisateurs et clients prévus peuvent accéder aux ressources sensibles. Pour des conseils pratiques, consultez [Azure API Management Your Auth Gateway For MCP Servers | Microsoft Community Hub](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690) et [Using Microsoft Entra ID To Authenticate With MCP Servers Via Sessions - Den Delimarsky](https://den.dev/blog/mcp-server-auth-entra-id-session/).
- **Appliquer des pratiques sécurisées pour les jetons :** Suivez les [meilleures pratiques de Microsoft pour la validation et la durée de vie des jetons](https://learn.microsoft.com/en-us/entra/identity-platform/access-tokens) pour prévenir l'utilisation abusive des jetons d'accès et réduire le risque de relecture ou de vol de jetons.
- **Protéger le stockage des jetons :** Stockez toujours les jetons de manière sécurisée et utilisez le chiffrement pour les protéger au repos et en transit. Pour des conseils de mise en œuvre, consultez [Use secure token storage and encrypt tokens](https://youtu.be/uRdX37EcCwg?si=6fSChs1G4glwXRy2).

# Permissions excessives pour les serveurs MCP

### Énoncé du problème
Les serveurs MCP peuvent avoir reçu des permissions excessives pour le service ou la ressource auxquels ils accèdent. Par exemple, un serveur MCP faisant partie d'une application de vente IA se connectant à un magasin de données d'entreprise devrait avoir un accès limité aux données de vente et ne pas être autorisé à accéder à tous les fichiers du magasin. En se référant au principe du moindre privilège (l'un des plus anciens principes de sécurité), aucune ressource ne devrait avoir des permissions excédant ce qui est nécessaire pour exécuter les tâches prévues. L'IA présente un défi accru dans ce domaine, car pour permettre sa flexibilité, il peut être difficile de définir les permissions exactes requises.

### Risques
- Accorder des permissions excessives peut permettre l'exfiltration ou la modification de données que le serveur MCP n'était pas censé pouvoir accéder. Cela pourrait également poser un problème de confidentialité si les données sont des informations personnellement identifiables (PII).

### Contrôles d'atténuation
- **Appliquer le principe du moindre privilège :** Accordez au serveur MCP uniquement les permissions minimales nécessaires pour effectuer ses tâches requises. Révisez et mettez régulièrement à jour ces permissions pour vous assurer qu'elles ne dépassent pas ce qui est nécessaire. Pour des conseils détaillés, consultez [Secure least-privileged access](https://learn.microsoft.com/entra/identity-platform/secure-least-privileged-access).
- **Utiliser le contrôle d'accès basé sur les rôles (RBAC) :** Attribuez des rôles au serveur MCP qui sont strictement limités à des ressources et actions spécifiques, en évitant des permissions larges ou inutiles.
- **Surveiller et auditer les permissions :** Surveillez en continu l'utilisation des permissions et auditez les journaux d'accès pour détecter et corriger rapidement les privilèges excessifs ou inutilisés.

# Attaques d'injection indirecte de prompts

### Énoncé du problème

Les serveurs MCP malveillants ou compromis peuvent introduire des risques importants en exposant des données client ou en permettant des actions non intentionnelles. Ces risques sont particulièrement pertinents dans les charges de travail basées sur l'IA et MCP, où :

- **Attaques d'injection de prompts :** Les attaquants intègrent des instructions malveillantes dans des prompts ou du contenu externe, amenant le système IA à effectuer des actions non intentionnelles ou à divulguer des données sensibles. En savoir plus : [Prompt Injection](https://simonwillison.net/2025/Apr/9/mcp-prompt-injection/)
- **Empoisonnement d'outils :** Les attaquants manipulent les métadonnées des outils (telles que les descriptions ou les paramètres) pour influencer le comportement de l'IA, contournant potentiellement les contrôles de sécurité ou exfiltrant des données. Détails : [Tool Poisoning](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks)
- **Injection de prompts inter-domaines :** Des instructions malveillantes sont intégrées dans des documents, pages web ou e-mails, qui sont ensuite traités par l'IA, entraînant des fuites de données ou des manipulations.
- **Modification dynamique d'outils (Rug Pulls) :** Les définitions d'outils peuvent être modifiées après approbation de l'utilisateur, introduisant de nouveaux comportements malveillants sans que l'utilisateur en soit conscient.

Ces vulnérabilités soulignent la nécessité d'une validation robuste, d'une surveillance et de contrôles de sécurité lors de l'intégration des serveurs MCP et des outils dans votre environnement. Pour une analyse approfondie, consultez les références liées ci-dessus.

![prompt-injection-lg-2048x1034](../../../translated_images/prompt-injection.ed9fbfde297ca877c15bc6daa808681cd3c3dc7bf27bbbda342ef1ba5fc4f52d.fr.png)

**L'injection indirecte de prompts** (également connue sous le nom d'injection de prompts inter-domaines ou XPIA) est une vulnérabilité critique dans les systèmes d'IA générative, y compris ceux utilisant le Model Context Protocol (MCP). Dans cette attaque, des instructions malveillantes sont dissimulées dans du contenu externe—comme des documents, des pages web ou des e-mails. Lorsque le système IA traite ce contenu, il peut interpréter les instructions intégrées comme des commandes utilisateur légitimes, entraînant des actions non intentionnelles telles que des fuites de données, la génération de contenu nuisible ou la manipulation des interactions utilisateur. Pour une explication détaillée et des exemples concrets, consultez [Prompt Injection](https://simonwillison.net/2025/Apr/9/mcp-prompt-injection/).

Une forme particulièrement dangereuse de cette attaque est **l'empoisonnement d'outils**. Ici, les attaquants injectent des instructions malveillantes dans les métadonnées des outils MCP (telles que les descriptions ou les paramètres des outils). Étant donné que les modèles de langage (LLM) s'appuient sur ces métadonnées pour décider quels outils invoquer, des descriptions compromises peuvent tromper le modèle en lui faisant exécuter des appels d'outils non autorisés ou contourner les contrôles de sécurité. Ces manipulations sont souvent invisibles pour les utilisateurs finaux mais peuvent être interprétées et exécutées par le système IA. Ce risque est accru dans les environnements de serveurs MCP hébergés, où les définitions d'outils peuvent être mises à jour après approbation de l'utilisateur—un scénario parfois appelé "[rug pull](https://www.wiz.io/blog/mcp-security-research-briefing#remote-servers-22)". Dans de tels cas, un outil auparavant sûr peut être modifié ultérieurement pour effectuer des actions malveillantes, telles que l'exfiltration de données ou la modification du comportement du système, à l'insu de l'utilisateur. Pour en savoir plus sur ce vecteur d'attaque, consultez [Tool Poisoning](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks).

![tool-injection-lg-2048x1239 (1)](../../../translated_images/tool-injection.3b0b4a6b24de6befe7d3afdeae44138ef005881aebcfc84c6f61369ce31e3640.fr.png)

## Risques
Les actions non intentionnelles de l'IA présentent divers risques de sécurité, notamment l'exfiltration de données et les atteintes à la vie privée.

### Contrôles d'atténuation
### Utilisation des Prompt Shields pour se protéger contre les attaques d'injection indirecte de prompts
-----------------------------------------------------------------------------

**Les AI Prompt Shields** sont une solution développée par Microsoft pour se défendre contre les attaques d'injection de prompts, qu'elles soient directes ou indirectes. Ils aident grâce à :

1.  **Détection et filtrage :** Les Prompt Shields utilisent des algorithmes avancés d'apprentissage automatique et de traitement du langage naturel pour détecter et filtrer les instructions malveillantes intégrées dans du contenu externe, comme des documents, des pages web ou des e-mails.
    
2.  **Spotlighting :** Cette technique aide le système IA à distinguer les instructions système valides des entrées externes potentiellement non fiables. En transformant le texte d'entrée de manière à le rendre plus pertinent pour le modèle, le Spotlighting garantit que l'IA peut mieux identifier et ignorer les instructions malveillantes.
    
3.  **Délimiteurs et marquage des données :** L'inclusion de délimiteurs dans le message système définit explicitement l'emplacement du texte d'entrée, aidant le système IA à reconnaître et séparer les entrées utilisateur des contenus externes potentiellement nuisibles. Le marquage des données étend ce concept en utilisant des marqueurs spéciaux pour mettre en évidence les limites entre les données fiables et non fiables.
    
4.  **Surveillance et mises à jour continues :** Microsoft surveille et met à jour en continu les Prompt Shields pour faire face aux menaces nouvelles et évolutives. Cette approche proactive garantit que les défenses restent efficaces contre les dernières techniques d'attaque.
5. **Intégration avec Azure Content Safety :** Les Prompt Shields font partie de la suite Azure AI Content Safety, qui propose des outils supplémentaires pour détecter les tentatives de contournement, les contenus nuisibles et d'autres risques de sécurité dans les applications d'IA.

Vous pouvez en savoir plus sur les Prompt Shields dans la [documentation des Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection).

![prompt-shield-lg-2048x1328](../../../translated_images/prompt-shield.ff5b95be76e9c78c6ec0888206a4a6a0a5ab4bb787832a9eceef7a62fe0138d1.fr.png)


# Problème du "Confused Deputy"

### Énoncé du problème

Le problème du "confused deputy" est une vulnérabilité de sécurité qui se produit lorsqu'un serveur MCP agit comme un proxy entre des clients MCP et des API tierces. Cette vulnérabilité peut être exploitée lorsque le serveur MCP utilise un ID client statique pour s'authentifier auprès d'un serveur d'autorisation tiers qui ne prend pas en charge l'enregistrement dynamique des clients.

### Risques

- **Contournement du consentement basé sur les cookies** : Si un utilisateur s'est déjà authentifié via le serveur proxy MCP, un serveur d'autorisation tiers peut définir un cookie de consentement dans le navigateur de l'utilisateur. Un attaquant peut exploiter cela en envoyant à l'utilisateur un lien malveillant contenant une requête d'autorisation avec une URI de redirection malveillante.
- **Vol de code d'autorisation** : Lorsque l'utilisateur clique sur le lien malveillant, le serveur d'autorisation tiers peut ignorer l'écran de consentement en raison du cookie existant, et le code d'autorisation pourrait être redirigé vers le serveur de l'attaquant.
- **Accès non autorisé à l'API** : L'attaquant peut échanger le code d'autorisation volé contre des jetons d'accès et se faire passer pour l'utilisateur afin d'accéder à l'API tierce sans approbation explicite.

### Mesures d'atténuation

- **Exiger un consentement explicite** : Les serveurs proxy MCP utilisant des ID clients statiques **DOIVENT** obtenir le consentement de l'utilisateur pour chaque client enregistré dynamiquement avant de transmettre les requêtes aux serveurs d'autorisation tiers.
- **Mise en œuvre correcte d'OAuth** : Suivez les meilleures pratiques de sécurité OAuth 2.1, y compris l'utilisation de défis de code (PKCE) pour les requêtes d'autorisation afin de prévenir les attaques par interception.
- **Validation des clients** : Implémentez une validation stricte des URI de redirection et des identifiants des clients pour empêcher les exploitations par des acteurs malveillants.


# Vulnérabilités liées au "Token Passthrough"

### Énoncé du problème

Le "token passthrough" est une mauvaise pratique où un serveur MCP accepte des jetons d'un client MCP sans valider que ces jetons ont été correctement émis pour le serveur MCP lui-même, puis les "transmet" aux API en aval. Cette pratique viole explicitement la spécification d'autorisation MCP et introduit de graves risques de sécurité.

### Risques

- **Contournement des contrôles de sécurité** : Les clients pourraient contourner des contrôles de sécurité importants comme la limitation du débit, la validation des requêtes ou la surveillance du trafic s'ils peuvent utiliser directement des jetons avec les API en aval sans validation appropriée.
- **Problèmes de responsabilité et de traçabilité** : Le serveur MCP sera incapable d'identifier ou de distinguer les clients MCP lorsque ceux-ci utilisent des jetons d'accès émis en amont, rendant les enquêtes sur les incidents et les audits plus difficiles.
- **Exfiltration de données** : Si les jetons sont transmis sans validation appropriée des revendications, un acteur malveillant avec un jeton volé pourrait utiliser le serveur comme proxy pour exfiltrer des données.
- **Violation des frontières de confiance** : Les serveurs de ressources en aval peuvent accorder leur confiance à des entités spécifiques en se basant sur des hypothèses concernant leur origine ou leurs comportements. Briser cette frontière de confiance pourrait entraîner des problèmes de sécurité inattendus.
- **Mauvais usage des jetons multi-services** : Si les jetons sont acceptés par plusieurs services sans validation appropriée, un attaquant compromettant un service pourrait utiliser le jeton pour accéder à d'autres services connectés.

### Mesures d'atténuation

- **Validation des jetons** : Les serveurs MCP **NE DOIVENT PAS** accepter de jetons qui n'ont pas été explicitement émis pour le serveur MCP lui-même.
- **Vérification de l'audience** : Validez toujours que les jetons contiennent la revendication d'audience correcte correspondant à l'identité du serveur MCP.
- **Gestion appropriée du cycle de vie des jetons** : Implémentez des jetons d'accès de courte durée et des pratiques de rotation des jetons pour réduire les risques de vol et de mauvais usage des jetons.


# Détournement de session

### Énoncé du problème

Le détournement de session est une méthode d'attaque où un client reçoit un ID de session du serveur, et une partie non autorisée obtient et utilise ce même ID de session pour se faire passer pour le client d'origine et effectuer des actions non autorisées en son nom. Cela est particulièrement préoccupant dans les serveurs HTTP avec état qui gèrent des requêtes MCP.

### Risques

- **Injection de prompts via détournement de session** : Un attaquant qui obtient un ID de session pourrait envoyer des événements malveillants à un serveur partageant l'état de session avec le serveur auquel le client est connecté, déclenchant potentiellement des actions nuisibles ou accédant à des données sensibles.
- **Usurpation via détournement de session** : Un attaquant avec un ID de session volé pourrait effectuer des appels directement au serveur MCP, contournant l'authentification et étant traité comme l'utilisateur légitime.
- **Flux reprenables compromis** : Lorsqu'un serveur prend en charge la rediffusion ou les flux reprenables, un attaquant pourrait interrompre prématurément une requête, entraînant sa reprise ultérieure par le client d'origine avec un contenu potentiellement malveillant.

### Mesures d'atténuation

- **Vérification de l'autorisation** : Les serveurs MCP qui implémentent l'autorisation **DOIVENT** vérifier toutes les requêtes entrantes et **NE DOIVENT PAS** utiliser les sessions pour l'authentification.
- **IDs de session sécurisés** : Les serveurs MCP **DOIVENT** utiliser des IDs de session sécurisés et non déterministes générés avec des générateurs de nombres aléatoires sécurisés. Évitez les identifiants prévisibles ou séquentiels.
- **Association des sessions aux utilisateurs** : Les serveurs MCP **DEVRAIENT** associer les IDs de session à des informations spécifiques à l'utilisateur, en combinant l'ID de session avec des informations uniques à l'utilisateur autorisé (comme son ID interne) dans un format tel que `<user_id>:<session_id>`.
- **Expiration des sessions** : Implémentez une expiration et une rotation appropriées des sessions pour limiter la fenêtre de vulnérabilité en cas de compromission d'un ID de session.
- **Sécurité des transports** : Utilisez toujours HTTPS pour toutes les communications afin d'éviter l'interception des IDs de session.


# Sécurité de la chaîne d'approvisionnement

La sécurité de la chaîne d'approvisionnement reste fondamentale à l'ère de l'IA, mais la portée de ce qui constitue votre chaîne d'approvisionnement s'est élargie. En plus des packages de code traditionnels, vous devez désormais vérifier et surveiller rigoureusement tous les composants liés à l'IA, y compris les modèles fondamentaux, les services d'embeddings, les fournisseurs de contexte et les API tierces. Chacun de ces éléments peut introduire des vulnérabilités ou des risques s'il n'est pas correctement géré.

**Pratiques clés pour la sécurité de la chaîne d'approvisionnement dans l'IA et le MCP :**
- **Vérifiez tous les composants avant intégration** : Cela inclut non seulement les bibliothèques open source, mais aussi les modèles d'IA, les sources de données et les API externes. Vérifiez toujours leur provenance, leur licence et les vulnérabilités connues.
- **Maintenez des pipelines de déploiement sécurisés** : Utilisez des pipelines CI/CD automatisés avec des analyses de sécurité intégrées pour détecter les problèmes tôt. Assurez-vous que seuls des artefacts de confiance sont déployés en production.
- **Surveillez et auditez en continu** : Implémentez une surveillance continue de toutes les dépendances, y compris les modèles et les services de données, pour détecter de nouvelles vulnérabilités ou attaques sur la chaîne d'approvisionnement.
- **Appliquez le principe du moindre privilège et des contrôles d'accès** : Limitez l'accès aux modèles, aux données et aux services uniquement à ce qui est nécessaire pour le fonctionnement de votre serveur MCP.
- **Réagissez rapidement aux menaces** : Mettez en place un processus pour corriger ou remplacer les composants compromis, et pour faire tourner les secrets ou les identifiants en cas de violation détectée.

[GitHub Advanced Security](https://github.com/security/advanced-security) propose des fonctionnalités telles que l'analyse des secrets, l'analyse des dépendances et l'analyse CodeQL. Ces outils s'intègrent à [Azure DevOps](https://azure.microsoft.com/products/devops) et [Azure Repos](https://azure.microsoft.com/products/devops/repos/) pour aider les équipes à identifier et à atténuer les vulnérabilités dans les composants de code et de la chaîne d'approvisionnement de l'IA.

Microsoft met également en œuvre des pratiques de sécurité rigoureuses pour la chaîne d'approvisionnement dans tous ses produits. En savoir plus dans [The Journey to Secure the Software Supply Chain at Microsoft](https://devblogs.microsoft.com/engineering-at-microsoft/the-journey-to-secure-the-software-supply-chain-at-microsoft/).


# Bonnes pratiques de sécurité établies pour renforcer la sécurité de votre implémentation MCP

Toute implémentation MCP hérite de la posture de sécurité existante de l'environnement de votre organisation sur lequel elle est construite. Par conséquent, pour sécuriser le MCP en tant que composant de vos systèmes d'IA globaux, il est recommandé d'améliorer votre posture de sécurité globale. Les contrôles de sécurité suivants sont particulièrement pertinents :

- Bonnes pratiques de codage sécurisé dans votre application d'IA : protégez-vous contre [les 10 principaux risques OWASP](https://owasp.org/www-project-top-ten/), les [10 principaux risques OWASP pour les LLMs](https://genai.owasp.org/download/43299/?tmstv=1731900559), utilisez des coffres sécurisés pour les secrets et les jetons, implémentez des communications sécurisées de bout en bout entre tous les composants de l'application, etc.
- Renforcement des serveurs : utilisez l'authentification multifacteur (MFA) lorsque possible, maintenez les correctifs à jour, intégrez le serveur à un fournisseur d'identité tiers pour l'accès, etc.
- Maintenez les appareils, l'infrastructure et les applications à jour avec les correctifs.
- Surveillance de la sécurité : implémentez la journalisation et la surveillance d'une application d'IA (y compris les clients/serveurs MCP) et envoyez ces journaux à un SIEM central pour détecter les activités anormales.
- Architecture Zero Trust : isolez les composants via des contrôles réseau et d'identité de manière logique pour minimiser les mouvements latéraux en cas de compromission d'une application d'IA.

# Points clés à retenir

- Les fondamentaux de la sécurité restent essentiels : le codage sécurisé, le principe du moindre privilège, la vérification de la chaîne d'approvisionnement et la surveillance continue sont indispensables pour les charges de travail MCP et IA.
- Le MCP introduit de nouveaux risques — tels que l'injection de prompts, l'empoisonnement des outils, le détournement de session, les problèmes de "confused deputy", les vulnérabilités de "token passthrough" et les permissions excessives — qui nécessitent des contrôles traditionnels et spécifiques à l'IA.
- Utilisez des pratiques robustes d'authentification, d'autorisation et de gestion des jetons, en tirant parti de fournisseurs d'identité externes comme Microsoft Entra ID lorsque possible.
- Protégez-vous contre l'injection indirecte de prompts et l'empoisonnement des outils en validant les métadonnées des outils, en surveillant les changements dynamiques et en utilisant des solutions comme Microsoft Prompt Shields.
- Implémentez une gestion sécurisée des sessions en utilisant des IDs de session non déterministes, en liant les sessions aux identités des utilisateurs et en évitant d'utiliser les sessions pour l'authentification.
- Prévenez les attaques de "confused deputy" en exigeant un consentement explicite de l'utilisateur pour chaque client enregistré dynamiquement et en appliquant les bonnes pratiques de sécurité OAuth.
- Évitez les vulnérabilités de "token passthrough" en vous assurant que les serveurs MCP n'acceptent que les jetons explicitement émis pour eux et en validant correctement les revendications des jetons.
- Traitez tous les composants de votre chaîne d'approvisionnement IA — y compris les modèles, les embeddings et les fournisseurs de contexte — avec la même rigueur que les dépendances de code.
- Restez à jour avec les spécifications MCP en évolution et contribuez à la communauté pour aider à façonner des normes sécurisées.

# Ressources supplémentaires

## Ressources externes
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

## Documents de sécurité supplémentaires

Pour des conseils de sécurité plus détaillés, veuillez consulter ces documents :

- [MCP Security Best Practices 2025](./mcp-security-best-practices-2025.md) - Liste complète des meilleures pratiques de sécurité pour les implémentations MCP
- [Azure Content Safety Implementation](./azure-content-safety-implementation.md) - Exemples d'implémentation pour intégrer Azure Content Safety avec les serveurs MCP
- [MCP Security Controls 2025](./mcp-security-controls-2025.md) - Derniers contrôles et techniques de sécurité pour sécuriser les déploiements MCP
- [MCP Best Practices](./mcp-best-practices.md) - Guide de référence rapide pour la sécurité MCP

### Suivant 

Suivant : [Chapitre 3 : Premiers pas](../03-GettingStarted/README.md)

**Avertissement** :  
Ce document a été traduit à l'aide du service de traduction automatique [Co-op Translator](https://github.com/Azure/co-op-translator). Bien que nous nous efforcions d'assurer l'exactitude, veuillez noter que les traductions automatisées peuvent contenir des erreurs ou des inexactitudes. Le document original dans sa langue d'origine doit être considéré comme la source faisant autorité. Pour des informations critiques, il est recommandé de recourir à une traduction professionnelle réalisée par un humain. Nous déclinons toute responsabilité en cas de malentendus ou d'interprétations erronées résultant de l'utilisation de cette traduction.