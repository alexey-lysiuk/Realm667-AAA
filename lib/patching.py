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


import re


# Configuration

no_set_pitch = True
detect_errors = True


# TODO:
# [?] Remove unused lumps like CREDITS or INFO
# [?] Optimize DECORATE lump: remove comments and extra line breaks


def replace_in_lump(name, wad, old, new, count = 1):
    lump = wad.find(name)

    if lump:
        if detect_errors and 0 == lump.data.count(old):
            print("Error: Failed to apply patch for lump {0}".format(name))
        else:
            lump.data = lump.data.replace(old, new, count)
    else:
        print("Error: Cannot find lump {0}".format(name))

def replace_in_decorate(wad, old, new, count = 1):
    replace_in_lump('DECORATE', wad, old, new, count)

def replace_in_keyconf(wad, old, new):
    replace_in_lump('KEYCONF', wad, old, new, 1)


# Armory

def apply_patch_242(wad): # Freeze Rifle
    replace_in_decorate(wad, 'PLSG', 'FRSG')  # fix incorrect sprite

def apply_patch_246(wad): # EgoSmasher
    replace_in_keyconf(wad, 'setslot', 'addslotdefault')

def apply_patch_260(wad): # Action Machine Gun
    replace_in_decorate(wad, ' replaces chaingun', '')

def apply_patch_308(wad): # Doom 2.5 SSG
    replace_in_decorate(wad, ' Replaces SuperShotgun', '')
    replace_in_keyconf(wad,
        'SetSlot 3 Shotgun Doom2.5SSG',
        'addslotdefault 3 Doom2.5SSG')

def apply_patch_330(wad): # Butchergun Chaingun
    replace_in_keyconf(wad,
        'setslot 4 Butchergun Chaingun',
        'addslotdefault 4 Butchergun')

def apply_patch_372(wad): # Autogun
    replace_in_lump('GLDEFS', wad, 'PlickerLight', 'FlickerLight')

def apply_patch_685(wad): # Ammo Satchels
    replace_in_decorate(wad, 'AmmoSatchel', 'AmmoSatchelR667', 100)


set_pitch_pattern = re.compile(r'\s+A_SetPitch\s*\([\+\w\s\.\+\-\*\\]+\)', re.IGNORECASE)

def remove_set_pitch(wad):
    decorate = wad.find('DECORATE')

    if decorate:
        decorate.data = set_pitch_pattern.sub('', decorate.data)
    else:
        print("Error: Cannot find DECORATE lump".format(name))


def apply_patch(id, wad):
    if no_set_pitch:
        remove_set_pitch(wad)

    func_name = 'apply_patch_{0}'.format(id)

    if func_name in globals():
        globals()[func_name](wad)
