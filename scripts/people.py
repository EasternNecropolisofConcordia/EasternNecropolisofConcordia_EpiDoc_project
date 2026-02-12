import os
from saxonche import PySaxonProcessor

def run():
    base_dir = os.getcwd()
    xml_dir = os.path.join(base_dir, 'inscriptions')
    output_dir = os.path.join(base_dir, 'docs', 'pages')
    output_file = os.path.join(output_dir, 'people.html')

    if not os.path.exists(xml_dir):
        return

    people_data = {}
    # Dizionario per mappare xml:id → nome completo (per i link relationship)
    people_names = {}

    with PySaxonProcessor(license=False) as proc:
        xpath_processor = proc.new_xpath_processor()
        files = [f for f in os.listdir(xml_dir) if f.lower().endswith('.xml')]

        # PRIMO PASSAGGIO: raccogli tutti i nomi
        for filename in files:
            xml_path = os.path.join(xml_dir, filename)
            try:
                node = proc.parse_xml(xml_file_name=xml_path)
                xpath_processor.set_context(xdm_item=node)
                
                persons = xpath_processor.evaluate("//*[local-name()='person']")
                if persons is not None and persons.size > 0:
                    for i in range(persons.size):
                        person = persons.item_at(i)
                        xpath_processor.set_context(xdm_item=person)
                        
                        # ID - prendi il primo attributo
                        p_id = None
                        try:
                            all_attrs = xpath_processor.evaluate("@*")
                            if all_attrs and all_attrs.size > 0:
                                first_attr = all_attrs.item_at(0)
                                p_id = first_attr.string_value.strip()
                        except:
                            pass
                        
                        if p_id:
                            full_name_item = xpath_processor.evaluate(".//*[local-name()='name'][@type='full']")
                            if full_name_item and full_name_item.size > 0:
                                people_names[p_id] = full_name_item.item_at(0).string_value.strip()
            except:
                pass

        # SECONDO PASSAGGIO: raccogli tutti i dati
        for filename in files:
            xml_path = os.path.join(xml_dir, filename)
            try:
                node = proc.parse_xml(xml_file_name=xml_path)
                xpath_processor.set_context(xdm_item=node)
                
                # Titolo iscrizione
                title_item = xpath_processor.evaluate("//*[local-name()='titleStmt']/*[local-name()='title'][1]")
                if title_item and title_item.size > 0:
                    display_title = title_item.item_at(0).string_value.strip()
                else:
                    display_title = filename
                target_link = "inscriptions/" + filename.replace('.xml', '.html')

                # Trova tutte le persone
                persons = xpath_processor.evaluate("//*[local-name()='person']")
                
                if persons is not None and persons.size > 0:
                    for i in range(persons.size):
                        person = persons.item_at(i)
                        xpath_processor.set_context(xdm_item=person)
                        
                        # ID - prendi il primo attributo (che è xml:id)
                        p_id = None
                        try:
                            all_attrs = xpath_processor.evaluate("@*")
                            if all_attrs and all_attrs.size > 0:
                                # Il primo attributo è sempre xml:id
                                first_attr = all_attrs.item_at(0)
                                p_id = first_attr.string_value.strip()
                                print(f"  File {filename}, persona {i}: xml:id = '{p_id}'")
                        except Exception as e:
                            print(f"  ERRORE leggendo attributi: {e}")
                        
                        # Fallback: genera ID automatico
                        if not p_id or p_id == "":
                            p_id = f"p_{filename}_{i}"
                        
                        print(f"DEBUG: File {filename}, persona {i}, ID trovato: {p_id}")

                        # Se già esiste, aggiungi solo il link E unisci le note se diverse
                        if p_id in people_data:
                            people_data[p_id]['links'].append({'title': display_title, 'url': target_link})
                            
                            # Aggiungi note se non già presenti
                            note_elements_new = xpath_processor.evaluate(".//*[local-name()='note']")
                            if note_elements_new and note_elements_new.size > 0:
                                for j in range(note_elements_new.size):
                                    n = note_elements_new.item_at(j)
                                    n_type = n.get_attribute_value("type") or "info"
                                    n_value = n.string_value.strip()
                                    corresp = n.get_attribute_value("corresp")
                                    
                                    # Verifica se questa nota esiste già
                                    note_exists = False
                                    for existing_note in people_data[p_id]['notes']:
                                        if existing_note['type'] == n_type and existing_note['value'] == n_value:
                                            note_exists = True
                                            break
                                    
                                    if not note_exists:
                                        people_data[p_id]['notes'].append({
                                            'type': n_type,
                                            'value': n_value,
                                            'corresp': corresp
                                        })
                            
                            continue

                        # Tutti i nomi
                        names_data = []
                        name_elements = xpath_processor.evaluate(".//*[local-name()='persName']/*[local-name()='name']")
                        if name_elements and name_elements.size > 0:
                            for j in range(name_elements.size):
                                name_elem = name_elements.item_at(j)
                                name_type = name_elem.get_attribute_value("type") or "name"
                                if name_type == "full":
                                    continue
                                name_value = name_elem.string_value.strip()
                                nymref = name_elem.get_attribute_value("nymRef")
                                
                                names_data.append({
                                    'type': name_type,
                                    'value': name_value,
                                    'nymref': nymref
                                })

                        # Nome completo per titolo
                        full_name_item = xpath_processor.evaluate(".//*[local-name()='name'][@type='full']")
                        if full_name_item and full_name_item.size > 0:
                            p_name = full_name_item.item_at(0).string_value.strip()
                        else:
                            p_name = "Unknown"

                        # Genere
                        g_item = xpath_processor.evaluate(".//*[local-name()='gender']")
                        if g_item and g_item.size > 0:
                            p_gender = g_item.item_at(0).string_value.strip()
                        else:
                            p_gender = "unknown"

                        # Note
                        notes_data = []
                        occupation = None
                        note_elements = xpath_processor.evaluate(".//*[local-name()='note']")
                        if note_elements and note_elements.size > 0:
                            for j in range(note_elements.size):
                                n = note_elements.item_at(j)
                                n_type = n.get_attribute_value("type") or "info"
                                n_value = n.string_value.strip()
                                corresp = n.get_attribute_value("corresp")
                                
                                notes_data.append({
                                    'type': n_type,
                                    'value': n_value,
                                    'corresp': corresp
                                })
                                
                                if n_type == "occupation":
                                    occupation = n_value

                        # Logica Silhouette
                        img = None
                        if p_gender == 'f':
                            img = "silhouette_female.png"
                        elif p_gender == 'm':
                            if occupation in ['civil', 'civil?']:
                                img = "silhouette_civil.png"
                            elif occupation in ['soldier', 'soldier?']:
                                img = "silhouette_soldier.png"
                            elif occupation in ['fabricensis', 'fabricensis?']:
                                img = "silhouette_fabricensis.png"
                            elif occupation in ['functionary', 'functionary?']:
                                img = "silhouette_functionary.png"

                        people_data[p_id] = {
                            'id': p_id,
                            'name': p_name,
                            'gender': p_gender,
                            'names': names_data,
                            'notes': notes_data,
                            'img': img,
                            'links': [{'title': display_title, 'url': target_link}]
                        }
                        
            except Exception as e:
                print(f"Errore su {filename}: {e}")

    # Generazione Card
    cards = ""
    for pid in sorted(people_data.keys(), key=lambda x: people_data[x]['name']):
        p = people_data[pid]
        
        # Prepara attributi data-* per filtri JavaScript
        data_attrs = []
        data_attrs.append(f'data-gender="{p["gender"]}"')
        
        # Raccogli tutti i valori per i filtri
        gens_set = set()
        origin_set = set()
        occupation_val = ""
        role_vals = []
        relationship_vals = []
        
        for name in p['names']:
            if name['type'] == 'gens' and name['value']:
                gens_set.add(name['value'])
            if name['type'] == 'cognomen' and name.get('nymref'):
                origin_set.add(name['nymref'])
        
        for note in p['notes']:
            if note['type'] == 'occupation':
                occupation_val = note['value']
            elif note['type'] == 'role':
                role_vals.append(note['value'])
            elif note['type'] == 'relationship':
                relationship_vals.append(note['value'])
        
        data_attrs.append(f'data-gens="{",".join(gens_set)}"')
        data_attrs.append(f'data-origin="{",".join(origin_set)}"')
        data_attrs.append(f'data-occupation="{occupation_val}"')
        data_attrs.append(f'data-role="{",".join(role_vals)}"')
        data_attrs.append(f'data-relationship="{",".join(relationship_vals)}"')
        data_attrs.append(f'data-name="{p["name"].lower()}"')
        
        data_attrs_str = " ".join(data_attrs)
        
        # Immagine
        img_html = ""
        if p['img']:
            img_html = f'<img src="../images/silhouette/{p["img"]}" alt="silhouette">'
        
        # Costruisci dl
        dl_content = ""
        
        # Nomi
        for name in p['names']:
            dl_content += f"<dt>{name['type']}</dt><dd>{name['value']}</dd>"
            if name['type'] == 'cognomen' and name['nymref']:
                dl_content += f"<dt>origin of the cognomen</dt><dd>{name['nymref']}</dd>"
        
        # Gender
        gender_display = "male" if p['gender'] == 'm' else ("female" if p['gender'] == 'f' else "unknown")
        dl_content += f"<dt>gender</dt><dd>{gender_display}</dd>"
        
        # Notes con gestione relationship
        for note in p['notes']:
            dl_content += f"<dt>{note['type']}</dt><dd>{note['value']}"
            
            # Se è relationship e c'è corresp, aggiungi link
            if note['type'] == 'relationship' and note.get('corresp'):
                corresp_id = note['corresp'].strip()
                # Rimuovi # iniziale se presente
                if corresp_id.startswith('#'):
                    corresp_id = corresp_id[1:]
                
                # Trova il nome della persona correlata
                if corresp_id in people_names:
                    related_name = people_names[corresp_id]
                    dl_content += f' (→ <a href="#{corresp_id}">{related_name}</a>)'
            
            dl_content += "</dd>"
        
        # Inscriptions
        links_str = " - ".join([f'<a href="{l["url"]}">{l["title"]}</a>' for l in p['links']])
        dl_content += f"<dt>inscription(s)</dt><dd>{links_str}</dd>"
        
        cards += f"""
        <div class="person" id="{p['id']}" {data_attrs_str}>
            {img_html}
            <div>
                <h3>{p['name']}</h3>
                <dl>
                    {dl_content}
                </dl>
            </div>
        </div>"""

    # Template HTML
    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>People - Iulia Concordia</title>
    <link rel="stylesheet" href="../css/style.css">
</head>
<body>
    <header>
        <h1 class="main_title">Digital Approaches to the Inscriptions of the Eastern Necropolis of <em>Iulia Concordia</em></h1>
        <nav class="navbar">
            <ul class="menu">
                <li><a href="../index.html">Home</a></li>
                <li><a href="./inscriptions.html">Inscriptions</a></li>
                <li><a href="people.html">People</a></li>
                <li class="dropdown">
                    <a href="#">Study & Context ▾</a>
                    <ul class="submenu">
                        <li><a href="./context/history.html">History</a></li>
                        <li><a href="./context/about_people.html">About People Buried</a></li>
                        <li><a href="./context/supports.html">Supports & Monuments</a></li>
                        <li><a href="./context/chronology.html">Dating & Chronology</a></li>
                    </ul>
                </li>
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
    <main class="container">
        <h2>People in the Inscriptions</h2>
        
        <div class="search-filter-section">
            <div class="search-box">
                <input type="text" id="searchInput" placeholder="Search by name..." />
                <button id="searchBtn">🔍</button>
                <span id="resultCount" class="result-count">Showing: <strong id="countCurrent">{len(people_data)}</strong>/<strong id="countTotal">{len(people_data)}</strong></span>
            </div>
        </div>
        
        <div class="people-container">
            <aside class="filters-sidebar">
                <h3>Filters</h3>
                
                <div class="filter-group">
                    <h4>Gender</h4>
                    <div class="filter-options" id="filterGender"></div>
                </div>
                
                <div class="filter-group">
                    <h4>Gens</h4>
                    <div class="filter-options" id="filterGens"></div>
                    <button class="show-more" id="showMoreGens" style="display:none">+ more</button>
                </div>
                
                <div class="filter-group">
                    <h4>Origin</h4>
                    <div class="filter-options" id="filterOrigin"></div>
                    <button class="show-more" id="showMoreOrigin" style="display:none">+ more</button>
                </div>
                
                <div class="filter-group">
                    <h4>Occupation</h4>
                    <div class="filter-options" id="filterOccupation"></div>
                </div>
                
                <div class="filter-group">
                    <h4>Role</h4>
                    <div class="filter-options" id="filterRole"></div>
                    <button class="show-more" id="showMoreRole" style="display:none">+ more</button>
                </div>
                
                <button id="clearFilters" class="clear-btn">Clear all filters</button>
            </aside>
            
            <div class="people-list" id="peopleList">
                {cards if cards else "<p>No people found.</p>"}
            </div>
        </div>
    </main>
    <style>
        /* Search and filter section */
        .search-filter-section {{
            margin: 20px 0;
            padding: 15px;
            background: rgba(255, 255, 252, 0.6);
            border-left: 5px solid #8B3A3A;
            box-shadow: 0 2px 10px rgba(0,0,0,0.03);
        }}
        .search-box {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        #searchInput {{
            flex: 1;
            padding: 10px;
            border: 1px solid rgba(139, 58, 58, 0.3);
            border-radius: 2px;
            font-size: 14px;
            font-family: 'Cardo', serif;
            background: white;
        }}
        #searchInput:focus {{
            outline: none;
            border-color: #8B3A3A;
        }}
        #searchBtn {{
            padding: 10px 20px;
            background: #8B3A3A;
            color: #FDFaf0;
            border: none;
            border-radius: 2px;
            cursor: pointer;
            font-family: 'Cardo', serif;
            transition: background 0.2s ease;
        }}
        #searchBtn:hover {{
            background: #6D2D2D;
        }}
        .result-count {{
            font-size: 14px;
            color: #2c3e50;
            font-family: 'Cardo', serif;
        }}
        .result-count strong {{
            color: #8B3A3A;
        }}
        
        /* Container con sidebar e lista */
        .people-container {{
            display: flex;
            gap: 20px;
            margin-top: 20px;
        }}
        
        /* Sidebar filtri */
        .filters-sidebar {{
            width: 250px;
            flex-shrink: 0;
            background: rgba(255, 255, 252, 0.6);
            border-left: 5px solid #8B3A3A;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.03);
            height: fit-content;
            max-height: calc(100vh - 100px);
            overflow-y: auto;
            position: sticky;
            top: 20px;
        }}
        .filters-sidebar::-webkit-scrollbar {{
            width: 8px;
        }}
        .filters-sidebar::-webkit-scrollbar-track {{
            background: rgba(239, 235, 216, 0.3);
            border-radius: 2px;
        }}
        .filters-sidebar::-webkit-scrollbar-thumb {{
            background: #8B3A3A;
            border-radius: 2px;
        }}
        .filters-sidebar::-webkit-scrollbar-thumb:hover {{
            background: #6D2D2D;
        }}
        .filters-sidebar h3 {{
            margin-top: 0;
            margin-bottom: 15px;
            font-size: 1.2rem;
            color: #6D2D2D;
            font-family: 'Cardo', serif;
            text-align: left;
            border-bottom: 1px solid rgba(139, 58, 58, 0.2);
            padding-bottom: 5px;
        }}
        .filter-group {{
            margin-bottom: 20px;
        }}
        .filter-group h4 {{
            font-size: 0.85rem;
            margin: 0 0 10px 0;
            color: #8B3A3A;
            font-weight: bold;
            font-family: 'Cardo', serif;
            text-transform: uppercase;
            letter-spacing: 0.8px;
        }}
        .filter-options {{
            display: flex;
            flex-direction: column;
            gap: 5px;
        }}
        .filter-option {{
            display: grid;
            grid-template-columns: auto 1fr auto;
            align-items: center;
            gap: 8px;
            font-size: 13px;
            cursor: pointer;
            padding: 3px 0;
            font-family: 'Cardo', serif;
        }}
        .filter-option input[type="checkbox"] {{
            cursor: pointer;
            margin: 0;
            accent-color: #8B3A3A;
        }}
        .filter-option label {{
            cursor: pointer;
            text-align: left;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            color: #2c3e50;
        }}
        .filter-option:hover label {{
            color: #8B3A3A;
        }}
        .filter-count {{
            color: #888;
            font-size: 12px;
            justify-self: end;
        }}
        .show-more {{
            background: none;
            border: none;
            color: #8B3A3A;
            cursor: pointer;
            font-size: 12px;
            padding: 5px 0;
            text-decoration: underline;
            font-family: 'Cardo', serif;
        }}
        .show-more:hover {{
            color: #6D2D2D;
            text-decoration-style: solid;
        }}
        .clear-btn {{
            width: 100%;
            padding: 10px;
            background: #8B3A3A;
            color: #FDFaf0;
            border: none;
            border-radius: 2px;
            cursor: pointer;
            font-size: 13px;
            margin-top: 10px;
            font-family: 'Cardo', serif;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            transition: background 0.2s ease;
        }}
        .clear-btn:hover {{
            background: #6D2D2D;
        }}
        
        /* Lista persone */
        .people-list {{
            flex: 1;
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
        }}
        .person.hidden {{
            display: none;
        }}
        
        /* Responsive */
        @media (max-width: 768px) {{
            .people-container {{
                flex-direction: column;
            }}
            .filters-sidebar {{
                width: 100%;
                position: relative;
                top: 0;
                max-height: none;
            }}
            .people-list {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
    <script>
        // Inizializzazione
        document.addEventListener('DOMContentLoaded', function() {{
            const peopleCards = document.querySelectorAll('.person');
            const totalCount = peopleCards.length;
            
            // Raccogli tutti i valori per i filtri
            const filterData = {{
                gender: {{}},
                gens: {{}},
                origin: {{}},
                occupation: {{}},
                role: {{}}
            }};
            
            peopleCards.forEach(card => {{
                // Gender
                const gender = card.getAttribute('data-gender');
                if (gender) {{
                    const genderLabel = gender === 'm' ? 'Male' : (gender === 'f' ? 'Female' : 'Unknown');
                    filterData.gender[gender] = (filterData.gender[gender] || 0) + 1;
                }}
                
                // Gens
                const gens = card.getAttribute('data-gens');
                if (gens) {{
                    gens.split(',').filter(g => g).forEach(g => {{
                        filterData.gens[g] = (filterData.gens[g] || 0) + 1;
                    }});
                }}
                
                // Origin
                const origin = card.getAttribute('data-origin');
                if (origin) {{
                    origin.split(',').filter(o => o).forEach(o => {{
                        filterData.origin[o] = (filterData.origin[o] || 0) + 1;
                    }});
                }}
                
                // Occupation
                const occupation = card.getAttribute('data-occupation');
                if (occupation) {{
                    filterData.occupation[occupation] = (filterData.occupation[occupation] || 0) + 1;
                }}
                
                // Role
                const role = card.getAttribute('data-role');
                if (role) {{
                    role.split(',').filter(r => r).forEach(r => {{
                        filterData.role[r] = (filterData.role[r] || 0) + 1;
                    }});
                }}
            }});
            
            // Popola i filtri
            populateFilter('filterGender', filterData.gender, 'gender');
            populateFilter('filterGens', filterData.gens, 'gens', 5);
            populateFilter('filterOrigin', filterData.origin, 'origin', 5);
            populateFilter('filterOccupation', filterData.occupation, 'occupation');
            populateFilter('filterRole', filterData.role, 'role', 5);
            
            // Funzione per popolare i filtri
            function populateFilter(containerId, data, attribute, limit = null) {{
                const container = document.getElementById(containerId);
                const entries = Object.entries(data).sort((a, b) => b[1] - a[1]);
                
                entries.forEach((([value, count], index) => {{
                    if (limit && index >= limit) {{
                        const option = createFilterOption(value, count, attribute);
                        option.style.display = 'none';
                        option.classList.add('extra-option');
                        container.appendChild(option);
                    }} else {{
                        container.appendChild(createFilterOption(value, count, attribute));
                    }}
                }}));
                
                // Gestisci pulsante "show more"
                if (limit && entries.length > limit) {{
                    const showMoreBtn = document.getElementById('showMore' + containerId.replace('filter', ''));
                    if (showMoreBtn) {{
                        showMoreBtn.style.display = 'block';
                        showMoreBtn.addEventListener('click', function() {{
                            container.querySelectorAll('.extra-option').forEach(opt => {{
                                opt.style.display = 'flex';
                            }});
                            showMoreBtn.style.display = 'none';
                        }});
                    }}
                }}
            }}
            
            function createFilterOption(value, count, attribute) {{
                const div = document.createElement('div');
                div.className = 'filter-option';
                
                const checkbox = document.createElement('input');
                checkbox.type = 'checkbox';
                checkbox.id = `filter_${{attribute}}_${{value}}`;
                checkbox.value = value;
                checkbox.dataset.attribute = attribute;
                
                const label = document.createElement('label');
                label.htmlFor = checkbox.id;
                
                // Formatta label per gender
                let displayValue = value;
                if (attribute === 'gender') {{
                    displayValue = value === 'm' ? 'Male' : (value === 'f' ? 'Female' : 'Unknown');
                }}
                
                label.textContent = displayValue.charAt(0).toUpperCase() + displayValue.slice(1);
                
                const countSpan = document.createElement('span');
                countSpan.className = 'filter-count';
                countSpan.textContent = `(${{count}})`;
                
                div.appendChild(checkbox);
                div.appendChild(label);
                div.appendChild(countSpan);
                
                checkbox.addEventListener('change', applyFilters);
                
                return div;
            }}
            
            // Ricerca per nome
            const searchInput = document.getElementById('searchInput');
            const searchBtn = document.getElementById('searchBtn');
            
            searchInput.addEventListener('input', applyFilters);
            searchBtn.addEventListener('click', applyFilters);
            
            // Clear filters
            document.getElementById('clearFilters').addEventListener('click', function() {{
                document.querySelectorAll('.filter-option input[type="checkbox"]').forEach(cb => {{
                    cb.checked = false;
                }});
                searchInput.value = '';
                applyFilters();
            }});
            
            // Funzione principale di filtraggio
            function applyFilters() {{
                const searchTerm = searchInput.value.toLowerCase().trim();
                const activeFilters = {{
                    gender: [],
                    gens: [],
                    origin: [],
                    occupation: [],
                    role: []
                }};
                
                // Raccogli filtri attivi
                document.querySelectorAll('.filter-option input[type="checkbox"]:checked').forEach(cb => {{
                    const attr = cb.dataset.attribute;
                    activeFilters[attr].push(cb.value);
                }});
                
                let visibleCount = 0;
                
                peopleCards.forEach(card => {{
                    let visible = true;
                    
                    // Filtro ricerca nome
                    if (searchTerm) {{
                        const name = card.getAttribute('data-name') || '';
                        if (!name.includes(searchTerm)) {{
                            visible = false;
                        }}
                    }}
                    
                    // Filtro gender
                    if (visible && activeFilters.gender.length > 0) {{
                        const gender = card.getAttribute('data-gender');
                        if (!activeFilters.gender.includes(gender)) {{
                            visible = false;
                        }}
                    }}
                    
                    // Filtro gens
                    if (visible && activeFilters.gens.length > 0) {{
                        const gens = (card.getAttribute('data-gens') || '').split(',').filter(g => g);
                        if (!gens.some(g => activeFilters.gens.includes(g))) {{
                            visible = false;
                        }}
                    }}
                    
                    // Filtro origin
                    if (visible && activeFilters.origin.length > 0) {{
                        const origin = (card.getAttribute('data-origin') || '').split(',').filter(o => o);
                        if (!origin.some(o => activeFilters.origin.includes(o))) {{
                            visible = false;
                        }}
                    }}
                    
                    // Filtro occupation
                    if (visible && activeFilters.occupation.length > 0) {{
                        const occupation = card.getAttribute('data-occupation');
                        if (!activeFilters.occupation.includes(occupation)) {{
                            visible = false;
                        }}
                    }}
                    
                    // Filtro role
                    if (visible && activeFilters.role.length > 0) {{
                        const roles = (card.getAttribute('data-role') || '').split(',').filter(r => r);
                        if (!roles.some(r => activeFilters.role.includes(r))) {{
                            visible = false;
                        }}
                    }}
                    
                    // Mostra/nascondi card
                    if (visible) {{
                        card.classList.remove('hidden');
                        visibleCount++;
                    }} else {{
                        card.classList.add('hidden');
                    }}
                }});
                
                // Aggiorna contatore
                document.getElementById('countCurrent').textContent = visibleCount;
                document.getElementById('countTotal').textContent = totalCount;
            }}
        }});
    </script>
    <footer>
        <p>Generated via Saxon-Che & GitHub Actions</p>
        <p>&copy; 2026 - Leonardo Battistella</p>
        <p><strong>Digital Approaches to the Inscriptions of the Eastern Necropolis of Julia Concordia</strong></p>
        <p>MA Thesis project in <em>Digital and Public Humanities</em> – Ca' Foscari University of Venice.</p>
        <p>This is a non-commercial, open-access research project for educational and scientific purposes only.</p>
    </footer>
</body>
</html>"""

    os.makedirs(output_dir, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(full_html)
    print(f"Fine: Pagina generata con {len(people_data)} persone.")

if __name__ == "__main__":
    run()
