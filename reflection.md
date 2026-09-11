# Reflektion

**1. Vilka var de viktigaste problemen i originalkoden?**
Allt låg i ett enda linjärt script utan funktioner, vilket blandade filinläsning, validering, beräkningar och rapportering i samma block. Det gjorde koden svåre att testa och förstå, eftersom inget kunde köras eller kontrolleras isolerat. Dessutom användes `print()` istället för loggning, och felhanteringen bestod av ett brett `except Exception` som dolde vad som faktiskt gick fel.

**2. Vilka förändringar tycker du förbättrade programmet mest?**
Att bryta ut beräkningarna (`order_value`, `discounted_value`, `return_rate`) till egna funktioner gjorde störst skillnad. Det gjorde dem mer testbara och tydligare vad varje beräkning faktiskt gör. Att samla den upprepade groupby-logiken i en gemensam `summarize_by`-funktion tog också bort upprepning mellan de tre rapporterna. 

**3. Varför valde du den projektstruktur du använde?**
Strukturen följer dataflödet genom programmet: `preprocessing` (läs in och rensa) → `transformation` (beräkna) → `reporting` (sammanställ) → `io_utils` (spara). `pipeline.py` binder ihop stegen, medan `__main__.py` bara ansvarar för konfiguration och felhantering. Det gör det tydligt var i koden man ska leta beroende på vad man vill ändra, utan att dela upp programmet i fler filer än nödvändigt (som vi har fått lära oss i kursen).

**4. Var använde du OOP/dataclass och varför passade det där?**
`ReportConfig` som en frozen dataclass för sökvägar till in- och utdata. Det passade bra eftersom konfigurationen är just data utan beteende, och `frozen=True` säkerställer att den inte kan ändras av misstag mitt i en körning.

**5. Vilka viktiga beteenden skyddar dina automatiska tester, och vilken nytta ger testerna om programmet förändras i framtiden?**
Testerna säkerställer att beräkningarna (ordervärde, rabatterat värde, returandel) ger rätt resultat, att validering upptäcker saknade kolumner, och att programmet hanterar tom indata utan att krascha. Om koden ändras i framtiden, till exempel om någon justerar en formel eller lägger till en ny kolumn, fångar testerna om ett beteende oavsiktligt förändras, istället för att felet upptäcks först när en rapport ser konstig ut.

**6. Vad var svårast?** Att förstå vad som är fel när något inte fungerar, ibland är felmeddelandena rätt så otydliga och då tar det gärna ett par försök att lokalisera exakt var problemet satt. Hade också lite problem med namngivning och importer i början och att få till de "konfigurerande"-scripten/funktionerna. Att komma fram till rätt logik i testerna var också utmanande och krävde några tanke- och testrundor.

**7. Vad hade du velat förbättra ytterligare om du haft mer tid?**
Jag hade velat skriva fler tester för `reporting.py` (t.ex `summarize_by`och `build_overview`), samt lägga till någon form av validering för orimliga värden, som negativa priser, vilket originalkoden aldrig hanterade. Jag hade också velat göra sökvägarna i `ReportConfig` mer robusta, till exempel oberoende av var i terminalen man befinner sig när programmet körs.