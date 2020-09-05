import xml.etree.ElementTree as et

class GeneInfo(object):

    def __init__(self):
        self.chnName = ""
        self.inheritance = "-"
        self.description = "No description"

def getDB(description):
    try:
        xp = et.parse("data.xml", )
    except FileNotFoundError:
        description['text'] = "There is no data file!"
        return {}
    else:
        root = xp.getroot()
        description['text'] = "\nThe current database:"
        description['text'] += "\nGenerated by file: " + root.attrib['file']
        description['text'] += "\nGenerated on date: " + root.attrib['date']

        dataDict = {}
        for item in root.findall('gene'):
            temp = GeneInfo()
            temp.chnName = item.attrib['chnName']
            if item.attrib['inheritance']:
                temp.inheritance = item.attrib['inheritance']
            if item.text:
                temp.description = item.text
            dataDict.update({item.attrib['name']: temp})
        return dataDict

def updateDB(dataSheet, fileName, genDate):

    def indent(elem, level=0):
        # function from website: https://www.jianshu.com/p/b916052bec4e
        i = "\n" + level * "  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                indent(elem, level+1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i

    geneNameCol = 0
    geneChnNameCol = 5
    geneDescriptionCol = 7
    inheritanceCol = 8


    root = et.Element('data') 
    root.attrib.update({"file": fileName})
    root.attrib.update({"date": genDate})
    for row in range(1, dataSheet.nrows):
        child = et.Element('gene')
        child.attrib.update({"name": dataSheet.cell(row, geneNameCol).value})
        child.attrib.update({"chnName": dataSheet.cell(row, geneChnNameCol).value})
        child.attrib.update({"inheritance": dataSheet.cell(row, inheritanceCol).value})
        child.text = dataSheet.cell(row, geneDescriptionCol).value
        root.append(child)

    indent(root)
    et.ElementTree(root).write("data.xml", "UTF-8")