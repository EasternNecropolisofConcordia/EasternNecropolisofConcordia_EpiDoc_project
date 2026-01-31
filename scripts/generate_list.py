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
                # Carichiamo il documento
                node = proc.parse_xml(xml_file_name=xml_path)
                
                # Metodo più compatibile: impostiamo il contesto separatamente
                xpath_processor.set_context_item(xdm_item=node)
                
                # Eseguiamo l'evaluate senza argomenti extra
                title_item = xpath_processor.evaluate("//*[local-name()='titleStmt']/*[local-name()='title'][1]")
                idno_item = xpath_processor.evaluate("//*[local-name()='idno'][@type='filename'][1]")
                
                # Recupero stringa
                display_title = title_item.string_value.strip() if title_item else filename
                
                if idno_item:
                    target_link = idno_item.string_value.strip().replace('.xml', '.html')
                else:
                    target_link = filename.replace('.xml', '.html')
                
                inscriptions_data.append({'title': display_title, 'link': target_link})
                print(f"REGISTRATO: {display_title}")
                
            except Exception as e:
                # Se fallisce ancora, proviamo l'ultimo metodo disperato: estrazione diretta dal nodo
                try:
                    display_title = node.children[0].string_value[:50] # Placeholder
                    inscriptions_data.append({'title': filename, 'link': filename.replace('.xml', '.html')})
                    print(f"REGISTRATO (Fallback): {filename}")
                except:
                    print(f"ERRORE persistente su {filename}: {str(e)}")

    inscriptions_data.sort(key=lambda x: x['title'])
    
    links_html = "".join([f'<li><a href="{item["link"]}">{item["title"]}</a></li>' for item in inscriptions_data])
    
    full_html = f"""<!DOCTYPE html>
<html lang="en">
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
        <ul class="inscription-list">{links_html}</ul>
    </main>
</body>
</html>"""

    os.makedirs(output_dir, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(full_html)
    print(f"Fine: Generati {len(inscriptions_data)} link.")

if __name__ == "__main__":
    run()
