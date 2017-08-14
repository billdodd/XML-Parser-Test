import argparse
# import bs4
from bs4 import BeautifulSoup
from bs4.diagnose import diagnose
from bs4.element import Tag
import requests

default_doc = """
<?xml version="1.0" encoding="UTF-8"?>
<!-- Copyright 2014-2016 Distributed Management Task Force, Inc. (DMTF). All rights reserved.-->
<edmx:Edmx xmlns:edmx="http://docs.oasis-open.org/odata/ns/edmx" Version="4.0">

    <edmx:Reference Uri="/redfish/v1/Schemas/ServiceRoot_v1.xml">
      <edmx:Include Namespace="ServiceRoot"/>
      <edmx:Include Namespace="ServiceRoot.v1_0_0"/>
          <edmx:Include Namespace="ServiceRoot.v1_0_2"/>
    </edmx:Reference>
</edmx:Edmx>
"""

# XML parsers: xml, lxml-xml
# HTML parsers: html.parser, lxml, html5lib
valid_parsers = ['html.parser', 'lxml', 'lxml-xml', 'xml', 'html5lib']

arg_parser = argparse.ArgumentParser(description='Tool to test various parsers')
arg_parser.add_argument('--diagnose', action='store_true', help='dump the results of beautiful4 diagnose() function')
arg_parser.add_argument('-d', '--document', help='document file name to open')
arg_parser.add_argument('-p', '--parser', help='name of parser to use - valid values are {}'.format(valid_parsers))
arg_parser.add_argument('-u', '--url', help='document URL to open')

args = arg_parser.parse_args()

bs4_diagnose = args.diagnose
doc_file = args.document
parser = args.parser
url = args.url

if parser is not None and parser not in valid_parsers:
    print('Parser "{}" is not a recognized parser.'.format(parser))
    print('Please specify a valid parser from the list: {}'.format(valid_parsers))
    exit(1)

doc = default_doc
if doc_file is not None and url is not None:
    print('Only specify the document to parse via one of the following options: --document or --url')
    exit(1)
elif doc_file is not None:
    # TODO: add exception handling
    doc = open(doc_file)
elif url is not None:
    # TODO: add exception handling and better response checking
    r = requests.get(url)
    if r.status_code == requests.codes.ok:
        doc = r.text
    else:
        print('Request to get doc at URL {} did not return expected OK status code; using default doc instead')

if bs4_diagnose:
    print('Option "--diagnose" option specified; running document through bs4 diagnose() function')
    print()
    diagnose(doc)
    exit(0)

if parser is None:
    print('No parser specified; using default parser')
    soup = BeautifulSoup(doc)
else:
    print('Parsing document with parser "{}"'.format(parser))
    soup = BeautifulSoup(doc, parser)

# print the parsed document
print()
print('Parsed document:')
print()
print(soup.prettify())

# is the document XML?
print()
print('is_xml = {}'.format(soup.is_xml))

# try to get the expected Redfish schema root tag 'Edmx' (or 'edmx:edmx' if using HTML parser)
print()
if soup.is_xml:
    tag = soup.Edmx
    if tag is not None:
        print('Found tag named "Edmx"')
        print('tag name = {}'.format(tag.name))
        print('tag namespace = {}'.format(tag.namespace))
        print('tag prefix = {}'.format(tag.prefix))
    else:
        print('Did not find tag named "Edmx"')
else:
    tag = soup.find('edmx:edmx')
    if tag is not None:
        print('Found tag named "edmx:edmx"')
        print('tag name = {}'.format(tag.name))
        print('tag namespace = {}'.format(tag.namespace))
        print('tag prefix = {}'.format(tag.prefix))
    else:
        print('Did not find tag named "edmx:edmx"')
        html = soup.html
        if html is not None:
            body = html.body
            if body is not None:
                if len(body.contents) > 0:
                    if isinstance(body.contents[0], Tag):
                        print('Found tag named "{}"'.format(body.contents[0].name))
                        print('len(html.body.contents) = {}'.format(len(body.contents)))
                        print('html.body.contents[0].name = {}'.format(body.contents[0].name))
                        print('html.body.contents[0].namespace = {}'.format(body.contents[0].namespace))
                        print('html.body.contents[0].prefix = {}'.format(body.contents[0].prefix))

# look for any tags in the first 10 children of the document
print()
print('len(soup.contents) = {}'.format(len(soup.contents)))
for n in range(10):
    if len(soup.contents) > n:
        print('child element [{}] found, type = {}'.format(n, type(soup.contents[n])))
        if isinstance(soup.contents[n], Tag):
            print('    soup.contents[{}].name = {}'.format(n, soup.contents[n].name))
            print('    soup.contents[{}].namespace = {}'.format(n, soup.contents[n].namespace))
            print('    soup.contents[{}].prefix = {}'.format(n, soup.contents[n].prefix))
