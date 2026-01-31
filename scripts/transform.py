#!/usr/bin/env python3

from lxml import etree
from pathlib import Path

def transform_xml_to_html():
    # Percorsi
    xml_dir = Path('inscriptions')              # File XML sorgente
    xslt_file = Path('xslt/epidoc-to-html.xsl') # Stylesheet XSLT
    output_dir = Path('docs/inscriptions')      # Dove salvare HTML
    
    # Crea la cartella output se non esiste
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Carica XSLT
    print(f"📄 Caricamento XSLT: {xslt_file}")
    try:
        xslt = etree.parse(str(xslt_file))
        transform = etree.XSLT(xslt)
    except Exception as e:
        print(f"❌ Errore nel caricamento XSLT: {e}")
        return
    
    # Trova tutti i file XML
    xml_files = list(xml_dir.glob('*.xml'))
    
    if not xml_files:
        print(f"⚠️  Nessun file XML trovato in {xml_dir}/")
        return
    
    print(f"\n📚 Trovati {len(xml_files)} file XML da trasformare\n")
    
    # Trasforma ogni file
    success_count = 0
    error_count = 0
    
    for xml_file in xml_files:
        try:
            print(f"⚙️  Trasformazione: {xml_file.name}...")
            
            # Parse XML
            xml = etree.parse(str(xml_file))
            
            # Applica trasformazione XSLT
            result = transform(xml)
            
            # Nome file output (stesso nome ma .html)
            output_file = output_dir / xml_file.with_suffix('.html').name
            
            # Salva HTML
            with open(output_file, 'wb') as f:
                f.write(etree.tostring(
                    result, 
                    pretty_print=True, 
                    method='html',
                    encoding='UTF-8'
                ))
            
            print(f"   ✓ Creato: {output_file}")
            success_count += 1
            
        except Exception as e:
            print(f"   ✗ Errore con {xml_file.name}: {e}")
            error_count += 1
    
    # Riepilogo
    print(f"\n{'='*50}")
    print(f"✓ Trasformazione completata!")
    print(f"  • File processati con successo: {success_count}")
    if error_count > 0:
        print(f"  • Errori: {error_count}")
    print(f"  • File HTML salvati in: {output_dir}/")
    print(f"{'='*50}\n")

if __name__ == '__main__':
    transform_xml_to_html()
