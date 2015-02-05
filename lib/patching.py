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

def rename_lump(wad, old, new):
    lump = wad.find(old)

    if lump:
        lump.name = new
    else:
        print("Error: Cannot find lump {0}".format(old))

def remove_lump(wad, name):
    lump = wad.find(name)

    if lump:
        wad.removelump(lump)
    else:
        print("Error: Cannot find lump {0}".format(name))

def remove_keyconf(wad):
    remove_lump(wad, 'KEYCONF')


# Armory

def apply_patch_242(wad): # Freeze Rifle
    # fix incorrect sprite
    replace_in_decorate(wad, 'PLSG', 'FRSG')

def apply_patch_246(wad): # EgoSmasher
    remove_keyconf(wad)

def apply_patch_308(wad): # Doom 2.5 SSG
    remove_keyconf(wad)

def apply_patch_329(wad): # Plasma Shotgun
    remove_keyconf(wad)

def apply_patch_330(wad): # Butchergun Chaingun
    remove_keyconf(wad)

def apply_patch_372(wad): # Autogun
    replace_in_lump('GLDEFS', wad, 'PlickerLight', 'FlickerLight')

def apply_patch_496(wad): # Nailgun (MG)
    # fix shared class name with #560 Nailgun (SG)
    replace_in_decorate(wad, 'NailBlur', 'NailBlurMG')

def apply_patch_521(wad): # Mag .60
    remove_keyconf(wad)

def apply_patch_522(wad): # Pulse Rifle
    # fix sprite name collisions with #659 Pulse Rifle UAC
    replace_in_decorate(wad, r'(\s)PULS(\s)', r'\1PLRF\2')
    rename_lump(wad, 'PULSA0', 'PLRFA0')
    rename_lump(wad, 'PULSB0', 'PLRFB0')

def apply_patch_560(wad): # Nailgun (SG)
    # fix shared class name with #496 Nailgun (MG)
    replace_in_decorate(wad, 'NailBlur', 'NailBlurSG')

def apply_patch_659(wad): # Pulse Rifle UAC
    # fix class name collision with #522 Pulse Rifle
    replace_in_decorate(wad,
        r'(actor\s+)PulseRifle(\s*:\s*\w+)',
        r'\1PulseRifleUAC\2')

def apply_patch_685(wad): # Ammo Satchels
    # fix class name collision with ammo from Strife
    replace_in_decorate(wad, 'AmmoSatchel', 'AmmoSatchelR667')

def apply_patch_762(wad): # Model 1887
    # fix wrong end marker
    rename_lump(wad, 'SS_STOP', 'SS_END')

def apply_patch_804(wad): # Light Machinegun
    # fix class name collision with #233 Machinegun
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
