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
                title_xpath = "//*[local-name()='titleStmt']/*[local-name()='title'][1]"
                title_item = xpath_processor.evaluate(title_xpath)
                display_title = title_item.item_at(0).string_value.strip() if title_item.size > 0 else filename
                target_link = "inscriptions/" + filename.replace('.xml', '.html')

                # Trova tutte le persone
                persons = xpath_processor.evaluate("//*[local-name()='person']")
                
                if persons is not None and persons.size > 0:
                    for i in range(persons.size):
                        person = persons.item_at(i)
                        xpath_processor.set_context(xdm_item=person)
                        
                        # ID
                        id_val = xpath_processor.evaluate("string(@*[local-name()='id'])")
                        p_id = id_val.string_value.strip() if id_val else f"p_{filename}_{i}"

                        if p_id in people_data:
                            people_data[p_id]['links'].append({'title': display_title, 'url': target_link})
                            continue

                        # Nome
                        n_item = xpath_processor.evaluate(".//*[local-name()='name']")
                        p_name = n_item.item_at(0).string_value.strip() if n_item.size > 0 else "Unknown"

                        # Genere
                        g_item = xpath_processor.evaluate(".//*[local-name()='gender']")
                        p_gender = g_item.item_at(0).string_value.strip().lower() if g_item.size > 0 else ""

                        # Occupazione per Silhouette
                        occ_xpath = ".//*[local-name()='note'][@type='occupation']"
                        occ_item = xpath_processor.evaluate(occ_xpath)
                        p_occ = occ_item.item_at(0).string_value.strip().lower() if occ_item.size > 0 else ""

                        # Logica Silhouette (Tua Specifica)
                        img = None
                        if p_gender == 'f':
                            img = "silhouette_female.png"
                        elif "soldier" in p_occ:
                            img = "silhouette_soldier.png"
                        elif "civil" in p_occ and p_gender == 'm':
                            img = "silhouette_civil.png"
                        elif "fabricensis" in p_occ:
                            img = "silhouette_fabricensis.png"
                        elif "functionary" in p_occ:
                            img = "silhouette_functionary.png"

                        # Note (per l'elenco della scheda)
                        notes_list = []
                        note_elements = xpath_processor.evaluate(".//*[local-name()='note']")
                        if note_elements.size > 0:
                            for j in range(note_elements.size):
                                n = note_elements.item_at(j)
                                n_type = n.get_attribute_value("type") or "info"
                                notes_list.append(f"<li><strong>{n_type.capitalize()}:</strong> {n.string_value.strip()}</li>")

                        people_data[p_id] = {
                            'name': p_name,
                            'gender': p_gender,
                            'notes': "".join(notes_list),
                            'img': img,
                            'links': [{'title': display_title, 'url': target_link}]
                        }
            except Exception as e:
                print(f"Errore su {filename}: {e}")

    # Generazione Card
    cards = ""
    for pid in sorted(people_data.keys()):
        p = people_data[pid]
        links_str = ", ".join([f'<a href="{l["url"]}">{l["title"]}</a>' for l in p['links']])
        img_html = f'<img src="../images/silhouette/{p["img"]}" style="width:70px; height:70px;" alt="silhouette">' if p['img'] else ''
        
        cards += f"""
        <div class="person-card" style="border:1px solid #ddd; padding:15px; margin-bottom:15px; display:flex; gap:20px; background:#f9f9f9; border-radius:8px;">
            {img_html}
            <div>
                <h3 style="margin:0; color:#800000;">{p['name']}</h3>
                <ul style="list-style:none; padding:0; margin:10px 0; font-size:0.9em;">
                    <li><strong>Gender:</strong> {p['gender']}</li>
                    {p['notes']}
                    <li style="margin-top:5px;"><strong>Found in:</strong> {links_str}</li>
                </ul>
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
                <li><a href="people.html">People</a></li>
            </ul>
        </nav>
    </header>
    <main class="container" style="padding:20px; max-width:800px; margin:auto;">
        <h2>Index of People</h2>
        <div class="people-list">
            {cards if cards else "<p>No people found.</p>"}
        </div>
    </main>
    <footer style="text-align:center; padding:20px; font-size:0.8em;">
        <p>Generated via Saxon-Che | &copy; 2026 - Leonardo Battistella</p>
    </footer>
</body>
</html>"""

    os.makedirs(output_dir, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(full_html)

if __name__ == "__main__":
    run()
