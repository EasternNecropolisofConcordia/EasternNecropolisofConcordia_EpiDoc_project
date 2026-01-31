import os
from saxonche import PySaxonProcessor

def run():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(script_dir, '..'))
    
    xml_dir = os.path.join(root_dir, 'inscriptions')
    output_dir = os.path.join(root_dir, 'docs', 'pages')
    output_file = os.path.join(output_dir, 'inscriptions.html')

    print(f"DEBUG: Cerco XML in: {xml_dir}")

    if not os.path.exists(xml_dir):
        print(f"ERRORE: La cartella {xml_dir} non esiste!")
        return

    files = [f for f in os.listdir(xml_dir) if f.lower().endswith('.xml')]
    print(f"DEBUG: File trovati: {files}")

    inscriptions_data = []

    with PySaxonProcessor(license=False) as proc:
        # Inizializziamo il processore XPath
        xpath_processor = proc.new_xpath_processor()
        
        for filename in files:
            xml_path = os.path.join(xml_dir, filename)
            try:
                # Carichiamo il documento XML
                node = proc.parse_xml(xml_file_name=xml_path)
                xpath_processor.set_context_item(xdm_item=node)
                
                # XPath per titoli e idno (ignora i namespace)
                title_val = xpath_processor.evaluate("//*[local-name()='titleStmt']/*[local-name()='title'][1]")
                idno_val = xpath_processor.evaluate("//*[local-name()='idno'][@type='filename'][1]")
                
                display_title = title_val.string_value.strip() if title_val else filename
                filename_idno = idno_val.string_value.strip() if idno_val else filename
                
                # Creiamo il link puntando al file .html generato da transform.py
                target_link = filename_idno.replace('.xml', '.html')
                
                inscriptions_data.append({'title': display_title, 'link': target_link})
                print(f"REGISTRATO: {display_title} -> {target_link}")
            except Exception as e:
                print(f"ERRORE nel file {filename}: {e}")

    inscriptions_data.sort(key=lambda x: x['title'])
    
    links_html = "".join([f'<li><a href="{item["link"]}">{item["title"]}</a></li>' for item in inscriptions_data])
    if not inscriptions_data:
        links_html = "<li>Nessuna iscrizione trovata.</li>"

    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Inscriptions - Iulia Concordia</title>
    <link rel="stylesheet" href="../css/style.css">
</head>
<body>
    <header>
        <h1 class="main_title">Digital Approaches to the Inscriptions of the Eastern Necropolis of Iulia Concordia</h1>
        <nav class="navbar">
            <ul class="menu">
                <li><a href="../index.html">Home</a></li>
                <li><a href="inscriptions.html">Inscriptions</a></li>
                <li><a href="history.html">History of the Eastern Necropolis</a></li>
                <li><a href="abouttheinscriptions.html">About the inscriptions</a></li>
                <li><a href="about.html">About this project</a></li>
            </ul>
        </nav>
    </header>
    <main style="padding: 20px;">
        <h2>Index of Encoded Inscriptions</h2>
        <ul class="inscription-list">
            {links_html}
        </ul>
    </main>
</body>
</html>"""

    os.makedirs(output_dir, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(full_html)
    print(f"SUCCESSO: Pagina generata con {len(inscriptions_data)} iscrizioni.")

if __name__ == "__main__":
    run()
