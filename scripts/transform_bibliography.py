import os
import subprocess # Per lanciare i comandi Git
from saxonche import PySaxonProcessor

def transform_bibliography():
    # 1. Gestione percorsi: usa la posizione dello script come base
    base_dir = os.path.dirname(os.path.abspath(__file__))
    xml_path = os.path.join(base_dir, 'Bibliography', 'Master_Bibliography.xml')
    xslt_path = os.path.join(base_dir, 'xslt', 'bibliography-to-html.xsl')
    output_dir = os.path.join(base_dir, 'docs', 'pages')
    output_path = os.path.join(output_dir, 'bibliography.html')
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Verifica esistenza file
    if not os.path.exists(xml_path) or not os.path.exists(xslt_path):
        print("Errore: File XML o XSLT non trovati!")
        return

    # Navbar (Assicurati che i link siano corretti per docs/pages/)
    header_html = """
    <header>
        <h1 class="main_title">Digital Approaches to the Inscriptions of Iulia Concordia</h1>
        <nav class="navbar">
            <ul class="menu">
                <li><a href="../index.html">Home</a></li>
                <li><a href="inscriptions.html">Inscriptions</a></li>
                <li><a href="bibliography.html">Bibliography</a></li>
            </ul>
        </nav>
    </header>
    """

    # 2. Trasformazione XSLT
    with PySaxonProcessor(license=False) as proc:
        xslt_proc = proc.new_xslt30_processor()
        try:
            executable = xslt_proc.compile_stylesheet(stylesheet_file=xslt_path)
            output = executable.transform_to_string(source_file=xml_path)
            
            full_page = f"<!DOCTYPE html><html><head><meta charset='UTF-8'><link rel='stylesheet' href='../css/style.css'></head><body>{header_html}<main>{output}</main></body></html>"
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(full_page)
            print(f"Successo: {output_path} creato.")

            # 3. AUTOMAZIONE GITHUB
            print("Invio aggiornamenti a GitHub...")
            # Eseguiamo i comandi git uno dopo l'altro
            subprocess.run(["git", "add", "."], cwd=base_dir)
            subprocess.run(["git", "commit", "-m", "Auto-update bibliography"], cwd=base_dir)
            subprocess.run(["git", "push", "origin", "main"], cwd=base_dir)
            print("Fatto! Il sito sarà online tra un minuto.")

        except Exception as e:
            print(f"Errore durante la trasformazione: {e}")

if __name__ == "__main__":
    transform_bibliography()
