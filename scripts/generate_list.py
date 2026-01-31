import os
from saxonche import PySaxonProcessor

def run():
    # 1. IDENTIFICAZIONE PERCORSI (Forziamo la ricerca dalla radice)
    # Cerchiamo di risalire alla root partendo dalla posizione dello script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(script_dir, '..'))
    
    xml_dir = os.path.join(root_dir, 'inscriptions')
    output_dir = os.path.join(root_dir, 'docs', 'pages')
    output_file = os.path.join(output_dir, 'inscriptions.html')

    print(f"DEBUG: Script si trova in: {script_dir}")
    print(f"DEBUG: Root del progetto individuata: {root_dir}")
    print(f"DEBUG: Cerco XML in: {xml_dir}")

    # 2. VERIFICA ESISTENZA CARTELLA
    if not os.path.exists(xml_dir):
        print(f"ERRORE CRITICO: La cartella {xml_dir} non esiste!")
        print(f"Contenuto della root attuale: {os.listdir(root_dir)}")
        return

    # 3. ELENCO FILE
    files = [f for f in os.listdir(xml_dir) if f.lower().endswith('.xml')]
    print(f"DEBUG: File trovati nella cartella: {files}")

    inscriptions_data = []

    # 4. ELABORAZIONE CON SAXON
    with PySaxonProcessor(license=False) as proc:
        for filename in files:
            xml_path = os.path.join(xml_dir, filename)
            try:
                node = proc.parse_xml(xml_file_name=xml_path)
                
                # XPath ultra-semplice per i titoli
                title_node = proc.xpath_eval("//*[local-name()='titleStmt']/*[local-name()='title']", node)
                idno_node = proc.xpath_eval("//*[local-name()='idno'][@type='filename']", node)
                
                title_text = title_node[0].string_value.strip() if title_node else filename
                
                if idno_node:
                    link_text = idno_node[0].string_value.strip().replace('.xml', '.html')
                else:
                    link_text = filename.replace('.xml', '.html')
                
                inscriptions_data.append({'title': title_text, 'link': link_text})
                print(f"REGISTRATO: {title_text}")
            except Exception as e:
                print(f"ERRORE nel file {filename}: {e}")

    # 5. GENERAZIONE HTML
    inscriptions_data.sort(key=lambda x: x['title'])
    
    links_html = ""
    if not inscriptions_data:
        links_html = "<li>Attenzione: Nessun file XML elaborato correttamente.</li>"
    else:
        for item in inscriptions_data:
            links_html += f'<li><a href="{item["link"]}">{item["title"]}</a></li>\n'

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
    </header>
    <main style="padding: 20px;">
        <h2>Index of Encoded Inscriptions</h2>
        <p>Trovate {len(inscriptions_data)} iscrizioni.</p>
        <ul>{links_html}</ul>
    </main>
</body>
</html>"""

    # 6. SCRITTURA FILE
    os.makedirs(output_dir, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(full_html)
    
    print(f"SUCCESSO: Pagina scritta in {output_file}")

if __name__ == "__main__":
    run()
