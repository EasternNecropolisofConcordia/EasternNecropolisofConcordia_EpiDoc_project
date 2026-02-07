<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:tei="http://www.tei-c.org/ns/1.0" xmlns="http://www.w3.org/1999/xhtml"
    xmlns:xs="http://www.w3.org/2001/XMLSchema" exclude-result-prefixes="tei xs" version="2.0">
    
    <xsl:output method="xml" indent="yes" encoding="UTF-8"/>
    
    <!-- MAIN TEMPLATE -->
    <xsl:template match="/">
        <html xml:lang="en">
            <head>
                <title>CORPORA AND DATABASES</title>
                <meta charset="UTF-8"/>
            </head>
            <body>
                <div class="epigraphic_corpora">
                    <h2>EPIGRAPHIC CORPORA</h2>
                    <table>
                        <caption>Epigraphic Corpora</caption>
                        <xsl:apply-templates
                            select="//tei:listBibl[@type = 'epigraphic_corpora']/tei:bibl"
                            mode="corpora"/>
                    </table>
                </div>
                
                <div class="prosopographical_corpora">
                    <h2>PROSOPOGRAPHICAL CORPORA</h2>
                    <table>
                        <caption>Prosopographical Corpora</caption>
                        <xsl:apply-templates
                            select="//tei:listBibl[@type = 'prosopographical_corpora']/tei:bibl"
                            mode="corpora"/>
                    </table>
                </div>
                
                <div class="databases">
                    <h2>DIGITAL DATABASES</h2>
                    <table>
                        <caption>Digital Databases</caption>
                        <xsl:apply-templates
                            select="//tei:listBibl[@type = 'databases']/tei:bibl"
                            mode="databases"/>
                    </table>
                </div>
            </body>
        </html>
    </xsl:template>
    
    <!-- CORPORA -->
    <xsl:template match="tei:bibl" mode="corpora">
        <tr>
            <td>
                <xsl:attribute name="id">
                    <xsl:value-of select="@xml:id"/>
                </xsl:attribute>
                <strong>
                    <xsl:apply-templates select="tei:abbr"/>
                </strong>
            </td>
            <td>
                <xsl:if test="tei:author">
                    <xsl:for-each select="tei:author">
                        <xsl:value-of select="normalize-space(.)"/>
                        <xsl:if test="position() != last()">, </xsl:if>
                    </xsl:for-each>
                    <xsl:text> (ed.), </xsl:text>
                </xsl:if>
                <xsl:value-of select="tei:title"/>
                <xsl:text>, </xsl:text>
                <xsl:value-of select="concat(tei:pubPlace, ' ', tei:date)"/>
            </td>
        </tr>
    </xsl:template>
    
    <!-- DATABASES -->
    <xsl:template match="tei:bibl" mode="databases">
        <tr>
            <td>
                <xsl:attribute name="id">
                    <xsl:value-of select="@xml:id"/>
                </xsl:attribute>
                <strong>
                    <xsl:value-of select="tei:abbr"/>
                </strong>
            </td>
            <td>
                <xsl:value-of select="tei:title"/>
                <xsl:if test="tei:ref">
                    <xsl:text> - </xsl:text>
                    <a href="{tei:ref/@target}">
                        <xsl:value-of select="tei:ref/@target"/>
                    </a>
                </xsl:if>
            </td>
        </tr>
    </xsl:template>
    
    <!-- Latin Terms -->
    <xsl:template match="tei:term[@xml:lang='la']">
        <em>
            <xsl:apply-templates/>
        </em>
    </xsl:template>
    
    <xsl:template match="tei:hi[@rend='sup']">
        <sup>
            <xsl:apply-templates/>
        </sup>
    </xsl:template>
    
    <xsl:template match="text()" mode="corpora"/>
    <xsl:template match="text()" mode="databases"/>
    
</xsl:stylesheet>