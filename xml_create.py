import xml.etree.cElementTree as ET

root = ET.Element("root")
doc = ET.SubElement(root, "doc")

i=0
while i < 20:
    ET.SubElement(doc, "field number: " + str(i), name=" ").text = "some value "
    i+=1

tree = ET.ElementTree(root)
tree.write("filename.xml")