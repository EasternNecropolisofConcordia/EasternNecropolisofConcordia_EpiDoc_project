import os
from lxml import etree

def generate_inscriptions_page():
    xml_dir = 'inscriptions/'
    output_file = 'docs/pages/inscriptions.html'
    namespaces = {'tei': 'http://www.tei-c.org/ns/1.0'}
    
    inscriptions_data = []

    # Leggi i dati da ogni file XML
    for filename in os.listdir(xml_dir):
        if filename.endswith('.xml'):
            path = os.path.join(xml_dir, filename)
            tree = etree.parse(path)
            
            # Estrazione Titolo e IDNO
            title = tree.xpath('//tei:titleStmt/tei:title/text()', namespaces=namespaces)
            idno = tree.xpath('//tei:idno[@type="filename"]/text()', namespaces=namespaces)
            
            display_title = title[0] if title else filename
            link_target = idno[0].replace('.xml', '.html') if idno else filename.replace('.xml', '.html')
            
            inscriptions_data.append({'title': display_title, 'link': link_target})

    # Ordina alfabeticamente per titolo
    inscriptions_data.sort(key=lambda x: x['title'])

    # Genera i list items HTML
    links_html = "".join([f'<li><a href="{item["link"]}">{item["title"]}</a></li>' for item in inscriptions_data])

    html_content = f"""
<!DOCTYPE html>
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
        <p>A total of {len(inscriptions_data)} inscriptions have been encoded.</p>
        <ul class="inscription-list">
            {links_html}
        </ul>
    </main>
    <footer>
        <p>&copy; 2026 - Digital Approaches to Iulia Concordia</p>
    </footer>
</body>
</html>
"""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Pagina inscriptions.html generata con {len(inscriptions_data)} voci.")

if __name__ == "__main__":
    generate_inscriptions_page()
