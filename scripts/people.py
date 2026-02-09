import os
from saxonche import PySaxonProcessor

def run():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(script_dir, '..'))
    xml_dir = os.path.join(root_dir, 'inscriptions')
    output_dir = os.path.join(root_dir, 'docs', 'pages')
    output_file = os.path.join(output_dir, 'people.html')

    os.makedirs(output_dir, exist_ok=True)

    people_data = {}

    with PySaxonProcessor(license=False) as proc:
        xpath_processor = proc.new_xpath_processor()
        xpath_processor.declare_namespace("tei", "http://www.tei-c.org/ns/1.0")
        
        if not os.path.exists(xml_dir):
            return

        for filename in [f for f in os.listdir(xml_dir) if f.lower().endswith('.xml')]:
            xml_path = os.path.join(xml_dir, filename)
            try:
                node = proc.parse_xml(xml_file_name=xml_path)
                xpath_processor.set_context(xdm_item=node)
                
                # Estrazione titolo
                title_xdm = xpath_processor.evaluate("//tei:titleStmt/tei:title/text()")
                insc_title = title_xdm.item_at(0).string_value.strip() if title_xdm is not None and title_xdm.size > 0 else filename
                insc_link = filename.replace('.xml', '.html')

                # Estrazione persone
                persons = xpath_processor.evaluate("//tei:person")
                if persons is None:
                    continue
                
                for i in range(persons.size):
                    person = persons.item_at(i)
                    xpath_processor.set_context(xdm_item=person)
                    
                    # Convertiamo l'ID in stringa Python per poterlo ordinare dopo
                    p_id_xdm = xpath_processor.evaluate("string(@xml:id)")
                    p_id = p_id_xdm.string_value.strip() if p_id_xdm else f"unknown_{i}"
                    
                    if p_id in people_data:
                        if insc_link not in [link['url'] for link in people_data[p_id]['links']]:
                            people_data[p_id]['links'].append({'title': insc_title, 'url': insc_link})
                        continue

                    # Nome
                    name_xdm = xpath_processor.evaluate("string(.//tei:name[@type='full'])")
                    name = name_xdm.string_value.strip() if name_xdm else "Unknown Name"
                    
                    # Genere
                    gender_xdm = xpath_processor.evaluate("string(tei:gender/@value | tei:gender)")
                    gender = gender_xdm.string_value.strip() if gender_xdm else "u"

                    # Note (estrazione dinamica di tutti i tipi di note presenti)
                    notes = []
                    note_elements = xpath_processor.evaluate("tei:note")
                    if note_elements is not None:
                        for j in range(note_elements.size):
                            n = note_elements.item_at(j)
                            n_type = n.get_attribute_value("type") or "note"
                            n_val = n.string_value.strip()
                            notes.append({'label': n_type, 'text': n_val})

                    # Silhouette
                    img = "silhouette_female.png" if gender == 'f' else "silhouette_civil.png"

                    people_data[p_id] = {
                        'name': name,
                        'gender': gender,
                        'notes': notes,
                        'img': img,
                        'links': [{'title': insc_title, 'url': insc_link}]
                    }
            except Exception as e:
                print(f"Saltato file {filename} per errore: {e}")

    # Ordinamento e generazione HTML
    cards_html = ""
    # Ora sorted() funziona perché p_id è una stringa
    for pid in sorted(people_data.keys()):
        p = people_data[pid]
        notes_li = "".join([f"<li><strong>{n['label'].capitalize()}:</strong> {n['text']}</li>" for n in p['notes']])
        links_html = " | ".join([f'<a href="inscriptions/{l["url"]}">{l["title"]}</a>' for l in p['links']])
        
        cards_html += f"""
        <div class="person-card" style="border:1px solid #ddd; padding:15px; margin-bottom:15px; display:flex; gap:20px; background:#f9f9f9; border-radius:8px;">
            <img src="../../images/silhouette/{p['img']}" alt="silhouette" style="width:70px; height:70px;">
            <div>
                <h3 style="margin:0 0 10px 0; color:#800000;">{p['name']}</h3>
                <ul style="list-style:none; padding:0; margin:0; font-size:0.9em;">
                    <li><strong>Gender:</strong> {p['gender']}</li>
                    {notes_li}
                    <li style="margin-top:8px;"><strong>Found in:</strong> {links_html}</li>
                </ul>
            </div>
        </div>"""

    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Index of People - Iulia Concordia</title>
    <link rel="stylesheet" href="../css/style.css">
</head>
<body>
    <header>
        <h1 class="main_title">Digital Approaches to the Inscriptions of the Eastern Necropolis of <em>Iulia Concordia</em></h1>
        <nav class="navbar">
            <ul class="menu">
                <li><a href="../index.html">Home</a></li>
                <li><a href="inscriptions.html">Inscriptions</a></li>
                <li><a href="people.html">People</a></li>
            </ul>
        </nav>
    </header>
    <main class="container" style="padding:20px; max-width:800px; margin:auto;">
        <h2>Index of People</h2>
        <div class="people-list">
            {cards_html if cards_html else "<p>No people found in the XML record.</p>"}
        </div>
    </main>
    <footer style="text-align:center; padding:20px; font-size:0.8em;">
        <p>Generated via Saxon-Che | &copy; 2026 - Leonardo Battistella</p>
    </footer>
</body>
</html>"""

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(full_html)

if __name__ == "__main__":
    run()
