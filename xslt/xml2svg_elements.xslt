<?xml version="1.0"?>
<xsl:stylesheet version="1.0" 
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
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
    <xsl:call-template name="transform_element_to_svg">
      <xsl:with-param name="element" select="//element[1]"/>
    </xsl:call-template>
  </xsl:template>

  <xsl:template name="transform_element_to_svg">
    <xsl:param name="element"/>
    <xsl:variable name="margin" select="40"/>
    <xsl:variable name="spacer_vertical" select="30"/>
    <xsl:variable name="spacer_horicontal" select="60"/>
    <xsl:variable name="font_size" select="12"/>
    <xsl:variable name="width_element" select="($font_size - 2) * string-length($element/@name)"/>
    <xsl:variable name="height_element" select="30"/>

    <xsl:variable name="number_of_children" select="count($element/child)"/>

    <xsl:variable name="max_string_length_children">
      <xsl:for-each select="$element/child/@id">
        <xsl:sort select="string-length(//element[@id = current()]/@name)" data-type="number" />
        <xsl:if test="position() = last()">
          <xsl:value-of select="string-length(//element[@id = current()]/@name)" />
        </xsl:if>
      </xsl:for-each>
    </xsl:variable>

    <xsl:variable name="width_svg" select="$margin + $width_element + $spacer_horicontal + ($max_string_length_children * ($font_size -2)) + $margin"/>
    <xsl:variable name="height_svg" select="($number_of_children * ($height_element + $spacer_vertical)) + $spacer_vertical"/> 
    <svg xmlns="http://www.w3.org/2000/svg" 
      width="{$width_svg}" height="{$height_svg}">

      <xsl:choose>
        <xsl:when test="$number_of_children mod 2 = 0">
          <xsl:call-template name="draw_element">
            <xsl:with-param name="name" select="$element/@name"/>
            <xsl:with-param name="id" select="$element/@id"/>
            <xsl:with-param name="class" select="'parent'"/>
            <xsl:with-param name="width" select="$width_element"/>
            <xsl:with-param name="height" select="$height_element"/>
            <xsl:with-param name="x_pos" select="$margin"/>
            <xsl:with-param name="y_pos" select="(($number_of_children div 2) * ($height_element + $spacer_vertical))"/>
          </xsl:call-template>
          <xsl:call-template name="children">
            <xsl:with-param name="y_pos" select="$height_svg - $spacer_vertical"/>
            <xsl:with-param name="x_pos" select="$width_element + $spacer_horicontal * 2"/>
            <xsl:with-param name="x_pos_parent" select="$margin + $width_element "/>
            <xsl:with-param name="y_pos_parent" select="(($number_of_children div 2) * ($height_element + $spacer_vertical)) + ($height_element div 2)"/>
            <xsl:with-param name="spacer" select="$height_element + $spacer_vertical"/>
            <xsl:with-param name="height_element" select="$height_element"/>
            <xsl:with-param name="font_size" select="$font_size"/>
            <xsl:with-param name="element" select="$element"/>
          </xsl:call-template>
        </xsl:when>
        <xsl:otherwise>
          <xsl:call-template name="draw_element">
            <xsl:with-param name="name" select="$element/@name"/>
            <xsl:with-param name="id" select="$element/@id"/>
            <xsl:with-param name="class" select="'parent'"/>
            <xsl:with-param name="width" select="$width_element"/>
            <xsl:with-param name="height" select="$height_element"/>
            <xsl:with-param name="x_pos" select="$margin"/>
            <xsl:with-param name="y_pos" select="(ceiling($number_of_children div 2) * $spacer_vertical) + ((ceiling($number_of_children div 2) - 1) * $height_element)"/>
          </xsl:call-template>
          <xsl:call-template name="children">
            <xsl:with-param name="y_pos" select="$height_svg - $spacer_vertical"/>
            <xsl:with-param name="x_pos" select="$width_element + $spacer_horicontal * 2"/>
            <xsl:with-param name="x_pos_parent" select="$margin + $width_element "/>
            <xsl:with-param name="y_pos_parent" select="((ceiling($number_of_children div 2) * $spacer_vertical) + ((ceiling($number_of_children div 2) - 1) * $height_element)) + ($height_element div 2)"/>
            <xsl:with-param name="spacer" select="$height_element + $spacer_vertical"/>
            <xsl:with-param name="height_element" select="$height_element"/>
            <xsl:with-param name="font_size" select="$font_size"/>
            <xsl:with-param name="element" select="$element"/>
          </xsl:call-template>  
        </xsl:otherwise>
      </xsl:choose>



    </svg>
  </xsl:template>


  <xsl:template name="children">
    <xsl:param name="y_pos" select="1"/>
    <xsl:param name="x_pos"/>
    <xsl:param name="x_pos_parent"/>
    <xsl:param name="y_pos_parent"/>
    <xsl:param name="spacer"/>
    <xsl:param name="height_element"/>
    <xsl:param name="font_size"/>
    <xsl:param name="element"/>
    <xsl:variable name="index" select="$y_pos div $spacer"/>
 
    <xsl:if test="$y_pos > 0">
      <xsl:variable name="temp_id" select="$element/child[$index]/@id"/>
      <xsl:call-template name="draw_element">
        <xsl:with-param name="name" select="//element[@id = $temp_id]/@name"/>
        <xsl:with-param name="id" select="$element/child[$index]/@id"/>
        <xsl:with-param name="class" select="'child'"/>
        <xsl:with-param name="width" select="($font_size -2) * string-length(//element[@id = $temp_id]/@name)"/>
        <xsl:with-param name="height" select="$height_element"/>
        <xsl:with-param name="x_pos" select="$x_pos"/>
        <xsl:with-param name="y_pos" select="$y_pos - $height_element"/>
      </xsl:call-template>     
      <xsl:call-template name="draw_line">
        <xsl:with-param name="x1_pos" select="$x_pos_parent"/>
        <xsl:with-param name="y1_pos" select="$y_pos_parent"/>
        <xsl:with-param name="x2_pos" select="$x_pos"/>
        <xsl:with-param name="y2_pos" select="$y_pos - ($height_element div 2)"/>
      </xsl:call-template>
      <xsl:call-template name="children">
        <xsl:with-param name="y_pos" select="$y_pos - $spacer"/>
        <xsl:with-param name="x_pos" select="$x_pos"/>
        <xsl:with-param name="x_pos_parent" select="$x_pos_parent"/>
        <xsl:with-param name="y_pos_parent" select="$y_pos_parent"/>
        <xsl:with-param name="spacer" select="$spacer"/>
        <xsl:with-param name="height_element" select="$height_element"/>
        <xsl:with-param name="font_size" select="$font_size"/>
        <xsl:with-param name="element" select="$element"/>
      </xsl:call-template>
    </xsl:if>
  </xsl:template>

  <xsl:template name="draw_element">
    <xsl:param name="name"/>
    <xsl:param name="id"/>
    <xsl:param name="class"/>
    <xsl:param name="width"/>
    <xsl:param name="height"/>
    <xsl:param name="x_pos"/>
    <xsl:param name="y_pos"/>
    <xsl:variable name="x_pos_text" select="$x_pos + $width div 2"/>
    <xsl:variable name="y_pos_text" select="$y_pos + ($height + 5) div 2"/>
    <rect
       style="fill:green"
       id="{$id}"
       class="{$class}"
       width="{$width}"
       height="{$height}"
       x="{$x_pos}"
       y="{$y_pos}"
       rx="5"
       ry="5" />
    <text
       x="{$x_pos_text}"
       y="{$y_pos_text}"
       font-family="Consolas,monaco,monospace;"
       font-size="12"
       style="fill:white"
       text-anchor="middle"
       id="text_{$id}"><xsl:value-of select="$name"/></text>
  </xsl:template>

  <xsl:template name="draw_line">
    <xsl:param name="x1_pos"/>
    <xsl:param name="y1_pos"/>
    <xsl:param name="x2_pos"/>
    <xsl:param name="y2_pos"/>
    <line x1="{$x1_pos}" y1="{$y1_pos}" x2="{$x2_pos}" y2="{$y2_pos}" stroke="black" stroke-width="1" />
  </xsl:template>

</xsl:stylesheet>
