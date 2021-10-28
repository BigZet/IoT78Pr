import matplotlib.pyplot as plt
import jsontoxml


def main():
    json_converter = jsontoxml.JsonConverter(path_js="data.json", path_xml="data.xml")
    jsontoxml.XMLparser()

if __name__ == '__main__':
    main()
