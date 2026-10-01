import os
from saxonche import PySaxonProcessor

def transform_bibliography():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    root_dir = os.path.dirname(script_dir) 
    

    xml_path = os.path.join(root_dir, 'bibliography', 'master_bibliography.xml')
    xslt_path = os.path.join(root_dir, 'xslt', 'bibliography-to-html.xsl')
    output_dir = os.path.join(root_dir, 'docs', 'pages', 'references')
    output_path = os.path.join(output_dir, 'bibliography.html')
    
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Searching for XML in: {xml_path}")
    print(f"Writing HTML to: {output_path}")

    if not os.path.exists(xml_path):
        print(f"ERROR: XML not found!")
        return

    header_html = """
    <header class="site-header">
        <h1 class="main_title">Digital Approaches to the Inscriptions of the Eastern Necropolis of <em>Iulia Concordia</em></h1>
        <h2 class="main_subtitle">From Autoptic Analysis to TEI-based Edition</h2>
        <nav class="navbar">
            <ul class="menu">
                <li><a href="../../index.html">Home</a></li>
                <li><a href="../inscriptions.html">Inscriptions</a></li>
                <li><a href="../people.html">People</a></li>
                <li><a href="../map.html">Map</a></li>
                <li class="dropdown">
                    <a href="#">Study & Context ▾</a>
                    <ul class="submenu">
                        <li><a href="../context/history.html">History</a></li>
                        <li><a href="../context/about_people.html">About People Buried</a></li>
                        <li><a href="../context/supports.html">Supports & Monuments</a></li>
                        <li><a href="../context/chronology.html">Dating & Chronology</a></li>
                    </ul>
                </li>
                <li><a href="../krummrey-panciera_epidoc.html">Krummrey-Panciera Conventions &amp; EpiDoc</a></li>
                <li class="dropdown">
                    <a href="#">References ▾</a>
                    <ul class="submenu">
                        <li><a href="bibliography.html">Bibliography</a></li>
                        <li><a href="./corpora_databases.html">Corpora and Databases</a></li>
                    </ul>
                </li>
            </ul>
        </nav>
    </header>
    """

    footer_html = """
    <footer>
      <p><strong><em>Tituli Concordienses</em></strong> – The Eastern Necropolis of <em>Iulia Concordia</em></p>
      <p>&copy; 2026 Leonardo Battistella · Contact: <a href="mailto:info@tituliconcordienses.eu">info@tituliconcordienses.eu</a></p>
      <p>Originated as an MA thesis in Digital and Public Humanities, Ca’ Foscari University of Venice. A non-commercial, open-access research project.</p>
      <p>Data: CC BY 4.0 · Code: MIT · Cite as: <a href="https://doi.org/10.5281/zenodo.22995898">doi:10.5281/zenodo.22995898</a> · Source on <a href="https://github.com/EasternNecropolisofConcordia/EasternNecropolisofConcordia_EpiDoc_project">GitHub</a></p>
      <p>________________________________________________________________________________________________________________________________</p>
      <p>Images are not covered by these licences. Images provided by the Ministry of Culture – Regional Directorate of National Museums of Veneto (Italy) are for non-commercial and non-profit use only.</p>
      <p>Any use of these images is strictly prohibited unless specifically authorized by the Regional Directorate of National Museums of Veneto.</p>
    </footer>
    <script>
(function() {{
    var header = document.querySelector('.site-header');
    if (!header) return;
    var headerH = header.offsetHeight;
    var peeking = false;

    window.addEventListener('scroll', function() {{
        if (window.scrollY <= headerH) {{
            header.classList.remove('header-fixed', 'header-animate', 'header-visible');
            peeking = false;
        }} else if (!peeking) {{
            header.classList.add('header-fixed');
            header.classList.remove('header-animate', 'header-visible');
        }}
    }});

    document.addEventListener('mousemove', function(e) {{
        if (window.scrollY <= headerH) return;
        if (e.clientY < 40 && !peeking) {{
            header.classList.add('header-fixed', 'header-animate', 'header-visible');
            peeking = true;
        }} else if (e.clientY > headerH && peeking) {{
            header.classList.remove('header-visible');
            peeking = false;
        }}
    }});
}})();
</script>
    """

    with PySaxonProcessor(license=False) as proc:
        xslt_proc = proc.new_xslt30_processor()
        try:
            executable = xslt_proc.compile_stylesheet(stylesheet_file=xslt_path)
            output = executable.transform_to_string(source_file=xml_path)
            
            full_page = f"<!DOCTYPE html><html lang='it'><head><meta charset='UTF-8'><link rel='stylesheet' href='../../css/style.css'><title>Bibliography</title></head><body>{header_html}<main>{output}</main>{footer_html}</body></html>"
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(full_page)
            print("Transformation completed successfully!")

        except Exception as e:
            print(f"Error during transformation: {e}")

if __name__ == "__main__":
    transform_bibliography()
