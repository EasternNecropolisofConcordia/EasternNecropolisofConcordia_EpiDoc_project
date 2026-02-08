import os
from saxonche import PySaxonProcessor

def run():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(script_dir, '..'))
    
    xml_dir = os.path.join(root_dir, 'inscriptions')
    output_dir = os.path.join(root_dir, 'docs', 'pages')
    output_file = os.path.join(output_dir, 'inscriptions.html')

    if not os.path.exists(xml_dir):
        print(f"ERRORE: La cartella {xml_dir} non esiste!")
        return

    files = [f for f in os.listdir(xml_dir) if f.lower().endswith('.xml')]
    inscriptions_data = []

    with PySaxonProcessor(license=False) as proc:
        xpath_processor = proc.new_xpath_processor()
        
        for filename in files:
            xml_path = os.path.join(xml_dir, filename)
            try:
                node = proc.parse_xml(xml_file_name=xml_path)
                xpath_processor.set_context(xdm_item=node)
                
                # XPath per il titolo TEI
                title_item = xpath_processor.evaluate("//*[local-name()='titleStmt']/*[local-name()='title'][1]")
                idno_item = xpath_processor.evaluate("//*[local-name()='idno'][@type='filename'][1]")
                
                # Usiamo .string_value per ottenere il testo contenuto nel tag
                if title_item is not None:
                    display_title = title_item.string_value.strip()
                else:
                    display_title = filename

                # Determiniamo il link
                if idno_item is not None:
                    target_link = "inscriptions/" + idno_item.string_value.strip().replace('.xml', '.html')
                else:
                    target_link = "inscriptions/" + filename.replace('.xml', '.html')
                
                inscriptions_data.append({'title': display_title, 'link': target_link})
                print(f"REGISTRATO: {display_title}")
                
            except Exception as e:
                print(f"ERRORE nel file {filename}: {str(e)}")
                inscriptions_data.append({'title': filename, 'link': "inscriptions/" + filename.replace('.xml', '.html')})

    # Ordinamento alfabetico
    inscriptions_data.sort(key=lambda x: x['title'])
    
    # Costruzione della lista link
    links_html = "".join([f'<li><a href="{item["link"]}">{item["title"]}</a></li>' for item in inscriptions_data])
    
    # Template con Navbar (uguale a quella delle singole iscrizioni)
    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Inscriptions - Iulia Concordia</title>
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
        <h2>Index of Encoded Inscriptions</h2>
        <p>This list is automatically updated from the EpiDoc XML files.</p>
        <ul class="inscription-list">
            {links_html}
        </ul>
    </main>
    <footer>
        <p>Generated via Saxon-Che & GitHub Actions</p>
        <p>&copy; 2026 - Leonardo Battistella</p>
        <p><strong>Digital Approaches to the Inscriptions of the Eastern Necropolis of Julia Concordia</strong></p>
        <p>MA Thesis project in <em>Digital and Public Humanities</em> – Ca’ Foscari University of Venice.</p>
        <p>This is a non-commercial, open-access research project for educational and scientific purposes only.</p>
    </footer>
</body>
</html>"""

    os.makedirs(output_dir, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(full_html)
    print(f"Fine: Pagina generata con {len(inscriptions_data)} link.")

if __name__ == "__main__":
    run()
