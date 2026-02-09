import os
from saxonche import PySaxonProcessor

def run():
    # 1. Setup percorsi
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(script_dir, '..'))
    xml_dir = os.path.join(root_dir, 'inscriptions')
    output_dir = os.path.join(root_dir, 'docs', 'pages')
    output_file = os.path.join(output_dir, 'people.html')

    os.makedirs(output_dir, exist_ok=True)

    if not os.path.exists(xml_dir):
        print(f"Errore: Cartella {xml_dir} non trovata.")
        return

    files = [f for f in os.listdir(xml_dir) if f.lower().endswith('.xml')]
    people_data = {}

    with PySaxonProcessor(license=False) as proc:
        xpath_processor = proc.new_xpath_processor()
        
        for filename in files:
            xml_path = os.path.join(xml_dir, filename)
            try:
                node = proc.parse_xml(xml_file_name=xml_path)
                xpath_processor.set_context(xdm_item=node)
                
                # Info Inscription per il link
                title_node = xpath_processor.evaluate("//*[local-name()='titleStmt']/*[local-name()='title']")
                insc_title = title_node.string_value.strip() if title_node else filename
                insc_link = filename.replace('.xml', '.html')

                # Trova tutti i tag <person>
                persons = xpath_processor.evaluate("//*[local-name()='person']")
                if persons is None: continue
                
                person_list = list(persons) if hasattr(persons, '__iter__') else [persons]

                for person in person_list:
                    xpath_processor.set_context(xdm_item=person)
                    
                    # xml:id (univoco)
                    p_id = xpath_processor.evaluate("@xml:id").string_value.strip()
                    
                    # Nome Full
                    full_name_node = xpath_processor.evaluate(".//*[local-name()='name'][@type='full']")
                    full_name = full_name_node.string_value.strip() if full_name_node else "Unknown"

                    # Se la persona esiste già (es. appare in 2 iscrizioni), aggiungiamo solo il link
                    if p_id in people_data:
                        if insc_link not in [i['link'] for i in people_data[p_id]['inscriptions']]:
                            people_data[p_id]['inscriptions'].append({'title': insc_title, 'link': insc_link})
                        continue

                    # Estrazione dettagli
                    gender_node = xpath_processor.evaluate(".//*[local-name()='gender']")
                    # Gestiamo sia <gender value="f"> che <gender>m</gender>
                    gender = gender_node.evaluate("@value").string_value.strip() if gender_node and xpath_processor.evaluate("@value") else (gender_node.string_value.strip() if gender_node else "u")
                    
                    occ_node = xpath_processor.evaluate(".//*[local-name()='note'][@type='occupation']")
                    occupation = occ_node.string_value.strip() if occ_node else ""
                    
                    # Altre note (rank, relationship, role)
                    extra_info = []
                    for note_type in ['rank', 'role', 'relationship']:
                        n_node = xpath_processor.evaluate(f".//*[local-name()='note'][@type='{note_type}']")
                        if n_node:
                            extra_info.append({'label': note_type, 'value': n_node.string_value.strip()})

                    # Logica Silhouette
                    silhouette = "silhouette_civil.png" # default
                    if gender == 'f':
                        silhouette = "silhouette_female.png"
                    elif 'soldier' in occupation.lower() or 'domesticus' in str(extra_info).lower():
                        silhouette = "silhouette_soldier.png"

                    people_data[p_id] = {
                        'name': full_name,
                        'gender': "Female" if gender == 'f' else ("Male" if gender == 'm' else "Unknown"),
                        'occupation': occupation,
                        'extra': extra_info,
                        'silhouette': silhouette,
                        'inscriptions': [{'title': insc_title, 'link': insc_link}]
                    }

            except Exception as e:
                print(f"Errore nel file {filename}: {e}")

    # 4. Generazione HTML
    cards_html = ""
    for pid in sorted(people_data.keys()):
        p = people_data[pid]
        
        # Percorso immagine (dalla cartella docs/pages/ va a docs/images/...)
        img_path = f"../../images/silhouette/{p['silhouette']}"
        
        cards_html += f"""
        <div class="person-card" style="border: 1px solid #ddd; border-radius: 8px; padding: 15px; margin-bottom: 20px; background: #fff; display: flex; align-items: center;">
            <img src="{img_path}" alt="silhouette" style="width: 80px; height: 80px; margin-right: 20px;">
            <div class="person-info">
                <h3 style="margin-top: 0; color: #800000;">{p['name']}</h3>
                <p><strong>Gender:</strong> {p['gender']}</p>
                <p><strong>Occupation:</strong> {p['occupation'] if p['occupation'] else 'N/A'}</p>
                {' '.join([f'<p><strong>{ex["label"].capitalize()}:</strong> {ex["value"]}</p>' for ex in p['extra']])}
                <p><strong>Found in:</strong> 
                    {' | '.join([f'<a href="inscriptions/{i["link"]}">{i["title"]}</a>' for i in p['inscriptions']])}
                </p>
            </div>
        </div>"""

    # Template
    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
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
    <main class="container" style="padding: 20px; max-width: 900px; margin: auto;">
        <h2>Index of People</h2>
        <p>This list includes all individuals mentioned in the epigraphic record of the Eastern Necropolis.</p>
        <div class="people-grid">
            {cards_html if cards_html else "<p>No people found.</p>"}
        </div>
    </main>
    <footer style="text-align:center; padding: 20px; font-size: 0.8em;">
        <p>Generated via Saxon-Che & GitHub Actions | &copy; 2026 - Leonardo Battistella</p>
    </footer>
</body>
</html>"""

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(full_html)
    print(f"Successo! Generata pagina per {len(people_data)} persone.")

if __name__ == "__main__":
    run()
