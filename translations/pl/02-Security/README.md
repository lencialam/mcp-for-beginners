<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "2e782fc6226cf5e2b5625b035d35e60a",
  "translation_date": "2025-08-11T11:34:12+00:00",
  "source_file": "02-Security/README.md",
  "language_code": "pl"
}
-->
# Najlepsze praktyki bezpieczeństwa

[![MCP Security Best Practices](../../../translated_images/03.175aed6dedae133f9d41e49cefd0f0a9a39c3317e1eaa7ef7182696af7534308.pl.png)](https://youtu.be/88No8pw706o)

_(Kliknij obrazek powyżej, aby obejrzeć wideo z tej lekcji)_

Ponieważ bezpieczeństwo jest niezwykle istotnym aspektem, traktujemy je priorytetowo jako naszą drugą sekcję. Jest to zgodne z zasadą **Bezpieczeństwo w projektowaniu** w ramach inicjatywy Microsoftu [Secure Future Initiative](https://www.microsoft.com/en-us/security/blog/2025/04/17/microsofts-secure-by-design-journey-one-year-of-success/).

Wdrożenie Model Context Protocol (MCP) wprowadza potężne nowe możliwości dla aplikacji opartych na AI, ale jednocześnie stawia przed nami unikalne wyzwania związane z bezpieczeństwem, które wykraczają poza tradycyjne ryzyka związane z oprogramowaniem. Oprócz znanych zagrożeń, takich jak bezpieczne kodowanie, zasada najmniejszych uprawnień czy bezpieczeństwo łańcucha dostaw, MCP i obciążenia AI są narażone na nowe zagrożenia, takie jak wstrzykiwanie poleceń, zatruwanie narzędzi, dynamiczne modyfikacje narzędzi, przejęcie sesji, ataki na zdezorientowanego zastępcę oraz podatności związane z przekazywaniem tokenów. Jeśli nie zostaną odpowiednio zarządzone, te ryzyka mogą prowadzić do wycieku danych, naruszenia prywatności i niezamierzonych zachowań systemu.

Ta lekcja omawia najważniejsze zagrożenia związane z MCP, w tym uwierzytelnianie, autoryzację, nadmierne uprawnienia, pośrednie wstrzykiwanie poleceń, bezpieczeństwo sesji, problemy z zdezorientowanym zastępcą, podatności związane z przekazywaniem tokenów oraz podatności łańcucha dostaw. Przedstawia również praktyczne środki zaradcze i najlepsze praktyki, które pozwalają je zminimalizować. Dowiesz się także, jak wykorzystać rozwiązania Microsoftu, takie jak Prompt Shields, Azure Content Safety i GitHub Advanced Security, aby wzmocnić implementację MCP. Dzięki zrozumieniu i zastosowaniu tych środków możesz znacząco zmniejszyć ryzyko naruszenia bezpieczeństwa i zapewnić, że Twoje systemy AI pozostaną solidne i godne zaufania.

# Cele nauki

Po ukończeniu tej lekcji będziesz w stanie:

- Zidentyfikować i wyjaśnić unikalne zagrożenia bezpieczeństwa wprowadzone przez Model Context Protocol (MCP), w tym wstrzykiwanie poleceń, zatruwanie narzędzi, nadmierne uprawnienia, przejęcie sesji, problemy z zdezorientowanym zastępcą, podatności związane z przekazywaniem tokenów oraz podatności łańcucha dostaw.
- Opisać i zastosować skuteczne środki zaradcze dla zagrożeń bezpieczeństwa MCP, takie jak solidne uwierzytelnianie, zasada najmniejszych uprawnień, bezpieczne zarządzanie tokenami, kontrola bezpieczeństwa sesji i weryfikacja łańcucha dostaw.
- Zrozumieć i wykorzystać rozwiązania Microsoftu, takie jak Prompt Shields, Azure Content Safety i GitHub Advanced Security, aby chronić MCP i obciążenia AI.
- Rozpoznać znaczenie weryfikacji metadanych narzędzi, monitorowania dynamicznych zmian, obrony przed pośrednimi atakami wstrzykiwania poleceń oraz zapobiegania przejęciu sesji.
- Zintegrować ustalone najlepsze praktyki bezpieczeństwa, takie jak bezpieczne kodowanie, utwardzanie serwerów i architektura zero trust, w implementacji MCP, aby zmniejszyć prawdopodobieństwo i skutki naruszeń bezpieczeństwa.

# Środki bezpieczeństwa MCP

Każdy system, który ma dostęp do ważnych zasobów, wiąże się z domyślnymi wyzwaniami związanymi z bezpieczeństwem. Wyzwania te można zazwyczaj rozwiązać poprzez właściwe zastosowanie podstawowych środków i koncepcji bezpieczeństwa. Ponieważ MCP jest nowo zdefiniowanym protokołem, jego specyfikacja zmienia się bardzo szybko wraz z rozwojem protokołu. Ostatecznie środki bezpieczeństwa w nim zawarte dojrzeją, umożliwiając lepszą integrację z architekturami bezpieczeństwa przedsiębiorstw i ustalonymi najlepszymi praktykami.

Badania opublikowane w [Microsoft Digital Defense Report](https://aka.ms/mddr) wskazują, że 98% zgłoszonych naruszeń można by zapobiec dzięki solidnej higienie bezpieczeństwa, a najlepszą ochroną przed jakimkolwiek naruszeniem jest zapewnienie podstawowej higieny bezpieczeństwa, najlepszych praktyk w zakresie bezpiecznego kodowania i bezpieczeństwa łańcucha dostaw — te sprawdzone praktyki, które już znamy, nadal mają największy wpływ na zmniejszenie ryzyka bezpieczeństwa.

Przyjrzyjmy się niektórym sposobom, w jakie możesz zacząć rozwiązywać problemy związane z bezpieczeństwem podczas wdrażania MCP.

> **Note:** Poniższe informacje są aktualne na dzień **29 maja 2025**. Protokół MCP stale się rozwija, a przyszłe implementacje mogą wprowadzać nowe wzorce uwierzytelniania i środki kontroli. Aby uzyskać najnowsze informacje i wskazówki, zawsze odwołuj się do [Specyfikacji MCP](https://spec.modelcontextprotocol.io/) oraz oficjalnego [repozytorium MCP na GitHub](https://github.com/modelcontextprotocol) i [strony najlepszych praktyk bezpieczeństwa](https://modelcontextprotocol.io/specification/draft/basic/security_best_practices).

### Problem
Pierwotna specyfikacja MCP zakładała, że deweloperzy będą pisać własny serwer uwierzytelniania. Wymagało to znajomości OAuth i powiązanych ograniczeń bezpieczeństwa. Serwery MCP działały jako serwery autoryzacji OAuth 2.0, zarządzając wymaganą autoryzacją użytkownika bezpośrednio, zamiast delegować ją do zewnętrznej usługi, takiej jak Microsoft Entra ID. Od **26 kwietnia 2025** aktualizacja specyfikacji MCP pozwala serwerom MCP delegować uwierzytelnianie użytkownika do zewnętrznej usługi.

### Ryzyka
- Nieprawidłowo skonfigurowana logika autoryzacji w serwerze MCP może prowadzić do ujawnienia wrażliwych danych i nieprawidłowo zastosowanych kontroli dostępu.
- Kradzież tokenów OAuth na lokalnym serwerze MCP. Jeśli token zostanie skradziony, może być użyty do podszywania się pod serwer MCP i uzyskania dostępu do zasobów i danych z usługi, dla której token OAuth jest przeznaczony.

#### Przekazywanie tokenów
Przekazywanie tokenów jest wyraźnie zabronione w specyfikacji autoryzacji, ponieważ wprowadza szereg zagrożeń bezpieczeństwa, w tym:

#### Omijanie środków bezpieczeństwa
Serwer MCP lub API downstream mogą implementować ważne środki bezpieczeństwa, takie jak ograniczanie liczby żądań, walidacja żądań czy monitorowanie ruchu, które zależą od odbiorcy tokena lub innych ograniczeń związanych z poświadczeniami. Jeśli klienci mogą uzyskać i używać tokenów bezpośrednio z API downstream bez odpowiedniej walidacji przez serwer MCP lub upewnienia się, że tokeny są wydane dla właściwej usługi, omijają te środki.

#### Problemy z odpowiedzialnością i śladem audytowym
Serwer MCP nie będzie w stanie zidentyfikować ani rozróżnić klientów MCP, gdy klienci korzystają z tokenów dostępu wydanych upstream, które mogą być nieprzejrzyste dla serwera MCP. Logi serwera zasobów downstream mogą pokazywać żądania, które wydają się pochodzić z innego źródła o innej tożsamości, zamiast z serwera MCP, który faktycznie przekazuje tokeny. Oba czynniki utrudniają dochodzenie incydentów, kontrolę i audyt.

#### Problemy z granicą zaufania
Serwer zasobów downstream udziela zaufania określonym podmiotom. To zaufanie może obejmować założenia dotyczące pochodzenia lub wzorców zachowań klientów. Naruszenie tej granicy zaufania może prowadzić do nieoczekiwanych problemów. Jeśli token jest akceptowany przez wiele usług bez odpowiedniej walidacji, atakujący, który skompromituje jedną usługę, może użyć tokena do uzyskania dostępu do innych połączonych usług.

#### Ryzyko zgodności w przyszłości
Nawet jeśli serwer MCP zaczyna jako "czysty proxy" dzisiaj, może być konieczne dodanie środków bezpieczeństwa później. Rozpoczęcie od właściwego rozdzielenia odbiorców tokenów ułatwia rozwój modelu bezpieczeństwa.

### Środki zaradcze

**Serwery MCP NIE MOGĄ akceptować żadnych tokenów, które nie zostały wyraźnie wydane dla serwera MCP**

- **Przegląd i wzmocnienie logiki autoryzacji:** Dokładnie przeanalizuj implementację autoryzacji swojego serwera MCP, aby upewnić się, że tylko zamierzeni użytkownicy i klienci mają dostęp do wrażliwych zasobów. Praktyczne wskazówki znajdziesz w [Azure API Management Your Auth Gateway For MCP Servers | Microsoft Community Hub](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690) oraz [Using Microsoft Entra ID To Authenticate With MCP Servers Via Sessions - Den Delimarsky](https://den.dev/blog/mcp-server-auth-entra-id-session/).
- **Wymuszanie bezpiecznych praktyk dotyczących tokenów:** Postępuj zgodnie z [najlepszymi praktykami Microsoftu dotyczącymi walidacji i czasu życia tokenów](https://learn.microsoft.com/en-us/entra/identity-platform/access-tokens), aby zapobiec niewłaściwemu użyciu tokenów dostępu i zmniejszyć ryzyko ich powtórnego użycia lub kradzieży.
- **Ochrona przechowywania tokenów:** Zawsze przechowuj tokeny w sposób bezpieczny i używaj szyfrowania, aby chronić je w stanie spoczynku i w tranzycie. Wskazówki dotyczące implementacji znajdziesz w [Use secure token storage and encrypt tokens](https://youtu.be/uRdX37EcCwg?si=6fSChs1G4glwXRy2).

# Nadmierne uprawnienia dla serwerów MCP

### Problem
Serwery MCP mogą mieć przyznane nadmierne uprawnienia do usługi/zasobu, z którym się łączą. Na przykład serwer MCP będący częścią aplikacji sprzedażowej AI łączącej się z przedsiębiorstwowym magazynem danych powinien mieć dostęp ograniczony do danych sprzedażowych, a nie do wszystkich plików w magazynie. Odwołując się do zasady najmniejszych uprawnień (jednej z najstarszych zasad bezpieczeństwa), żaden zasób nie powinien mieć uprawnień przekraczających to, co jest wymagane do wykonania zamierzonych zadań. AI stawia dodatkowe wyzwania w tym obszarze, ponieważ aby umożliwić jej elastyczność, trudno jest dokładnie zdefiniować wymagane uprawnienia.

### Ryzyka 
- Przyznanie nadmiernych uprawnień może umożliwić wyciek danych lub ich modyfikację, do których serwer MCP nie powinien mieć dostępu. Może to również stanowić problem z prywatnością, jeśli dane zawierają informacje umożliwiające identyfikację osób (PII).

### Środki zaradcze
- **Zastosowanie zasady najmniejszych uprawnień:** Przyznaj serwerowi MCP tylko minimalne uprawnienia niezbędne do wykonania wymaganych zadań. Regularnie przeglądaj i aktualizuj te uprawnienia, aby upewnić się, że nie przekraczają tego, co jest potrzebne. Szczegółowe wskazówki znajdziesz w [Secure least-privileged access](https://learn.microsoft.com/entra/identity-platform/secure-least-privileged-access).
- **Użycie kontroli dostępu opartej na rolach (RBAC):** Przypisz role serwerowi MCP, które są ściśle ograniczone do konkretnych zasobów i działań, unikając szerokich lub niepotrzebnych uprawnień.
- **Monitorowanie i audyt uprawnień:** Ciągle monitoruj użycie uprawnień i audytuj logi dostępu, aby szybko wykrywać i usuwać nadmierne lub nieużywane uprawnienia.

# Pośrednie ataki wstrzykiwania poleceń

### Problem

Złośliwe lub skompromitowane serwery MCP mogą wprowadzać znaczące ryzyka, takie jak ujawnienie danych klientów lub umożliwienie niezamierzonych działań. Ryzyka te są szczególnie istotne w obciążeniach opartych na AI i MCP, gdzie:

- **Ataki wstrzykiwania poleceń**: Atakujący osadzają złośliwe instrukcje w poleceniach lub treściach zewnętrznych, powodując, że system AI wykonuje niezamierzone działania lub ujawnia wrażliwe dane. Dowiedz się więcej: [Prompt Injection](https://simonwillison.net/2025/Apr/9/mcp-prompt-injection/)
- **Zatruwanie narzędzi**: Atakujący manipulują metadanymi narzędzi (takimi jak opisy czy parametry), aby wpłynąć na zachowanie AI, potencjalnie omijając środki bezpieczeństwa lub wykradając dane. Szczegóły: [Tool Poisoning](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks)
- **Pośrednie wstrzykiwanie poleceń między domenami**: Złośliwe instrukcje są osadzane w dokumentach, stronach internetowych lub e-mailach, które są następnie przetwarzane przez AI, prowadząc do wycieku danych lub manipulacji.
- **Dynamiczne modyfikacje narzędzi (Rug Pulls)**: Definicje narzędzi mogą być zmieniane po zatwierdzeniu przez użytkownika, wprowadzając nowe złośliwe zachowania bez świadomości użytkownika.

Te podatności podkreślają potrzebę solidnej walidacji, monitorowania i środków bezpieczeństwa podczas integracji serwerów MCP i narzędzi w Twoim środowisku. Aby zgłębić temat, zobacz powiązane odnośniki powyżej.

![prompt-injection-lg-2048x1034](../../../translated_images/prompt-injection.ed9fbfde297ca877c15bc6daa808681cd3c3dc7bf27bbbda342ef1ba5fc4f52d.pl.png)

**Pośrednie wstrzykiwanie poleceń** (znane również jako wstrzykiwanie poleceń między domenami lub XPIA) to krytyczna podatność w generatywnych systemach AI, w tym tych korzystających z Model Context Protocol (MCP). W tym ataku złośliwe instrukcje są ukryte w treściach zewnętrznych — takich jak dokumenty, strony internetowe czy e-maile. Gdy system AI przetwarza tę treść, może interpretować osadzone instrukcje jako prawdziwe polecenia użytkownika, co prowadzi do niezamierzonych działań, takich jak wyciek danych, generowanie szkodliwych treści czy manipulacja interakcjami użytkownika. Szczegółowe wyjaśnienie i przykłady z życia wzięte znajdziesz w [Prompt Injection](https://simonwillison.net/2025/Apr/9/mcp-prompt-injection/).

Szczególnie niebezpieczną formą tego ataku jest **Zatruwanie narzędzi**. W tym przypadku atakujący wstrzykują złośliwe instrukcje w metadane narzędzi MCP (takie jak opisy narzędzi czy parametry). Ponieważ modele językowe (LLM) polegają na tych metadanych, aby zdecydować, które narzędzia wywołać, skompromitowane opisy mogą oszukać model, aby wykonał nieautoryzowane wywołania narzędzi lub ominął środki bezpieczeństwa. Te manipulacje są często niewidoczne dla użytkowników końcowych, ale mogą być interpretowane i wykonywane przez system AI. Ryzyko to jest szczególnie wysokie w środowiskach hostowanych serwerów MCP, gdzie definicje narzędzi mogą być aktualizowane po zatwierdzeniu przez użytkownika — scenariusz czasami określany jako "[rug pull](https://www.wiz.io/blog/mcp-security-research-briefing#remote-servers-22)". W takich przypadkach narzędzie, które wcześniej było bezpieczne, może później zostać zmodyfikowane, aby wykonywać złośliwe działania, takie jak wykradanie danych czy zmiana zachowania systemu, bez wiedzy użytkownika. Więcej na temat tego wektora ataku znajdziesz w [Tool Poisoning](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks).

![tool-injection-lg-2048x1239 (1)](
5. **Integracja z Azure Content Safety:** Prompt Shields są częścią szerszego zestawu narzędzi Azure AI Content Safety, który oferuje dodatkowe rozwiązania do wykrywania prób obejścia zabezpieczeń, szkodliwych treści i innych zagrożeń bezpieczeństwa w aplikacjach AI.

Więcej informacji o Prompt Shields znajdziesz w [dokumentacji Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection).

![prompt-shield-lg-2048x1328](../../../translated_images/prompt-shield.ff5b95be76e9c78c6ec0888206a4a6a0a5ab4bb787832a9eceef7a62fe0138d1.pl.png)


# Problem "Zdezorientowanego Zastępcy"

### Opis problemu

Problem "zdezorientowanego zastępcy" to luka w zabezpieczeniach, która występuje, gdy serwer MCP działa jako proxy między klientami MCP a zewnętrznymi API. Luka ta może być wykorzystana, gdy serwer MCP używa statycznego identyfikatora klienta do uwierzytelniania z zewnętrznym serwerem autoryzacji, który nie obsługuje dynamicznej rejestracji klientów.

### Zagrożenia

- **Obejście zgody opartej na ciasteczkach**: Jeśli użytkownik wcześniej uwierzytelnił się przez serwer proxy MCP, zewnętrzny serwer autoryzacji może ustawić ciasteczko zgody w przeglądarce użytkownika. Atakujący może później wykorzystać to, wysyłając użytkownikowi złośliwy link z spreparowanym żądaniem autoryzacji zawierającym złośliwy URI przekierowania.
- **Kradzież kodu autoryzacji**: Gdy użytkownik kliknie złośliwy link, zewnętrzny serwer autoryzacji może pominąć ekran zgody z powodu istniejącego ciasteczka, a kod autoryzacji może zostać przekierowany na serwer atakującego.
- **Nieautoryzowany dostęp do API**: Atakujący może wymienić skradziony kod autoryzacji na tokeny dostępu i podszywać się pod użytkownika, aby uzyskać dostęp do zewnętrznego API bez wyraźnej zgody.

### Środki zaradcze

- **Wymóg wyraźnej zgody**: Serwery proxy MCP używające statycznych identyfikatorów klientów **MUSZĄ** uzyskać zgodę użytkownika dla każdego dynamicznie zarejestrowanego klienta przed przekazaniem żądania do zewnętrznych serwerów autoryzacji.
- **Poprawna implementacja OAuth**: Przestrzegaj najlepszych praktyk bezpieczeństwa OAuth 2.1, w tym używania wyzwań kodowych (PKCE) dla żądań autoryzacji, aby zapobiec przechwytywaniu.
- **Walidacja klientów**: Wprowadź rygorystyczną walidację URI przekierowania i identyfikatorów klientów, aby zapobiec wykorzystaniu przez złośliwych aktorów.


# Luki w przekazywaniu tokenów

### Opis problemu

"Przekazywanie tokenów" to niezalecany wzorzec, w którym serwer MCP akceptuje tokeny od klienta MCP bez weryfikacji, czy tokeny zostały poprawnie wydane dla samego serwera MCP, a następnie "przekazuje je" do dalszych API. Praktyka ta narusza specyfikację autoryzacji MCP i wprowadza poważne zagrożenia bezpieczeństwa.

### Zagrożenia

- **Obejście mechanizmów bezpieczeństwa**: Klienci mogą obejść ważne mechanizmy bezpieczeństwa, takie jak ograniczanie liczby żądań, walidacja żądań czy monitorowanie ruchu, jeśli mogą używać tokenów bezpośrednio z dalszymi API bez odpowiedniej weryfikacji.
- **Problemy z odpowiedzialnością i śledzeniem**: Serwer MCP nie będzie w stanie zidentyfikować ani rozróżnić klientów MCP, gdy ci używają tokenów dostępu wydanych przez inne źródła, co utrudnia dochodzenie incydentów i audyt.
- **Eksfiltracja danych**: Jeśli tokeny są przekazywane bez odpowiedniej walidacji roszczeń, złośliwy aktor ze skradzionym tokenem może użyć serwera jako proxy do eksfiltracji danych.
- **Naruszenie granic zaufania**: Zasoby serwerów mogą ufać określonym podmiotom, opierając się na założeniach dotyczących pochodzenia lub wzorców zachowań. Naruszenie tej granicy zaufania może prowadzić do nieoczekiwanych problemów bezpieczeństwa.
- **Niewłaściwe użycie tokenów w wielu usługach**: Jeśli tokeny są akceptowane przez wiele usług bez odpowiedniej walidacji, atakujący, który skompromituje jedną usługę, może użyć tokenu do uzyskania dostępu do innych powiązanych usług.

### Środki zaradcze

- **Walidacja tokenów**: Serwery MCP **NIE MOGĄ** akceptować żadnych tokenów, które nie zostały wyraźnie wydane dla samego serwera MCP.
- **Weryfikacja odbiorcy**: Zawsze sprawdzaj, czy tokeny mają poprawne roszczenie odbiorcy, które odpowiada tożsamości serwera MCP.
- **Poprawne zarządzanie cyklem życia tokenów**: Wprowadź tokeny dostępu o krótkim okresie ważności oraz odpowiednie praktyki rotacji tokenów, aby zmniejszyć ryzyko kradzieży i niewłaściwego użycia tokenów.


# Przejęcie sesji

### Opis problemu

Przejęcie sesji to wektor ataku, w którym klient otrzymuje identyfikator sesji od serwera, a nieautoryzowana strona uzyskuje i używa tego samego identyfikatora sesji, aby podszywać się pod oryginalnego klienta i wykonywać nieautoryzowane działania w jego imieniu. Jest to szczególnie niepokojące w przypadku serwerów HTTP obsługujących żądania MCP w trybie stanowym.

### Zagrożenia

- **Przejęcie sesji przez wstrzyknięcie polecenia**: Atakujący, który uzyska identyfikator sesji, może wysyłać złośliwe zdarzenia do serwera, który dzieli stan sesji z serwerem, z którym połączony jest klient, potencjalnie wywołując szkodliwe działania lub uzyskując dostęp do poufnych danych.
- **Podszywanie się przez przejęcie sesji**: Atakujący ze skradzionym identyfikatorem sesji może wykonywać żądania bezpośrednio do serwera MCP, omijając uwierzytelnianie i będąc traktowanym jako legalny użytkownik.
- **Kompromitacja strumieni wznowienia**: Gdy serwer obsługuje ponowne dostarczanie/strumienie wznowienia, atakujący może przedwcześnie zakończyć żądanie, co prowadzi do jego wznowienia przez oryginalnego klienta z potencjalnie złośliwą zawartością.

### Środki zaradcze

- **Weryfikacja autoryzacji**: Serwery MCP, które implementują autoryzację, **MUSZĄ** weryfikować wszystkie przychodzące żądania i **NIE MOGĄ** używać sesji do uwierzytelniania.
- **Bezpieczne identyfikatory sesji**: Serwery MCP **MUSZĄ** używać bezpiecznych, niedeterministycznych identyfikatorów sesji generowanych za pomocą bezpiecznych generatorów liczb losowych. Unikaj przewidywalnych lub sekwencyjnych identyfikatorów.
- **Powiązanie sesji z użytkownikiem**: Serwery MCP **POWINNY** powiązać identyfikatory sesji z informacjami specyficznymi dla użytkownika, łącząc identyfikator sesji z unikalnymi informacjami o autoryzowanym użytkowniku (np. wewnętrznym identyfikatorem użytkownika) w formacie `<user_id>:<session_id>`.
- **Wygaśnięcie sesji**: Wprowadź odpowiednie wygaśnięcie sesji i rotację, aby ograniczyć okno podatności w przypadku kompromitacji identyfikatora sesji.
- **Bezpieczeństwo transportu**: Zawsze używaj HTTPS dla całej komunikacji, aby zapobiec przechwytywaniu identyfikatorów sesji.


# Bezpieczeństwo łańcucha dostaw

Bezpieczeństwo łańcucha dostaw pozostaje kluczowe w erze AI, ale zakres tego, co stanowi łańcuch dostaw, znacznie się rozszerzył. Oprócz tradycyjnych pakietów kodu, należy teraz rygorystycznie weryfikować i monitorować wszystkie komponenty związane z AI, w tym modele bazowe, usługi osadzania, dostawców kontekstu i zewnętrzne API. Każdy z tych elementów może wprowadzać luki lub zagrożenia, jeśli nie jest odpowiednio zarządzany.

**Kluczowe praktyki bezpieczeństwa łańcucha dostaw dla AI i MCP:**
- **Weryfikacja wszystkich komponentów przed integracją:** Dotyczy to nie tylko bibliotek open-source, ale także modeli AI, źródeł danych i zewnętrznych API. Zawsze sprawdzaj pochodzenie, licencjonowanie i znane luki.
- **Utrzymanie bezpiecznych pipeline'ów wdrożeniowych:** Używaj zautomatyzowanych pipeline'ów CI/CD z wbudowanym skanowaniem bezpieczeństwa, aby wykrywać problemy na wczesnym etapie. Upewnij się, że do produkcji trafiają tylko zaufane artefakty.
- **Ciągłe monitorowanie i audyt:** Wprowadź ciągłe monitorowanie wszystkich zależności, w tym modeli i usług danych, aby wykrywać nowe luki lub ataki na łańcuch dostaw.
- **Zasada najmniejszych uprawnień i kontrola dostępu:** Ogranicz dostęp do modeli, danych i usług tylko do tego, co jest niezbędne dla funkcjonowania serwera MCP.
- **Szybka reakcja na zagrożenia:** Miej proces na wypadek konieczności załatania lub wymiany skompromitowanych komponentów oraz rotacji tajemnic lub poświadczeń w przypadku wykrycia naruszenia.

[GitHub Advanced Security](https://github.com/security/advanced-security) oferuje funkcje takie jak skanowanie tajemnic, skanowanie zależności i analiza CodeQL. Narzędzia te integrują się z [Azure DevOps](https://azure.microsoft.com/en-us/products/devops) i [Azure Repos](https://azure.microsoft.com/en-us/products/devops/repos/), pomagając zespołom identyfikować i łagodzić luki w kodzie oraz komponentach łańcucha dostaw AI.

Microsoft również wdraża rozbudowane praktyki bezpieczeństwa łańcucha dostaw wewnętrznie dla wszystkich produktów. Dowiedz się więcej w [The Journey to Secure the Software Supply Chain at Microsoft](https://devblogs.microsoft.com/engineering-at-microsoft/the-journey-to-secure-the-software-supply-chain-at-microsoft/).


# Ugruntowane najlepsze praktyki bezpieczeństwa, które poprawią bezpieczeństwo implementacji MCP

Każda implementacja MCP dziedziczy istniejący poziom bezpieczeństwa środowiska organizacji, na którym jest oparta, dlatego przy rozważaniu bezpieczeństwa MCP jako elementu ogólnych systemów AI zaleca się podniesienie ogólnego poziomu bezpieczeństwa. Następujące ugruntowane mechanizmy bezpieczeństwa są szczególnie istotne:

- Najlepsze praktyki bezpiecznego kodowania w aplikacjach AI - ochrona przed [OWASP Top 10](https://owasp.org/www-project-top-ten/), [OWASP Top 10 dla LLM](https://genai.owasp.org/download/43299/?tmstv=1731900559), użycie bezpiecznych skarbców dla tajemnic i tokenów, implementacja bezpiecznej komunikacji end-to-end między wszystkimi komponentami aplikacji, itd.
- Utwardzanie serwerów - użycie MFA, regularne aktualizacje, integracja serwera z zewnętrznym dostawcą tożsamości dla dostępu, itd.
- Aktualizowanie urządzeń, infrastruktury i aplikacji za pomocą poprawek
- Monitorowanie bezpieczeństwa - implementacja logowania i monitorowania aplikacji AI (w tym klientów/serwerów MCP) oraz przesyłanie tych logów do centralnego SIEM w celu wykrywania anomalii
- Architektura zero trust - izolowanie komponentów za pomocą kontroli sieciowych i tożsamości w sposób logiczny, aby zminimalizować ruch lateralny w przypadku kompromitacji aplikacji AI.

# Kluczowe wnioski

- Podstawy bezpieczeństwa pozostają kluczowe: Bezpieczne kodowanie, zasada najmniejszych uprawnień, weryfikacja łańcucha dostaw i ciągłe monitorowanie są niezbędne dla MCP i obciążeń AI.
- MCP wprowadza nowe zagrożenia—takie jak wstrzyknięcie polecenia, zatruwanie narzędzi, przejęcie sesji, problem zdezorientowanego zastępcy, luki w przekazywaniu tokenów i nadmierne uprawnienia—które wymagają zarówno tradycyjnych, jak i specyficznych dla AI mechanizmów kontroli.
- Używaj solidnych praktyk uwierzytelniania, autoryzacji i zarządzania tokenami, korzystając z zewnętrznych dostawców tożsamości, takich jak Microsoft Entra ID, gdzie to możliwe.
- Chroń przed pośrednim wstrzyknięciem polecenia i zatruwaniem narzędzi, walidując metadane narzędzi, monitorując dynamiczne zmiany i używając rozwiązań takich jak Microsoft Prompt Shields.
- Implementuj bezpieczne zarządzanie sesjami, używając niedeterministycznych identyfikatorów sesji, powiązując sesje z tożsamościami użytkowników i nigdy nie używając sesji do uwierzytelniania.
- Zapobiegaj atakom zdezorientowanego zastępcy, wymagając wyraźnej zgody użytkownika dla każdego dynamicznie zarejestrowanego klienta i wdrażając odpowiednie praktyki bezpieczeństwa OAuth.
- Unikaj luk w przekazywaniu tokenów, upewniając się, że serwery MCP akceptują tylko tokeny wyraźnie wydane dla nich i odpowiednio walidują roszczenia tokenów.
- Traktuj wszystkie komponenty w łańcuchu dostaw AI—w tym modele, osadzenia i dostawców kontekstu—z taką samą rygorystycznością jak zależności kodu.
- Bądź na bieżąco z ewoluującymi specyfikacjami MCP i aktywnie uczestnicz w społeczności, aby pomóc kształtować bezpieczne standardy.

# Dodatkowe zasoby

## Zasoby zewnętrzne
- [Microsoft Digital Defense Report](https://aka.ms/mddr)
- [Specyfikacja MCP](https://spec.modelcontextprotocol.io/)
- [Najlepsze praktyki bezpieczeństwa MCP](https://modelcontextprotocol.io/specification/draft/basic/security_best_practices)
- [Specyfikacja autoryzacji MCP](https://modelcontextprotocol.io/specification/draft/basic/authorization)
- [Najlepsze praktyki bezpieczeństwa OAuth 2.0 (RFC 9700)](https://datatracker.ietf.org/doc/html/rfc9700)
- [Wstrzyknięcie polecenia w MCP (Simon Willison)](https://simonwillison.net/2025/Apr/9/mcp-prompt-injection/)
- [Ataki zatruwania narzędzi (Invariant Labs)](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks)
- [Rug Pulls w MCP (Wiz Security)](https://www.wiz.io/blog/mcp-security-research-briefing#remote-servers-22)
- [Dokumentacja Prompt Shields (Microsoft)](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP Top 10 dla LLM](https://genai.owasp.org/download/43299/?tmstv=1731900559)
- [GitHub Advanced Security](https://github.com/security/advanced-security)
- [Azure DevOps](https://azure.microsoft.com/products/devops)
- [Azure Repos](https://azure.microsoft.com/products/devops/repos/)
- [The Journey to Secure the Software Supply Chain at Microsoft](https://devblogs.microsoft.com/engineering-at-microsoft/the-journey-to-secure-the-software-supply-chain-at-microsoft/)
- [Bezpieczny dostęp o najmniejszych uprawnieniach (Microsoft)](https://learn.microsoft.com/entra/identity-platform/secure-least-privileged-access)
- [Najlepsze praktyki walidacji tokenów i ich żywotności](https://learn.microsoft.com/entra/identity-platform/access-tokens)
- [Użycie bezpiecznego przechowywania tokenów i ich szyfrowanie (YouTube)](https://youtu.be/uRdX37EcCwg?si=6fSChs1G4glwXRy2)
- [Azure API Management jako brama autoryzacyjna dla MCP](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp

**Zastrzeżenie**:  
Ten dokument został przetłumaczony za pomocą usługi tłumaczenia AI [Co-op Translator](https://github.com/Azure/co-op-translator). Chociaż dokładamy wszelkich starań, aby tłumaczenie było precyzyjne, prosimy pamiętać, że automatyczne tłumaczenia mogą zawierać błędy lub nieścisłości. Oryginalny dokument w jego rodzimym języku powinien być uznawany za źródło autorytatywne. W przypadku informacji o kluczowym znaczeniu zaleca się skorzystanie z profesjonalnego tłumaczenia przez człowieka. Nie ponosimy odpowiedzialności za jakiekolwiek nieporozumienia lub błędne interpretacje wynikające z użycia tego tłumaczenia.