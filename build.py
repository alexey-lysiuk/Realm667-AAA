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

    # Doom Style
    (342, '40mm Grenade Launcher'),
    (585, 'AA12 Shotgun'),
    (260, 'Action MachineGun'),
    (516, 'AK47'),
    (685, 'Ammo Satchel'),
    (534, 'Angled Pistol'),
    (432, 'Autogun'),
    (884, 'Axe'),
    (874, 'BFG 2704'),
    (372, 'BFG10K'),
    (281, 'Bio Pipebomb Launcher'),
    (903, 'Black Hole Generator'),
    (330, 'Butcher (Gun)'),
    (403, 'Channeler'),
    (758, 'Claymore Mines'),
    (445, 'Coachgun'),
    (581, 'Colt 45'),
    (816, 'CryoBow'),
    (308, 'Doom 3 SSG'),
    (520, 'Double Bladed Chainsaw'),
    (344, 'Double Grenade Launcher'),
    (409, 'Duke Shotgun'),
    (246, 'Ego Smasher'),
    (262, 'Electro Gun'),
    (507, 'Fist Redux'),
    (541, 'Flamethrower'),
    (913, 'Flashlight'),
    (242, 'Freeze Rifle'),
    (559, 'Glock 18'),
    (373, 'Grenade Launcher'),
    (406, 'Grenade Launcher (KDiZD)'),
    (254, 'HandGrenade'),
    (760, 'Heavy Chaingun'),
    (803, 'Heavy Machinegun'),
    (255, 'HeavyRifle'),
    (508, 'Hellstorm Cannon'),
    (719, 'Hunting Rifle'),
    (315, 'iGun'),
    (381, 'Ionspray'),
    (239, 'Karasawa'),
    (247, 'Knife'),
    (717, 'LandMine Layer'),
    (804, 'Light Machinegun'),
    (514, 'M16'),
    (600, 'M40A1 Sniper Rifle'),
    (598, 'M79'),
    (265, 'Machete'),
    (233, 'MachineGun'),
    (521, 'Mag .60'),
    (256, 'Mancubus Arm'),
    (761, 'Micro Uzi'),
    (225, 'Minigun'),
    (762, 'Model 1887'),
    (599, 'MP40'),
    (684, 'MP5 '),
    (496, 'Nailgun (MG)'),
    (560, 'Nailgun (SG)'),
    (268, 'Nuclear Missile'),
    (245, 'Pipe Bombs'),
    (232, 'Plasma Beam'),
    (313, 'PlasmaBolter'),
    (763, 'Plasma Pistol'),
    (329, 'Plasma Shotgun'),
    (509, 'Prox Launcher'),
    (764, 'Pulse Nailgun '),
    (522, 'Pulse Rifle'),
    (659, 'Pulse Rifle'),
    (244, 'Pump-Action Shotgun'),
    (374, 'Railgun'),
    (718, 'Raptor Handgun'),
    (523, 'Ray Gun'),
    (561, 'Reaper'),
    (567, 'Repeater'),
    (407, 'Rifle'),
    (857, 'Rivet Gun'),
    (886, 'Scatter Pistol'),
    (368, 'Shield Gun'),
    (601, 'Side-By-Side Shotgun'),
    (512, 'Silenced Pistol'),
    (259, 'SmartGun'),
    (513, 'Smasher'),
    (272, 'Sniper Rifle'),
    (250, 'SPAS-12'),
    (876, 'Spray Cannon'),
    (767, 'Strife Pistol'),
    (568, 'Stunner Rifle'),
    (402, 'Super Shotgun (KDiZD)'),
    (273, 'Swat Shotgun'),
    (423, 'Toaster'),
    (912, 'UAC Plasmatic Rifle'),
    (235, 'Uber Minigun'),
    (243, 'Unmaker'),
    (543, 'UTNT Pyro-Cannon'),
    (227, 'Uzi'),
    (274, 'Western Shotgun'),
    (765, 'Winchester Yellowboy'),
    (228, 'Zombieman Rifle'),

    # Heretic / Hexen Style
    (327, 'Apotheosis'),
    (817, 'Arbalest of the Ancients '),
    (323, 'Blood Scepter'),
    (757, 'Bow'),
    (515, 'Cult of the Serpent Staff'),
    (626, 'D\'sparil Staff'),
    (759, 'Fire Crystal'),
    (234, 'FrostFang'),
    (862, 'Impaler Crossbow'),
    (674, 'Iron Crossbow'),
    (324, 'Jade Wand'),
    (511, 'Lightbringer'),
    (675, 'Lightening Rod'),
    (444, 'Necronomicon'),
    (495, 'Raven Staff'),
    (518, 'Scepter of Souls'),
    (282, 'Skull Staff'),
    (328, 'Spellbinder'),
    (582, 'Super Crossbow'),
    (638, 'Thunder Fork'),
    (510, 'Vile Staff'),
    (473, 'Wand of Embers'),

    # Other Sources / Styles
    (697, 'Bearkiller'),
    (267, 'Necrovision MG40'),
    (253, 'BlasterRifle'),
    (230, 'Plasma Gun'),
    (241, 'Devastators'),
    (258, 'PolyMorph'),
    (422, 'Deviation Launcher'),
    (269, 'Pulse Machinegun'),
    (408, 'Drummle'),
    (270, 'PyroCannon'),
    (404, 'Enforcer'),
    (229, 'Quake II Chaingun'),
    (236, 'FlareGun'),
    (314, 'Revolver PS'),
    (686, 'G3'),
    (271, 'Saw Thrower'),
    (263, 'Hunter Shotgun'),
    (226, 'Sawed Off'),
    (536, 'Jackbomb'),
    (240, 'Seeker Bazooka'),
    (238, 'M60'),
    (231, 'SMG'),
    #(249, 'MagnetSaw'),  # TODO: support .pk3
    (878, 'Swarm Plasma Gun '),
    (257, 'NailGun'),
    (252, 'Tesla Cannon'),
    (266, 'Napalm Launcher'),
    (283, 'TommyGun'),

##    # Beastiary
##    (  7, 'Afrit'),
##    (  8, 'Agathodemon'),
##    (316, 'Agaures'),
##    (  9, 'Annihilator'),
##    (284, 'Arachnobaron'),
##    ( 11, 'Arachnophyte'),
##    (285, 'Aracnorb'),
##    ( 12, 'Archon of Hell'),
##    (768, 'Augmented Arachnotron'),
##    (555, 'Auto Shotgun Guy'),
##    (148, 'Azazel'),
##    (877, 'Baby Cacodemon'),
##    ( 15, 'Belphegor'),

    # Items
    (490, 'Adrenaline Kit'),
    (897, 'Familiar Summon'),
    (898, 'Ritual Knife'),
    (926, 'Shield Spells'),
]

output_filename = 'realm667-aaa.pk3'

url_download = 'http://realm667.com/index.php/en/component/docman/?task=doc_download&gid={0}'


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
                url = url_download.format(id)
                response = urllib2.urlopen(url)
                data = response.read()

                # TODO: add error handling
                with open(cached_filename, 'wb') as cached_file:
                    cached_file.write(data)

                cached_file = zipfile.ZipFile(cached_filename, 'r')

            except Exception:
                # TODO: report error
                continue

        wad_filenames = []

        for zipped_filename in cached_file.namelist():
            if zipped_filename.lower().endswith('.wad'):
                wad_filenames.append(zipped_filename)

        if 0 == len(wad_filenames):
            cached_file.close()

            print('Error: no WAD files found')
            continue

        for filename in wad_filenames:
            try:
                wad_file = cached_file.open(filename)
                wad_data = wad_file.read()
                wad_file.close()

                wad = doomwad.WadFile(wad_data)

                if not wad.find('DECORATE'):
                    print('Warning: No DECORATE lump found in file {0}, skipping...'.format(filename))
                    continue

                patching.apply_patch(id, wad)

                wad_data = cStringIO.StringIO()
                wad.writeto(wad_data)

                output_file.writestr(os.path.basename(filename), wad_data.getvalue())

            except Exception:
                print('Error: Failed to add {0}'.format(filename))
                continue

        cached_file.close()

    add_lump(output_file, 'KEYCONF')
    add_lump(output_file, 'MENUDEF')

    output_file.close()

if __name__ == '__main__':
    main()
