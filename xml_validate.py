import argparse
from lxml import etree
from io import StringIO
import sys


def main():
    # Parse args
    arg_parser = argparse.ArgumentParser(description='Tool to validate XML file against XSD schema')
    arg_parser.add_argument('-d', '--document', required=True, help='file name of XML document to validate')
    arg_parser.add_argument('-s', '--schema', required=True, help='file name of XSD schema')
    args = arg_parser.parse_args()

    # open and read schema file
    with open(args.schema, 'r') as schema_file:
        schema_to_check = schema_file.read()

    # open and read xml file
    with open(args.document, 'r') as xml_file:
        xml_to_check = xml_file.read()

    print()

    # parse schema file
    try:
        xmlschema_doc = etree.parse(StringIO(schema_to_check))
        xmlschema = etree.XMLSchema(xmlschema_doc)
        print('Schema well-formed, syntax ok.')
        print()
    except IOError as e:
        print('IO Error parsing file {}. Exception: "{}"'.format(args.schema, e))
        print()
        sys.exit(1)
    except etree.XMLSyntaxError as e:
        print('XML syntax error in file {}. Error log:'.format(args.schema))
        print('{}'.format(e.error_log))
        print()
        sys.exit(1)
    except Exception as e:
        print('Error parsing file {}. Exception: "{}"'.format(args.schema, e))
        print()
        sys.exit(1)

    # parse xml file
    try:
        doc = etree.parse(StringIO(xml_to_check))
        print('XML well-formed, syntax ok.')
        print()
    except IOError as e:
        print('IO Error parsing file {}. Exception: "{}"'.format(args.document, e))
        print()
        sys.exit(1)
    except etree.XMLSyntaxError as e:
        print('XML syntax error in file {}. Error log:'.format(args.document))
        print('{}'.format(e.error_log))
        print()
        sys.exit(1)
    except Exception as e:
        print('Error parsing file {}. Exception: "{}"'.format(args.document, e))
        print()
        sys.exit(1)

    # validate xml against schema
    try:
        xmlschema.assertValid(doc)
        print('XML valid, schema validation ok.')
        print()
    except etree.DocumentInvalid as e:
        print('XML schema validation error in file {} (schema file {}). Error log:'.format(args.document, args.schema))
        print('{}'.format(e.error_log))
        print()
        sys.exit(1)
    except Exception as e:
        print('Error while validating file {} (schema file {}). Exception: "{}"'.format(args.document, args.schema, e))
        print()
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
