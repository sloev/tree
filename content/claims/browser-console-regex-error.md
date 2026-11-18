---
id: "browser-console-regex-error"
schema: claim/v1
branch: "Webstedets tekniske historik"
title: "Browserfejl: Invalid regular expression flags"
status: "needs"
validation: "lead"
sources:
  - "browser-console-2026-11-18"
person_ids: []
---

## Claim

En browserkonsolrapport registrerer én sidefejl med teksten `Invalid regular expression flags`.

## Evidence

Den lokale konsolrapport indeholder fejlteksten, men ingen stack trace, filsti eller linjenummer. Fejlen er derfor registreret som et reproduktions-/diagnostik-lead, ikke som en identificeret kodefejl.

## Missing

Fejlens udløsende JavaScript-fil, linjenummer, browser/version, reproduktionstrin og om fejlen stadig forekommer i den aktuelle build.

## Next

Kør den aktuelle hjemmeside i browserens konsol, reproducer fejlen, indfang fuld stack trace og isolér det ugyldige regulære udtryk. Ret først koden, når den konkrete kilde er identificeret, og tilføj en regressionstest.

## Note: Ingest 2026-11-18

Konsolrapporten er arkiveret uændret under `media/files/captures/`. Fejlen er ikke markeret løst, da capturet ikke indeholder tilstrækkelig diagnostik til at lokalisere årsagen.
