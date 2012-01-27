<?xml version='1.0'?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns="http://www.w3.org/1999/xhtml"
  xmlns:xhtml="http://www.w3.org/1999/xhtml"
  exclude-result-prefixes="xhtml xsl">

<xsl:output method="xml" version="1.0" encoding="UTF-8"
doctype-public="-//W3C//DTD XHTML 1.0 Strict//EN" 
doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd" indent="yes"/>

<!--<xsl:output method='html' version='1.0' encoding='UTF-8' indent='yes'/>
-->


<xsl:template match="*">
  <xsl:copy>
    <xsl:apply-templates select="@*" />
    <xsl:apply-templates />
  </xsl:copy>
</xsl:template>


<xsl:template match="@*">
  <xsl:copy-of select="." />
</xsl:template>


<xsl:template match="xhtml:tbody">
	<tbody>
	<xsl:apply-templates select="xhtml:tr">
		<xsl:sort select="substring-after(substring-after(xhtml:td[@headers='c2']/text(),' '),' ')"/>
	</xsl:apply-templates>
	</tbody>
</xsl:template>

<xsl:template match="xhtml:tr">
   <tr>
    <xsl:if test="position() mod 2 = 0">
        <xsl:attribute name="class">
           alternate
        </xsl:attribute>
    </xsl:if>
    <xsl:apply-templates/>
   </tr>
</xsl:template>

<xsl:template match="xhtml:th[@abbr='Prof']">
	<th id="c2" abbr="Prof" scope="col">Docente</th>
</xsl:template>

</xsl:stylesheet> 
