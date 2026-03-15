# Eastern Necropolis of *Iulia Concordia* — EpiDoc Project

**[English](#english)** · **[Italiano](#italiano)**

🔗 **Live site / Sito web**: [Eastern Necropolis of Concordia](https://easternnecropolisofconcordia.github.io/EasternNecropolisofConcordia_EpiDoc_project/index.html)

---

## English

### About the Project

This repository hosts a digital epigraphic corpus of the late-antique inscriptions from the **Eastern Necropolis** (*Sepolcreto dei Militi*) of ***Iulia Concordia*** (modern Concordia Sagittaria, Veneto, Italy). The project was developed as a **final thesis** for the Master's degree programme in **Digital and Public Humanities** at **Università Ca' Foscari Venezia**.

Each inscription is encoded in **TEI/EpiDoc XML**, a scholarly standard for the digital representation of ancient texts. All visualisations on the website — epigraphic records, prosopographic profiles, the necropolis plan, and the bibliography — are **generated exclusively from the XML source files**, so that the richness and granularity of the encoded data can be directly evaluated.

### What the XML Files Contain

Every EpiDoc file in `inscriptions/` captures a full epigraphic record:

- **Metadata & identifiers** — inventory number, Trismegistos ID, EDR ID, UEL ID.
- **Physical description** — object type, material, dimensions, state of preservation.
- **Palaeographic notes** — letter-height, *ductus*, letterform descriptions (bilingual EN/IT).
- **Decoration** — symbols such as Chi-Rho monograms and *hederae distinguentes*, linked to EAGLE and AAT vocabularies.
- **Provenance** — find-spot, discovery date, current location, pixel coordinates on the 1879 necropolis plan (`plan_x`, `plan_y`).
- **Dating** — chronological range with evidence criteria.
- **Prosopography** — structured person records (`<listPerson>`) with gender, occupation (soldier, civilian, *fabricensis*, functionary), military rank, unit (*numerus*), family relationships, and onomastic components (*praenomen*, *nomen*, *cognomen*, *gens*).
- **Controlled vocabularies** — taxonomies for military ranks, chronological periods, places, and occupations, with external links (EAGLE, AAT, Wikidata, Latin Lexicon, Trismegistos, DARE, VIAF, TGN).
- **Critical edition** — Leiden-convention transcription with apparatus criticus.
- **Translation** — bilingual English and Italian.
- **Commentary** — bilingual scholarly discussion.
- **Bibliography** — references to the `master_bibliography.xml`, corpora, and databases.

### Repository Structure

```
├── .github/workflows/
│   └── deploy.yml                  # GitHub Actions: runs all scripts on push
│
├── bibliography/
│   └── master_bibliography.xml     # Centralised bibliographic database
│
├── inscriptions/                   # TEI/EpiDoc XML source files (one per inscription)
│   ├── vassio.xml
│   ├── firmina.xml
│   └── ...                         (56 files)
│
├── scripts/
│   ├── transform.py                # XML → HTML epigraphic records (via XSLT)
│   ├── generate_list.py            # Generates the inscription index page
│   ├── generate_map.py             # Generates the Leaflet raster map
│   ├── people.py                   # Generates prosopographic profiles
│   ├── transform_bibliography.py   # master_bibliography.xml → bibliography.html
│   └── transform_corpora_databases.py  # → corpora_databases.html
│
├── xslt/
│   ├── epidoc-to-html.xsl          # Main XSLT stylesheet for inscriptions
│   ├── bibliography-to-html.xsl
│   └── corpora_databases-to-html.xsl
│
├── docs/                           # Published website (GitHub Pages root)
│   ├── index.html                  # Home page (manually authored)
│   ├── css/
│   ├── images/
│   │   ├── inscriptions/           # Photographs of the inscribed objects
│   │   ├── necropolis/             # Historical images and context
│   │   ├── plan/                   # 1879 necropolis plan (raster base for the map)
│   │   └── silhouette/             # Icons for prosopographic profiles
│   └── pages/
│       ├── inscriptions/           # Generated epigraphic record pages
│       ├── context/                # Manually authored contextual pages
│       │   ├── history.html
│       │   ├── about_people.html
│       │   ├── chronology.html
│       │   └── supports.html
│       ├── references/             # Generated bibliography & corpora pages
│       ├── inscriptions.html       # Generated inscription index
│       ├── people.html             # Generated prosopographic index
│       ├── map.html                # Generated Leaflet map
│       └── krummrey-panciera_epidoc.html  # Diacritical signs reference (manual)
│
├── requirements.txt
└── README.md
```

### How It Works

The website is built through an automated pipeline that transforms XML sources into HTML pages. The workflow can be summarised as follows:

1. **Epigraphic records** — `transform.py` applies `epidoc-to-html.xsl` to each file in `inscriptions/`, producing an HTML page per inscription (with linked photographs from `images/inscriptions/`).
2. **Inscription index** — `generate_list.py` reads the XML files and outputs `inscriptions.html`.
3. **Prosopographic profiles** — `people.py` extracts `<listPerson>` data from every inscription and generates `people.html`, assigning a silhouette icon based on each individual's occupation (civilian, soldier, *fabricensis*, functionary, Greek merchant).
4. **Necropolis map** — `generate_map.py` builds a Leaflet-based map using the 1879 plan as a raster layer and the `plan_x`/`plan_y` pixel coordinates from each inscription's `<provenance>` to place markers.
5. **Bibliography & corpora** — `transform_bibliography.py` and `transform_corpora_databases.py` process `master_bibliography.xml` through their respective XSLT stylesheets to generate the reference pages.
6. **Deployment** — `deploy.yml` (GitHub Actions) runs all scripts automatically on every push, keeping the published site in sync with the source data.

Only three groups of pages are manually authored: the home page (`index.html`), the contextual pages (`context/`), and the Krummrey-Panciera diacritical signs reference.

### Technologies

- **TEI/EpiDoc XML** — inscription encoding
- **XSLT** — XML-to-HTML transformation
- **Python** — scripting pipeline (lxml, etc.)
- **Leaflet.js** — interactive raster map
- **GitHub Actions** — continuous deployment
- **GitHub Pages** — hosting

---

## Italiano

### Il progetto

Questa repository ospita un corpus epigrafico digitale delle iscrizioni tardo-antiche della **Necropoli di Levante** (*Sepolcreto dei Militi*) di ***Iulia Concordia*** (l'odierna Concordia Sagittaria, Veneto). Il progetto è stato sviluppato come **tesi di laurea magistrale** per il corso di laurea in **Digital and Public Humanities** presso l'**Università Ca' Foscari Venezia**.

Ogni iscrizione è codificata in **TEI/EpiDoc XML**, lo standard accademico per la rappresentazione digitale dei testi antichi. Tutte le visualizzazioni del sito — schede epigrafiche, profili prosopografici, pianta della necropoli e bibliografia — sono **generate esclusivamente dai file XML sorgente**, in modo che la ricchezza e la granularità dei dati codificati possano essere direttamente valutate.

### Contenuto dei file XML

Ogni file EpiDoc in `inscriptions/` contiene una scheda epigrafica completa:

- **Metadati e identificativi** — numero di inventario, ID Trismegistos, ID EDR, ID UEL.
- **Descrizione fisica** — tipo di supporto, materiale, dimensioni, stato di conservazione.
- **Note paleografiche** — altezza delle lettere, *ductus*, descrizione delle forme letterarie (bilingue EN/IT).
- **Decorazione** — simboli come monogrammi Chi-Rho e *hederae distinguentes*, collegati ai vocabolari EAGLE e AAT.
- **Provenienza** — luogo di ritrovamento, data di scoperta, collocazione attuale, coordinate in pixel sulla pianta del 1879 della necropoli (`plan_x`, `plan_y`).
- **Datazione** — intervallo cronologico con criteri di evidenza.
- **Prosopografia** — schede strutturate per ogni individuo (`<listPerson>`) con genere, occupazione (soldato, civile, *fabricensis*, funzionario), grado militare, unità (*numerus*), relazioni familiari e componenti onomastiche (*praenomen*, *nomen*, *cognomen*, *gens*).
- **Vocabolari controllati** — tassonomie per gradi militari, periodi cronologici, luoghi e occupazioni, con link esterni (EAGLE, AAT, Wikidata, Latin Lexicon, Trismegistos, DARE, VIAF, TGN).
- **Edizione critica** — trascrizione secondo le convenzioni di Leida con apparato critico.
- **Traduzione** — bilingue inglese e italiano.
- **Commento** — discussione filologica bilingue.
- **Bibliografia** — riferimenti alla `master_bibliography.xml`, ai corpora e ai database.

### Struttura della repository

```
├── .github/workflows/
│   └── deploy.yml                  # GitHub Actions: esegue tutti gli script al push
│
├── bibliography/
│   └── master_bibliography.xml     # Database bibliografico centralizzato
│
├── inscriptions/                   # File sorgente TEI/EpiDoc XML (uno per iscrizione)
│   ├── vassio.xml
│   ├── firmina.xml
│   └── ...                         (56 file)
│
├── scripts/
│   ├── transform.py                # XML → HTML schede epigrafiche (via XSLT)
│   ├── generate_list.py            # Genera la pagina indice delle iscrizioni
│   ├── generate_map.py             # Genera la mappa Leaflet raster
│   ├── people.py                   # Genera i profili prosopografici
│   ├── transform_bibliography.py   # master_bibliography.xml → bibliography.html
│   └── transform_corpora_databases.py  # → corpora_databases.html
│
├── xslt/
│   ├── epidoc-to-html.xsl          # Foglio XSLT principale per le iscrizioni
│   ├── bibliography-to-html.xsl
│   └── corpora_databases-to-html.xsl
│
├── docs/                           # Sito pubblicato (root di GitHub Pages)
│   ├── index.html                  # Home page (redatta manualmente)
│   ├── css/
│   ├── images/
│   │   ├── inscriptions/           # Fotografie dei supporti iscritti
│   │   ├── necropolis/             # Immagini storiche e contestuali
│   │   ├── plan/                   # Pianta della necropoli del 1879 (base raster)
│   │   └── silhouette/             # Icone per i profili prosopografici
│   └── pages/
│       ├── inscriptions/           # Pagine delle schede epigrafiche (generate)
│       ├── context/                # Pagine contestuali (redatte manualmente)
│       │   ├── history.html
│       │   ├── about_people.html
│       │   ├── chronology.html
│       │   └── supports.html
│       ├── references/             # Pagine bibliografia e corpora (generate)
│       ├── inscriptions.html       # Indice delle iscrizioni (generato)
│       ├── people.html             # Indice prosopografico (generato)
│       ├── map.html                # Mappa Leaflet (generata)
│       └── krummrey-panciera_epidoc.html  # Segni diacritici (manuale)
│
├── requirements.txt
└── README.md
```

### Come funziona

Il sito è costruito attraverso una pipeline automatizzata che trasforma i sorgenti XML in pagine HTML. Il flusso di lavoro può essere riassunto come segue:

1. **Schede epigrafiche** — `transform.py` applica `epidoc-to-html.xsl` a ogni file in `inscriptions/`, producendo una pagina HTML per iscrizione (con le fotografie da `images/inscriptions/`).
2. **Indice delle iscrizioni** — `generate_list.py` legge i file XML e genera `inscriptions.html`.
3. **Profili prosopografici** — `people.py` estrae i dati `<listPerson>` da ogni iscrizione e genera `people.html`, assegnando un'icona silhouette in base all'occupazione dell'individuo (civile, soldato, *fabricensis*, funzionario, mercante greco).
4. **Mappa della necropoli** — `generate_map.py` costruisce una mappa basata su Leaflet utilizzando la pianta del 1879 come layer raster e le coordinate in pixel `plan_x`/`plan_y` dal `<provenance>` di ogni iscrizione per posizionare i marcatori.
5. **Bibliografia e corpora** — `transform_bibliography.py` e `transform_corpora_databases.py` elaborano `master_bibliography.xml` attraverso i rispettivi fogli XSLT per generare le pagine di riferimento.
6. **Deploy** — `deploy.yml` (GitHub Actions) esegue automaticamente tutti gli script ad ogni push, mantenendo il sito pubblicato sincronizzato con i dati sorgente.

Solo tre gruppi di pagine sono redatti manualmente: la home page (`index.html`), le pagine contestuali (`context/`) e la pagina di riferimento sui segni diacritici Krummrey-Panciera.

### Tecnologie

- **TEI/EpiDoc XML** — codifica delle iscrizioni
- **XSLT** — trasformazione XML-to-HTML
- **Python** — pipeline di scripting (lxml, ecc.)
- **Leaflet.js** — mappa raster interattiva
- **GitHub Actions** — deploy continuo
- **GitHub Pages** — hosting

---

## Author / Autore

**Leonardo Battistella**
Matricola / Student ID: 870645
Università Ca' Foscari Venezia — Digital and Public Humanities (MA)

📧 [easternnecropolisofconcordia@gmail.com]
