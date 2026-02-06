import os
from saxonche import PySaxonProcessor

def transform_xml():
    xml_dir = 'inscriptions'
    xslt_path = 'xslt/epidoc-to-html.xsl'
    output_dir = 'docs/pages'

    os.makedirs(output_dir, exist_ok=True)

    with PySaxonProcessor(license=False) as proc:
        xslt_proc = proc.new_xslt30_processor()
        
        if not os.path.exists(xslt_path):
            print(f"Errore: {xslt_path} non trovato")
            return

        # Navbar da iniettare per coerenza col tuo sito
        header_html = """
        <header>
            <h1 class="main_title">Digital Approaches to the Inscriptions of the Eastern Necropolis of <em>Iulia Concordia</em></h1>
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
        <link rel="stylesheet" href="../css/style.css">
        """

        for filename in os.listdir(xml_dir):
            if filename.endswith('.xml'):
                xml_path = os.path.join(xml_dir, filename)
                output_filename = filename.replace('.xml', '.html')
                output_path = os.path.join(output_dir, output_filename)

                try:
                    # Carica ed esegue XSLT 2.0/3.0
                    executable = xslt_proc.compile_stylesheet(stylesheet_file=xslt_path)
                    output = executable.transform_to_string(source_file=xml_path)
                    
                    # Uniamo l'output dell'XSLT con il tuo layout globale
                    # L'XSLT genera già <html>, quindi lo puliamo o lo avvolgiamo
                    full_page = f"<!DOCTYPE html><html><head><meta charset='UTF-8'><link rel='stylesheet' href='../css/style.css'></head><body>{header_html}<main>{output}</main></body></html>"
                    
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(full_page)
                    print(f"Trasformato con successo: {filename}")
                except Exception as e:
                    print(f"Errore su {filename}: {e}")

if __name__ == "__main__":
    transform_xml()
