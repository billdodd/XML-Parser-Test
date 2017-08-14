import argparse
from bs4 import BeautifulSoup
# from bs4.diagnose import diagnose
# import bs4

doc = """
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

valid_parsers = ['html.parser', 'lxml', 'lxml-xml', 'xml', 'html5lib']

arg_parser = argparse.ArgumentParser(description='Tool to test various parsers')
arg_parser.add_argument('-p', '--parser', help='name of parser to use - valid values are {}'.format(valid_parsers))
#                                           + '"html.parser", "lxml", "lxml-xml", "xml", "html5lib"')

args = arg_parser.parse_args()

parser = args.parser

if parser is not None and parser not in valid_parsers:
    print('Parser "{}" is not a recognized parser.'.format(parser))
    print('Please specify a valid parser from the list: {}'.format(valid_parsers))
    exit(1)

if parser is None:
    print('No parser specified; using default parser')
    soup = BeautifulSoup(doc)
else:
    print('Parsing document with parser "{}"'.format(parser))
    soup = BeautifulSoup(doc, parser)

print()
print('Parsed document:')
print()
print(soup.prettify())




