@echo off

if not exist "etc\xml\catalog" (
    bin\xmlcatalog --create --noout etc\xml\catalog
)
bin\xmlcatalog --noout --add nextCatalog  "" "docbook-dtd-4.2.xml"  etc\xml\catalog
