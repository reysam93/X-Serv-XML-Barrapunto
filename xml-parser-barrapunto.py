#!/usr/bin/python

from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import sys
import string


class headerHandler(ContentHandler):

    def __init__(self):
        self.inContent = False
        self.theContent = ""
        self.inItem = False
        self.title = ""
        self.html = "<html><body>"

    def startElement(self, name, attrs):
        if name == "item":
            self.inItem = True
        elif self.inItem:
            if name == "title" or name == "link":
                self.inContent = True

    def endElement(self, name):
        if name == "item":
            self.inItem = False
        elif self.inItem:
            if name == "title":
                print "Title: " + self.theContent + "."
                self.title = self.theContent
                self.inContent = False
                self.theContent = ""
            elif name == "link":
                print "\tLink: " + self.theContent + "."
                self.html += "Title: <a href=" + self.theContent + ">" +\
                            self.title + "</a><br/>"
                self.inContent = False
                self.theContent = ""

    def characters(self, chars):
        if self.inContent:
            self.theContent = self.theContent + chars


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage: python xml-parser-jokes.py <document>\n"
        sys.exit(1)
    parser = make_parser()
    handler = headerHandler()
    parser.setContentHandler(handler)

    try:
        xmlFile = open(sys.argv[1], "r")
    except IOError:
        print "file doesn't exit"
        sys.exit(1)
    parser.parse(xmlFile)
    print "Parse complete"
    handler.html += "</body></html>"
    htmlFile = open("barrapunto.html", "w")
    htmlFile.write(handler.html.encode("utf8"))
