<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:tei="http://www.tei-c.org/ns/1.0" xmlns="http://www.w3.org/1999/xhtml"
    xmlns:xs="http://www.w3.org/2001/XMLSchema" exclude-result-prefixes="tei xs" version="2.0">
    
    <xsl:output method="xml" indent="yes" encoding="UTF-8"/>
    
    <!-- MAIN TEMPLATE -->
    <xsl:template match="/">
        <html xml:lang="en">
            <head>
                <title>BIBLIOGRAPHY</title>
                <meta charset="UTF-8"/>
            </head>
            <body>
                <h2>BIBLIOGRAPHY</h2>
                <div class="bibliography">
                    <!-- Seleziona solo i bibl DIRETTI figli di listBibl[@type='bibliography'], escludendo quelli nei listBibl annidati -->
                    <xsl:apply-templates select="//tei:listBibl[@type='bibliography']/tei:bibl | //tei:listBibl[@type='bibliography']/tei:listBibl/tei:bibl[not(parent::tei:listBibl[@type='epigraphic_corpora' or @type='prosopographical_corpora' or @type='databases'])]" mode="bibliography"/>
                </div>
            </body>
        </html>
    </xsl:template>
    
    <!-- BIBLIOGRAPHY -->
    <xsl:template match="tei:bibl" mode="bibliography">
        <div class="biblio-item">
            <xsl:attribute name="id">
                <xsl:value-of select="@xml:id"/>
            </xsl:attribute>
            <dl>
                <dt>
                    <strong>Author</strong>
                </dt>
                <dd>
                    <xsl:choose>
                        <xsl:when test="tei:author//tei:surname">
                            <xsl:for-each select="tei:author">
                                <xsl:value-of select=".//tei:surname"/>
                                <xsl:if test=".//tei:forename">
                                    <xsl:text>, </xsl:text>
                                    <xsl:value-of select=".//tei:forename"/>
                                </xsl:if>
                                <xsl:if test="position() != last()">; </xsl:if>
                            </xsl:for-each>
                        </xsl:when>
                        <xsl:otherwise>unknown</xsl:otherwise>
                    </xsl:choose>
                </dd>
                
                <xsl:if test="tei:date">
                    <dt>
                        <strong>Year</strong>
                    </dt>
                    <dd>
                        <xsl:apply-templates select="tei:date" mode="bibliography"/>
                    </dd>
                </xsl:if>
                
                <dt>
                    <strong>Title</strong>
                </dt>
                <dd>
                    <xsl:choose>
                        <xsl:when test="tei:title[@level='a']">
                            <xsl:apply-templates select="tei:title[@level='a']" mode="bibliography"/>
                        </xsl:when>
                        <xsl:otherwise>
                            <xsl:apply-templates select="tei:title[1]" mode="bibliography"/>
                        </xsl:otherwise>
                    </xsl:choose>
                </dd>
                
                <xsl:if test="tei:title[@level='j']">
                    <dt>Journal</dt>
                    <dd><xsl:apply-templates select="tei:title[@level='j']" mode="bibliography"/></dd>
                </xsl:if>
                
                <xsl:if test="tei:pubPlace">
                    <dt>Place</dt>
                    <dd><xsl:value-of select="tei:pubPlace"/></dd>
                </xsl:if>
                
                <xsl:if test="tei:publisher">
                    <dt>Publisher</dt>
                    <dd><xsl:value-of select="tei:publisher"/></dd>
                </xsl:if>
                
                <xsl:if test="tei:biblScope">
                    <dt>Pages</dt>
                    <dd><xsl:value-of select="tei:biblScope"/></dd>
                </xsl:if>
            </dl>
        </div>
    </xsl:template>
    
    <!-- Latin Terms in bibliography mode -->
    <xsl:template match="tei:term[@xml:lang='la']" mode="bibliography">
        <em>
            <xsl:apply-templates mode="bibliography"/>
        </em>
    </xsl:template>
    
    <!-- Superscript in bibliography mode -->
    <xsl:template match="tei:hi[@rend='sup']" mode="bibliography">
        <sup>
            <xsl:apply-templates mode="bibliography"/>
        </sup>
    </xsl:template>
    
</xsl:stylesheet>