import os
from saxonche import PySaxonProcessor

def run():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(script_dir, '..'))
    
    xml_dir = os.path.join(root_dir, 'inscriptions')
    output_dir = os.path.join(root_dir, 'docs', 'pages')
    output_file = os.path.join(output_dir, 'people.html')

    if not os.path.exists(xml_dir):
        print(f"ERRORE: La cartella {xml_dir} non esiste!")
        return

    files = [f for f in os.listdir(xml_dir) if f.lower().endswith('.xml')]
    people_data = {}  # Dizionario per evitare duplicati, chiave = xml:id

    with PySaxonProcessor(license=False) as proc:
        xpath_processor = proc.new_xpath_processor()
        
        for filename in files:
            xml_path = os.path.join(xml_dir, filename)
            try:
                node = proc.parse_xml(xml_file_name=xml_path)
                xpath_processor.set_context(xdm_item=node)
                
                # Ottieni titolo e idno dell'iscrizione
                title_item = xpath_processor.evaluate("//*[local-name()='titleStmt']/*[local-name()='title'][1]")
                idno_item = xpath_processor.evaluate("//*[local-name()='idno'][@type='filename'][1]")
                
                inscription_title = title_item.string_value.strip() if title_item else filename
                inscription_link = idno_item.string_value.strip().replace('.xml', '.html') if idno_item else filename.replace('.xml', '.html')
                
                # Trova tutte le persone
                people = xpath_processor.evaluate("//*[local-name()='listPerson']/*[local-name()='person']")
                
                if people is None:
                    continue
                
                # Se people è un singolo item, lo convertiamo in lista
                if not hasattr(people, '__iter__'):
                    people = [people]
                
                for person in people:
                    xpath_processor.set_context(xdm_item=person)
                    
                    # xml:id
                    person_id_item = xpath_processor.evaluate("@xml:id")
                    person_id = person_id_item.string_value.strip() if person_id_item else None
                    
                    if not person_id:
                        continue
                    
                    # Se la persona esiste già, aggiungi solo l'iscrizione
                    if person_id in people_data:
                        people_data[person_id]['inscriptions'].append({
                            'title': inscription_title,
                            'link': inscription_link
                        })
                        continue
                    
                    # Nome completo
                    full_name_item = xpath_processor.evaluate("*[local-name()='persName']/*[local-name()='name'][@type='full']")
                    full_name = full_name_item.string_value.strip() if full_name_item else "Unknown"
                    
                    # Gender
                    gender_item = xpath_processor.evaluate("*[local-name()='gender']")
                    gender = gender_item.string_value.strip() if gender_item else "unknown"
                    
                    # Occupation
                    occupation_item = xpath_processor.evaluate("*[local-name()='note'][@type='occupation']")
                    occupation = occupation_item.string_value.strip() if occupation_item else None
                    
                    # Determina l'immagine
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
                    
                    # Tutti i nomi in persName
                    names = []
                    name_elements = xpath_processor.evaluate("*[local-name()='persName']/*[local-name()='name']")
                    if name_elements:
                        if not hasattr(name_elements, '__iter__'):
                            name_elements = [name_elements]
                        
                        for name_elem in name_elements:
                            xpath_processor.set_context(xdm_item=name_elem)
                            name_type_item = xpath_processor.evaluate("@type")
                            name_value = name_elem.string_value.strip()
                            name_type = name_type_item.string_value.strip() if name_type_item else "name"
                            
                            # Controlla nymRef
                            nymref_item = xpath_processor.evaluate("@nymRef")
                            nymref = nymref_item.string_value.strip() if nymref_item else None
                            
                            names.append({
                                'type': name_type,
                                'value': name_value,
                                'nymref': nymref
                            })
                            
                            xpath_processor.set_context(xdm_item=person)
                    
                    # Note elements
                    notes = []
                    note_elements = xpath_processor.evaluate("*[local-name()='note']")
                    if note_elements:
                        if not hasattr(note_elements, '__iter__'):
                            note_elements = [note_elements]
                        
                        for note_elem in note_elements:
                            xpath_processor.set_context(xdm_item=note_elem)
                            note_type_item = xpath_processor.evaluate("@type")
                            note_value = note_elem.string_value.strip()
                            note_type = note_type_item.string_value.strip() if note_type_item else "note"
                            
                            notes.append({
                                'type': note_type,
                                'value': note_value
                            })
                            
                            xpath_processor.set_context(xdm_item=person)
                    
                    # Salva i dati della persona
                    people_data[person_id] = {
                        'id': person_id,
                        'full_name': full_name,
                        'silhouette': silhouette,
                        'names': names,
                        'gender': gender,
                        'notes': notes,
                        'inscriptions': [{
                            'title': inscription_title,
                            'link': inscription_link
                        }]
                    }
                    
                print(f"PROCESSATO: {filename}")
                
            except Exception as e:
                print(f"ERRORE nel file {filename}: {str(e)}")

    # Genera HTML per ogni persona
    people_html = ""
    for person_id in sorted(people_data.keys(), key=lambda x: people_data[x]['full_name']):
        person = people_data[person_id]
        
        # Header con immagine e nome
        silhouette_html = ""
        if person['silhouette']:
            silhouette_html = f'<img src="../../images/silhouette/{person["silhouette"]}" alt="Silhouette" class="silhouette">'
        
        people_html += f'<div class="person" id="{person["id"]}">\n'
        people_html += f'  {silhouette_html}<h3>{person["full_name"]}</h3>\n'
        people_html += '  <dl>\n'
        
        # Nomi
        for name in person['names']:
            people_html += f'    <dt>{name["type"]}</dt>\n'
            people_html += f'    <dd>{name["value"]}</dd>\n'
            
            # Se c'è nymRef per cognomen
            if name['type'] == 'cognomen' and name['nymref']:
                people_html += f'    <dt>origin of the cognomen</dt>\n'
                people_html += f'    <dd>{name["nymref"]}</dd>\n'
        
        # Gender
        gender_display = "male" if person['gender'] == 'm' else ("female" if person['gender'] == 'f' else "unknown")
        people_html += f'    <dt>gender</dt>\n'
        people_html += f'    <dd>{gender_display}</dd>\n'
        
        # Notes
        for note in person['notes']:
            people_html += f'    <dt>{note["type"]}</dt>\n'
            people_html += f'    <dd>{note["value"]}</dd>\n'
        
        # Inscriptions
        people_html += f'    <dt>inscription(s)</dt>\n'
        people_html += f'    <dd>'
        
        inscription_links = []
        for insc in person['inscriptions']:
            inscription_links.append(f'<a href="./inscriptions/{insc["link"]}">{insc["title"]}</a>')
        
        people_html += ' - '.join(inscription_links)
        people_html += '</dd>\n'
        
        people_html += '  </dl>\n'
        people_html += '</div>\n\n'
    
    # Template HTML completo
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
    <main style="padding: 20px;">
        <h2>People in the Inscriptions</h2>
        <p>This list is automatically generated from the EpiDoc XML files.</p>
        {people_html}
    </main>
    <footer>
        <p>Generated via Saxon-Che & GitHub Actions</p>
        <p>&copy; 2026 - Leonardo Battistella</p>
        <p><strong>Digital Approaches to the Inscriptions of the Eastern Necropolis of Julia Concordia</strong></p>
        <p>MA Thesis project in <em>Digital and Public Humanities</em> – Ca' Foscari University of Venice.</p>
        <p>This is a non-commercial, open-access research project for educational and scientific purposes only.</p>
    </footer>
</body>
</html>"""

    os.makedirs(output_dir, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(full_html)
    print(f"Fine: Pagina generata con {len(people_data)} persone.")

if __name__ == "__main__":
    run()
