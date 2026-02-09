import os
from saxonche import PySaxonProcessor

def run():
    base_dir = os.getcwd()
    xml_dir = os.path.join(base_dir, 'inscriptions')
    output_dir = os.path.join(base_dir, 'docs', 'pages')
    output_file = os.path.join(output_dir, 'people.html')

    if not os.path.exists(xml_dir):
        return

    people_data = {}
    # Dizionario per mappare xml:id → nome completo (per i link relationship)
    people_names = {}

    with PySaxonProcessor(license=False) as proc:
        xpath_processor = proc.new_xpath_processor()
        files = [f for f in os.listdir(xml_dir) if f.lower().endswith('.xml')]

        # PRIMO PASSAGGIO: raccogli tutti i nomi
        for filename in files:
            xml_path = os.path.join(xml_dir, filename)
            try:
                node = proc.parse_xml(xml_file_name=xml_path)
                xpath_processor.set_context(xdm_item=node)
                
                persons = xpath_processor.evaluate("//*[local-name()='person']")
                if persons is not None and persons.size > 0:
                    for i in range(persons.size):
                        person = persons.item_at(i)
                        xpath_processor.set_context(xdm_item=person)
                        
                        id_item = xpath_processor.evaluate("string(@*[local-name()='id'])")
                        p_id = id_item.string_value.strip() if id_item and hasattr(id_item, 'string_value') and id_item.string_value else None
                        
                        if p_id:
                            full_name_item = xpath_processor.evaluate(".//*[local-name()='name'][@type='full']")
                            if full_name_item and full_name_item.size > 0:
                                people_names[p_id] = full_name_item.item_at(0).string_value.strip()
            except:
                pass

        # SECONDO PASSAGGIO: raccogli tutti i dati
        for filename in files:
            xml_path = os.path.join(xml_dir, filename)
            try:
                node = proc.parse_xml(xml_file_name=xml_path)
                xpath_processor.set_context(xdm_item=node)
                
                # Titolo iscrizione
                title_item = xpath_processor.evaluate("//*[local-name()='titleStmt']/*[local-name()='title'][1]")
                if title_item and title_item.size > 0:
                    display_title = title_item.item_at(0).string_value.strip()
                else:
                    display_title = filename
                target_link = "inscriptions/" + filename.replace('.xml', '.html')

                # Trova tutte le persone
                persons = xpath_processor.evaluate("//*[local-name()='person']")
                
                if persons is not None and persons.size > 0:
                    for i in range(persons.size):
                        person = persons.item_at(i)
                        xpath_processor.set_context(xdm_item=person)
                        
                        # ID
                        id_item = xpath_processor.evaluate("string(@*[local-name()='id'])")
                        p_id = id_item.string_value.strip() if id_item and hasattr(id_item, 'string_value') and id_item.string_value else f"p_{filename}_{i}"

                        # Se già esiste, aggiungi solo il link E unisci le note se diverse
                        if p_id in people_data:
                            people_data[p_id]['links'].append({'title': display_title, 'url': target_link})
                            
                            # Aggiungi note se non già presenti
                            note_elements_new = xpath_processor.evaluate(".//*[local-name()='note']")
                            if note_elements_new and note_elements_new.size > 0:
                                for j in range(note_elements_new.size):
                                    n = note_elements_new.item_at(j)
                                    n_type = n.get_attribute_value("type") or "info"
                                    n_value = n.string_value.strip()
                                    corresp = n.get_attribute_value("corresp")
                                    
                                    # Verifica se questa nota esiste già
                                    note_exists = False
                                    for existing_note in people_data[p_id]['notes']:
                                        if existing_note['type'] == n_type and existing_note['value'] == n_value:
                                            note_exists = True
                                            break
                                    
                                    if not note_exists:
                                        people_data[p_id]['notes'].append({
                                            'type': n_type,
                                            'value': n_value,
                                            'corresp': corresp
                                        })
                            
                            continue

                        # Tutti i nomi
                        names_data = []
                        name_elements = xpath_processor.evaluate(".//*[local-name()='persName']/*[local-name()='name']")
                        if name_elements and name_elements.size > 0:
                            for j in range(name_elements.size):
                                name_elem = name_elements.item_at(j)
                                name_type = name_elem.get_attribute_value("type") or "name"
                                if name_type == "full":
                                    continue
                                name_value = name_elem.string_value.strip()
                                nymref = name_elem.get_attribute_value("nymRef")
                                
                                names_data.append({
                                    'type': name_type,
                                    'value': name_value,
                                    'nymref': nymref
                                })

                        # Nome completo per titolo
                        full_name_item = xpath_processor.evaluate(".//*[local-name()='name'][@type='full']")
                        if full_name_item and full_name_item.size > 0:
                            p_name = full_name_item.item_at(0).string_value.strip()
                        else:
                            p_name = "Unknown"

                        # Genere
                        g_item = xpath_processor.evaluate(".//*[local-name()='gender']")
                        if g_item and g_item.size > 0:
                            p_gender = g_item.item_at(0).string_value.strip()
                        else:
                            p_gender = "unknown"

                        # Note
                        notes_data = []
                        occupation = None
                        note_elements = xpath_processor.evaluate(".//*[local-name()='note']")
                        if note_elements and note_elements.size > 0:
                            for j in range(note_elements.size):
                                n = note_elements.item_at(j)
                                n_type = n.get_attribute_value("type") or "info"
                                n_value = n.string_value.strip()
                                corresp = n.get_attribute_value("corresp")
                                
                                notes_data.append({
                                    'type': n_type,
                                    'value': n_value,
                                    'corresp': corresp
                                })
                                
                                if n_type == "occupation":
                                    occupation = n_value

                        # Logica Silhouette
                        img = None
                        if p_gender == 'f':
                            img = "silhouette_female.png"
                        elif p_gender == 'm':
                            if occupation in ['civil', 'civil?']:
                                img = "silhouette_civil.png"
                            elif occupation in ['soldier', 'soldier?']:
                                img = "silhouette_soldier.png"
                            elif occupation in ['fabricensis', 'fabricensis?']:
                                img = "silhouette_fabricensis.png"
                            elif occupation in ['functionary', 'functionary?']:
                                img = "silhouette_functionary.png"

                        people_data[p_id] = {
                            'id': p_id,
                            'name': p_name,
                            'gender': p_gender,
                            'names': names_data,
                            'notes': notes_data,
                            'img': img,
                            'links': [{'title': display_title, 'url': target_link}]
                        }
                        
            except Exception as e:
                print(f"Errore su {filename}: {e}")

    # Generazione Card
    cards = ""
    for pid in sorted(people_data.keys(), key=lambda x: people_data[x]['name']):
        p = people_data[pid]
        
        # Immagine
        img_html = ""
        if p['img']:
            img_html = f'<img src="../images/silhouette/{p["img"]}" alt="silhouette">'
        
        # Costruisci dl
        dl_content = ""
        
        # Nomi
        for name in p['names']:
            dl_content += f"<dt>{name['type']}</dt><dd>{name['value']}</dd>"
            if name['type'] == 'cognomen' and name['nymref']:
                dl_content += f"<dt>origin of the cognomen</dt><dd>{name['nymref']}</dd>"
        
        # Gender
        gender_display = "male" if p['gender'] == 'm' else ("female" if p['gender'] == 'f' else "unknown")
        dl_content += f"<dt>gender</dt><dd>{gender_display}</dd>"
        
        # Notes con gestione relationship
        for note in p['notes']:
            dl_content += f"<dt>{note['type']}</dt><dd>{note['value']}"
            
            # Se è relationship e c'è corresp, aggiungi link
            if note['type'] == 'relationship' and note.get('corresp'):
                corresp_id = note['corresp'].strip()
                # Rimuovi # iniziale se presente
                if corresp_id.startswith('#'):
                    corresp_id = corresp_id[1:]
                
                # Trova il nome della persona correlata
                if corresp_id in people_names:
                    related_name = people_names[corresp_id]
                    dl_content += f' (→ <a href="#{corresp_id}">{related_name}</a>)'
            
            dl_content += "</dd>"
        
        # Inscriptions
        links_str = " - ".join([f'<a href="{l["url"]}">{l["title"]}</a>' for l in p['links']])
        dl_content += f"<dt>inscription(s)</dt><dd>{links_str}</dd>"
        
        cards += f"""
        <div class="person" id="{p['id']}">
            {img_html}
            <div>
                <h3>{p['name']}</h3>
                <dl>
                    {dl_content}
                </dl>
            </div>
        </div>"""

    # Template HTML
    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>People - Iulia Concordia</title>
    <link rel="stylesheet" href="../css/style.css">
</head>
<body>
    <header>
        <h1 class="main_title">Digital Approaches to the Inscriptions of the Eastern Necropolis of <em>Iulia Concordia</em></h1>
        <nav class="navbar">
            <ul class="menu">
                <li><a href="../index.html">Home</a></li>
                <li><a href="./inscriptions.html">Inscriptions</a></li>
                <li><a href="people.html">People</a></li>
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
        <h2>People in the Inscriptions</h2>
        <p>This list is automatically generated from the EpiDoc XML files.</p>
        <div class="people-list">
            {cards if cards else "<p>No people found.</p>"}
        </div>
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
