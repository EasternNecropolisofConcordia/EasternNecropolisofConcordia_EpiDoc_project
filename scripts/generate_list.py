import os
from saxonche import PySaxonProcessor

def generate_inscriptions_page():
    # Cerchiamo di capire dove siamo
    base_dir = os.getcwd()
    xml_dir = os.path.join(base_dir, 'inscriptions')
    output_file = os.path.join(base_dir, 'docs', 'pages', 'inscriptions.html')
    
    inscriptions_data = []

    print(f"Cartella di lavoro attuale: {base_dir}")
    print(f"Cerco file XML in: {xml_dir}")

    if not os.path.exists(xml_dir):
        print(f"ERRORE: La cartella {xml_dir} NON ESISTE!")
        # Elenca i file presenti per debug
        print(f"Contenuto della root: {os.listdir(base_dir)}")
        return

    all_files = os.listdir(xml_dir)
    print(f"File trovati nella cartella inscriptions: {all_files}")

    with PySaxonProcessor(license=False) as proc:
        for filename in all_files:
            if filename.lower().endswith('.xml'): # .XML o .xml
                xml_path = os.path.join(xml_dir, filename)
                try:
                    node = proc.parse_xml(xml_file_name=xml_path)
                    
                    # XPath che cerca ovunque nel documento per sicurezza
                    title_xpath = "(//*[local-name()='titleStmt']/*[local-name()='title'])[1]"
                    idno_xpath = "//*[local-name()='idno'][@type='filename']"
                    
                    title_nodes = proc.xpath_eval(title_xpath, node)
                    idno_nodes = proc.xpath_eval(idno_xpath, node)
                    
                    display_title = title_nodes[0].string_value.strip() if title_nodes else filename
                    idno_val = idno_nodes[0].string_value.strip() if idno_nodes else None

                    target_link = idno_val.replace('.xml', '.html') if idno_val else filename.replace('.xml', '.html')
                    
                    inscriptions_data.append({'title': display_title, 'link': target_link})
                    print(f" -> OK: {display_title}")

                except Exception as e:
                    print(f" -> ERRORE nel file {filename}: {e}")

    inscriptions_data.sort(key=lambda x: x['title'])
    
    links_html = "".join([f'<li><a href="{item["link"]}">{item["title"]}</a></li>' for item in inscriptions_data])
    if not inscriptions_data:
        links_html = "<li>Nessuna iscrizione trovata (controlla i log delle Actions).</li>"

    full_html = f"""<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <title>Inscriptions - Iulia Concordia</title>
    <link rel="stylesheet" href="../css/style.css">
</head>
<body>
    <header>
        <h1 class="main_title">Digital Approaches to Iulia Concordia</h1>
        <nav class="navbar">
            <ul class="menu">
                <li><a href="../index.html">Home</a></li>
                <li><a href="inscriptions.html">Inscriptions</a></li>
                <li><a href="history.html">History</a></li>
                <li><a href="abouttheinscriptions.html">About</a></li>
                <li><a href="about.html">Project</a></li>
            </ul>
        </nav>
    </header>
    <main style="padding: 20px;">
        <h2>Index of Encoded Inscriptions</h2>
        <p>Trovate {len(inscriptions_data)} iscrizioni.</p>
        <ul>{links_html}</ul>
    </main>
</body>
</html>"""
    
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(full_html)
    print(f"Fine. Pagina generata in {output_file}")

if __name__ == "__main__":
    generate_inscriptions_page()
