# v1.2.0 — Twelve new inscriptions, shared vocabularies, automated validation

The corpus grows from 59 to 71 inscriptions, twelve of which are still being
completed and are marked as such. This release also introduces shared
vocabulary files, a first layer of encoding for commissioning and sepulchral
fines, and automated validation of every XML file before publication.

## Corpus

- Twelve inscriptions added, bringing the total to 71.
- Files still in progress carry `<revisionDesc status="unfinished">` and are
  flagged with a badge on their published page. Twelve are currently so marked:
  their transcription, sanctions and prosopography are encoded, while physical
  description, linguistic annotation and commentary are pending.

## New encoding layers

Applied so far to thirteen inscriptions, and to be extended to the rest:

- **Commissioning.** `<listRelation>` records the act by which each tomb was
  procured, the party who performed it and the party for whom, anchored to the
  verb in the edition. Where a text distributes the act across several agents
  or moments, each is recorded separately; where the text names no verb, or
  where the clause is lost, the two cases are distinguished rather than
  conflated.
- **Sepulchral fines.** `<measure>` now carries the amount, the unit and the
  metal in a declared vocabulary, and `<rs>` identifies the recipient — the
  *fiscus*, the *res publica*, a *schola* — as an entity rather than as a word.
  The kinds of penalty a text threatens, pecuniary or corporal, and whether
  they are alternative or cumulative, are declared in `<textClass>`.
- **Formulae.** Recurring clauses, such as the declaration of self-funding and
  the sanction, are identified in standoff with `<linkGrp>` and paired
  `<anchor>` elements, so that the marking does not interfere with the
  line structure of the edition.

## Shared vocabularies

The new `vocabularies/` folder holds two authority files:

- `taxonomy.xml` — ten taxonomies (decorations, military ranks, kinds of
  organization, periods, places, occupations, sanctions, roles, commissioning
  acts, formulae) and a declaration of the units of measure used for fines,
  with the conversions that can be stated as fact and none of those that
  cannot.
- `organizations.xml` — the institutions and military units named in the
  corpus, each identified once and classified by reference.

The inscription files still carry their own copy of the taxonomies. The
migration to the shared files is in progress and is not part of this release.

## Validation

`deploy.yml` now validates before it publishes. Every XML file is checked for
well-formedness, and the inscriptions are validated against the EpiDoc schema;
the scripts run only if those checks pass, so a defective file can no longer
reach the published site unnoticed.

## Corrections

Errors found and fixed while preparing this release include inscription
headers carrying another inscription's title, filename or external
identifiers; photograph captions naming the wrong person; bibliographic
identifiers not matching their titles; pointers to taxonomy categories that
did not exist; and two faults in the XSLT stylesheet that silently suppressed
the discovery date and a palaeographic rendering rule.
