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
import urllib2
import zipfile

sys.path.append(os.path.dirname(__file__) + '/lib')

import doomwad
import patching

# Configuration

repository = [
    # Armory
    (342, '40mm Grenade Launcher'),
    (585, 'AA12 Shotgun'),
    (260, 'Action Machine Gun'),
    (516, 'AK47'),
    (685, 'Ammo Satchels'),
    (534, 'Angled Pistol'),
    (432, 'Autogun'),
    (884, 'Axe'),
    (372, 'BFG10K'),
    (874, 'BFG 2704'),
    (281, 'Bio Pipebomb Launcher'),
    (903, 'Black Hole Generator'),
    (330, 'Butchergun Chaingun'),
    (403, 'Channeler Plasma Rifle'),
    (408, 'Drummle'),

    # Beastiary
    (  7, 'Afrit'),
    ( 15, 'Belphegor'),
    (877, 'Baby Cacodemon'),

    # Items
    (490, 'Adrenaline Kit'),
    (897, 'Familiar Summon'),
    (898, 'Ritual Knife'),
    (926, 'Shield Spells'),
]

output_filename = 'realm667-aaa.pk3'

url_template = 'http://realm667.com/index.php/en/component/docman/?task=doc_download&gid={0}'


def prepare():
    try:
        os.remove(output_filename)
    except OSError:
        # TODO: report error
        pass

    try:
        os.mkdir('cache')
    except OSError:
        # TODO: report error
        pass

def add_lump(zip, filename):
    zip.write('dat/{0}'.format(filename), filename)


def main():
    prepare()

    # TODO: add error handling
    output_file = zipfile.ZipFile(output_filename, 'a', zipfile.ZIP_DEFLATED)

    for item in repository:
        id   = item[0]
        name = item[1]

        print('Processing #{:04d}: {:s}...'.format(id, name))

        cached_filename = 'cache/{:04d}.zip'.format(id)
        cached_file = None

        try:
            cached_file = zipfile.ZipFile(cached_filename, 'r')

        except Exception:
            try:
                url = url_template.format(id)
                response = urllib2.urlopen(url)
                data = response.read()

                # TODO: add error handling
                with open(cached_filename, 'wb') as cached_file:
                    cached_file.write(data)

                cached_file = zipfile.ZipFile(cached_filename, 'r')

            except Exception:
                # TODO: report error
                continue

        wad_filename = None

        for zipped_filename in cached_file.namelist():
            if zipped_filename.lower().endswith('.wad'):
                wad_filename = zipped_filename
                break

        try:
            wad_file = cached_file.open(wad_filename)
            wad_data = wad_file.read()

            wad_file.close()
            cached_file.close()

            wad = doomwad.WadFile(wad_data)
            patching.apply_patch(id, wad)

            wad_data = cStringIO.StringIO()
            wad.writeto(wad_data)

            output_file.writestr(wad_filename, wad_data.getvalue())

        except Exception:
            # TODO: report error
            pass

    add_lump(output_file, 'KEYCONF')
    add_lump(output_file, 'MENUDEF')

    output_file.close()

if __name__ == '__main__':
    main()
