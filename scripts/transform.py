import os
from saxonche import PySaxonProcessor

def transform_xml():
    xml_dir = 'inscriptions'
    xslt_path = 'xslt/epidoc-to-html.xsl'
    output_dir = 'docs/pages'

    os.makedirs(output_dir, exist_ok=True)

    with PySaxonProcessor(license=False) as proc:
        xslt_proc = proc.new_xslt30_processor()
        
        # Controllo file XSLT
        if not os.path.exists(xslt_path):
            print(f"Errore: {xslt_path} non trovato")
            return

        for filename in os.listdir(xml_dir):
            if filename.endswith('.xml'):
                xml_path = os.path.join(xml_dir, filename)
                output_filename = filename.replace('.xml', '.html')
                output_path = os.path.join(output_dir, output_filename)

                # Trasformazione XSLT 2.0/3.0
                try:
                    executable = xslt_proc.compile_stylesheet(stylesheet_file=xslt_path)
                    output = executable.transform_to_string(source_file=xml_path)
                    
                    # Aggiungiamo il tuo layout HTML attorno all'output
                    header_html = """<header><h1 class="main_title">Digital Approaches to Iulia Concordia</h1><nav class="navbar"><ul class="menu"><li><a href="../index.html">Home</a></li><li><a href="inscriptions.html">Inscriptions</a></li><li><a href="history.html">History</a></li><li><a href="abouttheinscriptions.html">About</a></li></ul></nav></header><link rel="stylesheet" href="../css/style.css">"""
                    
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(f"<!DOCTYPE html><html><body>{header_html}<main>{output}</main></body></html>")
                    
                    print(f"Trasformato: {filename}")
                except Exception as e:
                    print(f"Errore durante la trasformazione di {filename}: {e}")

if __name__ == "__main__":
    transform_xml()
