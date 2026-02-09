import os
from saxonche import PySaxonProcessor

def run():
    # Setup percorsi
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(script_dir, '..'))
    
    xml_dir = os.path.join(root_dir, 'inscriptions')
    output_dir = os.path.join(root_dir, 'docs', 'pages')
    output_file = os.path.join(output_dir, 'people.html')

    if not os.path.exists(xml_dir):
        print(f"ERRORE: La cartella {xml_dir} non esiste!")
        return

    files = [f for f in os.listdir(xml_dir) if f.lower().endswith('.xml')]
    people_data = {}  # Chiave = xml:id

    with PySaxonProcessor(license=False) as proc:
        xpath_processor = proc.new_xpath_processor()
        
        for filename in files:
            xml_path = os.path.join(xml_dir, filename)
            try:
                node = proc.parse_xml(xml_file_name=xml_path)
                xpath_processor.set_context(xdm_item=node)
                
                # 1. Dati generali dell'iscrizione
                title_item = xpath_processor.evaluate("//*[local-name()='titleStmt']/*[local-name()='title'][1]")
                idno_item = xpath_processor.evaluate("//*[local-name()='publicationStmt']/*[local-name()='idno'][@type='filename'][1]")
                
                inscription_title = title_item.string_value.strip() if title_item else filename
                # Nome file HTML dell'iscrizione
                insc_filename = idno_item.string_value.strip() if idno_item else filename
                insc_link = insc_filename.replace('.xml', '.html')
                
                # 2. Trova le persone
                people = xpath_processor.evaluate("//*[local-name()='listPerson']/*[local-name()='person']")
                
                if people is None:
                    continue
                
                # Normalizza in lista se è un singolo item
                if not hasattr(people, '__iter__'):
                    people = [people]
                
                for person in people:
                    xpath_processor.set_context(xdm_item=person)
                    
                    # ID
                    person_id_item = xpath_processor.evaluate("@xml:id")
                    person_id = person_id_item.string_value.strip() if person_id_item else None
                    
                    if not person_id:
                        continue
                    
                    # Se la persona esiste già, aggiungiamo solo l'iscrizione e passiamo oltre
                    if person_id in people_data:
                        people_data[person_id]['inscriptions'].append({
                            'title': inscription_title,
                            'link': insc_link
                        })
                        continue

                    # --- RACCOLTA DATI PERSONA NUOVA ---

                    # Nome completo (per il titolo h3)
                    full_name_item = xpath_processor.evaluate("*[local-name()='persName']/*[local-name()='name'][@type='full']")
                    full_name = full_name_item.string_value.strip() if full_name_item else "Unknown"
                    
                    # Gender
                    gender_item = xpath_processor.evaluate("*[local-name()='gender']")
                    gender_val = gender_item.string_value.strip() if gender_item else "unknown"
                    
                    # Occupation (serve per l'immagine)
                    occupation_item = xpath_processor.evaluate("*[local-name()='note'][@type='occupation']")
                    occupation_val = occupation_item.string_value.strip() if occupation_item else ""

                    # --- LOGICA IMMAGINE ---
                    image_file = None
                    if gender_val == 'f':
                        image_file = "silhouette_female.png"
                    elif gender_val == 'm':
                        if occupation_val in ['civil', 'civil?']:
                            image_file = "silhouette_civil.png"
                        elif occupation_val in ['soldier', 'soldier?']:
                            image_file = "silhouette_soldier.png"
                        elif occupation_val in ['fabricensis', 'fabricensis?']:
                            image_file = "silhouette_fabricensis.png"
                        elif occupation_val in ['functionary', 'functionary?']:
                            image_file = "silhouette_functionary.png"
                    # Else rimane None

                    # --- LISTA NOMI (per il DL) ---
                    names_list = []
                    name_elements = xpath_processor.evaluate("*[local-name()='persName']/*[local-name()='name']")
                    if name_elements:
                        if not hasattr(name_elements, '__iter__'): name_elements = [name_elements]
                        for n in name_elements:
                            xpath_processor.set_context(xdm_item=n)
                            n_type = xpath_processor.evaluate("@type").string_value.strip()
                            n_val = n.string_value.strip()
                            n_nymRef_item = xpath_processor.evaluate("@nymRef")
                            n_nymRef = n_nymRef_item.string_value.strip() if n_nymRef_item else None
                            
                            names_list.append({
                                'type': n_type,
                                'value': n_val,
                                'nymRef': n_nymRef
                            })
                            xpath_processor.set_context(xdm_item=person) # Reset context

                    # --- NOTE (per il DL) ---
                    notes_list = []
                    note_elements = xpath_processor.evaluate("*[local-name()='note']")
                    if note_elements:
                        if not hasattr(note_elements, '__iter__'): note_elements = [note_elements]
                        for note in note_elements:
                            xpath_processor.set_context(xdm_item=note)
                            note_type_item = xpath_processor.evaluate("@type")
                            note_type = note_type_item.string_value.strip() if note_type_item else "note"
                            note_val = note.string_value.strip()
                            notes_list.append({'type': note_type, 'value': note_val})
                            xpath_processor.set_context(xdm_item=person) # Reset context

                    # Salva nel dizionario
                    people_data[person_id] = {
                        'id': person_id,
                        'full_name': full_name,
                        'gender': gender_val,
                        'image': image_file,
                        'names': names_list,
                        'notes': notes_list,
                        'inscriptions': [{
                            'title': inscription_title,
                            'link': insc_link
                        }]
                    }
                
                print(f"File processato: {filename}")

            except Exception as e:
                print(f"ERRORE su {filename}: {e}")

    # --- GENERAZIONE HTML ---
    
    html_content = ""
    
    # Ordiniamo per nome completo per pulizia
    sorted_ids = sorted(people_data.keys(), key=lambda x: people_data[x]['full_name'])

    for pid in sorted_ids:
        p = people_data[pid]
        
        # Preparazione immagine
        img_tag = ""
        if p['image']:
            # Percorso relativo: da docs/pages/ a images/silhouette/
            img_tag = f'<img src="../../images/silhouette/{p["image"]}" alt="{p["full_name"]}" style="float:left; margin-right:10px; height:50px;">'
            # Nota: ho aggiunto uno stile inline minimo per allinearla a sinistra come richiesto, 
            # ma l'ideale è gestirlo nel CSS con la classe .person img

        # Apertura Div
        html_content += f'<div class="person" id="{p["id"]}">\n'
        
        # Titolo con immagine a sinistra
        html_content += f'    {img_tag}<h3>{p["full_name"]}</h3>\n'
        html_content += f'    <div style="clear:both;"></div>\n' # Clear fix nel caso l'immagine fluttui
        
        # Apertura DL
        html_content += '    <dl>\n'

        # 1. Nomi
        for name in p['names']:
            html_content += f'        <dt>{name["type"]}</dt>\n'
            html_content += f'        <dd>{name["value"]}</dd>\n'
            # Logica nymRef
            if name['type'] == 'cognomen' and name['nymRef']:
                html_content += f'        <dt>origin of the cognomen</dt>\n'
                html_content += f'        <dd>{name["nymRef"]}</dd>\n'

        # 2. Gender
        gender_display = "male" if p['gender'] == 'm' else ("female" if p['gender'] == 'f' else "unknown")
        html_content += f'        <dt>gender</dt>\n'
        html_content += f'        <dd>{gender_display}</dd>\n'

        # 3. Note
        for note in p['notes']:
            html_content += f'        <dt>{note["type"]}</dt>\n'
            html_content += f'        <dd>{note["value"]}</dd>\n'

        # 4. Inscriptions
        html_content += f'        <dt>inscription(s)</dt>\n'
        html_content += f'        <dd>'
        links_html = []
        for insc in p['inscriptions']:
            # Link relativo a ./inscriptions/nomefile.html
            links_html.append(f'<a href="inscriptions/{insc["link"]}">{insc["title"]}</a>')
        html_content += ' - '.join(links_html)
        html_content += f'</dd>\n'

        html_content += '    </dl>\n'
        html_content += '</div>\n\n'

    # Template Base
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
        {html_content}
    </main>

    <footer>
        <p>Generated via Saxon-Che & GitHub Actions</p>
        <p>&copy; 2026 - Leonardo Battistella</p>
    </footer>
</body>
</html>"""

    # Scrittura su file
    os.makedirs(output_dir, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(final_html)
    
    print(f"Finito! Creato {output_file} con {len(people_data)} schede persona.")

if __name__ == "__main__":
    run()
