import os
from saxonche import PySaxonProcessor

def generate_inscriptions_page():
    # GitHub Actions definisce 'GITHUB_WORKSPACE' come la radice della repo
    # Se siamo in locale, usiamo il percorso corrente
    base_path = os.environ.get('GITHUB_WORKSPACE', os.getcwd())
    
    xml_dir = os.path.join(base_path, 'inscriptions')
    output_dir = os.path.join(base_path, 'docs', 'pages')
    output_file = os.path.join(output_dir, 'inscriptions.html')
    
    inscriptions_data = []

    print(f"--- DEBUG INFO ---")
    print(f"Base Path: {base_path}")
    print(f"XML Dir: {xml_dir}")
    
    if not os.path.exists(xml_dir):
        print(f"ERRORE: La cartella {xml_dir} non esiste!")
        return

    # Leggiamo i file
    files = [f for f in os.listdir(xml_dir) if f.lower().endswith('.xml')]
    print(f"File XML trovati: {len(files)}")

    with PySaxonProcessor(license=False) as proc:
        for filename in files:
            xml_path = os.path.join(xml_dir, filename)
            try:
                node = proc.parse_xml(xml_file_name=xml_path)
                
                # XPath per estrarre titolo e filename (senza preoccuparsi dei namespace)
                title_node = proc.xpath_eval("//*[local-name()='titleStmt']/*[local-name()='title']", node)
                idno_node = proc.xpath_eval("//*[local-name()='idno'][@type='filename']", node)
                
                display_title = title_node[0].string_value.strip() if title_node else filename
                
                # Determiniamo il link HTML
                if idno_node:
                    target_link = idno_node[0].string_value.strip().replace('.xml', '.html')
                else:
                    target_link = filename.replace('.xml', '.html')
                
                inscriptions_data.append({'title': display_title, 'link': target_link})
                print(f"Letto: {display_title}")
            except Exception as e:
                print(f"Errore nel file {filename}: {e}")

    # Ordinamento
    inscriptions_data.sort(key=lambda x: x['title'])

    # Creazione della lista HTML
    if inscriptions_data:
        links_html = "".join([f'<li><a href="{item["link"]}">{item["title"]}</a></li>' for item in inscriptions_data])
    else:
        links_html = "<li>Nessun file XML trovato nella cartella inscriptions.</li>"

    # Layout finale
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
        <p>Totale iscrizioni: {len(inscriptions_data)}</p>
        <ul class="inscription-list">{links_html}</ul>
    </main>
</body>
</html>"""

    os.makedirs(output_dir, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(full_html)
    print(f"Pagina generata con successo: {output_file}")

if __name__ == "__main__":
    generate_inscriptions_page()
