<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:tei="http://www.tei-c.org/ns/1.0" xmlns="http://www.w3.org/1999/xhtml"
    xmlns:xs="http://www.w3.org/2001/XMLSchema" exclude-result-prefixes="tei xs" version="2.0">
    
    <xsl:output method="xml" indent="yes" encoding="UTF-8"/>
    
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
                    <p><strong>City:</strong> <xsl:apply-templates select="//tei:history//tei:origPlace/tei:settlement/tei:placeName[@type = 'modern']"/></p>
                    <p><strong>Ancient city:</strong> <i><xsl:apply-templates select="//tei:history//tei:origPlace/tei:settlement/tei:placeName[@type = 'ancient']"/></i></p>
                    <p><strong>Date:</strong> <xsl:apply-templates select="//tei:history//tei:origDate[@xml:lang = 'en']"/></p>
                </div>
                
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
                
                <xsl:apply-templates select="//tei:facsimile/tei:graphic"/>
                
                <div class="people">
                    <h2>People</h2>
                    <xsl:for-each select="//tei:listPerson/tei:person">
                        <h3><xsl:value-of select="tei:persName/tei:name[@type = 'full']"/></h3>
                        <ul>
                            <li><strong>Gender:</strong> 
                                <xsl:choose>
                                    <xsl:when test="tei:gender = 'm'">male</xsl:when>
                                    <xsl:when test="tei:gender = 'f'">female</xsl:when>
                                    <xsl:otherwise>unknown</xsl:otherwise>
                                </xsl:choose>
                            </li>
                            <xsl:for-each select="tei:note">
                                <li><strong><xsl:value-of select="@type"/>:</strong> <xsl:text> </xsl:text><xsl:value-of select="."/>
                                    <xsl:if test="@type = 'relationship' and @corresp">
                                        <xsl:text> (→ </xsl:text>
                                        <xsl:value-of select="normalize-space(//tei:person[@xml:id = substring-after(current()/@corresp, '#')]/tei:persName/tei:name[@type = 'full'])"/>
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
    
    <xsl:template match="tei:div[@type = 'textpart']">
        <xsl:element name="{if (count(ancestor::tei:div[@type='textpart']) > 0) then 'h5' else 'h4'}">
            <xsl:choose>
                <xsl:when test="@subtype"><xsl:value-of select="upper-case(replace(@subtype, '_', ' '))"/></xsl:when>
                <xsl:when test="@source"><xsl:value-of select="upper-case(replace(@source, '_', ' '))"/></xsl:when>
                <xsl:otherwise>PART <xsl:value-of select="@n"/></xsl:otherwise>
            </xsl:choose>
            <xsl:text>:</xsl:text>
        </xsl:element>
        
        <div class="textpart" data-location="{(@subtype, @source)[1]}">
            <xsl:apply-templates select="tei:div[@type = 'textpart']"/>
            <xsl:apply-templates select="tei:ab" mode="interp"/>
        </div>
    </xsl:template>
    
    <xsl:template match="tei:ref">
        <a href="{@target}"><xsl:apply-templates/></a>
    </xsl:template>
    
    <xsl:template match="tei:graphic">
        <figure>
            <img src="{@url}">
                <xsl:attribute name="alt"><xsl:value-of select="tei:desc[@type='alt']"/></xsl:attribute>
            </img>
            <xsl:apply-templates select="tei:desc[@type='figDesc']"/>
        </figure>
    </xsl:template>
    
    <xsl:template match="tei:desc[@type='figDesc']">
        <figcaption><xsl:apply-templates/></figcaption>
    </xsl:template>
    
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
            
            <xsl:copy-of select="$lineContent"/>
            
            <xsl:if test="following-sibling::tei:lb[1]/@break='no'">
                <xsl:text> =</xsl:text>
            </xsl:if>
        </span>
        <xsl:apply-templates select="following-sibling::tei:lb[1]" mode="line-start"/>
    </xsl:template>
    
    <xsl:template match="tei:hi[@rend = 'ligature']" mode="interp">
        <xsl:variable name="text" select="string(.)"/>
        <xsl:analyze-string select="$text" regex=".">
            <xsl:matching-substring>
                <xsl:value-of select="."/>
                <xsl:variable name="pos" select="position()"/>
                <xsl:variable name="nextChar" select="substring($text, $pos + 1, 1)"/>
                <xsl:if test=". != ' ' and $nextChar != '' and $nextChar != ' '">
                    <xsl:text>&#x0302;</xsl:text>
                </xsl:if>
            </xsl:matching-substring>
        </xsl:analyze-string>
    </xsl:template>
    
    <xsl:template match="tei:choice[tei:reg and tei:orig]" mode="interp">
        <xsl:apply-templates select="tei:orig" mode="interp"/>
        
        <xsl:variable name="currentChoice" select="."/>
        <xsl:variable name="nextLb" select="following::tei:lb[1]"/>
        
        <xsl:variable name="textBetween" select="following::text()[. &gt;&gt; $currentChoice and . &lt;&lt; $nextLb]"/>
        
        <xsl:variable name="isWordBroken" select="$nextLb/@break='no' and normalize-space(string-join($textBetween, '')) = ''"/>
        
        <xsl:if test="not($isWordBroken)">
            <xsl:text> (!)</xsl:text>
        </xsl:if>
    </xsl:template>
    
    <xsl:template match="text()[preceding::*[1][self::tei:lb[@break='no']]]" mode="interp" priority="10">
        <xsl:variable name="prevLb" select="preceding::tei:lb[1]"/>
        <xsl:variable name="isFirstTextAfterLb" select="generate-id(.) = generate-id($prevLb/following::text()[1])"/>
        
        <xsl:choose>
            <xsl:when test="$isFirstTextAfterLb">
                <xsl:variable name="lastElemBefore" select="$prevLb/preceding::*[not(self::tei:reg) and not(self::tei:sic)][1]"/>
                <xsl:variable name="textInBetween" select="$lastElemBefore/following::text()[. &lt;&lt; $prevLb]"/>
                <xsl:variable name="isBrokenChoice" select="$lastElemBefore/ancestor-or-self::tei:choice[tei:reg and tei:orig] and normalize-space(string-join($textInBetween, '')) = ''"/>
                
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
    
    <xsl:template match="tei:unclear" mode="interp">
        <xsl:analyze-string select="string(.)" regex=".">
            <xsl:matching-substring><xsl:value-of select="."/><xsl:text>&#x0323;</xsl:text></xsl:matching-substring>
        </xsl:analyze-string>
    </xsl:template>
    
    <xsl:template match="tei:ex" mode="interp">
        <xsl:text>(</xsl:text><xsl:apply-templates mode="interp"/><xsl:if test="@cert = 'low'"><xsl:text>?</xsl:text></xsl:if><xsl:text>)</xsl:text>
    </xsl:template>
    
    <xsl:template match="tei:supplied[@reason = 'omitted']" mode="interp">
        <xsl:text>&lt;</xsl:text><xsl:apply-templates mode="interp"/><xsl:text>&gt;</xsl:text>
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
    
    <xsl:template match="tei:surplus" mode="interp">
        <xsl:text>{</xsl:text><xsl:apply-templates mode="interp"/><xsl:text>}</xsl:text>
    </xsl:template>
    
    <xsl:template match="tei:choice[tei:corr and tei:sic]" mode="interp">
        <xsl:text>⸢</xsl:text>
        <xsl:apply-templates select="tei:corr" mode="interp"/>
        <xsl:text>⸣</xsl:text>
    </xsl:template>
    
    <xsl:template match="tei:g" mode="interp">
        <xsl:choose>
            <xsl:when test="@ref='#chi-rho'">☧</xsl:when>
            <xsl:when test="@ref='#cross'">†</xsl:when>
            <xsl:when test="@ref='#hedera'">❧</xsl:when>
            <xsl:otherwise>[<xsl:value-of select="substring-after(@ref, '#')"/>]</xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template match="tei:reg | tei:sic" mode="interp" />
    
    <xsl:template match="text()" mode="interp" priority="1">
        <xsl:value-of select="."/>
    </xsl:template>
    
    <xsl:template match="*" mode="interp">
        <xsl:apply-templates mode="interp"/>
    </xsl:template>
    
    <xsl:template match="tei:gap[@reason='lost']" mode="interp">
        <xsl:choose>
            <xsl:when test="@extent='unknown' and @unit='character'">[---]</xsl:when>
            <xsl:when test="@extent='unknown' and @unit='line'">- - - - - -</xsl:when>
            <xsl:otherwise> </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
</xsl:stylesheet>
