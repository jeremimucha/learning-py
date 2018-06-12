#! python3
import sys
import os
import pickle
import shelve
import tempfile
import xml.etree.ElementTree
import xml.parsers.expat
import xml.sax.saxutils
import Console
import Util
from operator import itemgetter

DISPLAY_LIMIT = 20


def main():
    functions = dict(a=add_bookmark, e=edit_bookmark, l=list_bookmarks,
                     r=remove_bookmark, i=import_xml, x=export_xml, q=quit)
    filename = os.path.join(os.path.dirname(__file__), "bookmarks.dbm")
    db = None
    try:
        db = shelve.open(filename, protocol=pickle.HIGHEST_PROTOCOL)
        action = ''
        while True:
            print("\nBookmarks: ({0})".format(os.path.basename(filename)))
            if action != 'l' and 1 <= len(db) < DISPLAY_LIMIT:
                list_bookmarks(db)
            else:
                print("{0} bookmark{1}\n".format(len(db), Util.s(len(db))))
            menu = ("(A)dd  (E)dit  (L)ist  (R)emove (I)import"
                    "e(X)port (Q)uit"
                    if len(db) else "(A)dd  (I)mport (Q)uit")
            valid = frozenset("aelirxq" if len(db) else "aiq")
            action = Console.get_menu_choice(menu, valid,
                'l' if len(db) else 'a', True)
            functions[action](db)
    finally:
        if db is not None:
            db.close()


def _prepend_protocol(address):
    parts = []
    if not address.startswith('http'):
        parts.append('http://')
        if not address.startswith('www.'):
            parts.append('www.')
    elif not address.startswith('www.'):
        parts.append('www.')

    parts.append(address)
    return ''.join(parts)


def add_bookmark(db):
    name = Console.get_string("Bookmark name", "name")
    if not name:
        return
    address = Console.get_string("Address", "address")
    if not address:
        return
    address = _prepend_protocol(address)
    db[name] = address
    db.sync()


def edit_bookmark(db):
    old_name = find_bookmark(db, 'edit')
    if old_name is None:
        return
    address = db[old_name]
    name = Console.get_string("Bookmark name", 'name', old_name)
    if not name:
        return
    address = Console.get_string("Address", 'address', address)
    if not address:
        return
    db[name] = address
    if name != old_name:
        del db[old_name]
    db.sync()


def list_bookmarks(db):
    start = ''
    if len(db) > DISPLAY_LIMIT:
        start = Console.get_string("List bookmarks starting with"
                                   "[Enter=all]", "start")
    print()
    for index, pair in enumerate(sorted(db.items(), key=itemgetter(0)), start=1):
        if not start or pair[0].lower().startswith(start.lower()):
            print('({index}) {pair[0]:.<30} {pair[1]}'.format(index=index, pair=pair))


def remove_bookmark(db):
    name = find_bookmark(db, 'remove')
    if name is None:
        return
    address = db[name]
    ans = Console.get_bool("Remove {0}: {1}?".format(name, address), 'no')
    if ans:
        del db[name]
        db.sync()


def import_xml(db):
    filename = Console.get_string("Import from", "filename")
    if not filename:
        return
    try:
        tree = xml.etree.ElementTree.parse(filename)
    except (EnvironmentError, xml.parsers.expat.ExpatError) as err:
        print("ERROR: ", err)
        return
    db.clear()
    for element in tree.findall("bookmark"):
        try:
            name = element.get('name')
            address = element.text
            db[name] = address
        except ValueError as err:
            print("ERROR: ", err)
            return
    print("Imported {0} bookmark{1}".format(len(db), Util.s(len(db))))
    db.sync()


def export_xml(db):
    filename = os.path.join(os.path.dirname(__file__), 'bookmarks.xml')
    with open(filename, 'w', encoding='utf8') as fh:
        fh.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        fh.write('<bookmarks>\n')
        for name, address in sorted(db.items(), key=itemgetter(0)):
            fh.write('<bookmark name="{name}">'.format(xml.sax.saxutils.
                quoteattr(name), name=name))
            fh.write(xml.sax.saxutils.escape(address))
            fh.write('</bookmark>\n')
        fh.write('</bookmarks>\n')
        fh.close()
    print("exported {0} bookmark{1} to {2}".format(len(db),
                                                    Util.s(len(db)), filename))


def quit(db):
    print("Saved {0} bookmark{1}".format(len(db), Util.s(len(db))))
    db.close()
    sys.exit()


def find_bookmark(db, message):
    message = "Index of bookmark to " + message
    valid_min = 1
    valid_max = len(db)
    enumdict = {k: v for k, v in enumerate(sorted(db.keys()), start=1)}
    while True:
        index = Console.get_integer(message, 'index', minimum=valid_min,
                                    maximum=valid_max, allow_zero=False)
        if index is None:
            return None
        return enumdict[index]


main()
