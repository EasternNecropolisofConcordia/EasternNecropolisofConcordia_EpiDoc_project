import os
from saxonche import PySaxonProcessor

def run():
    # 1. Configurazione percorsi relativi
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(script_dir, '..'))
    
    xml_dir = os.path.join(root_dir, 'inscriptions')
    output_dir = os.path.join(root_dir, 'docs', 'pages')
    output_file = os.path.join(output_dir, 'people.html')

    # Verifica esistenza directory input
    if not os.path.exists(xml_dir):
        print(f"ERRORE: La cartella {xml_dir} non esiste!")
        return

    files = [f for f in os.listdir(xml_dir) if f.lower().endswith('.xml')]
    people_data = {}  # Dizionario per deduplicazione (Key: xml:id)

    # 2. Elaborazione XML
    with PySaxonProcessor(license=False) as proc:
        xpath_processor = proc.new_xpath_processor()
        
        for filename in files:
            xml_path = os.path.join(xml_dir, filename)
            try:
                node = proc.parse_xml(xml_file_name=xml_path)
                xpath_processor.set_context(xdm_item=node)
                
                # Recupera Titolo Iscrizione e Nome File
                title_item = xpath_processor.evaluate("//*[local-name()='titleStmt']/*[local-name()='title'][1]")
                idno_item = xpath_processor.evaluate("//*[local-name()='publicationStmt']/*[local-name()='idno'][@type='filename'][1]")
                
                inscription_title = title_item.string_value.strip() if title_item else filename
                
                # Calcola il link all'iscrizione (da .xml a .html)
                raw_filename = idno_item.string_value.strip() if idno_item else filename
                inscription_link_file = raw_filename.replace('.xml', '.html')
                
                # Trova tutte le persone nel file
                people = xpath_processor.evaluate("//*[local-name()='listPerson']/*[local-name()='person']")
                
                if people is None:
                    continue
                
                # Gestione singolo risultato vs lista
                if not hasattr(people, '__iter__'):
                    people = [people]
                
                for person in people:
                    xpath_processor.set_context(xdm_item=person)
                    
                    # ID (xml:id)
                    person_id_item = xpath_processor.evaluate("@xml:id")
                    person_id = person_id_item.string_value.strip() if person_id_item else None
                    
                    if not person_id:
                        continue
                    
                    # Se la persona è già nel dizionario, aggiungi solo l'iscrizione e salta il resto
                    if person_id in people_data:
                        people_data[person_id]['inscriptions'].append({
                            'title': inscription_title,
                            'link': inscription_link_file
                        })
                        continue

                    # --- RACCOLTA DATI PERSONA (Solo se nuova) ---

                    # Nome completo
                    full_name_item = xpath_processor.evaluate("*[local-name()='persName']/*[local-name()='name'][@type='full']")
                    full_name = full_name_item.string_value.strip() if full_name_item else "Unknown"
                    
                    # Gender
                    gender_item = xpath_processor.evaluate("*[local-name()='gender']")
                    gender = gender_item.string_value.strip() if gender_item else "unknown"
                    
                    # Occupation (per logica immagine)
                    occupation_item = xpath_processor.evaluate("*[local-name()='note'][@type='occupation']")
                    occupation = occupation_item.string_value.strip() if occupation_item else ""

                    # LOGICA IMMAGINI (Silhouette)
                    silhouette = None
                    if gender == 'f':
                        silhouette = 'silhouette_female.png'
                    elif gender == 'm':
                        if occupation in ['civil', 'civil?']:
                            silhouette = 'silhouette_civil.png'
                        elif occupation in ['soldier', 'soldier?']:
                            silhouette = 'silhouette_soldier.png'
                        elif occupation in ['fabricensis', 'fabricensis?']:
                            silhouette = 'silhouette_fabricensis.png'
                        elif occupation in ['functionary', 'functionary?']:
                            silhouette = 'silhouette_functionary.png'
                        else:
                            silhouette = 'silhouette_civil.png' # Fallback default maschio se occupazione non matcha o vuota? (Opzionale: rimuovi se vuoi 'nessuna immagine')
                            # Rileggendo la richiesta: "nessuna immagine se else".
                            # Correggo logica stretta richiesta:
                            if occupation not in ['civil', 'civil?', 'soldier', 'soldier?', 'fabricensis', 'fabricensis?', 'functionary', 'functionary?']:
                                silhouette = None # Nessuna immagine se maschio ma occupazione diversa o assente

                    # Lista Nomi (persName/name)
                    names_data = []
                    name_elements = xpath_processor.evaluate("*[local-name()='persName']/*[local-name()='name']")
                    if name_elements:
                        if not hasattr(name_elements, '__iter__'): name_elements = [name_elements]
                        for name_el in name_elements:
                            xpath_processor.set_context(xdm_item=name_el)
                            
                            n_type = xpath_processor.evaluate("@type").string_value.strip()
                            n_val = name_el.string_value.strip()
                            
                            n_nymref_item = xpath_processor.evaluate("@nymRef")
                            n_nymref = n_nymref_item.string_value.strip() if n_nymref_item else None
                            
                            names_data.append({
                                'type': n_type,
                                'value': n_val,
                                'nymref': n_nymref
                            })
                            # Reset contesto a person per sicurezza loop
                            xpath_processor.set_context(xdm_item=person)

                    # Note (tutte le note dirette figlie di person)
                    notes_data = []
                    note_elements = xpath_processor.evaluate("*[local-name()='note']")
                    if note_elements:
                        if not hasattr(note_elements, '__iter__'): note_elements = [note_elements]
                        for note_el in note_elements:
                            xpath_processor.set_context(xdm_item=note_el)
                            nt_type_item = xpath_processor.evaluate("@type")
                            nt_type = nt_type_item.string_value.strip() if nt_type_item else "note"
                            nt_val = note_el.string_value.strip()
                            
                            notes_data.append({'type': nt_type, 'value': nt_val})
                            xpath_processor.set_context(xdm_item=person)

                    # Salva struttura dati
                    people_data[person_id] = {
                        'id': person_id,
                        'full_name': full_name,
                        'gender': gender,
                        'silhouette': silhouette,
                        'names': names_data,
                        'notes': notes_data,
                        'inscriptions': [{
                            'title': inscription_title,
                            'link': inscription_link_file
                        }]
                    }
                
                print(f"File processato: {filename}")

            except Exception as e:
                print(f"ERRORE nel file {filename}: {str(e)}")

    # 3. Generazione Contenuto HTML (Il blocco centrale)
    content_html = ""
    
    # Ordina per nome completo
    sorted_ids = sorted(people_data.keys(), key=lambda x: people_data[x]['full_name'])

    for pid in sorted_ids:
        p = people_data[pid]
        
        # HTML Immagine
        img_html = ""
        if p['silhouette']:
            # Path relativo da docs/pages/ a images/silhouette/
            img_html = f'<img src="../../images/silhouette/{p["silhouette"]}" alt="Silhouette">'

        # Costruzione DIV Person
        content_html += f'<div class="person" id="{p["id"]}">\n'
        content_html += f'   {img_html}<h3>{p["full_name"]}</h3>\n'
        content_html += '   <dl>\n'
        
        # A. Nomi
        for name in p['names']:
            content_html += f'      <dt>{name["type"]}</dt>\n'
            content_html += f'      <dd>{name["value"]}</dd>\n'
            # Logica nymRef
            if name['type'] == 'cognomen' and name['nymref']:
                 content_html += f'      <dt>origin of the cognomen</dt>\n'
                 content_html += f'      <dd>{name["nymref"]}</dd>\n'

        # B. Gender
        g_display = "male" if p['gender'] == 'm' else ("female" if p['gender'] == 'f' else "unknown")
        content_html += f'      <dt>gender</dt>\n'
        content_html += f'      <dd>{g_display}</dd>\n'

        # C. Note
        for note in p['notes']:
            content_html += f'      <dt>{note["type"]}</dt>\n'
            content_html += f'      <dd>{note["value"]}</dd>\n'

        # D. Iscrizioni
        content_html += f'      <dt>inscription(s)</dt>\n'
        content_html += f'      <dd>'
        links = []
        for insc in p['inscriptions']:
            # Path: ./inscriptions/nomefile.html
            links.append(f'<a href="./inscriptions/{insc["link"]}">{insc["title"]}</a>')
        content_html += ' - '.join(links)
        content_html += '</dd>\n'

        content_html += '   </dl>\n'
        content_html += '</div>\n\n'

    # 4. Inserimento nel Template HTML Finale
    final_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>People - Iulia Concordia</title>
    <link rel="stylesheet" href="../css/style.css">
    <style>
       /* Stile di base per testare le immagini se non presenti nel CSS principale */
       .person {{ margin-bottom: 2rem; border-bottom: 1px solid #ccc; padding-bottom: 1rem; }}
       .person img {{ vertical-align: middle; margin-right: 10px; max-height: 50px; }}
       .person h3 {{ display: inline-block; vertical-align: middle; margin: 0; }}
    </style>
</head>
<body>
    <header>
        <h1 class="main_title">Digital Approaches to the Inscriptions of the Eastern Necropolis of <em>Iulia Concordia</em></h1>
        <nav class="navbar">
            <ul class="menu">
                <li><a href="../index.html">Home</a></li>
                <li><a href="inscriptions.html">Inscriptions</a></li>
                <li class="dropdown">
                    <a href="#">Study & Context ▾</a>
                    <ul class="submenu">
                        <li><a href="./context/history.html">History</a></li>
                        <li><a href="./context/about_people.html">About People Buried</a></li>
                        <li><a href="./context/supports.html">Supports & Monuments</a></li>
                        <li><a href="./context/chronology.html">Dating & Chronology</a></li>
                    </ul>
                </li>
                <li class="dropdown">
                    <a href="#">References ▾</a>
                    <ul class="submenu">
                        <li><a href="./references/bibliography.html">Bibliography</a></li>
                        <li><a href="./references/corpora_databases.html">Corpora and Databases</a></li>
                      </ul>
                </li>
            </ul>
        </nav>
    </header>
    
    <main class="container">
        <h2>Index of People</h2>
        {content_html}
    </main>

    <footer>
        <p>Generated via Saxon-Che & GitHub Actions</p>
        <p>&copy; 2026 - Leonardo Battistella</p>
    </footer>
</body>
</html>"""

    # 5. Scrittura su file
    os.makedirs(output_dir, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(final_html)
    
    print(f"SUCCESS: {output_file} generato con {len(people_data)} persone.")

if __name__ == "__main__":
    run()
