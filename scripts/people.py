import os
from saxonche import PySaxonProcessor

def run():
    print("--- INIZIO DEBUG ---")
    
    # 1. Verifica Percorsi
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(script_dir, '..'))
    xml_dir = os.path.join(root_dir, 'inscriptions')
    output_dir = os.path.join(root_dir, 'docs', 'pages')
    output_file = os.path.join(output_dir, 'people.html')

    print(f"Root Directory: {root_dir}")
    print(f"Cerco XML in: {xml_dir}")

    if not os.path.exists(xml_dir):
        print(f"ERRORE FATALE: La cartella {xml_dir} NON esiste.")
        return

    files = [f for f in os.listdir(xml_dir) if f.lower().endswith('.xml')]
    print(f"File XML trovati: {len(files)}")

    if len(files) == 0:
        print("ERRORE: Nessun file .xml trovato. Controlla che abbiano l'estensione giusta.")
        return

    people_data = {}

    with PySaxonProcessor(license=False) as proc:
        xpath_processor = proc.new_xpath_processor()
        
        for filename in files:
            print(f"\nAnalisi file: {filename}")
            xml_path = os.path.join(xml_dir, filename)
            
            try:
                node = proc.parse_xml(xml_file_name=xml_path)
                xpath_processor.set_context(xdm_item=node)
                
                # TEST 1: Vediamo se l'XPath trova le persone
                # Usiamo una query molto generica per vedere se trova ALMENO l'elemento person
                people = xpath_processor.evaluate("//*[local-name()='person']")
                
                if people is None:
                    print("  -> NESSUNA persona trovata (people is None).")
                    continue

                # Conversione in lista sicura
                people_list = []
                if hasattr(people, '__iter__'):
                    people_list = list(people)
                else:
                    people_list = [people]
                
                if len(people_list) == 0:
                     print("  -> Lista persone VUOTA (XPath non ha matchato).")
                     continue

                print(f"  -> Trovate {len(people_list)} occorrenze di <person>.")

                for i, person in enumerate(people_list):
                    xpath_processor.set_context(xdm_item=person)
                    
                    # TEST 2: Controllo ID
                    person_id_item = xpath_processor.evaluate("@xml:id")
                    person_id = person_id_item.string_value.strip() if person_id_item else None
                    
                    if not person_id:
                        print(f"    -> Persona #{i+1}: SALTATA (Manca xml:id)")
                        continue
                    
                    print(f"    -> Persona #{i+1}: ID '{person_id}' trovata. Estraggo dati...")
                    
                    # Se arrivi qui, il problema non è nel trovare la persona, ma forse nel salvarla
                    # ... (resto della logica di estrazione semplificata per il debug) ...

                    # Estrazione minima per verificare che funzioni
                    full_name_item = xpath_processor.evaluate("*[local-name()='persName']/*[local-name()='name'][@type='full']")
                    full_name = full_name_item.string_value.strip() if full_name_item else "Unknown"

                    # Recupero dati iscrizione
                    xpath_processor.set_context(xdm_item=node) # Reset al documento per cercare il titolo
                    title_item = xpath_processor.evaluate("//*[local-name()='titleStmt']/*[local-name()='title'][1]")
                    insc_title = title_item.string_value.strip() if title_item else filename

                    # Salvataggio
                    if person_id not in people_data:
                        people_data[person_id] = {
                            'id': person_id,
                            'full_name': full_name,
                            'gender': 'debug', # semplificato
                            'silhouette': None,
                            'names': [],
                            'notes': [],
                            'inscriptions': []
                        }
                    
                    people_data[person_id]['inscriptions'].append({'title': insc_title, 'link': '#'})

            except Exception as e:
                print(f"  -> ERRORE ECCEZIONE: {e}")

    print("\n--- RISULTATO FINALE ---")
    print(f"Persone uniche raccolte nel dizionario: {len(people_data)}")
    
    if len(people_data) == 0:
        print("Il dizionario è vuoto. Il problema è nell'XPath o negli ID.")
    else:
        print("Dati trovati! Il problema potrebbe essere nella generazione dell'HTML.")

if __name__ == "__main__":
    run()
