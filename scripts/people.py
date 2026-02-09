import os
from saxonche import PySaxonProcessor

def run():
    # Percorsi assoluti per evitare errori su GitHub Actions
    base_dir = os.getcwd()
    xml_dir = os.path.join(base_dir, 'inscriptions')
    output_dir = os.path.join(base_dir, 'docs', 'pages')
    output_file = os.path.join(output_dir, 'people.html')

    print(f"Cercando file XML in: {xml_dir}")

    if not os.path.exists(xml_dir):
        print("ERRORE: Cartella inscriptions non trovata!")
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
                
                # Recupero dati iscrizione (uguale al tuo script funzionante)
                title_item = xpath_processor.evaluate("//*[local-name()='titleStmt']/*[local-name()='title'][1]")
                display_title = title_item.string_value.strip() if title_item else filename
                target_link = "inscriptions/" + filename.replace('.xml', '.html')

                # Cerchiamo le persone ovunque nel documento
                # Usiamo //*[local-name()='person'] per massima compatibilità
                persons = xpath_processor.evaluate("//*[local-name()='person']")
                
                if persons is not None:
                    for i in range(persons.size):
                        person = persons.item_at(i)
                        xpath_processor.set_context(xdm_item=person)
                        
                        # ID della persona
                        id_val = xpath_processor.evaluate("string(@*[local-name()='id'])")
                        p_id = id_val.string_value.strip() if id_val else f"id_{filename}_{i}"

                        if p_id in people_data:
                            people_data[p_id]['links'].append({'title': display_title, 'url': target_link})
                            continue

                        # Nome e Genere
                        name_item = xpath_processor.evaluate(".//*[local-name()='name'][@type='full']")
                        name = name_item.string_value.strip() if name_item else "Unknown"

                        gen_item = xpath_processor.evaluate(".//*[local-name()='gender']")
                        gender = gen_item.string_value.strip() if gen_item else "not specified"

                        # Note
                        notes = []
                        note_elements = xpath_processor.evaluate(".//*[local-name()='note']")
                        if note_elements:
                            for j in range(note_elements.size):
                                n = note_elements.item_at(j)
                                n_type = n.get_attribute_value("type") or "note"
                                notes.append(f"<li><strong>{n_type.capitalize()}:</strong> {n.string_value.strip()}</li>")

                        img = "silhouette_female.png" if gender == 'f' else "silhouette_civil.png"

                        people_data[p_id] = {
                            'name': name,
                            'gender': gender,
                            'notes': "".join(notes),
                            'img': img,
                            'links': [{'title': display_title, 'url': target_link}]
                        }
            except Exception as e:
                print(f"Errore su {filename}: {e}")

    # Costruzione schede
    cards = ""
    for pid in sorted(people_data.keys()):
        p = people_data[pid]
        links = ", ".join([f'<a href="{l["url"]}">{l["title"]}</a>' for l in p['links']])
        cards += f"""
        <div class="person-card" style="border:1px solid #ddd; padding:15px; margin-bottom:15px; display:flex; gap:20px; background:#f9f9f9;">
            <img src="../../images/silhouette/{p['img']}" style="width:70px; height:70px;">
            <div>
                <h3 style="margin:0; color:#800000;">{p['name']}</h3>
                <ul style="list-style:none; padding:0; margin:10px 0; font-size:0.9em;">
                    <li><strong>Gender:</strong> {p['gender']}</li>
                    {p['notes']}
                    <li style="margin-top:5px;"><strong>Found in:</strong> {links}</li>
                </ul>
            </div>
        </div>"""

    # HTML finale
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
                <li><a href="people.html">People</a></li>
            </ul>
        </nav>
    </header>
    <main class="container" style="padding:20px; max-width:800px; margin:auto;">
        <h2>Index of People</h2>
        <div class="people-list">
            {cards if cards else "<p>No people found in the XML record.</p>"}
        </div>
    </main>
    <footer style="text-align:center; padding:20px;">
        <p>Generated via Saxon-Che | &copy; 2026 - Leonardo Battistella</p>
    </footer>
</body>
</html>"""

    os.makedirs(output_dir, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(full_html)

if __name__ == "__main__":
    run()
