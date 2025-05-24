# 📦 HOWTO: Release erstellen mit Auto-Changelog-Workflow

Dieses Repository nutzt einen automatisierten CI/CD-Workflow zur **Versionsverwaltung, Changelog-Generierung und Release-Erstellung**.  
Der gesamte Prozess ist deklarativ und läuft automatisch – ausgelöst durch Änderungen an einer Datei: `VERSION`.

---

## 🧭 Was passiert automatisch?

Sobald Änderungen in `main` landen, prüft der Workflow:

- 🔍 **Hat sich die Datei `VERSION` geändert?**
  - ❌ **Nein** → es wird nur das `CHANGELOG.md` aktualisiert (unreleased Abschnitt)
  - ✅ **Ja** → es wird:
    - ein vollständiger Changelog für diese Version erzeugt
    - ein Git-Tag `vX.Y.Z` erstellt
    - ein Release in Gitea veröffentlicht (inkl. Beschreibung aus dem Changelog)

---

## ✅ Wie erzeuge ich ein Release?

### 1. Erhöhe die Version in der Datei `VERSION`

Beispiel:

```txt
1.2.3
```

> Diese Datei muss **als eigene Commit-Änderung** erfolgen – idealerweise als letzter Commit in einem PR.
> Die Commit-Nachricht sollte mit `chore(version)` beginnen, damit dieser nicht im Changelog auftaucht.

---

### 2. Mergen in `main`

Sobald `main` den Commit mit neuer `VERSION` enthält, wird automatisch:

- das `CHANGELOG.md` regeneriert und committed
- der neue Git-Tag erstellt (`v1.2.3`)
- ein Gitea Release mit genau diesem Changelog erzeugt

---

## 🛡️ Hinweis zu Tokens & Webhooks

Damit das Release auch korrekt weitere Workflows auslösen kann (z. B. über `on: release`), ist **ein Personal Access Token notwendig**.

### 🔐 Secret: `RELEASE_PUBLISH_TOKEN`

> Lege ein Repository-Secret mit diesem Namen an.  
> Es sollte ein **Gitea Personal Access Token** mit folgenden Berechtigungen sein:

- `write:repo`
- `write:release`
- idealerweise: keine Ablaufzeit

Wird dieser Token **nicht** gesetzt, fällt der Workflow auf `ACTIONS_RUNTIME_TOKEN` zurück, aber:
- Release wird trotzdem erstellt
- **⚠️ andere Workflows, die auf `release.published` reagieren, könnten nicht getriggert werden**

---

## 🧪 Debugging-Tipps

- Stelle sicher, dass `VERSION` exakt **eine gültige neue semver-Version** enthält
- Achte auf den Commit-Log: Changelog-Commits sind mit `chore(changelog):` gekennzeichnet
- Verwende nur `main` als Trigger-Zweig

---

## 🧩 Erweiterung

In `upload-assets.yml` kannst du beliebige Build-Artefakte automatisch an das Release anhängen, sobald es veröffentlicht ist.

Dafür:
- liegt das Script `.gitea/scripts/get-release-id.sh`
- sowie `.gitea/scripts/upload-asset.sh` bereit

Mehr dazu in der Datei: `.gitea/workflows/upload-assets.yml`

---

## 🧘 Best Practice

- Changelog-Generierung nie manuell ausführen
- Nur `VERSION` ändern, um ein neues Release auszulösen
- Auf `CHANGELOG.md` nie direkt committen
- Release-Daten niemals per Hand in Gitea pflegen

📎 Alles wird versioniert, automatisiert und reproduzierbar erzeugt.

---

## 🧠 Commit-Gruppierung & Changelog-Erzeugung

Der Changelog wird auf Basis definierter **Commit-Gruppen** erzeugt.  
Diese Regeln sind in `cliff.toml` unter `commit_parsers` konfiguriert.

| Prefix / Muster                | Gruppe                    | Beschreibung                                     |
|-------------------------------|---------------------------|--------------------------------------------------|
| `feat:`                       | 🚀 Features               | Neue Funktionalität                              |
| `fix:`                        | 🐛 Bug Fixes              | Fehlerbehebungen                                 |
| `doc:`                        | 📚 Documentation          | Änderungen an Doku, Readmes etc.                 |
| `perf:`                       | ⚡ Performance             | Leistungsverbesserungen                          |
| `refactor:`                   | 🚜 Refactor               | Reorganisation ohne Verhaltensänderung           |
| `style:`                      | 🎨 Styling                | Formatierung, Whitespaces, Code-Style            |
| `test:`                       | 🧪 Testing                | Neue oder angepasste Tests                       |
| `ci:` oder `chore:` (ohne Spezifizierung) | ⚙️ Miscellaneous Tasks | CI-Änderungen, Aufgaben, Wartung etc.            |
| `chore(changelog)`, `chore(version)`, `chore(release): prepare for`, `chore(deps...)`, `chore(pr)`, `chore(pull)` | *(ignoriert)* | Diese Commits werden im Changelog **ausgelassen** |
| Commit-Body enthält `security` | 🛡️ Security              | Sicherheitsrelevante Änderungen                  |
| `revert:`                     | ◀️ Revert                | Rückgängig gemachte Commits                      |
| alles andere                  | 💼 Other                 | Fallback für nicht erkannte Formate              |

### ✍️ Beispiel:

```bash
git commit -m "feat: add login endpoint"
git commit -m "fix: prevent crash on null input"
git commit -m "chore(version): bump to 1.2.3"
```

> Nur die ersten beiden erscheinen im Changelog – der dritte wird **automatisch übersprungen**.

---

## 🧾 Umgang mit `CHANGELOG.md` beim Mergen und Releasen

Wenn du automatisiert einen Changelog mit `git-cliff` erzeugst, ist `CHANGELOG.md` ein **generiertes Artefakt** – und kein handgepflegter Quelltext.

Beim Mergen von Feature-Branches in `main` kann es deshalb zu **unnötigen Konflikten** in dieser Datei kommen, obwohl der Inhalt später sowieso neu erzeugt wird.

---

## 🧼 Umgang mit `CHANGELOG.md` in Feature-Branches

Wenn du mit **Feature-Branches** arbeitest, wird `CHANGELOG.md` dort oft automatisch erzeugt.
Das kann beim späteren Merge in `main` zu **unnötigen Merge-Konflikten** führen.

### ✅ Empfohlene Vorgehensweise

**Bevor du den Branch mit `main` zusammenführst** (Merge oder Cherry-Pick):

```bash
git rm CHANGELOG.md
git commit -m "chore(changelog): remove generated CHANGELOG.md before merge"
git push
```

Dadurch:

* verhinderst du Merge-Konflikte mit `CHANGELOG.md`
* wird die Datei bei Feature-Branches nicht mehr automatisch erzeugt
* bleibt deine Historie sauber und konfliktfrei

> 💡 Der Workflow erzeugt `CHANGELOG.md` automatisch **nur**, wenn:
>
> * die Datei schon vorhanden ist **oder**
> * der Branch `main` heißt

---

## 🧩 Merge-Konflikte verhindern mit `.gitattributes`

Damit Git bei Konflikten in `CHANGELOG.md` **automatisch deine Version bevorzugt**, kannst du folgende Zeile in die Datei `.gitattributes` aufnehmen:

```gitattributes
CHANGELOG.md merge=ours
```

Das bedeutet:

* Beim Merge wird die Version aus dem aktuellen Branch (`ours`) behalten
* Änderungen aus dem Ziel-Branch (`theirs`) werden verworfen

### ✅ So verwendest du es richtig:

1. **Füge die Regel in `main` hinzu**:

```bash
echo "CHANGELOG.md merge=ours" >> .gitattributes
git add .gitattributes
git commit -m "chore(git): prevent merge conflicts in CHANGELOG.md"
git push origin main
```

2. **Hole sie in deinen Feature-Branch**:

```bash
git checkout feature/xyz
git rebase origin/main
```

3. **Ab sofort werden Konflikte in `CHANGELOG.md` automatisch aufgelöst** – lokal.

> ⚠️ Hinweis: Plattformen wie **Gitea, GitHub oder GitLab ignorieren `.gitattributes` beim Merge über die Web-Oberfläche**.
> Führe Merges daher **lokal** durch, wenn du Konflikte verhindern willst.
