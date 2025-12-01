# Testiplaan (täida tudengi poolt)

_Kasuta `docs/testplan-template.md` skeemi ja asenda see fail valminud dokumendiga._

- Projekti nimi: Testimisprojekt kombineeritud
- Autorid ja kuupäev: Jelizaveta Ostapjuk, 01.12.2024
- Versioon: 1.0

## 1. Sissejuhatus
Eesmärk:
Käesoleva testiplaani eesmärk on struktureerida mitmefaasilise õppeprojekti testimisstrateegia, mis hõlmab FastAPI backendit, HTML/JS frontendit, Google Analytics 4 integratsiooni, A/B eksperimente ning koormustes timist. Testimine tagab, et kõik komponendid töötavad usaldusväärselt nii eraldiseisvalt kui ka koostöös.

Kontekst:
Projekt on õppekeskkond, mis simuleerib reaalset tootearendust. Süsteem integreerub väliste API-dega (JSONPlaceholder, Rick & Morty API), jälgib kasutajategevusi GA4 abil, rakendab A/B testimist layout-variantide vahel ja pakub REST API backendit. Kogu testimine on automatiseeritud CI/CD pipeline'i kaudu.

## 2. Ulatus
Kaasatud komponendid

Backend (FastAPI):

/api/koond endpoint, mis integreerub JSONPlaceholder ja Rick & Morty API-dega
JSON skeemi normaliseerimine ja valideerimine
Veakäsitlus ja ajatempli formaatide kontroll


Frontend (HTML/JS):

Andmete kuvamine backendist
A/B testimise variandid (kaks erinevat layout'i)
Kasutaja eelistuste säilitamine localStorage-is
Variant toggle funktsioon


Google Analytics 4:

gtag.js integreerimine
Kohandatud sündmused: variant_vaade, variant_vahetus
Sündmuste logimine ja valideerimine


Automaattestimine:

Pytest ühiktestid (vähemalt 5 testi)
Jest testid (vähemalt 4 testi)
Integratsioonitestid FastAPI kliendiga
Locust koormustestid (20-50 kasutajat)


CI/CD:

GitHub Actions workflow
Automaatne testimine igal commit'il
Testitulemuste artefaktid



Välistatud komponendid

Väliste API-de (JSONPlaceholder, Rick & Morty) sisemine loogika
Tootmiskeskkonna deploy (kasutatakse ainult lokaalset ja CI keskkonda)
Manuaalne UX/UI disaini testimine
Turvatestid ja penetratsioonitestimine
Andmebaasi püsivus (projekt kasutab API-sid, mitte DB-d)

## 3. Nõuded ja aktsepteerimiskriteeriumid
Funktsionaalsed nõuded
Backend pärib JSONPlaceholder ja Rick & Morty andmeid - /api/koond tagastab normaliseeritud JSON skeemi mõlemast allikast

Frontend kuvab backend andmeid - index.html renderdab API vastuse kasutajale loetavas vormis

A/B variandid on vaheldatavad - Kasutaja saab toggle nupuga vahetada kahe layout'i vahel

Variandi eelistus säilib - localStorage salvestab valitud variandi, mis taastatakse lehekülje laadimisel

GA4 sündmused logitakse - variant_vaade ja variant_vahetus sündmused saadetakse GA4-le

Veakäsitlus töötab - API vead (timeouts, 404 jne) tagastavad selged veateated


Mittefunktsionaalsed nõuded
API vastusaeg - /api/koond endpoint vastab < 2 sekundiga normaal koormusel

Koodi katvus - Pytest katvus ≥ 70%, Jest katvus ≥ 60%

Koormustaluvus - Süsteem töötab stabiilselt 50 samaaegse kasutajaga 3 minuti jooksul

Andmete formaadi järjekindlus - Kõik API vastused vastavad määratletud JSON skeemile

Brauseriühilduvus - Frontend töötab Chrome, Firefox, Safari viimastes versioonides


Aktsepteeritavuse kontroll-leht
 1.Kõik 5+ pytest testi mööduvad
 2.Kõik 4+ Jest testi mööduvad
 3.Integratsioonitestid kinnitavad API kliendi koostoimet
 4.Locust koormustest näitab vastuvõetavaid vastusaegu
 5.GA4 sündmused on dokumenteeritud docs/results/analytics/
 6.GitHub Actions pipeline töötab vigadeta
 7.Kõik tulemused on arhiveeritud docs/results/

## 4. Riskid ja maandus
Väliste API-de (JSONPlaceholder, Rick & Morty) kättesaamatus - Mõju 5 - Tõenäosus 3 - Mock-vastuste kasutamine testides, retry-loogika, timeout seadistamine

localStorage ei toeta vanemad brauserid - Mõju 2 - Tõenäosus 2 - Fallback in-memory salvestusele, brauseri kontroll

GA4 sündmused ei jõua kohale (ad-blockerid) - Mõju 3 - Tõenäosus 4 - DebugView kasutamine testimiseks, dokumenteerida piirangud

CI/CD pipeline ebaõnnestub sõltuvuste muutumise tõttu - Mõju 4 - Tõenäosus 3 - Fikseeritud versioonid requirements.txt ja package.json, cache kasutamine

Locust koormustest koormab üle lokaalse masina - Mõju 3 - Tõenäosus 4 - Koormus parameetrite vähendamine (20 kasutajat, 3 min), headless režiim

Testandmete puudumine või ebapiisavus - Mõju 3 - Tõenäosus 3 - Mock API vastused, fixtures failide kasutamine

Ebapiisav dokumenteerimine tulemuste kohta - Mõju 4 - Tõenäosus 4 - Template'ide kasutamine, struktureeritud docs/results/ kaustad

## 5. Meetodid ja tööriistad
Testimise liigid

Ühiktestimine: Üksikute funktsioonide ja komponentide testimine

Backend: API endpoint loogika, JSON skeem a valideerimine, veakäsitlus
Frontend: A/B toggle loogika, localStorage operatsioonid, GA4 sündmuse keha


Integratsioonitestimine: Komponentide vahelise koostöö kontrollimine

FastAPI klient + mock API vastused
Frontend + backend API integratsioon


A/B testimine: Kahe layout-variandi võrdlemine

Variant A vs Variant B kasutajakogemus
GA4 sündmuste mõõtmine


Koormustestimine: Süsteemi jõudluse kontrollimine

Locust simulatsioon 20-50 kasutajaga
Vastusaegade ja läbilaskevõime mõõtmine

Tööriistad
Backend - FastAPI + Uvicorn - REST API raamistik ja server

Frontend - HTML/JS + http.server - Lihtne staatline serverimine (port 4173)

Backend testid - pytest - Python ühik- ja integratsioonitestid

Frontend testid - Jest - JavaScript ühiktestid

API mocking - responses teek -  HTTP päringute mockimine

Koormustestimine - Locust - HTTP koormu se simuleerimine

Analüütika - Google Analytics 4 - Kasutajasündmuste jälgimine

CI/CD - GitHub Actions - Automaatne testimine

Versioonihaldu s - Git + GitHub - Koodi ja tulemuste versioonihaldus


Seadistused
Backend:

backend/requirements.txt - Python sõltuvused (FastAPI, uvicorn, httpx, pytest jne)
Käivitamine: uvicorn backend.main:rakendus --reload


Frontend:

frontend/package.json - Jest ja sõltuvused
Käivitamine: python -m http.server 4173


Pytest:

Konfiguratsioon: pytest.ini või pyproject.toml
Käivitamine: pytest tests-python tests-integration -v


Jest:

Konfiguratsioon: tests-js/package.json
Käivitamine: cd tests-js && npm test


Locust:

Fail: tests-performance-locust/locustfile.py
Käivitamine: locust -f tests-performance-locust/locustfile.py --headless -u 20 -r 2 --run-time 3m --host http://localhost:8000


GitHub Actions:

Workflow: .github/workflows/tests.yml
Käivitab pytest ja Jest testid, salvestab artefaktid

## 6. Testkeskkonnad ja andmed
Lokaalne (Windows) - Windows 11 - Python 3.11+ - Node.js 18+ - Backend port 8000 - Frontend port 4173

Virtuaalkeskkond

Python: .venv kaust projekti juurkaustas
Aktiveerimine:

Windows PowerShell: .\.venv\Scripts\Activate.ps1



Testandmete strateegia

Välised API-d (tootmine):

JSONPlaceholder: https://jsonplaceholder.typicode.com/
Rick & Morty API: https://rickandmortyapi.com/api/


Mock-andmed (testimine):

responses teek pytest integratsioonitestides
Fixtures JSON failid (kui kasutatakse)
Fikseeritud vastused etteaimatavaks testimiseks


GA4 andmed:

Measurement ID: [Teie GA4 ID]
DebugView testimiseks arenduskeskkonnas
Testandmed: docs/results/analytics/ kaustast



Sõltuvuste haldus

Python: backend/requirements.txt
JavaScript: tests-js/package.json
Versioonihaldu s Git'is, täpsed versioonid fikseeritud

## 7. Ajajoon ja vastutajad
Ülesanne 1: Testiplaan (1 tund)

Ülesanne 2-3: Backend ja Frontend (2 tundi)

Ülesanne 4-5: GA4 ja A/B (1.5 tundi)

Ülesanne 6-7: Testide kirjutamine (2 tundi)

Ülesanne 8-9: Integratsioon ja CI (1.5 tundi)

Ülesanne 10: Locust koormustestid (1 tund)

Ülesanne 11: Dokumenteerimine (1 tund)


## 8. Raporteerimine
Aruannete formaadid

Pytest raportid: Terminal verbose output (-v), HTML raport (pytest-html plugin)
Jest raportid: JSON ja terminal output
Integratsioonitestide raportid: Logifailid docs/results/integration/
Locust raportid: HTML raport ja CSV statistika
GA4 raportid: Screenshot'id DebugView'st, sündmuste JSON näited
CI raportid: GitHub Actions logid ja artefaktid
Kokkuvõtlik dokument: docs/results/test-summary.md


Edukriteeriumid

Pytest: Kõik 5+ testi mööduvad, katvus ≥ 70%
Jest: Kõik 4+ testi mööduvad, katvus ≥ 60%
Integratsioonitestid: FastAPI klient töötab mock-vastustega vigadeta
Locust: 95% päringuid < 2s vastusajaga, 0% ebaõnnestumisi
GA4: Mõlemad sündmused (variant_vaade, variant_vahetus) logitud
CI/CD: GitHub Actions pipeline töötab rohelist märguannet
Dokumentatsioon: Kõik tulemused arhiveeritud struktureeritud kujul

Aruandluse sagedus

Iga ülesande lõpus: Konkreetse ülesande tulemused dokumenteeritud
Projekti lõpus: Koondraport docs/results/test-summary.md valmis
CI/CD: Automaatsed raportid igal push'il GitHub'i

Failide linkimine

README.md sisaldab viiteid kõigile põhidokumentidele
Testiplaan viitab tulemustele docs/results/
CI artefaktid linkitud GitHub Actions tab'ilt
