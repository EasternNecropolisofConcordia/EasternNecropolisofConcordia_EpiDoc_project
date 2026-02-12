<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:tei="http://www.tei-c.org/ns/1.0" xmlns="http://www.w3.org/1999/xhtml"
    xmlns:xs="http://www.w3.org/2001/XMLSchema" exclude-result-prefixes="tei xs" version="2.0">

    <xsl:output method="xml" indent="yes" encoding="UTF-8"/>

    <!-- ========================================== -->
    <!-- MAIN TEMPLATE: HTML STRUCTURE              -->
    <!-- ========================================== -->
    <xsl:template match="/">
        <html xml:lang="en">
            <head>
                <title>
                    <xsl:value-of select="//tei:titleStmt/tei:title"/>
                </title>
                <meta charset="UTF-8"/>
            </head>
            <body>
                <h1>
                    <xsl:value-of select="//tei:titleStmt/tei:title"/>
                </h1>

                <!-- METADATA SECTION -->
                <div class="metadata">
                    <h2>METADATA</h2>
                    <div class="metadata-grid">
                        <div class="repository">
                            <h3>Current Location</h3>
                            <dl>
                                <dt>
                                    <strong>Institution</strong>
                                </dt>
                                <dd>
                                    <div class="dropdown">
                                        <button class="dropbtn">
                                            <xsl:value-of
                                                select="//tei:repository/tei:orgName/tei:name/text()"
                                            />
                                        </button>
                                        <div class="dropdown-content">
                                            <xsl:for-each
                                                select="//tei:encodingDesc//tei:category[@xml:id = substring-after(//tei:repository/tei:orgName/@ref, '#')]/tei:catDesc/tei:ref">
                                                <xsl:element name="a">
                                                  <xsl:attribute name="href"><xsl:value-of
                                                  select="@target"/></xsl:attribute>
                                                  <xsl:value-of select="upper-case(@type)"/> ID:
                                                  <xsl:value-of select="tei:idno"/>
                                                </xsl:element>
                                            </xsl:for-each>
                                        </div>
                                    </div>
                                    <xsl:text> </xsl:text>
                                    <div class="dropdown">
                                        <button class="dropbtn">
                                            <xsl:value-of
                                                select="//tei:repository/tei:orgName/tei:name/tei:settlement"
                                            />
                                        </button>
                                        <div class="dropdown-content">
                                            <xsl:for-each
                                                select="//tei:encodingDesc//tei:category[@xml:id = substring-after(//tei:repository/tei:orgName//tei:settlement/@ref, '#')]/tei:catDesc/tei:ref">
                                                <xsl:element name="a">
                                                  <xsl:attribute name="href"><xsl:value-of
                                                  select="@target"/></xsl:attribute>
                                                  <xsl:value-of select="upper-case(@type)"/> ID:
                                                  <xsl:value-of select="tei:idno"/>
                                                </xsl:element>
                                            </xsl:for-each>
                                        </div>
                                    </div>
                                </dd>
                                <dt>
                                    <strong>Inventory Number</strong>
                                </dt>
                                <dd>
                                    <xsl:value-of
                                        select="//tei:msIdentifier/tei:idno[@type = 'inventory']"/>
                                </dd>
                            </dl>
                        </div>
                        <div class="external_databases">
                            <h3>External Resources</h3>
                            <xsl:if test="//tei:publicationStmt/tei:idno[@type != 'filename']">
                                <dl>
                                    <xsl:if test="//tei:publicationStmt/tei:idno[@type = 'tm']">
                                        <dt>
                                            <strong>TrisMegistos</strong>
                                        </dt>
                                        <dd>
                                            <xsl:element name="a">
                                                <xsl:attribute name="href"
                                                  >https://www.trismegistos.org/text/<xsl:value-of
                                                  select="//tei:publicationStmt/tei:idno[@type = 'tm']"
                                                  /></xsl:attribute>
                                                <xsl:value-of
                                                  select="//tei:publicationStmt/tei:idno[@type = 'tm']"
                                                />
                                            </xsl:element>
                                        </dd>
                                    </xsl:if>
                                    <xsl:if test="//tei:publicationStmt/tei:idno[@type = 'edr']">
                                        <dt>
                                            <strong>Epigraphic Database Rome</strong>
                                        </dt>
                                        <dd>
                                            <xsl:element name="a">
                                                <xsl:attribute name="href"
                                                  >http://www.edr-edr.it/edr_programmi/res_complex_comune.php?do=book&amp;id_nr=<xsl:value-of
                                                  select="//tei:publicationStmt/tei:idno[@type = 'edr']"
                                                  /></xsl:attribute>
                                                <xsl:value-of
                                                  select="//tei:publicationStmt/tei:idno[@type = 'edr']"
                                                />
                                            </xsl:element>
                                        </dd>
                                    </xsl:if>
                                    <xsl:if test="//tei:publicationStmt/tei:idno[@type = 'uel']">
                                        <dt>
                                            <strong>Ubi Erat Lupa</strong>
                                        </dt>
                                        <dd>
                                            <xsl:element name="a">
                                                <xsl:attribute name="href"
                                                  >https://lupa.at/<xsl:value-of
                                                  select="//tei:publicationStmt/tei:idno[@type = 'uel']"
                                                  /></xsl:attribute>
                                                <xsl:value-of
                                                  select="//tei:publicationStmt/tei:idno[@type = 'uel']"
                                                />
                                            </xsl:element>
                                        </dd>
                                    </xsl:if>
                                </dl>
                            </xsl:if>
                        </div>
                    </div>
                    <div class="findspot">
                        <h3>Findspot and Place of Origin</h3>
                        <dl>
                            <dt>
                                <strong>Country</strong>
                            </dt>
                            <dd>
                                <xsl:value-of
                                    select="//tei:history/tei:provenance[@type = 'found']/tei:placeName[@type = 'country' and @subtype = 'modern' and @xml:lang = 'en']"
                                />
                            </dd>
                            <dt>
                                <strong>Region</strong>
                            </dt>
                            <dd>
                                <xsl:value-of
                                    select="//tei:history/tei:provenance[@type = 'found']/tei:placeName[@type = 'region' and @subtype = 'modern']"
                                />
                            </dd>
                            <dt>
                                <strong>Ancient Region</strong>
                            </dt>
                            <dd>
                                <em>
                                    <xsl:value-of
                                        select="//tei:history/tei:provenance[@type = 'found']/tei:placeName[@type = 'region' and @subtype = 'ancient']"
                                    />
                                </em>
                            </dd>
                            <dt>
                                <strong>City</strong>
                            </dt>
                            <dd>
                                <xsl:value-of
                                    select="//tei:history/tei:provenance[@type = 'found']/tei:settlement[@type = 'city' and @subtype = 'modern']"
                                />
                            </dd>
                            <dt>
                                <strong>Ancient City</strong>
                            </dt>
                            <dd>
                                <div class="dropdown">
                                    <button class="dropbtn">
                                        <em>
                                            <xsl:value-of
                                                select="//tei:history/tei:provenance[@type = 'found']/tei:settlement[@type = 'city' and @subtype = 'ancient']"
                                            />
                                        </em>
                                    </button>
                                    <div class="dropdown-content">
                                        <xsl:for-each
                                            select="//tei:encodingDesc//tei:category[@xml:id = substring-after(//tei:history/tei:provenance[@type = 'found']/tei:settlement[@type = 'city' and @subtype = 'ancient']/@ref, '#')]/tei:catDesc/tei:ref">
                                            <xsl:element name="a">
                                                <xsl:attribute name="href"><xsl:value-of
                                                  select="@target"/></xsl:attribute>
                                                <xsl:value-of select="upper-case(@type)"/> ID:
                                                  <xsl:value-of select="tei:idno"/>
                                            </xsl:element>
                                        </xsl:for-each>
                                    </div>
                                </div>
                            </dd>
                            <xsl:if
                                test="normalize-space(//tei:history/tei:provenance[@type = 'found']/tei:settlement[@type = 'site' and @xml:lang = 'en']) != ''">
                                <dt>
                                    <strong>Site</strong>
                                </dt>
                                <dd>
                                    <xsl:value-of
                                        select="//tei:history/tei:provenance[@type = 'found']/tei:settlement[@type = 'site' and @xml:lang = 'en']"
                                    />
                                </dd>
                            </xsl:if>
                            <xsl:if
                                test="normalize-space(//tei:history/tei:provenance[@type = 'found']/tei:settlement[@type = 'plot']) != ''">
                                <dt>
                                    <strong>Plot</strong>
                                </dt>
                                <dd>
                                    <xsl:value-of
                                        select="//tei:history/tei:provenance[@type = 'found']/tei:settlement[@type = 'plot']"
                                    />
                                </dd>
                            </xsl:if>
                        </dl>
                    </div>
                    <div class="chronology">
                        <h3>Chronology</h3>
                        <xsl:if
                            test="normalize-space(//tei:history//tei:provenance[@type = 'found']/date[@type = 'discovery']) != ''">
                            <h4>Discovery date</h4>
                            <dl>
                                <dt>
                                    <strong>Date</strong>
                                </dt>
                                <dd>
                                    <xsl:value-of
                                        select="//tei:history//tei:provenance[@type = 'found']/date[@type = 'discovery']"
                                    />
                                </dd>
                            </dl>
                        </xsl:if>
                        <h4>Date of the inscription</h4>
                        <dl>
                            <dt>
                                <strong>Date</strong>
                            </dt>
                            <dd>
                                <xsl:value-of
                                    select="normalize-space(//tei:origDate[@xml:lang = 'en'])"/>
                            </dd>
                            <dt>
                                <strong>Dating criteria</strong>
                            </dt>
                            <dd>
                                <xsl:apply-templates select="//tei:origDate[@xml:lang = 'en']"
                                    mode="orig_date"/>
                            </dd>
                        </dl>
                    </div>
                    <div class="autopsy">
                        <h3>Autopsy</h3>
                        <dl>
                            <dt>
                                <strong>Institution</strong>
                            </dt>
                            <dd>
                                <div class="dropdown">
                                    <button class="dropbtn">
                                        <xsl:value-of
                                            select="//tei:repository/tei:orgName/tei:name/text()"/>
                                    </button>
                                    <div class="dropdown-content">
                                        <xsl:for-each
                                            select="//tei:encodingDesc//tei:category[@xml:id = substring-after(//tei:repository/tei:orgName/@ref, '#')]/tei:catDesc/tei:ref">
                                            <xsl:element name="a">
                                                <xsl:attribute name="href"><xsl:value-of
                                                  select="@target"/></xsl:attribute>
                                                <xsl:value-of select="upper-case(@type)"/> ID:
                                                  <xsl:value-of select="tei:idno"/>
                                            </xsl:element>
                                        </xsl:for-each>
                                    </div>
                                </div>
                            </dd>
                            <dt>
                                <strong>Location within museum</strong>
                            </dt>
                            <dd>
                                <xsl:value-of
                                    select="//tei:provenance[@type = 'observed']/tei:note[@type = 'observed' and @xml:lang = 'en']/tei:seg[@type = 'location']"
                                />
                            </dd>
                            <dt>
                                <strong>Date of observation</strong>
                            </dt>
                            <dd>
                                <xsl:value-of
                                    select="//tei:provenance[@type = 'observed']/tei:date[@type = 'autopsy']"
                                />
                            </dd>
                        </dl>
                    </div>
                </div>
                <div class="physical_description">
                    <h2>PHYSICAL DESCRIPTION</h2>
                    <dl>
                        <dt><strong>Type</strong></dt>
                        <dd><xsl:value-of select="normalize-space(//tei:physDesc//tei:objectType[@xml:lang='en'])"/></dd>
                        <dt><strong>Material(s)</strong></dt>
                        <dd><xsl:value-of select="normalize-space(//tei:physDesc//tei:material[@xml:lang='en'])"/></dd>
                        <dt><strong>Execution</strong></dt>
                        <dd><xsl:value-of select="normalize-space(//tei:layoutDesc/tei:layout/tei:rs)"/>.</dd>
                        <dt><strong>Dimensions</strong></dt>
                        <dd><xsl:value-of select="//tei:supportDesc/tei:support/tei:dimensions/tei:height"/> × <xsl:value-of select="//tei:supportDesc/tei:support/tei:dimensions/tei:width"/><xsl:if test="//tei:supportDesc/tei:support/tei:dimensions/tei:depth"> × <xsl:value-of select="//tei:supportDesc/tei:support/tei:dimensions/tei:depth"/> </xsl:if><xsl:text> cm</xsl:text>
                        </dd>
                        <dt><strong>Epigraphic Field</strong></dt>
                        <dd>
                            <xsl:value-of select="//tei:layoutDesc/tei:layout/tei:dimensions/tei:height"/> × <xsl:value-of select="//tei:layoutDesc/tei:layout/tei:dimensions/tei:width"/><xsl:text> cm</xsl:text>
                        </dd>
                        <dt>Letters Height</dt>
                        <dd><xsl:value-of select="normalize-space(//tei:handDesc/tei:handNote/tei:height)"/></dd>
                    </dl>
                    <details class="palaeography">
                        <summary><h3>Palaeographic comment</h3></summary>
                        <xsl:for-each
                            select="//tei:handNote/tei:note[@type = 'palaeographic' and @xml:lang = 'en']/tei:p">
                            <p>
                                <xsl:value-of select="normalize-space(.)"/>
                            </p>
                        </xsl:for-each>
                    </details>
                </div>
                

                <!-- IMAGES -->
                <xsl:apply-templates select="//tei:facsimile/tei:graphic"/>

                <!-- INSCRIPTION SECTION -->
                <div class="inscription">
                    <h2>INSCRIPTION</h2>
                    <h3>TRANSCRIPTION</h3>
                    <xsl:for-each select="//tei:div[@type = 'edition']">
                        <div class="transcription" lang="la">
                            <xsl:choose>
                                <xsl:when test="tei:div[@type = 'textpart']">
                                    <xsl:apply-templates select="tei:div[@type = 'textpart']"/>
                                </xsl:when>
                                <xsl:otherwise>
                                    <xsl:apply-templates select="tei:ab" mode="interp"/>
                                </xsl:otherwise>
                            </xsl:choose>
                        </div>
                    </xsl:for-each>
                </div>


                <!-- APPARATUS CRITICUS -->
                <xsl:if test="//tei:div[@type = 'apparatus']/tei:listApp/tei:app">
                    <div class="apparatus">
                        <h2>
                            <em>APPARATUS CRITICUS</em>
                        </h2>
                        <xsl:variable name="root" select="/"/>
                        <xsl:for-each
                            select="//tei:div[@type = 'apparatus']/tei:listApp/tei:app/@loc[not(. = preceding::tei:app/@loc)]">
                            <xsl:variable name="current_loc" select="."/>
                            <span class="app-line" data-line="{.}">
                                <xsl:value-of select="."/>
                                <xsl:text>. </xsl:text>
                                <xsl:for-each
                                    select="$root//tei:div[@type = 'apparatus']/tei:listApp/tei:app[@loc = $current_loc]">
                                    <xsl:variable name="from_id"
                                        select="substring-after(@from, '#')"/>
                                    <xsl:variable name="to_id" select="substring-after(@to, '#')"/>
                                    <span class="app-entry"
                                        id="{if ($from_id = $to_id) then $from_id else $from_id}">
                                        <xsl:for-each select="tei:rdg">
                                            <xsl:variable name="rdg_content">
                                                <xsl:apply-templates select="." mode="apparatus"/>
                                            </xsl:variable>

                                            <!-- Only show content if rdg is not empty -->
                                            <xsl:if test="normalize-space($rdg_content) != ''">
                                                <xsl:value-of select="normalize-space($rdg_content)"/>
                                                <xsl:text>, </xsl:text>
                                            </xsl:if>

                                            <xsl:variable name="sources"
                                                select="tokenize(normalize-space(@source), '\s+')"/>
                                            <xsl:for-each select="$sources">
                                                <xsl:variable name="source_id">
                                                  <xsl:choose>
                                                  <xsl:when test="starts-with(., '#')">
                                                  <xsl:value-of select="substring-after(., '#')"/>
                                                  </xsl:when>
                                                  <xsl:otherwise>
                                                  <xsl:value-of select="."/>
                                                  </xsl:otherwise>
                                                  </xsl:choose>
                                                </xsl:variable>
                                                <a href="#{$source_id}">
                                                  <xsl:apply-templates
                                                  select="$root//tei:listBibl/tei:bibl[@xml:id = $source_id]/tei:title"
                                                  />
                                                </a>
                                                <xsl:if test="position() != last()">
                                                  <xsl:text>, </xsl:text>
                                                </xsl:if>
                                            </xsl:for-each>
                                            <xsl:if test="position() != last()">
                                                <xsl:text>; </xsl:text>
                                            </xsl:if>
                                        </xsl:for-each>
                                    </span>
                                    <xsl:if test="position() != last()">
                                        <xsl:text> </xsl:text>
                                    </xsl:if>
                                </xsl:for-each>
                                <xsl:text>.</xsl:text>
                            </span>
                            <xsl:text> </xsl:text>
                        </xsl:for-each>
                    </div>
                </xsl:if>
                
                <!-- TRANSLATION -->
                <details class="translation">
                    <summary><h2>TRANSLATION</h2></summary>
                    <xsl:for-each select="//tei:div[@type = 'translation'][@xml:lang = 'en']/tei:p">
                        <p>
                            <xsl:apply-templates/>
                        </p>
                    </xsl:for-each>
                </details>
                
                <!-- COMMENTARY -->
                <details class="commentary">
                    <summary><h2>COMMENTARY</h2></summary>
                    <xsl:for-each select="//tei:div[@type = 'commentary'][@xml:lang = 'en']/tei:p">
                        <p>
                            <xsl:apply-templates/>
                        </p>
                    </xsl:for-each>
                </details>

                <!-- PEOPLE SECTION -->
                <div class="people">
                    <h2>PEOPLE</h2>
                    <xsl:for-each select="//tei:listPerson/tei:person">
                        <xsl:element name="div">
                            <xsl:attribute name="class">person_record</xsl:attribute>
                            <xsl:attribute name="id">
                                <xsl:value-of select="@xml:id"/>
                            </xsl:attribute>
                            <h3>
                                <xsl:value-of select="tei:persName/tei:name[@type = 'full']"/>
                            </h3>
                            <dl>
                                <xsl:for-each select="tei:persName/tei:name">
                                    <xsl:if test="@type != 'full'">
                                        <dt>
                                            <strong>
                                                <xsl:value-of select="upper-case(@type)"/>
                                            </strong>
                                        </dt>
                                        <dd>
                                            <xsl:value-of select="."/>
                                        </dd>
                                    </xsl:if>
                                </xsl:for-each>
                                <xsl:if test="tei:persName/tei:name[@type = 'cognomen'][@nymRef]">
                                    <xsl:for-each
                                        select="tei:persName/tei:name[@type = 'cognomen' and @nymRef]">
                                        <dt>
                                            <strong>ORIGIN (of the name <xsl:value-of select="."
                                                />)</strong>
                                        </dt>
                                        <dd>
                                            <xsl:value-of select="@nymRef"/>
                                        </dd>
                                    </xsl:for-each>
                                </xsl:if>
                                <dt>
                                    <strong>GENDER</strong>
                                </dt>
                                <dd>
                                    <xsl:choose>
                                        <xsl:when test="tei:gender = 'm'">male</xsl:when>
                                        <xsl:when test="tei:gender = 'f'">female</xsl:when>
                                        <xsl:otherwise>unknown</xsl:otherwise>
                                    </xsl:choose>
                                </dd>
                                <xsl:for-each select="tei:note">
                                    <dt>
                                        <strong>
                                            <xsl:value-of select="upper-case(@type)"/>
                                        </strong>
                                    </dt>
                                    <dd>
                                        <xsl:value-of select="."/>
                                        <xsl:if test="@type = 'relationship' and @corresp">
                                            <xsl:text> (→ </xsl:text>
                                            <xsl:element name="a">
                                                <xsl:attribute name="href">
                                                  <xsl:value-of select="@corresp"/>
                                                </xsl:attribute>
                                                <xsl:value-of
                                                  select="normalize-space(//tei:person[@xml:id = substring-after(current()/@corresp, '#')]/tei:persName/tei:name[@type = 'full'])"/>
                                                <xsl:text>)</xsl:text>
                                            </xsl:element>
                                        </xsl:if>
                                    </dd>
                                </xsl:for-each>
                            </dl>
                        </xsl:element>
                    </xsl:for-each>
                </div>

                <!-- BIBLIOGRAPHY -->
                <div class="bibliography">
                    <h2>Bibliography</h2>
                    <xsl:apply-templates select="//tei:listBibl/tei:bibl[not(@type = 'database')]"
                        mode="bibliography"/>
                    <xsl:apply-templates select="//tei:listBibl/tei:bibl[@type = 'database']"
                        mode="bibliography_database"/>
                </div>
            </body>
        </html>
    </xsl:template>

    <!-- ========================================== -->
    <!-- DATING CRITERIA CONVERSION                 -->
    <!-- Converts EpiDoc evidence values to        -->
    <!-- human-readable dating criteria             -->
    <!-- ========================================== -->
    <xsl:template match="tei:origDate[@xml:lang = 'en']" mode="orig_date">
        <xsl:variable name="evidence-tokens" select="tokenize(@evidence, '\s+')"/>
        <xsl:for-each select="$evidence-tokens">
            <xsl:choose>
                <xsl:when test=". = 'archaeological-context'">archaeological context</xsl:when>
                <xsl:when test=". = 'internal-date'">explicit internal date</xsl:when>
                <xsl:when test=". = 'lettering'">palaeography</xsl:when>
                <xsl:when test=". = 'material-context'">material and monument type</xsl:when>
                <xsl:when test=". = 'nomenclature'">onomastics</xsl:when>
                <xsl:when test=". = 'office'">office, rank, or reign</xsl:when>
                <xsl:when test=". = 'prosopography'">prosopography</xsl:when>
                <xsl:when test=". = 'textual-content'">textual/linguistic content</xsl:when>
                <xsl:when test=". = 'textual-context'">textual/linguistic content</xsl:when>
                <xsl:when test=". = 'titulature'">official titles</xsl:when>
                <xsl:when test=". = 'iconography'">iconography</xsl:when>
                <xsl:when test=". = 'artistic-style'">artistic style</xsl:when>
                <xsl:otherwise>
                    <xsl:value-of select="."/>
                </xsl:otherwise>
            </xsl:choose>
            <xsl:if test="position() != last()">
                <xsl:text>, </xsl:text>
            </xsl:if>
        </xsl:for-each>
    </xsl:template>

    <!-- ========================================== -->
    <!-- TEXTPART HANDLING                          -->
    <!-- Handles div[@type='textpart'] elements     -->
    <!-- for multi-location inscriptions            -->
    <!-- ========================================== -->
    <xsl:template match="tei:div[@type = 'textpart']">
        <xsl:element
            name="{if (count(ancestor::tei:div[@type='textpart']) > 0) then 'h5' else 'h4'}">
            <xsl:choose>
                <xsl:when test="@subtype">
                    <xsl:value-of select="upper-case(replace(@subtype, '_', ' '))"/>
                </xsl:when>
                <xsl:when test="@source">
                    <xsl:value-of select="upper-case(replace(@source, '_', ' '))"/>
                </xsl:when>
                <xsl:otherwise>PART <xsl:value-of select="@n"/></xsl:otherwise>
            </xsl:choose>
            <xsl:text>:</xsl:text>
        </xsl:element>

        <div class="textpart" data-location="{(@subtype, @source)[1]}">
            <xsl:apply-templates select="tei:div[@type = 'textpart']"/>
            <xsl:apply-templates select="tei:ab" mode="interp"/>
        </div>
    </xsl:template>

    <!-- ========================================== -->
    <!-- REFERENCE LINKS                            -->
    <!-- ========================================== -->
    <xsl:template match="tei:ref">
        <a href="{@target}">
            <xsl:apply-templates/>
        </a>
    </xsl:template>

    <!-- ========================================== -->
    <!-- IMAGE HANDLING                             -->
    <!-- ========================================== -->
    <xsl:template match="tei:graphic">
        <figure>
            <img src="{@url}">
                <xsl:attribute name="alt">
                    <xsl:value-of select="tei:desc[@type = 'alt']"/>
                </xsl:attribute>
            </img>
            <xsl:apply-templates select="tei:desc[@type = 'figDesc']"/>
            <xsl:apply-templates select="tei:label[@type = 'disclaimer']"/>
        </figure>
    </xsl:template>

    <xsl:template match="tei:desc[@type = 'figDesc']">
        <figcaption>
            <xsl:apply-templates/>
        </figcaption>
    </xsl:template>

    <xsl:template match="tei:label[@type = 'disclaimer']">
        <span class="disclaimer">
            <xsl:apply-templates/>
        </span>
    </xsl:template>

    <!-- ========================================== -->
    <!-- LINE-BY-LINE TRANSCRIPTION BUILDER         -->
    <!-- Constructs text line by line from lb       -->
    <!-- elements within ab                         -->
    <!-- ========================================== -->
    <xsl:template match="tei:ab" mode="interp">
        <div class="ab-content">
            <xsl:apply-templates select=".//tei:lb[1]" mode="line-start"/>
        </div>
    </xsl:template>

    <xsl:template match="tei:lb" mode="line-start">
        <span class="line" n="{@n}">
            <xsl:variable name="lineContent">
                <xsl:apply-templates
                    select="following-sibling::node()[not(self::tei:lb) and count(preceding-sibling::tei:lb) = count(current()/preceding-sibling::tei:lb) + 1]"
                    mode="interp"/>
            </xsl:variable>

            <xsl:copy-of select="$lineContent"/>

            <!-- Add line-break marker if next line continues the word -->
            <xsl:if test="following-sibling::tei:lb[1]/@break = 'no'">
                <xsl:text> =</xsl:text>
            </xsl:if>
        </span>
        <xsl:apply-templates select="following-sibling::tei:lb[1]" mode="line-start"/>
    </xsl:template>

    <!-- ========================================== -->
    <!-- BIBLIOGRAPHY RENDERING                     -->
    <!-- ========================================== -->
    <xsl:template match="tei:bibl" mode="bibliography">
        <xsl:element name="span">
            <xsl:attribute name="id">
                <xsl:value-of select="@xml:id"/>
            </xsl:attribute>

            <!-- Find ptr with 'references' in path and convert .xml to .html -->
            <xsl:variable name="ref-target"
                select="tei:ptr[contains(@target, 'references')]/@target"/>
            <xsl:variable name="html-target" select="replace($ref-target, '\.xml', '.html')"/>

            <xsl:element name="a">
                <xsl:attribute name="href">
                    <xsl:value-of select="$html-target"/>
                </xsl:attribute>

                <xsl:choose>
                    <xsl:when test="@type = 'corpus'">
                        <xsl:apply-templates select="tei:title"/>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:value-of select="tei:title"/>
                        <xsl:if test="tei:citedRange">, <xsl:value-of select="tei:citedRange"
                            /></xsl:if>
                        <xsl:if test="tei:note[@type = 'number']">, <xsl:value-of
                                select="tei:note[@type = 'number']"/></xsl:if>. </xsl:otherwise>
                </xsl:choose>
            </xsl:element>
        </xsl:element>
    </xsl:template>

    <xsl:template match="tei:bibl[@type = 'database']" mode="bibliography_database">
        <dl>
            <xsl:element name="dt">
                <xsl:attribute name="id">
                    <xsl:value-of select="@xml:id"/>
                </xsl:attribute>
                EDR
            </xsl:element>
            <dd>
                <h5>
                    <xsl:apply-templates select="tei:title"/>
                </h5>
            </dd>
            <xsl:if test="tei:author">
                <dt>Author of the record:</dt>
                <dd>
                    <xsl:value-of select="tei:author"/>
                </dd>
            </xsl:if>
            <xsl:if test="tei:date">
                <dt>Date:</dt>
                <dd>
                    <xsl:value-of select="tei:date"/>
                </dd>
            </xsl:if>
        </dl>
    </xsl:template>

    <!-- ========================================== -->
    <!-- KRUMMREY-PANCIERA DIACRITICS (mode="interp") -->
    <!-- Convert TEI markup to Leiden conventions   -->
    <!-- for epigraphic transcription               -->
    <!-- ========================================== -->

    <!-- Ligature: add combining circumflex between letters -->
    <xsl:template match="tei:hi[@rend = 'ligature']" mode="interp">
        <xsl:for-each select="text()">
            <xsl:variable name="text" select="."/>
            <xsl:analyze-string select="$text" regex=".">
                <xsl:matching-substring>
                    <xsl:value-of select="."/>
                    <xsl:variable name="pos" select="position()"/>
                    <xsl:variable name="nextChar" select="substring($text, $pos + 1, 1)"/>
                    <xsl:if
                        test=". != ' ' and $nextChar != '' and $nextChar != ' ' and $nextChar != '('">
                        <xsl:text>&#x0302;</xsl:text>
                    </xsl:if>
                </xsl:matching-substring>
            </xsl:analyze-string>
        </xsl:for-each>
        <xsl:apply-templates select="*" mode="interp"/>
    </xsl:template>

    <!-- Regularization: show original with (!) marker -->
    <xsl:template match="tei:choice[tei:reg and tei:orig]" mode="interp">
        <xsl:apply-templates select="tei:orig" mode="interp"/>

        <xsl:variable name="currentChoice" select="."/>
        <xsl:variable name="nextLb" select="following::tei:lb[1]"/>

        <xsl:variable name="textBetween"
            select="following::text()[. &gt;&gt; $currentChoice and . &lt;&lt; $nextLb]"/>

        <xsl:variable name="isWordBroken"
            select="$nextLb/@break = 'no' and normalize-space(string-join($textBetween, '')) = ''"/>

        <xsl:if test="not($isWordBroken)">
            <xsl:text> (!)</xsl:text>
        </xsl:if>
    </xsl:template>

    <!-- Handle (!) marker placement for line-broken regularizations -->
    <xsl:template match="text()[preceding::*[1][self::tei:lb[@break = 'no']]]" mode="interp"
        priority="10">
        <xsl:variable name="prevLb" select="preceding::tei:lb[1]"/>
        <xsl:variable name="isFirstTextAfterLb"
            select="generate-id(.) = generate-id($prevLb/following::text()[1])"/>

        <xsl:choose>
            <xsl:when test="$isFirstTextAfterLb">
                <xsl:variable name="lastElemBefore"
                    select="$prevLb/preceding::*[not(self::tei:reg) and not(self::tei:sic)][1]"/>
                <xsl:variable name="textInBetween"
                    select="$lastElemBefore/following::text()[. &lt;&lt; $prevLb]"/>
                <xsl:variable name="isBrokenChoice"
                    select="$lastElemBefore/ancestor-or-self::tei:choice[tei:reg and tei:orig] and normalize-space(string-join($textInBetween, '')) = ''"/>

                <xsl:variable name="trimmed" select="normalize-space(.)"/>

                <xsl:choose>
                    <xsl:when test="$isBrokenChoice">
                        <xsl:choose>
                            <xsl:when test="contains($trimmed, ' ')">
                                <xsl:value-of select="substring-before($trimmed, ' ')"/>
                                <xsl:text> (!)</xsl:text>
                                <xsl:text> </xsl:text>
                                <xsl:value-of select="substring-after($trimmed, ' ')"/>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:value-of select="$trimmed"/>
                                <xsl:text> (!)</xsl:text>
                            </xsl:otherwise>
                        </xsl:choose>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:value-of select="."/>
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="."/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <!-- Unclear letters: add combining dot below -->
    <xsl:template match="tei:unclear" mode="interp">
        <xsl:analyze-string select="string(.)" regex=".">
            <xsl:matching-substring>
                <xsl:value-of select="."/>
                <xsl:text>&#x0323;</xsl:text>
            </xsl:matching-substring>
        </xsl:analyze-string>
    </xsl:template>

    <!-- Abbreviation expansion: (text) -->
    <xsl:template match="tei:ex" mode="interp">
        <xsl:text>(</xsl:text>
        <xsl:apply-templates mode="interp"/>
        <xsl:if test="@cert = 'low'">
            <xsl:text>?</xsl:text>
        </xsl:if>
        <xsl:text>)</xsl:text>
    </xsl:template>

    <!-- Supplied text (omitted): <text> -->
    <xsl:template match="tei:supplied[@reason = 'omitted']" mode="interp">
        <xsl:text>&lt;</xsl:text>
        <xsl:apply-templates mode="interp"/>
        <xsl:text>&gt;</xsl:text>
    </xsl:template>

    <!-- Supplied text from previous editor: underline with source tooltip -->
    <xsl:template match="tei:supplied[@reason = 'lost'][@evidence = 'previouseditor']" mode="interp">
        <u style="cursor: help;">
            <xsl:attribute name="title">
                <xsl:text>Source(s): </xsl:text>
                <xsl:variable name="context" select="/"/>
                <xsl:for-each select="tokenize(normalize-space(@source), '\s+')">
                    <xsl:variable name="id" select="substring-after(., '#')"/>
                    <xsl:value-of select="$context//tei:bibl[@xml:id = $id]/tei:title"/>
                    <xsl:if test="position() != last()">
                        <xsl:text>, </xsl:text>
                    </xsl:if>
                </xsl:for-each>
            </xsl:attribute>

            <xsl:apply-templates mode="interp"/>
        </u>
    </xsl:template>

    <!-- Surplus text: {text} -->
    <xsl:template match="tei:surplus" mode="interp">
        <xsl:text>{</xsl:text>
        <xsl:apply-templates mode="interp"/>
        <xsl:text>}</xsl:text>
    </xsl:template>

    <!-- Editorial correction: ⸢text⸣ -->
    <xsl:template match="tei:choice[tei:corr and tei:sic]" mode="interp">
        <xsl:text>⸢</xsl:text>
        <xsl:apply-templates select="tei:corr" mode="interp"/>
        <xsl:text>⸣</xsl:text>
    </xsl:template>

    <!-- Symbols and glyphs -->
    <xsl:template match="tei:g" mode="interp">
        <xsl:choose>
            <xsl:when test="@ref = '#chi-rho'">☧</xsl:when>
            <xsl:when test="@ref = '#cross'">†</xsl:when>
            <xsl:when test="@ref = '#hedera'">❧</xsl:when>
            <xsl:otherwise>[<xsl:value-of select="substring-after(@ref, '#')"/>]</xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <!-- ========================================== -->
    <!-- INTERACTIVE REFERENCES                     -->
    <!-- Link words to apparatus and persons        -->
    <!-- ========================================== -->

    <!-- Word with both apparatus and person reference: create dropdown -->
    <xsl:template match="tei:w[@xml:id][ancestor::tei:persName[@ref]]" mode="interp">
        <span class="dropdown dual-reference">
            <button class="dropbtn word-with-refs">
                <xsl:apply-templates mode="interp"/>
            </button>
            <div class="dropdown-content">
                <a href="#{@xml:id}">→ Apparatus</a>
                <a href="{ancestor::tei:persName[@ref][1]/@ref}">→ Person</a>
            </div>
        </span>
    </xsl:template>

    <!-- Person name without apparatus reference: simple link -->
    <xsl:template match="tei:persName[@ref][not(.//tei:w[@xml:id])]" mode="interp">
        <a class="person_reference" href="{@ref}">
            <xsl:apply-templates mode="interp"/>
        </a>
    </xsl:template>

    <!-- Person name containing apparatus reference: pass through to child w -->
    <xsl:template match="tei:persName[@ref][.//tei:w[@xml:id]]" mode="interp">
        <xsl:apply-templates mode="interp"/>
    </xsl:template>

    <!-- Word with apparatus reference only: simple link -->
    <xsl:template match="tei:w[@xml:id][not(ancestor::tei:persName[@ref])]" mode="interp">
        <a class="apparatus_reference" href="#{@xml:id}">
            <xsl:apply-templates mode="interp"/>
        </a>
    </xsl:template>

    <!-- Suppress reg and sic in interpretive mode -->
    <xsl:template match="tei:reg | tei:sic" mode="interp"/>

    <!-- Default text handling in interpretive mode -->
    <xsl:template match="text()" mode="interp" priority="1">
        <xsl:value-of select="."/>
    </xsl:template>

    <!-- Default element handling in interpretive mode -->
    <xsl:template match="*" mode="interp">
        <xsl:apply-templates mode="interp"/>
    </xsl:template>

    <!-- Gap in text -->
    <xsl:template match="tei:gap[@reason = 'lost']" mode="interp">
        <xsl:choose>
            <xsl:when test="@extent = 'unknown' and @unit = 'character'">[---]</xsl:when>
            <xsl:when test="@extent = 'unknown' and @unit = 'line'">- - - - - -</xsl:when>
            <xsl:otherwise> </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <!-- ========================================== -->
    <!-- APPARATUS CRITICUS RENDERING               -->
    <!-- Converts to uppercase with u→v             -->
    <!-- ========================================== -->

    <!-- Convert text to uppercase and u→v for apparatus -->
    <xsl:template match="text()" mode="apparatus" priority="1">
        <xsl:value-of select="upper-case(translate(., 'u', 'v'))"/>
    </xsl:template>

    <!-- Abbreviation expansion in apparatus -->
    <xsl:template match="tei:ex" mode="apparatus">
        <xsl:text>(</xsl:text>
        <xsl:apply-templates mode="apparatus"/>
        <xsl:if test="@cert = 'low'">
            <xsl:text>?</xsl:text>
        </xsl:if>
        <xsl:text>)</xsl:text>
    </xsl:template>

    <!-- Abbreviation in apparatus -->
    <xsl:template match="tei:abbr" mode="apparatus">
        <xsl:apply-templates mode="apparatus"/>
    </xsl:template>

    <!-- Expansion in apparatus -->
    <xsl:template match="tei:expan" mode="apparatus">
        <xsl:apply-templates mode="apparatus"/>
    </xsl:template>

    <!-- Supplied text (lost) in apparatus -->
    <xsl:template match="tei:supplied[@reason = 'lost']" mode="apparatus">
        <xsl:text>[</xsl:text>
        <xsl:apply-templates mode="apparatus"/>
        <xsl:text>]</xsl:text>
    </xsl:template>

    <!-- Supplied text (omitted) in apparatus -->
    <xsl:template match="tei:supplied[@reason = 'omitted']" mode="apparatus">
        <xsl:text>&lt;</xsl:text>
        <xsl:apply-templates mode="apparatus"/>
        <xsl:text>&gt;</xsl:text>
    </xsl:template>

    <!-- Surplus text in apparatus -->
    <xsl:template match="tei:surplus" mode="apparatus">
        <xsl:text>{</xsl:text>
        <xsl:apply-templates mode="apparatus"/>
        <xsl:text>}</xsl:text>
    </xsl:template>

    <!-- Editorial correction in apparatus -->
    <xsl:template match="tei:choice[tei:corr and tei:sic]" mode="apparatus">
        <xsl:text>⸢</xsl:text>
        <xsl:apply-templates select="tei:corr" mode="apparatus"/>
        <xsl:text>⸣</xsl:text>
    </xsl:template>

    <!-- Regularization in apparatus: show original -->
    <xsl:template match="tei:choice[tei:reg and tei:orig]" mode="apparatus">
        <xsl:apply-templates select="tei:orig" mode="apparatus"/>
    </xsl:template>

    <!-- Ligature in apparatus: add combining circumflex between letters -->
    <xsl:template match="tei:hi[@rend = 'ligature']" mode="apparatus">
        <xsl:for-each select="text()">
            <xsl:variable name="text" select="."/>
            <xsl:analyze-string select="$text" regex=".">
                <xsl:matching-substring>
                    <xsl:value-of select="upper-case(translate(., 'u', 'v'))"/>
                    <xsl:variable name="pos" select="position()"/>
                    <xsl:variable name="nextChar" select="substring($text, $pos + 1, 1)"/>
                    <xsl:if
                        test=". != ' ' and $nextChar != '' and $nextChar != ' ' and $nextChar != '('">
                        <xsl:text>&#x0302;</xsl:text>
                    </xsl:if>
                </xsl:matching-substring>
            </xsl:analyze-string>
        </xsl:for-each>
        <xsl:apply-templates select="*" mode="apparatus"/>
    </xsl:template>

    <!-- Symbols and glyphs in apparatus -->
    <xsl:template match="tei:g" mode="apparatus">
        <xsl:choose>
            <xsl:when test="@ref = '#chi-rho'">☧</xsl:when>
            <xsl:when test="@ref = '#cross'">†</xsl:when>
            <xsl:when test="@ref = '#hedera'">❧</xsl:when>
            <xsl:otherwise>[<xsl:value-of select="upper-case(substring-after(@ref, '#'))"
                />]</xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <!-- Gap in apparatus -->
    <xsl:template match="tei:gap[@reason = 'lost']" mode="apparatus">
        <xsl:choose>
            <xsl:when test="@extent = 'unknown' and @unit = 'character'">[---]</xsl:when>
            <xsl:when test="@extent = 'unknown' and @unit = 'line'">- - - - - -</xsl:when>
            <xsl:otherwise> </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <!-- Suppress reg and sic in apparatus mode (but NOT corr) -->
    <xsl:template match="tei:reg | tei:sic" mode="apparatus"/>

    <!-- Default element handling in apparatus mode -->
    <xsl:template match="*" mode="apparatus">
        <xsl:apply-templates mode="apparatus"/>
    </xsl:template>

    <!-- ========================================== -->
    <!-- TEXT STYLING                               -->
    <!-- ========================================== -->

    <!-- Italicize Latin terms outside edition -->
    <xsl:template match="tei:term[@xml:lang = 'la'][not(ancestor::tei:div[@type = 'edition'])]">
        <em>
            <xsl:apply-templates/>
        </em>
    </xsl:template>

    <!-- Bold Palmyrene letters outside edition -->
    <xsl:template match="tei:g[@xml:type = 'pl'][not(ancestor::tei:div[@type = 'edition'])]">
        <strong>
            <xsl:apply-templates/>
        </strong>
    </xsl:template>

</xsl:stylesheet>
