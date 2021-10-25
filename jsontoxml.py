import json
import xml.etree.ElementTree as ET

class JsonConverter:
    def __init__(self, path_js:str, path_xml:str):
        self.path_js = path_js
        self.path_xml = path_xml
        self.openFiles()

        self.data = list(json.load(self.fjs))
        self.ROOT = ET.Element('root')
        self.createXML()
        self.saveXML()



    def openFiles(self):
        self.fjs = open(self.path_js, 'r')
        self.fxml = open(self.path_xml, 'w')
        
    def createXML(self):
        for i in self.data:
            self.ROOT.append(self._create_xml_block(i))

    def saveXML(self):
        self.fxml.write(ET.tostring(self.ROOT, encoding="utf-8", method="xml").decode(encoding="utf-8"))
        self.fxml.close()
        self.fjs.close()

        
    def _create_xml_block(self, row:dict):
        PACKET = ET.SubElement(self.ROOT, 'packet')
        SOUND = ET.SubElement(PACKET, 'sound')
        ILLUMINATION = ET.SubElement(PACKET, 'illumination')
        CO2 = ET.SubElement(PACKET, 'co2')
        TEMPERATURE = ET.SubElement(PACKET, 'temperature')
        PACKET.set('id', row['id'])
        PACKET.set('timestamp', row['time'])
        SOUND.text = row['sound']
        ILLUMINATION.text = row['illumination']
        CO2.text = row['CO2']
        TEMPERATURE.text = row['temperature']
        return PACKET
