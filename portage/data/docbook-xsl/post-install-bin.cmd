@echo off

if not exist "etc\xml\catalog" (
    bin\xmlcatalog --create --noout etc\xml\catalog
)
bin\xmlcatalog --noout --add delegateSystem  "http://docbook.sourceforge.net/release/xsl/" "docbook-xsl-stylesheets.xml" etc\xml\catalog
