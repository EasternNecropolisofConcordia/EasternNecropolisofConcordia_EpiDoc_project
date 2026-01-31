import os
from saxonche import PySaxonProcessor

def generate_inscriptions_page():
    xml_dir = 'inscriptions'
    output_file = 'docs/pages/inscriptions.html'
    inscriptions_data = []

    if not os.path.exists(xml_dir):
        print(f"Errore: la cartella {xml_dir} non esiste.")
        return

    # Inizializziamo Saxon per leggere i titoli dai file XML
    with PySaxonProcessor(license=False) as proc:
        for filename in os.listdir(xml_dir):
            if filename.endswith('.xml'):
                xml_path = os.path.join(xml_dir, filename)
                try:
                    # Carica il file XML
                    node = proc.parse_xml(xml_file_name=xml_path)
                    
                    # Estrae il titolo e il nome file usando XPath (compatibile TEI)
                    # Usiamo *: per ignorare temporaneamente i problemi di namespace
                    title_xpath = "/*:TEI/*:teiHeader/*:fileDesc/*:titleStmt/*:title/text()"
                    idno_xpath = "//*:idno[@type='filename']/text()"
                    
                    title_nodes = proc.xpath_eval(title_xpath, node)
                    idno_nodes = proc.xpath_eval(idno_xpath, node)
                    
                    display_title = str(title_nodes[0]) if title_nodes else filename
                    # Se idno non c'è, usa il nome del file originale cambiando estensione
                    target_link = str(idno_nodes[0]).replace('.xml', '.html') if idno_nodes else filename.replace('.xml', '.html')
                    
                    inscriptions_data.append({'title': display_title, 'link': target_link})
                except Exception as e:
                    print(f"Errore nel leggere {filename}: {e}")

    # Ordina la lista alfabeticamente
    inscriptions_data.sort(key=lambda x: x['title'])
    
    # Genera i link HTML
    links_html = "".join([f'<li><a href="{item["link"]}">{item["title"]}</a></li>' for item in inscriptions_data])
    
    # Template della pagina (navbar inclusa)
    full_html = f"""<!DOCTYPE html>
<html lang="it">
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
    <footer>
        <p>&copy; 2026 - Nome del sito</p>
    </footer>
</body>
</html>"""
    
    # Assicurati che la cartella docs/pages esista
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(full_html)
    
    print(f"Pagina {output_file} generata con successo!")

if __name__ == "__main__":
    generate_inscriptions_page()
