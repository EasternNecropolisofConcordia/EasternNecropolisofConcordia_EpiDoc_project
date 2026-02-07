import os
from saxonche import PySaxonProcessor

def transform_corpora_databases():
    xml_path = 'Bibliography/Master_Bibliography.xml'
    xslt_path = 'xslt/corpora_databases-to-html.xsl'
    output_dir = 'docs/pages'
    output_path = os.path.join(output_dir, 'corpora_databases.html')
    
    os.makedirs(output_dir, exist_ok=True)
    
    if not os.path.exists(xml_path):
        print(f"Error: {xml_path} not found")
        return
    
    if not os.path.exists(xslt_path):
        print(f"Error: {xslt_path} not found")
        return
    
    # Navbar da iniettare per coerenza col sito
    header_html = """
        <header>
            <h1 class="main_title">Digital Approaches to the Inscriptions of the Eastern Necropolis of <em>Iulia Concordia</em></h1>
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
            
            full_page = f"<!DOCTYPE html><html><head><meta charset='UTF-8'><link rel='stylesheet' href='../css/style.css'></head><body>{header_html}<main>{output}</main></body></html>"
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(full_page)
            print(f"Corpora and Databases transformed successfully: corpora_databases.html")
        except Exception as e:
            print(f"Error transforming corpora and databases: {e}")

if __name__ == "__main__":
    transform_corpora_databases()
