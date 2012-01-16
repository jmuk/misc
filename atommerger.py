#!/usr/bin/env python

from xml.etree import ElementTree
import iso8601
import urllib2

atom_source = [
  ]

target_file = './atom.xml'


def MergeDocuments(urls, target_file):
  if len(urls) == 0:
    return

  atom_prefix = '{http://www.w3.org/2005/Atom}'
  entry_tag = atom_prefix + 'entry'
  published_tag = atom_prefix + 'published'

  primary = urls[0]
  primary_doc = ElementTree.parse(urllib2.urlopen(primary)).getroot()
  base_cursor = 0
  for elem in primary_doc.getchildren():
    if elem.tag == entry_tag:
      break
    base_cursor += 1

  for url in urls[1:]:
    sub_doc = ElementTree.parse(urllib2.urlopen(url)).getroot()
    cursor = base_cursor
    for entry in sub_doc.findall('{http://www.w3.org/2005/Atom}entry'):
      published = iso8601.parse_date(entry.find(published_tag).text)
      while cursor < len(primary_doc.getchildren()):
        cursor_entry = primary_doc.getchildren()[cursor]
        cursor_published = iso8601.parse_date(
          cursor_entry.find(published_tag).text)

        cursor += 1
        # it's safe to compare by lexicographical order
        if published > cursor_published:
          primary_doc.insert(cursor - 1, entry)
          break
  out = file(target_file, 'w')
  out.write(ElementTree.tostring(primary_doc, 'UTF-8'))
  out.close()


if __name__ == '__main__':
  MergeDocuments(atom_source, target_file)
