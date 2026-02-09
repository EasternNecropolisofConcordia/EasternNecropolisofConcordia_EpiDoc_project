import os
from saxonche import PySaxonProcessor

def run():
    # 1. Configurazione percorsi (relativi alla root della repo)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(script_dir, '..'))
    
    xml_dir = os.path.join(root_dir, 'inscriptions')
    output_dir = os.path.join(root_dir, 'docs', 'pages')
    output_file = os.path.join(output_dir, 'people.html')

    # Assicuriamoci che la cartella di output esista
    os.makedirs(output_dir, exist_ok=True)

    if not os.path.exists(xml_dir):
        print(f"ERRORE: La cartella {xml_dir} non esiste!")
        return

    files = [f for f in os.listdir(xml_dir) if f.lower().endswith('.xml')]
    people_data = {} # Per evitare doppioni

    with PySaxonProcessor(license=False) as proc:
        xpath_processor = proc.new_xpath_processor()
        
        for filename in files:
            xml_path = os.path.join(xml_dir, filename)
            try:
                node = proc.parse_xml(xml_file_name=xml_path)
                xpath_processor.set_context(xdm_item=node)
                
                # Info Iscrizione (per il link)
                title_item = xpath_processor.evaluate("//*[local-name()='titleStmt']/*[local-name()='title'][1]")
                idno_item = xpath_processor.evaluate("//*[local-name()='publicationStmt']/*[local-name()='idno'][@type='filename'][1]")
                
                insc_title = title_item.string_value.strip() if title_item else filename
                raw_filename = idno_item.string_value.strip() if idno_item else filename
                insc_link = raw_filename.replace('.xml', '.html')

                # Trova Persone
                people = xpath_processor.evaluate("//*[local-name()='listPerson']/*[local-name()='person']")
                if people is None: continue
                
                people_list = list(people) if hasattr(people, '__iter__') else [people]

                for person in people_list:
                    xpath_processor.set_context(xdm_item=person)
                    
                    # xml:id
                    p_id_item = xpath_processor.evaluate("@xml:id")
                    p_id = p_id_item.string_value.strip() if p_id_item else None
                    if not p_id: continue

                    # Se la persona esiste già, aggiungi solo l'iscrizione
                    if p_id in people_data:
                        if insc_link not in [i['link'] for i in people_data[p_id]['inscriptions']]:
                            people_data[p_id]['inscriptions'].append({'title': insc_title, 'link': insc_link})
                        continue

                    # --- Estrazione Dati ---
                    
                    # Nome Full
                    fn_item = xpath_processor.evaluate("*[local-name()='persName']/*[local-name()='name'][@type='full']")
                    full_name = fn_item.string_value.strip() if fn_item else "Unknown"

                    # Gender
                    g_item = xpath_processor.evaluate("*[local-name()='gender']")
                    gender = g_item.string_value.strip() if g_item else "unknown"

                    # Occupation
                    occ_item = xpath_processor.evaluate("*[local-name()='note'][@type='occupation']")
                    occupation = occ_item.string_value.strip() if occ_item else ""

                    # Immagine Silhouette
                    silhouette = None
                    if gender == 'f':
                        silhouette = "silhouette_female.png"
                    elif gender == 'm':
                        if occupation in ['civil', 'civil?']: silhouette = "silhouette_civil.png"
                        elif occupation in ['soldier', 'soldier?']: silhouette = "silhouette_soldier.png"
                        elif occupation in ['fabricensis', 'fabricensis?']: silhouette = "silhouette_fabricensis.png"
                        elif occupation in ['functionary', 'functionary?']: silhouette = "silhouette_functionary.png"

                    # Nomi e nymRef
                    names = []
                    name_els = xpath_processor.evaluate("*[local-name()='persName']/*[local-name()='name']")
                    if name_els:
                        for n_el in (list(name_els) if hasattr(name_els, '__iter__') else [name_els]):
                            xpath_processor.set_context(xdm_item=n_el)
                            n_type = xpath_processor.evaluate("@type").string_value.strip() if xpath_processor.evaluate("@type") else "name"
                            n_val = n_el.string_value.strip()
                            n_ref = xpath_processor.evaluate("@nymRef").string_value.strip() if xpath_processor.evaluate("@nymRef") else None
                            names.append({'type': n_type, 'value': n_val, 'nymref': n_ref})
                    
                    # Note dirette
                    notes = []
                    note_els = xpath_processor.evaluate("*[local-name()='note']")
                    if note_els:
                        for nt_el in (list(note_els) if hasattr(note_els, '__iter__') else [note_els]):
                            xpath_processor.set_context(xdm_item=nt_el)
                            nt_type = xpath_processor.evaluate("@type").string_value.strip() if xpath_processor.evaluate("@type") else "note"
                            notes.append({'type': nt_type, 'value': nt_el.string_value.strip()})

                    people_data[p_id] = {
                        'id': p_id, 'full_name': full_name, 'gender': gender,
                        'silhouette': silhouette, 'names': names, 'notes': notes,
                        'inscriptions': [{'title': insc_title, 'link': insc_link}]
                    }
            except Exception as e:
                print(f"Errore in {filename}: {e}")

    # 4. Generazione HTML
    cards_html = ""
    for pid in sorted(people_data.keys()):
        p = people_data[pid]
        img_tag = f'<img src="../../images/silhouette/{p["silhouette"]}" alt="silhouette" style="width:50px; float:left; margin-right:15px;">' if p['silhouette'] else ""
        
        cards_html += f'<div class="person" id="{p["id"]}">\n'
        cards_html += f'    {img_tag}<h3>{p["full_name"]}</h3>\n'
        cards_html += '    <dl>\n'
        
        for n in p['names']:
            cards_html += f'        <dt>{n["type"]}</dt><dd>{n["value"]}</dd>\n'
            if n['type'] == 'cognomen' and n['nymref']:
                cards_html += f'        <dt>origin of the cognomen</dt><dd>{n["nymref"]}</dd>\n'
        
        g_text = "male" if p['gender'] == 'm' else ("female" if p['gender'] == 'f' else "unknown")
        cards_html += f'        <dt>gender</dt><dd>{g_text}</dd>\n'
        
        for nt in p['notes']:
            cards_html += f'        <dt>{nt["type"]}</dt><dd>{nt["value"]}</dd>\n'
            
        links = [f'<a href="./inscriptions/{i["link"]}">{i["title"]}</a>' for i in p['inscriptions']]
        cards_html += f'        <dt>inscription(s)</dt><dd>{" - ".join(links)}</dd>\n'
        cards_html += '    </dl>\n'
        cards_html += '    <div style="clear:both;"></div>\n'
        cards_html += '</div>\n\n'

    # 5. Scrittura finale (con il tuo template)
    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>People - Iulia Concordia</title>
    <link rel="stylesheet" href="../css/style.css">
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
    <main class="container" style="padding:20px;">
        <h2>Index of People</h2>
        {cards_html if cards_html else "<p>No people found in XML files.</p>"}
    </main>
    <footer>
        <p>Generated via Saxon-Che & GitHub Actions</p>
        <p>&copy; 2026 - Leonardo Battistella</p>
    </footer>
</body>
</html>"""

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(full_html)
    print(f"Processo completato: {len(people_data)} persone trovate.")

if __name__ == "__main__":
    run()
