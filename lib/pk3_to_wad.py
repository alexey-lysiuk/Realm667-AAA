#!/usr/bin/env python

#
#    Realm667 - An Awesome Awesomeness
#    Copyright (C) 2015 Alexey Lysiuk
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#


import cStringIO
import os, sys
import zipfile

sys.path.append(os.path.dirname(__file__))

import doomwad


def _add_lump(wad, name, namespace = '', data = ''):
    lump = doomwad.Lump(name, data)
    lump.marker = '' == data
    lump.namespace = namespace
    wad.lumps.append(lump)

def pk3_to_wad(pk3_data):
    """
    Return Doom WAD file binary content converted from .pk3 ZIP file
    in the same form (bytes as a string or string-like object)
    NOTE: Namespaces support is limited to sprites only
    """

    mem_file = cStringIO.StringIO()
    mem_file.write(pk3_data)
    mem_file.seek(0)

    zip_file = zipfile.ZipFile(mem_file)

    directory = ''
    namespace = ''

    zip_infos = sorted(zip_file.infolist(), \
        key = lambda info : info.filename.lower())
    wad = doomwad.WadFile()

    sprite_namespace = 'S_START'

    for info in zip_infos:
        filename = info.filename.lower()

        if info.external_attr & 0x10:
            directory = filename
            namespace = ''

            if 'sprites/' == directory.lower():
                # add opening marker
                namespace = sprite_namespace
                _add_lump(wad, namespace, namespace)

            continue

        if not filename.startswith(directory):
            if namespace == sprite_namespace:
                # add closing marker
                _add_lump(wad, 'S_END')

            directory = ''
            namespace = ''

        lumpname = filename.upper()[len(directory):]
        if '.' in lumpname:
            lumpname = lumpname[:lumpname.rfind('.')]

        data = zip_file.open(info.filename).read()
        _add_lump(wad, lumpname, namespace, data)

    if namespace == sprite_namespace:
        # add closing marker, if file from sprites directory was the last one
        _add_lump(wad, 'S_END')

    wad_file = cStringIO.StringIO()
    wad.writeto(wad_file)

    return wad_file.getvalue()


if __name__ == '__main__':
    if 3 != len(sys.argv):
        print('Usage: {0} input.pk3 output.wad'.format(__file__))
        exit(1)

    with open(sys.argv[1], 'rb') as f:
        pk3_data = f.read()

    wad_data = pk3_to_wad(pk3_data)

    with open(sys.argv[2], 'wb') as f:
        f.write(wad_data)