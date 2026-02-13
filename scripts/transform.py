import os
from saxonche import PySaxonProcessor

def transform_xml():
    xml_dir = 'inscriptions'
    xslt_path = 'xslt/epidoc-to-html.xsl'
    output_dir = 'docs/pages/inscriptions'
    os.makedirs(output_dir, exist_ok=True)

    with PySaxonProcessor(license=False) as proc:
        xslt_proc = proc.new_xslt30_processor()

        if not os.path.exists(xslt_path):
            print(f"Error: {xslt_path} not found")
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
                        <a href="#">Study &amp; Context ▾</a>
                        <ul class="submenu">
                            <li><a href="../context/history.html">History</a></li>
                            <li><a href="../context/about_people.html">About People Buried</a></li>
                            <li><a href="../context/supports.html">Supports &amp; Monuments</a></li>
                            <li><a href="../context/chronology.html">Dating &amp; Chronology</a></li>
                        </ul>
                    </li>
                    <li><a href="../krummrey-panciera_epidoc.html">Krummrey-Panciera Conventions &amp; EpiDoc</a></li>
                    <li class="dropdown">
                        <a href="#">References ▾</a>
                        <ul class="submenu">
                            <li><a href="../references/bibliography.html">Bibliography</a></li>
                            <li><a href="../references/corpora_databases.html">Corpora and Databases</a></li>
                        </ul>
                    </li>
                </ul>
            </nav>
        </header>
        """

        footer_html = """
        <footer>
            <p>Generated via Saxon-Che &amp; GitHub Actions</p>
            <p>&copy; 2026 - Leonardo Battistella</p>
            <p><strong>Digital Approaches to the Inscriptions of the Eastern Necropolis of Julia Concordia</strong></p>
            <p>MA Thesis project in <em>Digital and Public Humanities</em> – Ca’ Foscari University of Venice.</p>
            <p>This is a non-commercial, open-access research project for educational and scientific purposes only.</p>
            <p>____________________________________________________________________________________________________</p>
            <p>The images provided by the Ministry of Culture and the Regional Directorate of National Museums of Veneto (Italy) are for non-commercial and non-profit use only.</p>
            <p>Any use of these images is strictly prohibited unless specifically authorized by the Regional Directorate of National Museums of Veneto.</p>
        </footer>
        """

        for filename in os.listdir(xml_dir):
            if filename.endswith('.xml'):
                xml_path = os.path.join(xml_dir, filename)
                output_filename = filename.replace('.xml', '.html')
                output_path = os.path.join(output_dir, output_filename)

                try:
                    executable = xslt_proc.compile_stylesheet(stylesheet_file=xslt_path)
                    output = executable.transform_to_string(source_file=xml_path)

                    full_page = f"""<!DOCTYPE html>
<html lang='en'>
<head>
    <meta charset='UTF-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <link rel='stylesheet' href='../../css/style.css'>
</head>
<body>
    {header_html}
    <main>
        {output}
    </main>
        {footer_html}
</body>
</html>"""

                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(full_page)
                    print(f"Successfully transformed: {filename}")
                except Exception as e:
                    print(f"Error on {filename}: {e}")

if __name__ == "__main__":
    transform_xml()
