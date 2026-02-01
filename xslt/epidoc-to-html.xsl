<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:tei="http://www.tei-c.org/ns/1.0" xmlns="http://www.w3.org/1999/xhtml"
    xmlns:xs="http://www.w3.org/2001/XMLSchema" exclude-result-prefixes="tei xs" version="2.0">

    <!-- Output XHTML -->
    <xsl:output method="xml" indent="yes" encoding="UTF-8"/>

    <!-- Template principale -->
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

                <div class="metadata">
                    <h2>Findspot</h2>
                    <p>
                        <strong>City:</strong>
                        <xsl:apply-templates
                            select="//tei:history//tei:origPlace/tei:settlement/tei:placeName[@type = 'modern']"
                        />
                    </p>
                    <p>
                        <strong>Ancient city:</strong>
                        <i>
                            <xsl:apply-templates
                                select="//tei:history//tei:origPlace/tei:settlement/tei:placeName[@type = 'ancient']"
                            />
                        </i>
                    </p>
                    <p>
                        <strong>Date:</strong>
                        <xsl:apply-templates select="//tei:history//tei:origDate[@xml:lang = 'en']"
                        />
                    </p>
                </div>

                <div class="inscription">
                    <h2>INSCRIPTION</h2>
                    <h3>TRANSCRIPTION</h3>
                    <xsl:for-each select="//tei:div[@type = 'edition']">
                        <div class="transcription" lang="la">
                            <xsl:choose>
                                <xsl:when test=".//tei:div[@type = 'textpart']">
                                    <xsl:for-each select=".//tei:div[@type = 'textpart']">
                                        <h4><xsl:value-of select="upper-case(./@source)"/>:</h4>
                                        <div class="textpart" source="{@source}">
                                            <xsl:apply-templates select="tei:ab" mode="interp"/>
                                        </div>
                                    </xsl:for-each>
                                </xsl:when>
                                <xsl:otherwise>
                                    <xsl:apply-templates select="tei:ab" mode="interp"/>
                                </xsl:otherwise>
                            </xsl:choose>
                        </div>
                    </xsl:for-each>
                </div>
                
                <xsl:apply-templates select="//tei:facsimile/tei:graphic"/>

                <div class="people">
                    <h2>People</h2>
                    <xsl:for-each select="//tei:listPerson/tei:person">
                        <h3>
                            <xsl:value-of select="tei:persName/tei:name[@type = 'full']"/>
                        </h3>

                        <ul>
                            <li>
                                <strong>Gender:</strong>
                                <xsl:choose>
                                    <xsl:when test="tei:gender = 'm'">male</xsl:when>
                                    <xsl:when test="tei:gender = 'f'">female</xsl:when>
                                    <xsl:otherwise>unknown</xsl:otherwise>
                                </xsl:choose>
                            </li>
                            <xsl:for-each select="tei:note">
                                <li>
                                    <strong><xsl:value-of select="@type"/>:</strong>
                                    <xsl:text> </xsl:text>
                                    <xsl:value-of select="."/>

                                    <!-- relazione opzionale -->
                                    <xsl:if test="@type = 'relationship' and @corresp">
                                        <xsl:text> (→ </xsl:text>
                                        <xsl:value-of
                                            select="normalize-space(//tei:person[@xml:id = substring-after(current()/@corresp, '#')]/tei:persName/tei:name[@type = 'full'])"/>
                                        <xsl:text>)</xsl:text>
                                    </xsl:if>
                                </li>
                            </xsl:for-each>
                        </ul>
                    </xsl:for-each>
                </div>
            </body>
        </html>
    </xsl:template>
    
    <!-- ========= -->
    <!-- TEMPLATES -->
    <!-- ========= -->

    <!-- ref -->
    <xsl:template match="tei:ref">
        <a href="{@target}">
            <xsl:apply-templates/>
        </a>
    </xsl:template>
    
    <!-- Image -->
    <xsl:template match="tei:graphic">
        <figure>
            <img src="{@url}">
                <xsl:attribute name="alt">
                    <xsl:value-of select="tei:desc[@type='alt']"/>
                </xsl:attribute>
            </img>
            
            <xsl:apply-templates select="tei:desc[@type='figDesc']"/>
        </figure>
    </xsl:template>
    
    <xsl:template match="tei:desc[@type='figDesc']">
        <figcaption>
            <xsl:apply-templates/>
        </figcaption>
    </xsl:template>

    <!-- ========================================== -->
    <!-- KRUMMREY-PANCIERA DIACRITICS (mode="interp") -->
    <!-- ========================================== -->

    <xsl:template match="tei:ab" mode="interp">
        <div class="ab-content">
            <xsl:apply-templates select=".//tei:lb[1]" mode="line-start"/>
        </div>
    </xsl:template>
    
    <xsl:template match="tei:lb" mode="line-start">
        <span class="line" n="{@n}">
            <xsl:variable name="lineContent">
                <xsl:apply-templates select="following-sibling::node()[not(self::tei:lb) and count(preceding-sibling::tei:lb) = count(current()/preceding-sibling::tei:lb) + 1]" mode="interp"/>
            </xsl:variable>
            
            <xsl:variable name="nextLb" select="following-sibling::tei:lb[1]"/>
            
            <xsl:choose>
                <xsl:when test="$nextLb/@break='no'">
                    <xsl:value-of select="replace($lineContent, '\s+$', '')"/>
                    <xsl:text>=</xsl:text>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:copy-of select="$lineContent"/>
                </xsl:otherwise>
            </xsl:choose>
        </span>
        <br/>
        <xsl:apply-templates select="following-sibling::tei:lb[1]" mode="line-start"/>
    </xsl:template>
    
    <xsl:template match="tei:orig[not(parent::tei:choice)]" mode="interp">
        <span style="text-transform: uppercase;">
            <xsl:apply-templates mode="interp"/>
        </span>
    </xsl:template>
    
    <xsl:template match="tei:unclear" mode="interp">
        <xsl:variable name="text" select="string(.)"/>
        <xsl:analyze-string select="$text" regex=".">
            <xsl:matching-substring>
                <xsl:value-of select="."/><xsl:text>&#x0323;</xsl:text>
            </xsl:matching-substring>
        </xsl:analyze-string>
    </xsl:template>
    
    <xsl:template match="tei:supplied[@reason = 'lost'][@evidence = 'previouseditor']" mode="interp">
        <u style="cursor: help;">
            <xsl:attribute name="title">
                <xsl:text>Source(s): </xsl:text>
                <xsl:variable name="context" select="/"/>
                <xsl:for-each select="tokenize(normalize-space(@corresp), '\s+')">
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
    
    <xsl:template match="tei:hi[@rend = 'apex']" mode="interp">
        <xsl:variable name="char" select="string(.)"/>
        <xsl:choose>
            <xsl:when test="$char = 'a'">á</xsl:when>
            <xsl:when test="$char = 'e'">é</xsl:when>
            <xsl:when test="$char = 'i'">í</xsl:when>
            <xsl:when test="$char = 'o'">ó</xsl:when>
            <xsl:when test="$char = 'u'">ú</xsl:when>
            <xsl:otherwise><xsl:value-of select="$char"/></xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template match="tei:hi[@rend = 'supraline']" mode="interp">
        <xsl:analyze-string select="string(.)" regex=".">
            <xsl:matching-substring>
                <xsl:value-of select="."/><xsl:text>&#x0304;</xsl:text>
            </xsl:matching-substring>
        </xsl:analyze-string>
    </xsl:template>
    
    <xsl:template match="tei:hi[@rend = 'ligature']" mode="interp">
        <xsl:for-each select="string-to-codepoints(string(.))">
            <xsl:value-of select="codepoints-to-string(.)"/>
            <xsl:if test="position() != last()"><xsl:text>&#x0302;</xsl:text></xsl:if>
        </xsl:for-each>
    </xsl:template>
    
    <xsl:template match="tei:del[@rend = 'erasure']" mode="interp">
        <xsl:text>⟦</xsl:text><xsl:apply-templates mode="interp"/><xsl:text>⟧</xsl:text>
    </xsl:template>
    
    <xsl:template match="tei:subst" mode="interp">
        <xsl:text>«</xsl:text><xsl:apply-templates select="tei:add[@place = 'overstrike']" mode="interp"/><xsl:text>»</xsl:text>
    </xsl:template>
    
    <xsl:template match="tei:add[@place = 'above'] | tei:add[@place = 'below']" mode="interp">
        <xsl:text>‵</xsl:text><xsl:apply-templates mode="interp"/><xsl:text>′</xsl:text>
    </xsl:template>
    
    <xsl:template match="tei:supplied[@reason = 'lost'][not(@evidence = 'previouseditor')]" mode="interp">
        <xsl:text>[</xsl:text>
        <xsl:apply-templates mode="interp"/>
        <xsl:if test="@cert = 'low'"><xsl:text>?</xsl:text></xsl:if>
        <xsl:text>]</xsl:text>
    </xsl:template>
    
    <xsl:template match="tei:gap[@reason = 'lost'][@unit = 'character'][@quantity]" mode="interp">
        <xsl:text>[</xsl:text>
        <xsl:for-each select="1 to xs:integer(@quantity)"><xsl:text>·</xsl:text></xsl:for-each>
        <xsl:text>]</xsl:text>
    </xsl:template>
    
    <xsl:template match="tei:gap[@reason = 'lost'][@unit = 'character'][@extent = 'unknown']" mode="interp">
        <xsl:text>[---]</xsl:text>
    </xsl:template>
    
    <xsl:template match="tei:gap[@reason = 'illegible'][@unit = 'character']" mode="interp">
        <xsl:choose>
            <xsl:when test="@quantity">
                <xsl:text>[</xsl:text><xsl:for-each select="1 to xs:integer(@quantity)"><xsl:text>·</xsl:text></xsl:for-each><xsl:text>]</xsl:text>
            </xsl:when>
            <xsl:otherwise><xsl:text>[---]</xsl:text></xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template match="tei:surplus" mode="interp">
        <xsl:text>{</xsl:text><xsl:apply-templates mode="interp"/><xsl:text>}</xsl:text>
    </xsl:template>
    
    <xsl:template match="tei:supplied[@reason = 'omitted']" mode="interp">
        <xsl:text>&lt;</xsl:text><xsl:apply-templates mode="interp"/><xsl:text>&gt;</xsl:text>
    </xsl:template>
    
    <xsl:template match="tei:choice[tei:corr and tei:sic]" mode="interp">
        <xsl:text>⸢</xsl:text>
        <xsl:apply-templates select="tei:corr" mode="interp"/>
        <xsl:text>⸣</xsl:text>
    </xsl:template>
    
    <xsl:template match="tei:expan" mode="interp">
        <xsl:apply-templates mode="interp"/>
        <xsl:if test="ancestor::tei:orig or ancestor::tei:sic">
            <xsl:text> (!)</xsl:text>
        </xsl:if>
    </xsl:template>
    
    <xsl:template match="tei:ex" mode="interp">
        <xsl:text>(</xsl:text>
        <xsl:apply-templates mode="interp"/>
        <xsl:if test="@cert = 'low'"><xsl:text>?</xsl:text></xsl:if>
        <xsl:text>)</xsl:text>
    </xsl:template>
    
    <xsl:template match="tei:choice[tei:reg and tei:orig]" mode="interp">
        <xsl:apply-templates select="tei:orig" mode="interp"/>
        <xsl:if test="not(tei:orig//tei:expan)">
            <xsl:text> (!)</xsl:text>
        </xsl:if>
    </xsl:template>
    
    <xsl:template match="tei:reg | tei:sic" mode="interp" />
    
    <xsl:template match="text()" mode="interp">
        <xsl:value-of select="."/>
    </xsl:template>
    
    <xsl:template match="*" mode="interp">
        <xsl:apply-templates mode="interp"/>
    </xsl:template>

</xsl:stylesheet>
