# XML-Parser-Test
Python programs for testing various XML parsers and XML schema validation

## Prerequisites

Install `requests`, `beautifulsoup4`, and `lxml`:

```
pip install requests
pip install beautifulsoup4
pip install lxml
```

## XML Parser Test

### Syntax
```
usage: xml_parser_test.py [-h] (--diagnose | --bs4 BS4 | --etree | --edmx)
                          [-d DOCUMENT | -u URL]

Tool to test various parsers

optional arguments:
  -h, --help            show this help message and exit
  --diagnose            dump the results of the beautiful4 diagnose() function
  --bs4 BS4             parse with specified BeautifulSoup4 parser; list of
                        valid parsers: ['html.parser', 'lxml', 'lxml-xml',
                        'xml', 'html5lib']
  --etree               parse with ElementTree parser
  --edmx                use BS4 xml parser and check for valid edm/edmx tags
  -d DOCUMENT, --document DOCUMENT
                        file name of document to parse
  -u URL, --url URL     URL of document to parse
```

### Examples
Parse document `sample.xml` using BeautifulSoup4 with the 'xml' parser.

```
$ python3 xml_parser_test.py -d sample.xml --bs4 xml
Parsing document with BeautifulSoup4 and parser "xml"

Parsed document (BeautifulSoup4 xml):

<?xml version="1.0" encoding="utf-8"?>
<!-- Copyright 2014-2016 Distributed Management Task Force, Inc. (DMTF). All rights reserved.-->
<edmx:Edmx Version="4.0" xmlns:edmx="http://docs.oasis-open.org/odata/ns/edmx">
 <edmx:Reference Uri="/redfish/v1/Schemas/ServiceRoot_v1.xml">
  <edmx:Include Namespace="ServiceRoot"/>
  <edmx:include Namespace="ServiceRoot.v1_0_0"/>
  <edmx:Include Namespace="ServiceRoot.v1_0_2"/>
 </edmx:Reference>
</edmx:Edmx>

is_xml = True
```

Parse document `sample.xml` using BeautifulSoup4 with the 'xml' parser and show any tags found that are not valid `edm` or `edmx` tags. Note that there is one bad `edmx` tag in the sample doc (`<edmx:include .../>` with a lowercase 'i').

```
$ python3 xml_parser_test.py -d sample.xml --edmx
Bad edm tags:

Bad edmx tags:
edmx:include (ns=http://docs.oasis-open.org/odata/ns/edmx)

Tags not in edm or edmx namespaces:

```

## XML Validation

### Syntax
```
usage: xml_validate.py [-h] -d DOCUMENT -s SCHEMA

Tool to validate XML file against XSD schema

optional arguments:
  -h, --help            show this help message and exit
  -d DOCUMENT, --document DOCUMENT
                        file name of XML document to validate
  -s SCHEMA, --schema SCHEMA
                        file name of XSD schema
```

### Example
Validate document `sample.xml` against the `schemas/edms.xsd` schema. Note that the sample doc does not conform to the schema, so a schema validation error is shown.

```
$ python3 xml_validate.py -d sample.xml -s schemas/edmx.xsd

Schema well-formed, syntax ok.

XML well-formed, syntax ok.

XML schema validation error in file sample.xml (schema file schemas/edmx.xsd). Error log:
<string>:7:0:ERROR:SCHEMASV:SCHEMAV_ELEMENT_CONTENT: Element '{http://docs.oasis-open.org/odata/ns/edmx}include': This element is not expected.
<string>:3:0:ERROR:SCHEMASV:SCHEMAV_ELEMENT_CONTENT: Element '{http://docs.oasis-open.org/odata/ns/edmx}Edmx': Missing child element(s). Expected is one of ( {http://docs.oasis-open.org/odata/ns/edmx}Reference, {http://docs.oasis-open.org/odata/ns/edmx}DataServices ).
```
