import os
import json
from saxonche import PySaxonProcessor


# ── Colour categories ──────────────────────────────────────────────
# Each entry: (category_key, english_label, hex_colour)
CATEGORY_COLOURS = {
    'soldier':           ('Soldier',                '#DC143C'),   # red
    'civilian':          ('Civilian',               '#4169E1'),   # blue
    'fabricensis':       ('Fabricensis',             '#FF8C00'),   # orange
    'functionary':       ('Functionary',            '#8A2BE2'),   # violet
    'greek_merchant':    ('Greek Merchant',          '#228B22'),   # green
    'fabricensis_civil': ('Fabricensis & Civilian',  '#2E8B8B'),   # teal
    'soldier_civil':     ('Soldier & Civilian',      '#8B2252'),   # dark magenta
    'unknown':           ('Unknown / Other',         '#888888'),   # grey
}


def determine_category(occupations: set) -> tuple:
    """Return (category_key, hex_colour) from a set of base occupations."""
    if not occupations:
        return 'unknown', CATEGORY_COLOURS['unknown'][1]

    if occupations == {'civil'}:
        return 'civilian', CATEGORY_COLOURS['civilian'][1]
    if occupations == {'soldier'}:
        return 'soldier', CATEGORY_COLOURS['soldier'][1]
    if occupations == {'fabricensis'}:
        return 'fabricensis', CATEGORY_COLOURS['fabricensis'][1]
    if occupations == {'functionary'}:
        return 'functionary', CATEGORY_COLOURS['functionary'][1]
    if occupations == {'greek_merchant'}:
        return 'greek_merchant', CATEGORY_COLOURS['greek_merchant'][1]

    # Mixed burials
    if occupations == {'fabricensis', 'civil'}:
        return 'fabricensis_civil', CATEGORY_COLOURS['fabricensis_civil'][1]
    if occupations == {'soldier', 'civil'}:
        return 'soldier_civil', CATEGORY_COLOURS['soldier_civil'][1]

    return 'unknown', CATEGORY_COLOURS['unknown'][1]


def collect_markers(xml_dir: str) -> list:
    """Parse every TEI/EpiDoc XML and return a list of marker dicts."""
    markers = []

    with PySaxonProcessor(license=False) as proc:
        xp = proc.new_xpath_processor()
        files = sorted(f for f in os.listdir(xml_dir) if f.lower().endswith('.xml'))

        for filename in files:
            xml_path = os.path.join(xml_dir, filename)
            try:
                node = proc.parse_xml(xml_file_name=xml_path)
                xp.set_context(xdm_item=node)

                # ── Coordinates ─────────────────────────────────
                px = xp.evaluate("//*[local-name()='note'][@type='plan_x']")
                py = xp.evaluate("//*[local-name()='note'][@type='plan_y']")
                if not px or px.size == 0 or not py or py.size == 0:
                    continue
                plan_x = float(px.item_at(0).string_value.strip())
                plan_y = float(py.item_at(0).string_value.strip())

                # ── Title ───────────────────────────────────────
                ti = xp.evaluate(
                    "//*[local-name()='titleStmt']/*[local-name()='title'][1]"
                )
                title = (ti.item_at(0).string_value.strip()
                         if ti and ti.size > 0 else filename)

                # ── Paths (relative to docs/pages/map.html) ────
                base = filename.replace('.xml', '')
                url   = f"inscriptions/{base}.html"
                image = f"../images/inscriptions/{base}.jpg"

                # ── People & occupation logic ───────────────────
                persons = xp.evaluate("//*[local-name()='person']")
                people_names = []
                deceased_occupations = set()

                if persons and persons.size > 0:
                    for i in range(persons.size):
                        person = persons.item_at(i)
                        xp.set_context(xdm_item=person)

                        # Full name
                        nm = xp.evaluate(
                            ".//*[local-name()='name'][@type='full']"
                        )
                        full_name = (nm.item_at(0).string_value.strip()
                                     if nm and nm.size > 0 else "Unknown")

                        # Role
                        rl = xp.evaluate(
                            ".//*[local-name()='note'][@type='role']"
                        )
                        role = (rl.item_at(0).string_value.strip()
                                if rl and rl.size > 0 else "")

                        # Annotate dedicators in the display name
                        display_name = full_name
                        role_lower = role.lower().strip()
                        if role_lower == 'dedicator':
                            display_name += ' (dedicator)'
                        elif role_lower == 'dedicator?':
                            display_name += ' (dedicator?)'
                        elif role_lower == 'dedicator (restoration)':
                            display_name += ' (restoration patron)'
                        elif role_lower == 'mentioned':
                            display_name += ' (mentioned)'

                        people_names.append(display_name)

                        # Occupation
                        oc = xp.evaluate(
                            ".//*[local-name()='note'][@type='occupation']"
                        )
                        occupation = (oc.item_at(0).string_value.strip()
                                      if oc and oc.size > 0 else "")

                        # Only deceased (any variant) count for
                        # the colour classification
                        if 'deceased' in role.lower():
                            base_occ = occupation.rstrip('?').strip()
                            if base_occ:
                                deceased_occupations.add(base_occ)

                cat_key, colour = determine_category(deceased_occupations)

                markers.append({
                    'x': plan_x,
                    'y': plan_y,
                    'title': title,
                    'url': url,
                    'image': image,
                    'people': people_names,
                    'category': cat_key,
                    'color': colour,
                })

            except Exception as exc:
                print(f"[map] Error on {filename}: {exc}")

    return markers


# ── HTML template ──────────────────────────────────────────────────
# Uses __PLACEHOLDER__ tokens so we avoid f-string brace headaches.

HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Map – Eastern Necropolis of Iulia Concordia</title>
    <link rel="stylesheet" href="../css/style.css">
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <style>
        /* ── Map container ─────────────────────────────── */
        #map-container {
            width: 100%;
            margin: 20px auto;
        }
        #map {
            width: 100%;
            border: 1px solid rgba(139, 58, 58, 0.3);
            border-radius: 2px;
            background: #f5f3e8;
        }

        /* ── Leaflet tooltip override ──────────────────── */
        .inscription-tooltip {
            background: rgba(255, 255, 252, 0.97);
            border: 1px solid #8B3A3A;
            border-radius: 2px;
            padding: 0;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            font-family: 'Cardo', serif;
            max-width: 260px;
        }
        .inscription-tooltip .leaflet-tooltip-content {
            margin: 0;
        }
        .tooltip-inner {
            padding: 10px 12px;
        }
        .tooltip-inner a.tooltip-title {
            display: block;
            color: #8B3A3A;
            font-weight: bold;
            font-size: 0.9rem;
            text-decoration: none;
            margin-bottom: 6px;
            line-height: 1.3;
        }
        .tooltip-inner a.tooltip-title:hover {
            text-decoration: underline;
        }
        .tooltip-inner img {
            display: block;
            max-width: 100%;
            max-height: 120px;
            object-fit: contain;
            margin: 6px 0;
            border: 1px solid #ddd;
            border-radius: 2px;
        }
        .tooltip-inner .tooltip-people {
            font-size: 0.8rem;
            color: #2c3e50;
            line-height: 1.4;
            border-top: 1px solid rgba(139,58,58,0.15);
            padding-top: 6px;
            margin-top: 4px;
        }

        /* ── Leaflet popup override (click) ────────────── */
        .inscription-popup .leaflet-popup-content-wrapper {
            background: rgba(255, 255, 252, 0.97);
            border: 1px solid #8B3A3A;
            border-radius: 2px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            font-family: 'Cardo', serif;
            padding: 0;
        }
        .inscription-popup .leaflet-popup-content {
            margin: 0;
            max-width: 260px;
        }
        .inscription-popup .leaflet-popup-tip {
            background: rgba(255, 255, 252, 0.97);
            border: 1px solid #8B3A3A;
        }

        /* ── Custom legend ─────────────────────────────── */
        .map-legend {
            background: rgba(255, 255, 252, 0.95);
            border: 1px solid #8B3A3A;
            border-radius: 2px;
            padding: 10px 14px;
            font-family: 'Cardo', serif;
            font-size: 0.8rem;
            line-height: 1.8;
            box-shadow: 0 2px 8px rgba(0,0,0,0.12);
        }
        .map-legend h4 {
            margin: 0 0 6px 0;
            font-size: 0.85rem;
            color: #8B3A3A;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .legend-item {
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .legend-circle {
            display: inline-block;
            width: 14px;
            height: 14px;
            border-radius: 50%;
            border: 2px solid;
            flex-shrink: 0;
        }

        /* ── Intro text ────────────────────────────────── */
        .map-intro {
            max-width: 800px;
            margin: 0 auto 15px auto;
            text-align: justify;
            font-family: 'Cardo', serif;
            color: #2c3e50;
            line-height: 1.6;
            font-size: 0.95rem;
        }

        /* ── Responsive ────────────────────────────────── */
        @media (max-width: 600px) {
            .map-legend {
                font-size: 0.7rem;
                padding: 8px 10px;
            }
        }
    </style>
</head>
<body>
    <header class="site-header">
        <h1 class="main_title">Digital Approaches to the Inscriptions of the Eastern Necropolis of <em>Iulia Concordia</em></h1>
        <nav class="navbar">
            <ul class="menu">
                <li><a href="../index.html">Home</a></li>
                <li><a href="./inscriptions.html">Inscriptions</a></li>
                <li><a href="./people.html">People</a></li>
                <li><a href="./map.html">Map</a></li>
                <li>
                    <a href="#">Study &amp; Context ▾</a>
                    <ul class="submenu">
                        <li><a href="./context/history.html">History</a></li>
                        <li><a href="./context/about_people.html">About People Buried</a></li>
                        <li><a href="./context/supports.html">Supports &amp; Monuments</a></li>
                        <li><a href="./context/chronology.html">Dating &amp; Chronology</a></li>
                    </ul>
                </li>
                <li>
                    <a href="#">References ▾</a>
                    <ul class="submenu">
                        <li><a href="./references/bibliography.html">Bibliography</a></li>
                        <li><a href="./references/corpora_databases.html">Corpora and Databases</a></li>
                    </ul>
                </li>
            </ul>
        </nav>
    </header>

    <main>
        <h2>Interactive Map of the Eastern Necropolis</h2>

        <p class="map-intro">
            The map below shows the positions of the inscribed sarcophagi within the
            Eastern Necropolis (<em>Sepolcreto dei Militi</em>) of <em>Iulia Concordia</em>,
            based on the 1879 planimetry. Each marker is colour-coded according to the
            occupation of the deceased. Hover over a marker for a quick preview;
            click on it to pin the card in place. Click anywhere else on the map to dismiss it.
        </p>

        <div id="map-container">
            <div id="map"></div>
        </div>
    </main>

    <footer>
        <p>Generated via Saxon-Che &amp; GitHub Actions</p>
        <p>&copy; 2026 – Leonardo Battistella</p>
        <p><strong>Digital Approaches to the Inscriptions of the Eastern Necropolis of Julia Concordia</strong></p>
        <p>MA Thesis project in <em>Digital and Public Humanities</em> – Ca' Foscari University of Venice.</p>
        <p>This is a non-commercial, open-access research project for educational and scientific purposes only.</p>
    </footer>

<script>
// ── Marker data injected by Python ────────────────────────────────
var MARKERS = __MARKERS_JSON__;

// ── Legend entries ─────────────────────────────────────────────────
var LEGEND = __LEGEND_JSON__;

// ── Initialise map once the planimetry image has loaded ───────────
(function () {
    var IMG_URL = '../images/plan/Eastern_Necropolis_Plan_1879.jpg';
    var img = new Image();

    img.onload = function () {
        var h = this.naturalHeight;
        var w = this.naturalWidth;
        initMap(w, h);
    };

    img.onerror = function () {
        console.warn('Could not load planimetry image; using fallback dimensions.');
        initMap(3000, 2000);
    };

    img.src = IMG_URL;

    function initMap(imgW, imgH) {
        // ── Set map container height to match image aspect ratio ──
        var mapEl = document.getElementById('map');
        var containerW = mapEl.offsetWidth;
        var aspectH = Math.round(containerW * (imgH / imgW));
        // Clamp between 350px and 85vh
        var maxH = Math.round(window.innerHeight * 0.85);
        var minH = 350;
        aspectH = Math.max(minH, Math.min(aspectH, maxH));
        mapEl.style.height = aspectH + 'px';

        var bounds = [[0, 0], [imgH, imgW]];

        var map = L.map('map', {
            crs: L.CRS.Simple,
            minZoom: -2,
            maxZoom: 3,
            zoomSnap: 0.25,
            attributionControl: false
        });

        L.imageOverlay(IMG_URL, bounds).addTo(map);
        map.fitBounds(bounds);

        // ── Resize handler ────────────────────────────────────────
        window.addEventListener('resize', function () {
            var newW = mapEl.offsetWidth;
            var newH = Math.round(newW * (imgH / imgW));
            var maxH2 = Math.round(window.innerHeight * 0.85);
            newH = Math.max(350, Math.min(newH, maxH2));
            mapEl.style.height = newH + 'px';
            map.invalidateSize();
        });

        // ── Build shared card HTML for tooltip & popup ────────────
        function buildCardHtml(m) {
            var peopleHtml = m.people.map(function (n) { return n; }).join(', ');
            return '<div class="tooltip-inner">' +
                '<a class="tooltip-title" href="' + m.url + '">' + m.title + '</a>' +
                '<img src="' + m.image + '" alt="inscription" onerror="this.style.display=\'none\'">' +
                '<div class="tooltip-people">' + peopleHtml + '</div>' +
            '</div>';
        }

        // ── Add markers ───────────────────────────────────────────
        MARKERS.forEach(function (m) {
            var latLng = [m.y, m.x];

            var circle = L.circleMarker(latLng, {
                radius: 10,
                color: m.color,
                weight: 2.5,
                opacity: 0.9,
                fillColor: m.color,
                fillOpacity: 0.25
            }).addTo(map);

            var cardHtml = buildCardHtml(m);

            // Hover → tooltip (disappears on mouse out)
            circle.bindTooltip(cardHtml, {
                direction: 'top',
                offset: [0, -12],
                className: 'inscription-tooltip',
                opacity: 1
            });

            // Click → popup (stays until user closes / clicks elsewhere)
            circle.bindPopup(cardHtml, {
                className: 'inscription-popup',
                maxWidth: 260,
                offset: [0, -10],
                closeButton: true
            });

            // When popup opens, hide tooltip to avoid overlap
            circle.on('click', function () {
                circle.closeTooltip();
            });
        });

        // ── Legend control ─────────────────────────────────────────
        var legend = L.control({ position: 'bottomright' });
        legend.onAdd = function () {
            var div = L.DomUtil.create('div', 'map-legend');
            var html = '<h4>Legend</h4>';
            LEGEND.forEach(function (entry) {
                html +=
                    '<div class="legend-item">' +
                        '<span class="legend-circle" style="background:' +
                            entry.color + ';border-color:' + entry.color + '"></span>' +
                        '<span>' + entry.label + '</span>' +
                    '</div>';
            });
            div.innerHTML = html;
            return div;
        };
        legend.addTo(map);
    }
})();
</script>
</body>
</html>"""


def generate_html(markers: list, output_file: str):
    """Write the final HTML file, injecting markers and legend as JSON."""

    markers_json = json.dumps(markers, ensure_ascii=False, indent=2)

    # Build legend from the categories actually present in the data
    present_categories = sorted(
        {m['category'] for m in markers},
        key=lambda k: list(CATEGORY_COLOURS.keys()).index(k)
            if k in CATEGORY_COLOURS else 99
    )
    legend_entries = []
    for cat in present_categories:
        label, colour = CATEGORY_COLOURS.get(cat, ('Unknown', '#888888'))
        legend_entries.append({'label': label, 'color': colour})
    legend_json = json.dumps(legend_entries, ensure_ascii=False)

    html = HTML_TEMPLATE
    html = html.replace('__MARKERS_JSON__', markers_json)
    html = html.replace('__LEGEND_JSON__', legend_json)

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)


# ── Entry point ────────────────────────────────────────────────────
def run():
    base_dir  = os.getcwd()
    xml_dir   = os.path.join(base_dir, 'inscriptions')
    out_file  = os.path.join(base_dir, 'docs', 'pages', 'map.html')

    if not os.path.exists(xml_dir):
        print("[map] inscriptions/ directory not found – nothing to do.")
        return

    markers = collect_markers(xml_dir)
    generate_html(markers, out_file)
    print(f"[map] Done – {len(markers)} markers written to {out_file}")


if __name__ == '__main__':
    run()
