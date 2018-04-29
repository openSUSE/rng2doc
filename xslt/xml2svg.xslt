<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" 
  xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

  <xsl:output method="xml" version="1.0" encoding="UTF-8" indent="yes" doctype-public="-//W3C//DTD SVG 1.0/EN" doctype-system="http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd"/>

  <xsl:template match="element">
    <svg>
      <g id="layer1">
      <xsl:variable name="size_of_rect" select="11 * string-length(@name)"/>
      <xsl:call-template name="draw_element">
        <xsl:with-param name="name" select="@name"/>
        <xsl:with-param name="size" select="$size_of_rect"/>
        <xsl:with-param name="x_pos" select="25"/>
        <xsl:with-param name="y_pos" select="(count(child) * 40) div 2"/>
      </xsl:call-template>
      <xsl:call-template name="children">
        <xsl:with-param name="max_height" select="count(child)*40"/>
        <xsl:with-param name="max_length" select="$size_of_rect + 40"/>
      </xsl:call-template>
      </g>
    </svg>
  </xsl:template>

  <xsl:template name="children">
    <xsl:param name="max_height" select="1"/>
    <xsl:param name="max_length"/>
    <xsl:variable name="index" select="$max_height div 40"/>
 
    <xsl:if test="$max_height > 0">
      <xsl:call-template name="draw_element">
        <xsl:with-param name="name" select="child[$index]/@id"/>
        <xsl:with-param name="x_pos" select="$max_length"/>
        <xsl:with-param name="y_pos" select="$max_height"/>
        <xsl:with-param name="size" select="11 * string-length(child[$index]/@id)"/>
      </xsl:call-template>     
      <xsl:call-template name="children">
        <xsl:with-param name="max_height" select="$max_height - 40"/>
        <xsl:with-param name="max_length" select="$max_length"/>
      </xsl:call-template>
    </xsl:if>
  </xsl:template>

  <xsl:template name="draw_element">
    <xsl:param name="name"/>
    <xsl:param name="size"/>
    <xsl:param name="x_pos"/>
    <xsl:param name="y_pos"/>
    <xsl:variable name="x_pos_text" select="$x_pos+10"/>
    <xsl:variable name="y_pos_text" select="$y_pos+18"/>
    <rect
       style="fill:green"
       id="{$name}"
       width="{$size}"
       height="30"
       x="{$x_pos}"
       y="{$y_pos}"
       rx="15"
       ry="15" />
    <text
       x="{$x_pos_text}"
       y="{$y_pos_text}"
       font-family="Consolas,monaco,monospace;"
       font-size="11"
       id="text_{$name}"><xsl:value-of select="$name"/></text>
  </xsl:template>

  </xsl:stylesheet>
