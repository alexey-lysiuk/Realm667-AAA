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


def replace_in_lump(name, wad, old, new):
    lump = wad.find(name)

    if lump:
        lump.data = lump.data.replace(old, new, 1)

def replace_in_decorate(wad, old, new):
   replace_in_lump('DECORATE', wad, old, new)


# Armory

def apply_patch_372(wad): # BFG10K
    replace_in_decorate(wad,
        'Weapon.Kickback 100\r\n  Inventory.Pickupmessage',
        'Weapon.Kickback 100\r\n  Weapon.SlotNumber 7\r\n  Inventory.Pickupmessage')
    replace_in_lump('GLDEFS', wad, 'PlickerLight', 'FlickerLight')

def apply_patch_585(wad): # AA12 Shotgun
    replace_in_decorate(wad, ' A_SetPitch (pitch-0.5)', '')

def apply_patch_884(wad): # Axe
    replace_in_decorate(wad,
        '+WEAPON.NOALERT\r\n\tInventory.Icon',
        '+WEAPON.NOALERT\r\n\tWeapon.SlotNumber 1\r\n\tInventory.Icon')


def apply_patch(id, wad):
    func_name = 'apply_patch_{0}'.format(id)

    if func_name in globals():
        globals()[func_name](wad)
