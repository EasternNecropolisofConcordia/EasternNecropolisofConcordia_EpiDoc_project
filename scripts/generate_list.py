import os
from saxonche import PySaxonProcessor

def generate_inscriptions_page():
    xml_dir = 'inscriptions'
    output_file = 'docs/pages/inscriptions.html'
    inscriptions_data = []

    if not os.path.exists(xml_dir):
        print(f"Errore: la cartella {xml_dir} non esiste.")
        return

    print(f"Analisi dei file in {xml_dir}...")

    # Inizializziamo Saxon
    with PySaxonProcessor(license=False) as proc:
        for filename in os.listdir(xml_dir):
            if filename.endswith('.xml'):
                xml_path = os.path.join(xml_dir, filename)
                try:
                    # Carica il file XML
                    node = proc.parse_xml(xml_file_name=xml_path)
                    
                    # XPath ultra-robusto che ignora i namespace (usa local-name)
                    # Cerca il titolo dentro titleStmt
                    title_xpath = "//*[local-name()='titleStmt']/*[local-name()='title']"
                    # Cerca l'idno con tipo filename
                    idno_xpath = "//*[local-name()='idno'][@type='filename']"
                    
                    title_nodes = proc.xpath_eval(title_xpath, node)
                    idno_nodes = proc.xpath_eval(idno_xpath, node)
                    
                    # Estrazione dei valori testuali
                    display_title = title_nodes[0].string_value.strip() if title_nodes else filename
                    idno_val = idno_nodes[0].string_value.strip() if idno_nodes else None

                    # Definizione del link (usa idno se esiste, altrimenti il nome file)
                    if idno_val:
                        target_link = idno_val.replace('.xml', '.html')
                    else:
                        target_link = filename.replace('.xml', '.html')
                    
                    inscriptions_data.append({'title': display_title, 'link': target_link})
                    print(f" -> Trovata iscrizione: {display_title} (Link: {target_link})")

                except Exception as e:
                    print(f" -> Errore nel leggere {filename}: {e}")

    # Ordina la lista alfabeticamente per titolo
    inscriptions_data.sort(key=lambda x: x['title'])
    
    # Genera i link HTML per la lista
    if not inscriptions_data:
        links_html = "<li>Nessuna iscrizione trovata.</li>"
    else:
        links_html = "".join([f'<li><a href="{item["link"]}">{item["title"]}</a></li>' for item in inscriptions_data])
    
    # Template HTML completo (con la tua navbar)
    full_html = f"""<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Inscriptions - Iulia Concordia</title>
    <link rel="stylesheet" href="../css/style.css">
</head>
<body>
    <header>
        <h1 class="main_title">Digital Approaches to the Inscriptions of the Eastern Necropolis of Iulia Concordia: from Autoptic Analysis to TEI-based Edition</h1>
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
        <p>Currently displaying {len(inscriptions_data)} inscriptions.</p>
        <ul class="inscription-list">
            {links_html}
        </ul>
    </main>
    <footer>
        <p>&copy; 2026 - Nome del sito</p>
    </footer>
</body>
</html>"""
    
    # Assicurati che la cartella di output esista
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Scrittura del file finale
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(full_html)
    
    print(f"\nPagina {output_file} generata con {len(inscriptions_data)} voci.")

if __name__ == "__main__":
    generate_inscriptions_page()
