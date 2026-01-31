import os
from lxml import etree

def transform_xml():
    xml_dir = 'inscriptions/'
    xslt_path = 'xslt/epidoc-to-html.xsl'
    output_dir = 'docs/pages/'
    
    # Definizione del namespace TEI
    namespaces = {'tei': 'http://www.tei-c.org/ns/1.0'}

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    xslt_tree = etree.parse(xslt_path)
    transform = etree.XSLT(xslt_tree)

    header_html = """
    <header>
        <h1 class="main_title">Digital Approaches to the Inscriptions of the Eastern Necropolis of Iulia Concordia</h1>
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
            tree = etree.parse(xml_path)
            
            # Estraiamo il nome del file desiderato dal tag <idno type="filename">
            idno = tree.xpath('//tei:idno[@type="filename"]/text()', namespaces=namespaces)
            if idno:
                # Se il file si chiama Vassio.xml, l'output sarà Vassio.html
                output_filename = idno[0].replace('.xml', '.html')
            else:
                output_filename = filename.replace('.xml', '.html')

            # Trasformazione XSLT
            new_dom = transform(tree)
            content = etree.tostring(new_dom, encoding='unicode', method='html')
            
            full_html = f"<!DOCTYPE html><html><body>{header_html}<main>{content}</main></body></html>"

            with open(os.path.join(output_dir, output_filename), 'w', encoding='utf-8') as f:
                f.write(full_html)
            
            print(f"Trasformato: {filename} -> {output_filename}")

if __name__ == "__main__":
    transform_xml()
