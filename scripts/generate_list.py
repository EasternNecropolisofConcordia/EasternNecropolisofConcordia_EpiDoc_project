import os
from saxonche import PySaxonProcessor

def run():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(script_dir, '..'))
    
    xml_dir = os.path.join(root_dir, 'inscriptions')
    output_dir = os.path.join(root_dir, 'docs', 'pages')
    output_file = os.path.join(output_dir, 'inscriptions.html')

    if not os.path.exists(xml_dir):
        print(f"ERROR: Directory {xml_dir} does not exist!")
        return

    files = [f for f in os.listdir(xml_dir) if f.lower().endswith('.xml')]
    inscriptions_data = []

    with PySaxonProcessor(license=False) as proc:
        xpath_processor = proc.new_xpath_processor()
        
        for filename in files:
            xml_path = os.path.join(xml_dir, filename)
            try:
                node = proc.parse_xml(xml_file_name=xml_path)
                xpath_processor.set_context(xdm_item=node)
                
                title_item = xpath_processor.evaluate("//*[local-name()='titleStmt']/*[local-name()='title'][1]")
                idno_item = xpath_processor.evaluate("//*[local-name()='idno'][@type='filename'][1]")
                
                if title_item is not None and title_item.size > 0:
                    display_title = title_item.item_at(0).string_value.strip()
                else:
                    display_title = filename

                if idno_item is not None and idno_item.size > 0:
                    target_link = "inscriptions/" + idno_item.item_at(0).string_value.strip().replace('.xml', '.html')
                else:
                    target_link = "inscriptions/" + filename.replace('.xml', '.html')
                
                inscriptions_data.append({'title': display_title, 'link': target_link})
                print(f"REGISTERED: {display_title}")
                
            except Exception as e:
                print(f"ERROR on file {filename}: {str(e)}")
                inscriptions_data.append({'title': filename, 'link': "inscriptions/" + filename.replace('.xml', '.html')})

    # Alphabetic Order
    inscriptions_data.sort(key=lambda x: x['title'])
    
    # Link
    links_html = "".join([f'<li><a href="{item["link"]}">{item["title"]}</a></li>' for item in inscriptions_data])
    
    # Template with Navbar
    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Inscriptions - Iulia Concordia</title>
    <link rel="stylesheet" href="../css/style.css">
</head>
<body>
    <header class="site-header">
        <h1 class="main_title">Digital Approaches to the Inscriptions of the Eastern Necropolis of <em>Iulia Concordia</em></h1>
        <h2 class="main_subtitle">From Autoptic Analysis to TEI-based Edition</h2>
        <nav class="navbar">
            <ul class="menu">
                <li><a href="../index.html">Home</a></li>
                <li><a href="inscriptions.html">Inscriptions</a></li>
                <li><a href="./people.html">People</a></li>
                <li><a href="./map.html">Map</a></li>
                <li class="dropdown">
                    <a href="#">Study &amp; Context ▾</a>
                    <ul class="submenu">
                        <li><a href="./context/history.html">History</a></li>
                        <li><a href="./context/about_people.html">About People Buried</a></li>
                        <li><a href="./context/supports.html">Supports &amp; Monuments</a></li>
                        <li><a href="./context/chronology.html">Dating &amp; Chronology</a></li>
                    </ul>
                </li>
                <li><a href="./krummrey-panciera_epidoc.html">Krummrey-Panciera Conventions &amp; EpiDoc</a></li>
                <li class="dropdown">
                    <a href="#">References ▾</a>
                    <ul class="submenu">
                        <li><a href="./references/bibliography.html">Bibliography</a></li>
                        <li><a href="./references/corpora_databases.html">Corpora and Databases</a></li>
                    </ul>
                </li>
            </ul>
        </nav>
    </header>
    <main style="padding: 20px;">
        <h2>Index of Encoded Inscriptions</h2>
        <p>This list is automatically updated from the EpiDoc XML files.</p>
        <ul class="inscription-list">
            {links_html}
        </ul>
    </main>
    <footer>
        <p>&copy; 2026 - Leonardo Battistella</p>
        <p>Generated via Saxon-Che &amp; GitHub Actions</p>
        <p><strong>Digital Approaches to the Inscriptions of the Eastern Necropolis of Julia Concordia</strong></p>
        <p>MA Thesis project in <em>Digital and Public Humanities</em> – Ca' Foscari University of Venice.</p>
        <p>This is a non-commercial, open-access research project for educational and scientific purposes only.</p>
        <p>____________________________________________________________________________________________________</p>
        <p>The images provided by the Ministry of Culture and the Regional Directorate of National Museums of Veneto (Italy) are for non-commercial and non-profit use only.</p>
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
</body>
</html>"""

    os.makedirs(output_dir, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(full_html)
    print(f"Done: Page generated with {len(inscriptions_data)} links.")

if __name__ == "__main__":
    run()
