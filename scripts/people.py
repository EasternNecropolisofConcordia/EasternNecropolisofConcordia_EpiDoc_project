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

    with PySaxonProcessor(license=False) as proc:
        xpath_processor = proc.new_xpath_processor()
        files = [f for f in os.listdir(xml_dir) if f.lower().endswith('.xml')]

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

                        # Se già esiste, aggiungi solo il link
                        if p_id in people_data:
                            people_data[p_id]['links'].append({'title': display_title, 'url': target_link})
                            continue

                        # Tutti i nomi
                        names_data = []
                        name_elements = xpath_processor.evaluate(".//*[local-name()='persName']/*[local-name()='name']")
                        if name_elements and name_elements.size > 0:
                            for j in range(name_elements.size):
                                name_elem = name_elements.item_at(j)
                                name_type = name_elem.get_attribute_value("type") or "name"
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
                                notes_data.append({
                                    'type': n_type,
                                    'value': n_value
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
            img_html = f'<img src="../images/silhouette/{p["img"]}" style="width:70px; height:70px;" alt="silhouette">'
        
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
        
        # Notes
        for note in p['notes']:
            dl_content += f"<dt>{note['type']}</dt><dd>{note['value']}</dd>"
        
        # Inscriptions
        links_str = " - ".join([f'<a href="{l["url"]}">{l["title"]}</a>' for l in p['links']])
        dl_content += f"<dt>inscription(s)</dt><dd>{links_str}</dd>"
        
        cards += f"""
        <div class="person" id="{p['id']}" style="border:1px solid #ddd; padding:15px; margin-bottom:15px; display:flex; gap:20px; background:#f9f9f9; border-radius:8px;">
            {img_html}
            <div style="flex:1;">
                <h3 style="margin:0 0 10px 0; color:#800000;">{p['name']}</h3>
                <dl style="margin:0; font-size:0.9em;">
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
    <main class="container" style="padding:20px; max-width:900px; margin:auto;">
        <h2>People in the Inscriptions</h2>
        <p>This list is automatically generated from the EpiDoc XML files.</p>
        <div class="people-list">
            {cards if cards else "<p>No people found.</p>"}
        </div>
    </main>
    <footer style="text-align:center; padding:20px; font-size:0.8em; margin-top:40px; border-top:1px solid #ddd;">
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
