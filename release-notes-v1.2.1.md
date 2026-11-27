# v1.2.1 — Encoding layers extended to the whole corpus

The commissioning, sanction and formula layers introduced in v1.2.0 on thirteen
inscriptions are now applied to all 71. This release also fixes how the website
links words to the critical apparatus, renames one inscription whose file and
person records carried the wrong name, and corrects a series of encoding errors
found while completing the work.

## Commissioning and entrusting

- Every inscription now has a `<listRelation>`, for 79 relations in total.
- Relation names are now in Latin, like the rest of the vocabulary for ancient
  concepts. `dedicatio` replaces `commission` for the acts by which a tomb was
  procured. The new `commendatio` records a tomb entrusted to a third party: the
  church of Concordia (the tombs of Fl. Andia, Fl. Fandigildus, and Fl.
  Alatancus and Bitorta) or the veterans (the tomb of Fl. Mansuetus).
- Three acts are new to the taxonomy:
  - `dedico` (*memoriam dedicaverunt*);
  - `sepelio` (*quem sepelivit coniux*; *amici honore sepultus*);
  - `peto`, under the acts of guardianship (*petimus omnem clerum*).
- Every verb of an act now carries a lemma, and each relation points directly
  to that verb's `<w>`. Anchors are no longer used for acts, only to mark the
  span of a formula.
- The encoding follows the grammar of the text:
  - when the verb is plural, both spouses are recorded as agents, even when the
    syntax subordinates the wife (*cum coniuge sua*, or the dative);
  - when the verb is passive (*empta est*, *positus est*), the agent is left
    unrecorded unless the text names one;
  - where the text names no act, `act-unexpressed` is used; where the clause
    with the act is lost, `act-lost`.

## Fines and formulae

- 48 inscriptions now declare the amount of their fine (`<measure
  type="poena">`), and 47 identify its recipient. One of the new recipients is
  the *res publica*, attested in the necropolis for the first time (Aristo and
  Veneria).
- Two pecuniary penalties joined by *vel* are now classified as alternatives,
  exactly as *aut … aut* is.
- Corporal penalties are classified in `<textClass>` and no longer wrapped in
  `<measure>`, which is reserved for quantities.
- 53 inscriptions identify their formulae in standoff: *de proprio* and its
  variants (*de labore suo*, *de re sua*, *ex proprio*), the *sanctio*, and the
  *commendatio*. A *sanctio* includes the prohibition when one precedes or
  replaces the conditional clause (*ita ut … nullus*, *ut nullus … ponatur*).

## Edition

- Editorial punctuation is encoded as `<pc type="editorial">` throughout. It was
  added where it was missing, without altering any reading.
- A word split across lines is encoded as two `<w>` elements linked by
  `@next`/`@prev`. An entity name or an amount split across lines is encoded as
  two `<rs>` or two `<measure>` elements, so that no element contains a line
  break.

## People

- Personal names in editions, translations and commentaries now point to their
  person with `@ref` (67 occurrences changed). `@corresp` remains on
  relationship notes and relations.
- References to people recorded in another inscription's file use the form
  `./file.xml#id`.
- Missing `<persName>` elements were added in five inscriptions.
- `martinianus_severina.xml` is now `martinianus_severiana.xml`: the wife's name
  is Severiana. The person's identifier, the photograph and every reference to
  her were updated with it.

## Website

The XSLT now links a word to the critical apparatus only if an apparatus entry
points to it. A word reached as the end of a range links to the start of that
entry. Across the 71 pages, dead internal links went from 108 to none, with no
change to the visible text.

## Corrections

Errors found and fixed while completing the corpus:

- apparatus readings credited to editions of other inscriptions;
- two apparatus sections that were never displayed because they lacked
  `<listApp>`;
- a line break nested inside an amount;
- a person record carrying another woman's name;
- relationship notes pointing to the wrong person, or to the person themselves;
- a cross-reference to the wrong file;
- one wrong and many incomplete links to Ubi Erat Lupa;
- an inconsistent gender value;
- typos in captions and notes.

## Known issues

- Seven military units and the veterans of Concordia are referenced but not yet
  in `organizations.xml`. The same holds for the general `commendatio` formula
  in `taxonomy.xml`. These pointers will resolve once the entries are added.
- The emperors named in dating formulae are not yet in an authority file.
- The inscription files still carry their own copy of the taxonomies.
- Twelve inscriptions remain marked as unfinished.
