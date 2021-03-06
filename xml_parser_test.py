import argparse
from bs4 import BeautifulSoup
from bs4.diagnose import diagnose
from bs4.element import Tag
from io import StringIO
import requests
import sys
from xml.etree import ElementTree

EDM_NAMESPACE = "http://docs.oasis-open.org/odata/ns/edm"
EDMX_NAMESPACE = "http://docs.oasis-open.org/odata/ns/edmx"

EDM_TAGS = ['Action', 'Annotation', 'Collection', 'ComplexType', 'EntityContainer', 'EntityType', 'EnumType', 'Key',
            'Member', 'NavigationProperty', 'Parameter', 'Property', 'PropertyRef', 'PropertyValue', 'Record',
            'Schema', 'Singleton', 'Term', 'TypeDefinition']
EDMX_TAGS = ['DataServices', 'Edmx', 'Include', 'Reference']

default_doc = """<?xml version="1.0" encoding="UTF-8"?>
<!-- Copyright 2014-2016 Distributed Management Task Force, Inc. (DMTF). All rights reserved.-->
<edmx:Edmx xmlns:edmx="http://docs.oasis-open.org/odata/ns/edmx" Version="4.0">

    <edmx:Reference Uri="/redfish/v1/Schemas/ServiceRoot_v1.xml">
      <edmx:Include Namespace="ServiceRoot"/>
      <edmx:Include Namespace="ServiceRoot.v1_0_0"/>
          <edmx:Include Namespace="ServiceRoot.v1_0_2"/>
    </edmx:Reference>
</edmx:Edmx>
"""


def exercise_soup(soup):
    """
    Sandbox function to test out walking and searching XML document
    :param soup: BS4 soup instance to navigate
    :return:
    """

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


def run_bs4_diagnose(doc):
    print('Option "--diagnose" option specified; running document through bs4 diagnose() function')
    print()
    diagnose(doc)


def bs4_parse(doc, bs4_parser):
    try:
        print('Parsing document with BeautifulSoup4 and parser "{}"'.format(bs4_parser))
        soup = BeautifulSoup(doc, bs4_parser)
        print()
        print('Parsed document (BeautifulSoup4 {}):'.format(bs4_parser))
        print()
        print(soup.prettify())
        # is the document XML?
        print()
        print('is_xml = {}'.format(soup.is_xml))
        # exercise_soup(soup)
    except Exception as e:
        print('Error parsing document with BeautifulSoup4, error: {}'.format(e))


def et_parse(doc):
    try:
        print('Parsing document with ElementTree')
        # print('doc is of type {}'.format(type(doc)))
        # print('doc is {}'.format(doc))
        xml = ElementTree.parse(doc)
        print()
        print('Parsed document (ElementTree):')
        print()
        xml.write(sys.stdout, encoding='unicode', xml_declaration=True, method='xml')
        print()
    except ElementTree.ParseError as e:
        print('Error parsing document with ElementTree, error: {}'.format(e))


def bad_edm_tags(tag):
    return tag.namespace == EDM_NAMESPACE and tag.name not in EDM_TAGS


def bad_edmx_tags(tag):
    return tag.namespace == EDMX_NAMESPACE and tag.name not in EDMX_TAGS


def other_ns_tags(tag):
    return tag.namespace != EDM_NAMESPACE and tag.namespace != EDMX_NAMESPACE


def check_edmx(doc, bs4_parser):
    try:
        soup = BeautifulSoup(doc, bs4_parser)
        print('Bad edm tags:')
        for tag in soup.find_all(bad_edm_tags):
            if tag.prefix is None:
                print('{} (ns={})'.format(tag.name, tag.namespace))
            else:
                print('{}:{} (ns={})'.format(tag.prefix, tag.name, tag.namespace))
        print()
        print('Bad edmx tags:')
        for tag in soup.find_all(bad_edmx_tags):
            if tag.prefix is None:
                print('{} (ns={})'.format(tag.name, tag.namespace))
            else:
                print('{}:{} (ns={})'.format(tag.prefix, tag.name, tag.namespace))
        print()
        print('Tags not in edm or edmx namespaces:')
        for tag in soup.find_all(other_ns_tags):
            if tag.prefix is None:
                print('{} (ns={})'.format(tag.name, tag.namespace))
            else:
                print('{}:{} (ns={})'.format(tag.prefix, tag.name, tag.namespace))
        print()
    except Exception as e:
        print('Error parsing document with BeautifulSoup4, error: {}'.format(e))


def main():
    # For BeautifulSoup4:
    #     XML parsers: xml, lxml-xml
    #     HTML parsers: html.parser, lxml, html5lib
    # For ElementTree:
    #     Uses a default XML parser

    valid_parsers = ['html.parser', 'lxml', 'lxml-xml', 'xml', 'html5lib']

    # Parse args
    arg_parser = argparse.ArgumentParser(description='Tool to test various parsers')
    group1 = arg_parser.add_mutually_exclusive_group(required=True)
    group1.add_argument('--diagnose', action='store_true',
                        help='dump the results of the beautiful4 diagnose() function')
    group1.add_argument('--bs4', help='parse with specified BeautifulSoup4 parser; list of valid parsers: {}'
                        .format(valid_parsers))
    group1.add_argument('--etree', action='store_true', help='parse with ElementTree parser')
    group1.add_argument('--edmx', action='store_true', help='use BS4 xml parser and check for valid edm/edmx tags')
    group2 = arg_parser.add_mutually_exclusive_group()
    group2.add_argument('-d', '--document', help='file name of document to parse')
    group2.add_argument('-u', '--url', help='URL of document to parse')

    args = arg_parser.parse_args()

    bs4_diagnose = args.diagnose
    doc_file = args.document
    bs4_parser = args.bs4
    use_etree = args.etree
    edmx_check = args.edmx
    url = args.url

    # Get the doc to parse as a file object
    doc = None
    if doc_file is not None:
        # TODO: add exception handling
        doc = open(doc_file)
    elif url is not None:
        # TODO: add exception handling and better response checking
        r = requests.get(url, verify=False)
        if r.status_code == requests.codes.ok:
            doc = StringIO(r.text)
        else:
            print('Request to get doc at URL {} did not return expected OK status code; status returned: {}'
                  .format(url, r.status_code))
            exit(1)
    else:
        doc = StringIO(default_doc)

    # Do the parsing
    if edmx_check:
        check_edmx(doc, 'xml')
    if bs4_diagnose:
        run_bs4_diagnose(doc)
    elif bs4_parser is not None:
        # Parse with BeautifulSoup4
        bs4_parse(doc, bs4_parser)
    elif use_etree:
        # Parse with ElementTree
        et_parse(doc)


if __name__ == "__main__":
    main()
