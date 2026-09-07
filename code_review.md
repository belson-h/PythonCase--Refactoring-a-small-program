# Kodgranskning av legacy_order_report

## Utgångsläge
Scriptet går att köra och sparar fyra rapporter i output-mappen: `overview.csv`, `sales_by_category.csv`, `sales_by_region.csv`, `returns_by_category.csv` som tillsammans ger en säljöversikt. 

## Granskningsfynd

### Fynd 1 - Projektstruktur/Ansvarsområden

**Observation:** Scriptet blandar olika ansvarsområden som filhantering, validering, transformation, rapportering och programflöde i ett enda linjärt block.

**Konsekvens:** Det blir svårt att förstå, testa och vidareutveckla koden eftersom inget kan användas eller kontrolleras isolerat. En ändring i en del (tex hur regioner rensas) riskerar att påverka andra delar av samma block.

**Förslag:** Dela upp koden i moduler med tydliga ansvar, t.ex. inläsning, validering, transformation, rapportering och en tydlig startpunkt `(main())`.

### Fynd 2 - Löpande kod, skriv om till funktioner

**Observation:** Koden körs som ett långt, löpande skript på toppnivå istället för att vara uppdelad i funktioner.

**Konsekvens:** Koden går inte att återanvända eller testa i mindre delar. Allt körs så fort filen importeras eller startas, vilket gör det omöjligt att tex bara köra valideringen eller en enskild beräkning separat.

**Förslag:** Bryt ut logiska steg i egna funktioner, tex `load_orders()`, `validate_columns()`, `calculate_order_value()`, `summarize_by_category()`.


### Fynd 3 - Centrala regler saknar tydliga tester

**Observation:** Beräkningar som `order_value`, `discounted_value` och `return_rate`, samt hanteringen av saknade/ogiltiga värden (tex `fillna(median)`), testas inte separat, de är inbäddade i ett enda script utan funktioner.

**Konsekvens:** För att kontrollera reglerna måste hela scriptet köras och resultatfilen läsas manuellt. Testerna blir långsamma, och det går inte att isolera vilken beräkning som gick fel.

**Förslag:** Bryt ut beräkningarna till egna, testbara funktioner och skriv pytest-tester mot dem direkt, utan filsystemet.


### Fynd 4 - Statusmeddelande använder print

**Observation:** `print()` används genomgående för att beskriva händelser i programmets körning (tex "Läste in ... rader", "Sparade overview.csv"). 

**Konsekvens:** Det går inte att styra nivå, format, destination på meddelandena, och det framgår inte vilken modul som skapade meddelandet.

**Förslag:** Ersätt `print()` med modulloggers (`logger = logging.getLogger(__name__)`) och konfigurera loggning centralt vid programmets startpunkt.


### Fynd 5 - Bred och otydlig felhantering

**Observation:** Koden använder `raise Exception("Fel data")` för valideringsfel, och ett enda yttre `except Exception as error: print(...)` fångar allt som kan gå fel i hela scriptet.

**Konsekvens:** Ett riktigt programmeringsfel (t.ex. en bugg i koden eller en saknad output-mapp) ser likadant ut som ett förväntat datavalideringsfel. Användaren får ett generiskt meddelande som inte hjälper till att förstå vad som faktiskt gick fel, och felet syns bara som text i terminalen istället för att kunna hanteras programmatiskt.

**Förslag:** Använd specifika undantag (t.ex. en egen `MissingColumnsError` eller inbyggda som `FileNotFoundError`) och fånga bara de fel som faktiskt förväntas kunna uppstå. Låt oväntade fel gå vidare istället för att tystas.


### Fynd 6 - Duplicerad aggregeringslogik

**Observation:** `result1` (per kategori), `result2` (per region) och `returns_by_category` följer samma mönster: groupby → agg → avrunda → beräkna return_rate → sortera → spara till CSV, men koden är skriven separat tre gånger med endast smärre variationer.

**Konsekvens:** Samma logik måste underhållas på tre ställen. En ändring (tex hur `return_rate` avrundas) riskerar att bara göras på ett eller två av de tre ställena, vilket kan ge inkonsekventa rapporter.

**Förslag:** Bryt ut mönstret till en återanvändbar funktion, tex `summarize_by(data, group_column, sort_by)`, som de tre rapporterna sedan
anropar med olika parametrar.

### Fynd 7 - Hårdkodade sökvägar och tyst datahantering

**Observation:** `INPUT_FILE` och `OUTPUT_FOLDER` är hårdkodade konstanter i scriptet. Saknade eller ogiltiga värden fylls dessutom tyst (`fillna(median)`, `fillna(1)`, `fillna("Unknown")`) utan att detta loggas eller går att konfigurera.

**Konsekvens:** Koden går inte att återanvända mot annan indata eller annan utdatamapp utan att redigera själva scriptet. Tyst datarensning gör det
dessutom svårt att upptäcka och undersöka datakvalitetsproblem, eftersom inget varnar om att t.ex. många rader saknade ett pris.

**Förslag:** Gör sökvägar konfigurerbara (tex via `ReportConfig`-dataclass eller funktionsargument) och logga en varning när värden fylls i eller rensas, så att det syns hur mycket av datan som faktiskt var ren från början.