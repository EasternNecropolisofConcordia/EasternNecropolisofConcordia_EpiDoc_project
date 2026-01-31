#!/usr/bin/env python3
"""
Genera automaticamente la pagina HTML con lista di tutte le iscrizioni
"""
from lxml import etree
from pathlib import Path

def generate_inscription_list():
    xml_dir = Path('inscriptions')
    output_file = Path('docs/pages/inscriptions.html')
    
    # Namespace TEI
    ns = {'tei': 'http://www.tei-c.org/ns/1.0'}
    
    # Raccogli informazioni dai file XML
    inscriptions = []
    
    print("📋 Raccolta metadati dalle iscrizioni...\n")
    
    for xml_file in sorted(xml_dir.glob('*.xml')):
        try:
            tree = etree.parse(str(xml_file))
            
            # Estrai titolo
            title_elem = tree.find('.//tei:titleStmt/tei:title', ns)
            title = title_elem.text if title_elem is not None else 'Titolo non disponibile'
            
            # Estrai filename
            filename_elem = tree.find('.//tei:publicationStmt/tei:idno[@type="filename"]', ns)
            filename = filename_elem.text if filename_elem is not None else xml_file.stem
            
            # Estrai città moderna
            city_elem = tree.find('.//tei:origPlace//tei:placeName[@type="modern"]', ns)
            city = city_elem.text if city_elem is not None else ''
            
            # Estrai datazione
            date_elem = tree.find('.//tei:origDate[@xml:lang="en"]', ns)
            date = date_elem.text if date_elem is not None else ''
            
            inscriptions.append({
                'title': title.strip(),
                'filename': filename.strip(),
                'city': city.strip(),
                'date': date.strip(),
                'html_file': f"{filename}.html"
            })
            
            print(f"   ✓ {title}")
            
        except Exception as e:
            print(f"   ✗ Errore con {xml_file.name}: {e}")
    
    # Genera HTML
    html = """<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lista Iscrizioni - Necropoli di Levante</title>
    <link rel="stylesheet" href="../css/style.css">
    <style>
        .inscription-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        
        .inscription-table th,
        .inscription-table td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        
        .inscription-table th {
            background-color: #8b4513;
            color: white;
        }
        
        .inscription-table tr:hover {
            background-color: #f5f5f5;
        }
        
        .inscription-table a {
            color: #8b4513;
            text-decoration: none;
            font-weight: bold;
        }
        
        .inscription-table a:hover {
            text-decoration: underline;
        }
        
        .count {
            color: #666;
            font-style: italic;
            margin: 20px 0;
        }
    </style>
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

    <main>
        <h2>Catalogo delle Iscrizioni</h2>
        <p class="intro">
            Elenco completo delle iscrizioni funerarie della Necropoli di Levante.
        </p>
        <p class="count">Totale iscrizioni: """ + str(len(inscriptions)) + """</p>
        
        <table class="inscription-table">
            <thead>
                <tr>
                    <th>Titolo</th>
                    <th>Località</th>
                    <th>Datazione</th>
                </tr>
            </thead>
            <tbody>
"""
    
    # Aggiungi righe per ogni iscrizione
    for insc in sorted(inscriptions, key=lambda x: x['title']):
        html += f"""                <tr>
                    <td><a href="{insc['html_file']}">{insc['title']}</a></td>
                    <td>{insc['city']}</td>
                    <td>{insc['date']}</td>
                </tr>
"""
    
    html += """            </tbody>
        </table>
    </main>

    <footer>
        <p>&copy; 2025 Leonardo Battistella - Università Ca' Foscari Venezia</p>
    </footer>
</body>
</html>"""
    
    # Salva file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"\n✓ Lista generata: {output_file}")
    print(f"  Totale iscrizioni: {len(inscriptions)}")

if __name__ == '__main__':
    generate_inscription_list()
