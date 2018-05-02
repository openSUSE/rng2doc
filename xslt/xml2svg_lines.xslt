<?xml version="1.0"?>
<xsl:stylesheet version="1.0" 
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:s="http://www.w3.org/2000/svg"
  xmlns="http://www.w3.org/2000/svg">

  <xsl:output
    method="xml"
    version="1.0"
    encoding="UTF-8"
    indent="yes"
    doctype-public="-//W3C//DTD SVG 1.1//EN"
    doctype-system="http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd"
    media-type="image/svg"/>

  <xsl:template match="/">
      <xsl:apply-templates select="/s:svg"/>
  </xsl:template>

  <xsl:template match="/s:svg">
    <xsl:copy>
      <xsl:copy-of select="@*"/>
      <xsl:apply-templates select="s:rect"/>
    </xsl:copy>
  </xsl:template>

  <xsl:template match="s:rect[@class = 'parent']">
    <xsl:copy-of select="."/>
    <xsl:copy-of select="./following-sibling::s:text[1]"/>
    <xsl:call-template name="children">
      <xsl:with-param name="number_of_children" select="count(//s:rect[@class = 'child'])"/>
      <xsl:with-param name="parent_x" select="@x + @width"/>
      <xsl:with-param name="parent_y" select="@y + (@height div 2)"/>
    </xsl:call-template>
  </xsl:template>

  <xsl:template name="children">
    <xsl:param name="number_of_children" select="1"/>
    <xsl:param name="parent_x"/>
    <xsl:param name="parent_y"/>
    
    <xsl:if test="$number_of_children > 0">
      <xsl:copy-of select="//s:rect[$number_of_children + 1]"/>
      <xsl:copy-of select="//s:text[$number_of_children + 1]"/>
      <xsl:call-template name="draw_line">
        <xsl:with-param name="x1_pos" select="$parent_x"/>
        <xsl:with-param name="y1_pos" select="$parent_y"/>
        <xsl:with-param name="x2_pos" select="//s:rect[$number_of_children + 1]/@x"/>
        <xsl:with-param name="y2_pos" select="//s:rect[$number_of_children + 1]/@y + (//s:rect[$number_of_children + 1]/@height div 2)"/>
      </xsl:call-template>
      <xsl:call-template name="children">
        <xsl:with-param name="number_of_children" select="$number_of_children - 1"/>
        <xsl:with-param name="parent_x" select="$parent_x"/>
        <xsl:with-param name="parent_y" select="$parent_y"/>
      </xsl:call-template>
    </xsl:if>
  </xsl:template>

  <xsl:template name="draw_line">
    <xsl:param name="x1_pos"/>
    <xsl:param name="y1_pos"/>
    <xsl:param name="x2_pos"/>
    <xsl:param name="y2_pos"/>
    <line x1="{$x1_pos}" y1="{$y1_pos}" x2="{$x2_pos}" y2="{$y2_pos}" stroke="black" stroke-width="1" />
  </xsl:template>

</xsl:stylesheet>
