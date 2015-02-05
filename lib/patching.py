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


# Disable A_SetPitch() calls in DECORATE, suitable for playing without mouselook
no_set_pitch = True

# Disallow class replacement in DECORATE
no_class_replacement = True

# Disallow editor number (doomednum) assignment in DECORATE
no_doomednum = True


# TODO:
# [?] Remove unused lumps like CREDITS or INFO
# [?] Optimize DECORATE lump: remove comments and extra line breaks


def replace_in_lump(name, wad, old, new):
    lump = wad.find(name)

    if lump:
        lump.data = re.sub(old, new, lump.data, 0, re.IGNORECASE)
    else:
        print("Error: Cannot find lump {0}".format(name))

def replace_in_decorate(wad, old, new):
    replace_in_lump('DECORATE', wad, old, new)

def replace_in_keyconf(wad, old, new):
    replace_in_lump('KEYCONF', wad, old, new)

def fix_generic_setslot(wad):
    replace_in_keyconf(wad, 'setslot', 'addslotdefault')


# Armory

def apply_patch_242(wad): # Freeze Rifle
    # fix incorrect sprite
    replace_in_decorate(wad, 'PLSG', 'FRSG')

def apply_patch_246(wad): # EgoSmasher
    fix_generic_setslot(wad)

def apply_patch_308(wad): # Doom 2.5 SSG
    replace_in_keyconf(wad,
        'SetSlot 3 Shotgun Doom2.5SSG',
        'addslotdefault 3 Doom2.5SSG')

def apply_patch_330(wad): # Butchergun Chaingun
    replace_in_keyconf(wad,
        'setslot 4 Butchergun Chaingun',
        'addslotdefault 4 Butchergun')

def apply_patch_372(wad): # Autogun
    replace_in_lump('GLDEFS', wad, 'PlickerLight', 'FlickerLight')

def apply_patch_496(wad): # Nailgun (MG)
    # fix shared class name with #560 Nailgun (SG)
    replace_in_decorate(wad, 'NailBlur', 'NailBlurMG')

def apply_patch_521(wad): # Mag .60
    # fix wrong class name
    # put here to avoid 'MagSixty is not a weapon' message in console
    replace_in_keyconf(wad, 'MagSixty', 'Mag60')

def apply_patch_560(wad): # Nailgun (SG)
    # fix shared class name with #496 Nailgun (MG)
    replace_in_decorate(wad, 'NailBlur', 'NailBlurSG')

def apply_patch_685(wad): # Ammo Satchels
    # fix class name collision with Strife
    replace_in_decorate(wad, 'AmmoSatchel', 'AmmoSatchelR667')

def apply_patch_804(wad): # Light Machinegun
    # fix class name collision with Machinegun weapon
    replace_in_decorate(wad,
        r'(actor\s+)Machinegun(\s*:\s*\w+)',
        r'\1LightMachinegun\2')


def apply_patch(id, wad):
    if no_set_pitch:
        replace_in_decorate(wad, r'\s+A_SetPitch\s*\([\+\w\s\.\+\-\*\\]+\)', '')
    if no_class_replacement:
        replace_in_decorate(wad, r'(actor\s+[\w\.]+\s*:\s*[\w\.]+)\s+replaces\s+[\w\.]+', r'\1')
    if no_doomednum:
        replace_in_decorate(wad, r'(actor\s+[\w\.]+\s*:\s*[\w\.]+\s+(replaces\s+[\w\.]+)?)\s*\d*', r'\1')

    func_name = 'apply_patch_{0}'.format(id)

    if func_name in globals():
        globals()[func_name](wad)
