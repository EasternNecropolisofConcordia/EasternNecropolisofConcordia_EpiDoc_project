import os
from saxonche import PySaxonProcessor

def transform_bibliography():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    root_dir = os.path.dirname(script_dir) 
    

    xml_path = os.path.join(root_dir, 'bibliography', 'master_bibliography.xml')
    xslt_path = os.path.join(root_dir, 'xslt', 'corpora_databases-to-html.xsl')
    output_dir = os.path.join(root_dir, 'docs', 'pages', 'references')
    output_path = os.path.join(output_dir, 'corpora_databases.html')
    
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Sto cercando l'XML in: {xml_path}")
    print(f"Sto scrivendo l'HTML in: {output_path}")

    if not os.path.exists(xml_path):
        print(f"ERRORE: XML non trovato!")
        return

    header_html = """
    <header>
        <h1 class="main_title">Digital Approaches to the Inscriptions of Iulia Concordia</h1>
        <nav class="navbar">
            <ul class="menu">
                <li><a href="../index.html">Home</a></li>
                <li><a href="inscriptions.html">Inscriptions</a></li>
                <li><a href="history.html">History of the Eastern Necropolis</a></li>
                <li><a href="abouttheinscriptions.html">About the inscriptions</a></li>
                <li><a href="corpora_databases.html">Corpora and Databases</a></li>
                <li><a href="bibliography.html">Bibliography</a></li>
            </ul>
        </nav>
    </header>
    """

    with PySaxonProcessor(license=False) as proc:
        xslt_proc = proc.new_xslt30_processor()
        try:
            executable = xslt_proc.compile_stylesheet(stylesheet_file=xslt_path)
            output = executable.transform_to_string(source_file=xml_path)
            
            full_page = f"<!DOCTYPE html><html lang='it'><head><meta charset='UTF-8'><link rel='stylesheet' href='../css/style.css'><title>Bibliography</title></head><body>{header_html}<main>{output}</main></body></html>"
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(full_page)
            print("Trasformazione completata con successo!")

        except Exception as e:
            print(f"Errore durante la trasformazione: {e}")

if __name__ == "__main__":
    transform_bibliography()
