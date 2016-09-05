#
#    Realm667 - An Awesome Awesomeness
#    Copyright (C) 2015, 2016 Alexey Lysiuk
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

import case_insensitive
import utils

# zero ID designates a category name
# negative ID means that the given asset is excluded

_ARMORY_DOOM = (
    (  0, 'Armory: Doom Style'),
    (342, '40mm Grenade Launcher'),
    (585, 'AA12 Shotgun'),
    (260, 'Action MachineGun'),
    (516, 'AK47'),
    (685, 'Ammo Satchel'),
    (534, 'Angled Pistol'),
    (972, 'Auto Shotgun'),
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
    (973, 'Gatling Laser'),
    (559, 'Glock 18'),
    (373, 'Grenade Launcher'),
    (406, 'Grenade Launcher (KDiZD)'),
    (254, 'HandGrenade'),
    (760, 'Heavy Chaingun'),
    (803, 'Heavy Machinegun'),
    (255, 'Heavy Rifle'),
    (508, 'Hellstorm Cannon'),
    (719, 'Hunting Rifle'),
    (315, 'iGun'),
    (381, 'Ionspray'),
    (239, 'Karasawa'),
    (247, 'Knife'),
    (717, 'Landmine Layer'),
    (804, 'Light Machinegun'),
    (514, 'M16'),
    (600, 'M40A1 Sniper Rifle'),
    (598, 'M79'),
    (265, 'Machete'),
    (233, 'Machinegun'),
    (521, 'Mag .60'),
    (256, 'Mancubus Arm'),
    (761, 'Micro Uzi'),
    (225, 'Minigun'),
    (762, 'Model 1887'),
    (599, 'MP40'),
    (684, 'MP5'),
    (496, 'Nailgun (MG)'),
    (560, 'Nailgun (SG)'),
    (268, 'Nuclear Missile'),
    (245, 'Pipe Bombs'),
    (232, 'Plasma Beam'),
    (313, 'Plasma Bolter'),
    (763, 'Plasma Pistol'),
    (329, 'Plasma Shotgun'),
    (509, 'Prox Launcher'),
    (764, 'Pulse Nailgun'),
    (522, 'Pulse Rifle'),
    (659, 'Pulse Rifle UAC'),
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
)

_ARMORY_HERETIC_HEXEN = (
    (  0, 'Armory: Heretic / Hexen Style'),
    (327, 'Apotheosis'),
    (817, 'Arbalest of the Ancients'),
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
)

_ARMORY_OTHER = (
    (  0, 'Armory: Other Sources / Styles'),
    (697, 'Bearkiller'),
    (253, 'Blaster Rifle'),
    (241, 'Devastator'),
    (422, 'Deviation Launcher'),
    (408, 'Drummle'),
    (404, 'Enforcer'),
    (236, 'Flare Gun'),
    (686, 'G3'),
    (970, 'Heat-Seeker Launcher'),
    (263, 'Hunter Shotgun'),
    (536, 'Jackbomb'),
    (238, 'M60'),
    (249, 'Magnet Saw'),
    (266, 'Napalm Launcher'),
    (267, 'Necrovision MG40'),
    (230, 'Plasma Gun'),
    (258, 'Poly Morph'),
    (257, 'Power Nailgun'),
    (269, 'Pulse Machinegun'),
    (270, 'PyroCannon'),
    (229, 'Quake II Chaingun'),
    (314, 'Revolver PS'),
    (271, 'Saw Thrower'),
    (226, 'Sawed Off'),
    (240, 'Seeker Bazooka'),
    (231, 'SMG'),
    (878, 'Swarm Plasma Gun'),
    (252, 'Tesla Cannon'),
    (283, 'TommyGun'),
)


# ==============================================================================


_BEASTIARY_DOOM = (
    (  0, 'Beastiary: Doom Style'),
    (  7, 'Afrit'),
    (  8, 'Agathodemon'),
    (316, 'Agaures'),
    (  9, 'Annihilator'),
    (284, 'Arachnobaron'),
    ( 11, 'Arachnophyte'),
    (285, 'Aracnorb'),
    (931, 'Aracnorb Queen'),
    ( 12, 'Archon of Hell'),
    (768, 'Augmented Arachnotron'),
    (555, 'Auto Shotgun Guy'),
    (148, 'Azazel'),
    (877, 'Baby Cacodemon'),
    (779, 'Bad'),
    (185, 'Baphomet\'s Eyes'),
    (788, 'Beam Revenant'),
    (550, 'Beam Zombie'),
    (317, 'Beheaded Kamikaze'),
    ( 15, 'Belphegor'),
    (451, 'BFG Commando'),
    ( 16, 'Blood Demon'),
    ( 17, 'Blood Fiend'),
    (907, 'Blood Skull'),
    (309, 'Blot'),
    ( 18, 'Bruiser Demon'),
    ( 20, 'Cacolich'),
    ( 19, 'Cacolantern'),
    ( 21, 'Catharsi'),
    (814, 'Chaingun Demon'),
    ( 22, 'Chaingun Major'),
    (194, 'Chaingun Spider'),
    ( 23, 'Chainsaw Zombie'),
    (620, 'Chesire Cacodemon'),
    ( 24, 'Core Tentacles'),
    ( 25, 'Cracko Demon'),
    (807, 'Crash'),
    ( 27, 'Cyber Baron'),
    (331, 'Cyber Fiend'),
    (809, 'Cyber Imp'),
    ( 28, 'Cyber Mastermind'),
    ( 29, 'Cybruiser'),
    (334, 'Dark Cardinal'),
    (472, 'Dark Imp Pack'),
    ( 33, 'Darkness Rift'),
    ( 34, 'Death Incarnate'),
    (569, 'Deep One'),
    (177, 'Defiler'),
    ( 36, 'Demolisher'),
    (633, 'Devastator Zombie'),
    ( 37, 'Devil'),
    ( 38, 'Diabolist'),
    ( 40, 'Double Chaingunner'),
    ( 41, 'Dune Warrior'),
    ( 42, 'Enhanced Cacodemon'),
    ( 43, 'Ethereal Soul'),
    (908, 'Exterminator'),
    ( 44, 'Fallen'),
    (-688, 'Female Scientist'), # the same as in #802 Former Scientists Pack
    (488, 'Female Zombie Pack'),
    (410, 'Flamer Zombie'),
    (415, 'Flesh Spawn'),
    (186, 'Flesh Wizard'),
    ( 45, 'Flying Imp'),
    (556, 'Forgotten One'),
    (900, 'Former Ranger'),
    (802, 'Former Scientists Pack'),
    (865, 'Former Scientists Pack 2'),
    (333, 'Freezer Zombie'),
    ( 46, 'Fusion Spider'),
    (769, 'Grell'),
    ( 48, 'Guardian Cube'),
    ( 51, 'Hades Elemental'),
    ( 49, 'Hades Sphere'),
    (952, 'Haedexebus'),
    (191, 'Hangman'),
    (864, 'Hazmat Zombie'),
    (605, 'Heaven Guard'),
    ( 50, 'Hectebus'),
    ( 56, 'Hell Warrior'),
    ( 57, 'Hell\'s Fury'),
    (183, 'Hellion'),
    ( 59, 'Hellstorm Archon'),
    (552, 'Hierophant'),
    ( 60, 'Illus'),
    ( 61, 'Imp Trite'),
    (477, 'Imp Variants'),
    ( 63, 'Inferno'),
    (288, 'Jetpack Zombie'),
    (553, 'Karasawa Zombie'),
    (150, 'Lesser Mutant'),
    ( 64, 'Lord of Heresy'),
    ( 65, 'Mauler Demon'),
    (901, 'Minigunner'),
    ( 66, 'Nail Borg'),
    (337, 'Nail Borg Commando'),
    ( 69, 'Nightmare'),
    ( 70, 'Nightmare Demon'),
    (954, 'Nightmare Spectre'),
    (369, 'Nightshade'),
    ( 72, 'Obsidian Statue'),
    (289, 'Overlord'),
    (859, 'Phantasm'),
    (151, 'Phantom'),
    (178, 'Phase Imp'),
    ( 71, 'Plasma Demon'),
    ( 73, 'Plasma Elemental'),
    ( 74, 'Plasma Zombie'),
    (300, 'Poe'),
    ( 75, 'Poison Soul'),
    (339, 'Profane One'),
    ( 76, 'Psychic Soul'),
    (774, 'Pulse Nailgun Zombie'),
    (144, 'Pyro Demon'),
    (319, 'Pyro Imp'),
    (798, 'Pyro Zombie'),
    (456, 'Quad-Shotgun Zombie'),
    ( 77, 'Rail Arachnotron'),
    (188, 'Rail Bot'),
    ( 78, 'Rapid Fire Trooper'),
    (290, 'Repeater Zombie'),
    (147, 'Rictus'),
    (910, 'Rifle Commando'),
    (291, 'Roach'),
    ( 79, 'Rocket Zombie'),
    (299, 'Rocket Zombie II'),
    (320, 'Rottweiler'),
    ( 80, 'Satyr'),
    (301, 'SawedOff Zombie'),
    (292, 'Segway Zombie'),
    (575, 'Shade'),
    ( 82, 'Shadow'),
    (902, 'Shadow Trooper'),
    ( 83, 'SlimeImp'),
    (179, 'Slime Worm'),
    (602, 'SMG Zombie'),
    (770, 'Smoke Monster'),
    ( 84, 'Snake Imp'),
    (322, 'Sniper Zombie'),
    (294, 'Sonic Railgun Zombie'),
    ( 85, 'Soul Harvester'),
    ( 86, 'Spirit Imp'),
    (307, 'Squire'),
    (815, 'Stalker'),
    ( 87, 'Stealth Fighter'),
    ( 88, 'Stone Demon'),
    ( 89, 'Stone Imp'),
    ( 90, 'Suicide Bomber'),
    (296, 'Super Demon'),
    (295, 'Super Flying Imp'),
    ( 91, 'Super Imp'),
    ( 92, 'Super Shotgun Zombie'),
    (190, 'Supreme Fiend'),
    (297, 'Swarm'),
    (153, 'Terminator'),
    ( 93, 'Terror'),
    (312, 'Tesla Coil'),
    ( 94, 'Thamuz'),
    (749, 'Time Imp'),
    ( 96, 'Tornado Demon'),
    ( 97, 'Tortured Soul'),
    (557, 'Trite'),
    (505, 'UAC Bot'),
    (606, 'Undead Hunter'),
    (193, 'Undead Priest'),
    (298, 'Unmaker Zombie'),
    (812, 'Volacubi'),
    (-777, 'Vore'),  # no longer present in Repository
    (100, 'Vulgar'),
    (101, 'Warlord of Hell'),
    (102, 'Watcher'),
    (748, 'Weakener'),
    (184, 'Wicked'),
    (571, 'Doom III Wraith'),
    (104, 'ZSec'),
    (182, 'Zombie Flyer'),
    (448, 'Zombie Henchman'),
    (105, 'Zombie Marine'),
    (911, 'Zombie Missile Tank'),
    (341, 'Zombie Plasma Tank'),
    (946, 'Zombie Plasma Scientist'),
    (106, 'Zombie Railgunner'),
    (-730, 'Zombie Scientist'), # the same as in #802 Former Scientists Pack
    (107, 'ZombieTank'),
    (554, 'ZSpecOps'),
)

_BEASTIARY_HERETIC_HEXEN = (
    (  0, 'Beastiary: Heretic / Hexen Style'),
    (  6, 'Acolyte'),
    ( 10, 'Apprentice of D\'Sparil'),
    ( 13, 'Avatar'),
    (572, 'Banshee'),
    (539, 'Blood Lich'),
    (152, 'Bormereth'),
    (540, 'Boss Shooters'),
    (195, 'Butcher'),
    (914, 'Chainmail Ettin'),
    (551, 'Chaos Wyvern'),
    (433, 'Chiller'),
    (808, 'Crimson Disciple'),
    ( 26, 'Cultist'),
    (286, 'Dark Clink'),
    (468, 'Dark Gargoyle'),
    ( 35, 'Death Knight'),
    (915, 'Demon Wizard'),
    ( 39, 'Disciple'),
    (794, 'Disciple (with melee)'),
    ( 47, 'Ghoul'),
    (745, 'Gold Lich'),
    ( 52, 'Hell Apprentice'),
    ( 58, 'Hell Guard'),
    ( 55, 'Hell Smith'),
    (836, 'Hex Prism'),
    (192, 'Horn Beast'),
    (310, 'Hornet'),
    (726, 'Ice Golem'),
    (573, 'Ice Lich'),
    (470, 'Ice Stalker'),
    ( 62, 'Imp Warlord'),
    (287, 'Inferno Demon'),
    (196, 'Invisible Warrior'),
    (187, 'Knight Archer'),
    (493, 'Lava Demon'),
    (899, 'Lost Spirit'),
    (574, 'Magma Serpent'),
    (687, 'Medusa'),
    (839, 'Nosferati'),
    (747, 'Plague Imp'),
    (846, 'Pyro Succubus'),
    (494, 'Rot Wraith'),
    (321, 'Scimitar'),
    ( 81, 'Sentinel'),
    (293, 'Shadow Beast'),
    ( 95, 'Thor'),
    (810, 'Undead Knight (Dual Axe)'),
    (355, 'Vampire'),
    (103, 'Wraith'),
    (607, 'Zardaz'),
)

_BEASTIARY_STRIFE = (
    (  0, 'Beastiary: Strife Style'),
    (657, 'Black Ops'),
    (604, 'Dark Inquisitor'),
    (570, 'Kull Warrior'),
    (746, 'Mini Sentinel'),
    (338, 'Paladin'),
    (637, 'Prison Guard'),
    (909, 'Rebels Pack'),
)

_BEASTIARY_OTHER = (
    (  0, 'Beastiary: Other Style'),
    ( 14, 'Bat'),
    (436, 'Cheogh'),
    (634, 'Drone'),
    (863, 'Elite Guard'),
    (386, 'Evil Knight'),
    (621, 'Gatekeeper'),
    (469, 'Giant Bat'),
    (709, 'Giant Rat'),
    (336, 'Head Monster'),
    ( 53, 'Hell Hound'),
    ( 54, 'Hell Rose'),
    (149, 'Incubus'),
    (143, 'Infernal Spider'),
    (471, 'Juggernaut'),
    (622, 'Maephisto'),
    (318, 'Moloch'),
    ( 67, 'Netherworld Drone'),
    ( 68, 'Netherworld Queen'),
    (625, 'Pustule'),
    (811, 'Shark'),
    (958, 'Shark with Laser'),
    (813, 'Skeleton'),
    (189, 'Source Guardian'),
    (623, 'Trash Monster'),
)


# ==============================================================================


_ITEMSTORE_POWERUP_ARTIFACTS = (
    (  0, 'Item Store: PowerUps & Artifacts'),
    (391, 'AmmoSphere'),
    (827, 'Ankh of Life'),
    (392, 'Armor Sphere'),
    (399, 'Berserk Sphere'),
    (479, 'BioSphere'),
    (824, 'Blood Amulet'),
    (385, 'Bloodlust Sphere'),
    (711, 'Book of the Dead'),
    (492, 'Boots of the North'),
    (487, 'Bracers of Force'),
    (830, 'Crucifix Rosary'),
    (400, 'Doom Sphere'),
    (416, 'Double Damage Sphere'),
    (480, 'Emerald Amulet'),
    (897, 'Familiar Summon'),
    (370, 'Flight Sphere'),
    (577, 'Guard Sphere'),
    (506, 'Hand of the Wraith'),
    (378, 'Haste Sphere'),
    (535, 'Icon of the Raven'),
    (588, 'Invisibility Sphere'),
    (658, 'Jet Thruster'),
    (367, 'Lich Skull'),
    (537, 'Life Sphere'),
    (868, 'Lifeshield Sphere'),
    (486, 'Mask of Terror'),
    (578, 'Morph Cheddar'),
    (829, 'Mutant Sphere'),
    (850, 'Possession Sphere'),
    (481, 'Potion of Fire Resistance'),
    (412, 'Power Stimpack'),
    (589, 'Rage Sphere'),
    (482, 'Rebreather'),
    (379, 'Regeneration Sphere'),
    (682, 'Resistance Rings'),
    (483, 'Ring of Regeneration'),
    (491, 'Ring of the Owl'),
    (898, 'Ritual Knife'),
    (465, 'Salvation Sphere'),
    (484, 'Scroll of Hellfire'),
    (384, 'Shield Sphere'),
    (380, 'Shrink Sphere'),
    (447, 'Summon Sphere'),
    (713, 'Talisman'),
    (485, 'Talisman of the Depths'),
    (397, 'Terror Sphere'),
    (579, 'Time Freeze Sphere'),
    (673, 'Tome of the Forsaken'),
    (414, 'Tome of the Unholy'),
    (580, 'Turbo Sphere'),
)

_ITEMSTORE_KEYS_PUZZLE = (
    (  0, 'Item Store: Keys & Puzzle'),
    (867, 'Cross Keys'),
    (710, 'Doom 3 Keycards'),
    (955, 'Power Cube'),
    (825, 'Skull Orbs'),
    (826, 'Supply Chest Key'),
    (558, 'Various Doom Keys'),
)

_ITEMSTORE_OTHER = (
    (  0, 'Item Store: Others'),
    (490, 'Adrenaline Kit'),
    (375, 'Ammo Belt'),
    (437, 'Armor Set'),
    (608, 'Armor Shard'),
    (524, 'Beacon'),
    (387, 'Biosuit'),
    (497, 'Blaze Orb'),
    (690, 'Bullet Cartridge'),
    (393, 'Bullet Kit'),
    (442, 'Small Blood Container'),
    (438, 'Large Blood Container'),
    (394, 'Cell Kit'),
    (376, 'Combat Pack'),
    (823, 'Crusader Shield'),
    (498, 'Crystal Gem'),
    (417, 'Deployable Sentry Gun'),
    (957, 'Deployable Shield'),
    (691, 'Electric Bolt Bundle'),
    (787, 'Electric Pod'),
    (860, 'Elemental Gems'),
    (692, 'Energy Kit'),
    (500, 'Ethereal Arrow Bundle'),
    (382, 'Field Kit'),
    (828, 'Flame Turret'),
    (565, 'Flares'),
    (671, 'Food Barrel'),
    (501, 'Greater Mace Sphere'),
    (693, 'HE Grenade Box'),
    (869, 'Jump Boots'),
    (478, 'Heavy Armor'),
    (896, 'Magic Apples'),
    (956, 'Marine Supply Pack'),
    (502, 'Median Runes'),
    (875, 'Medical Backpack'),
    (371, 'Medipack'),
    (377, 'Mega Map'),
    (576, 'Megapack'),
    (694, 'Mini Missile Bundle'),
    (795, 'Missile Pod'),
    (712, 'Oxygen Canister'),
    (439, 'PDA'),
    (695, 'Phosphorus Grenade Box'),
    (696, 'Poison Bolt Bundle'),
    (778, 'Portable Rejuvenation Unit'),
    (656, 'Potion Variants'),
    (499, 'Power Orb'),
    (776, 'Quake Item Pack'),
    (395, 'Rocket Pile'),
    (396, 'Shell Kit'),
    (926, 'Shield Spells'),
    (835, 'Sigil Scroll'),
    (689, 'Spiritual Armor Orb'),
    (840, 'Spring Mine'),
    (628, 'Stim Bonus'),
    (383, 'SuperStim'),
    (930, 'Super Armor Bonus'),
    (566, 'Super Shield'),
    (413, 'Supply Box'),
    (881, 'Swarmers'),
    (489, 'Tech Armor'),
    (831, 'Vitality Serum'),
)


# ==============================================================================


_PROPSTOP_TECHNICAL = (
    (  0, 'Prop Stop: Technical'),
    (450, 'Beach Umbrella'),
    (449, 'Box'),
    (953, 'Breakable Hydrant'),
    (347, 'Broken Lamp'),
    (348, 'Brown Metal Barrel'),
    (349, 'Chair'),
    (780, 'Czech Hedgehog'),
    (503, 'Doom Doll'),
    (351, 'Empty Nukage Barrel'),
    (646, 'Food Pieces'),
    (851, 'Glass Tech Pillars'),
    (352, 'Grey Metal Barrel'),
    (834, 'Junk Piles'),
    (648, 'Lab Glass Pack'),
    (458, 'Marine Stuff'),
    (772, 'Necrodome Barrels'),
    (736, 'Oil Drum'),
    (650, 'Pipe Pack'),
    (782, 'Plasma Globe'),
    (411, 'Radioactive Barrel'),
    (773, 'Sea Mine'),
    (873, 'Specimen Tank'),
    (421, 'Switchable Tech Lamp'),
    (526, 'Tech Barrels'),
    (476, 'Tech Gizmos'),
    (783, 'Tech Gizmos (v2)'),
    (529, 'Toilet'),
    (467, 'Trash Cans'),
    (714, 'UAC Holograms'),
    (364, 'Zapper')
)

_PROPSTOP_VEGETATION = (
    (  0, 'Prop Stop: Vegetation'),
    (917, 'Bushes'),
    (676, 'Cacti'),
    (644, 'Cactus'),
    (832, 'Dead/Swamp Trees'),
    (672, 'Garden Trees'),
    (627, 'Glowing Mushrooms'),
    (792, 'Hell Trees'),
    (610, 'Ice Stalagmites'),
    (632, 'Limestone Cave Formations'),
    (649, 'Liquid Fountains'),
    (613, 'Mushrooms'),
    (771, 'Necrodome Rocks'),
    (678, 'Palm Trees'),
    (797, 'Palm Trees (burnt)'),
    (466, 'Phobos Rocks'),
    (587, 'Root Pack'),
    (624, 'Seaweed'),
    (527, 'Skull Tree'),
    (679, 'Small Trees and Bushes'),
    (528, 'Stalagmites and Stalactite'),
    (562, 'Winter Tree Spawner'),
)

_PROPSTOP_LIGHT_SOURCES = (
    (  0, 'Prop Stop: Light Sources'),
    (819, 'Black Torch'),
    (784, 'Bronze Lamps'),
    (801, 'Candle Color Variations'),
    (586, 'Ceiling Lamp'),
    (517, 'Chandelier Pack'),
    (715, 'Doom64 Lamps'),
    (699, 'Doom64 Torches'),
    (871, 'Fire Bowl'),
    (820, 'Firewood'),
    (821, 'Golden Eagle Statue'),
    (357, 'Grey Lamp'),
    (549, 'Lamps'),
    (611, 'Lava Cauldron'),
    (647, 'Light Column Variations'),
    (920, 'Marble Brazier'),
    (563, 'Roof Lights'),
    (614, 'Serpent Braziers'),
    (398, 'Skull Lamp'),
    (615, 'Stone Torch'),
    (887, 'Strife Columns'),
    (716, 'Strobe Lights'),
    (459, 'Torch Variations'),
    (700, 'Doom Wall Torches'),
    (363, 'Yellow Lamp'),
)

_PROPSTOP_GORE_CORPSES = (
    (  0, 'Prop Stop: Gore & Corpses'),
    (353, 'Bloody Chain (PSX Doom)'),
    (365, 'Bloody Heads'),
    (619, 'Bone Pile'),
    (789, 'Bound Marines'),
    (356, 'Brown Scientist Carcass'),
    (643, 'Burning Corpses'),
    (544, 'Burning Corpse'),
    (918, 'Corpse Pile'),
    (443, 'Cow Skulls'),
    (545, 'Crucified Corpses'),
    (519, 'Cyberdemon Gore'),
    (530, 'Daisy Scenes'),
    (595, 'Dead Corvus'),
    (461, 'Dead General'),
    (701, 'Dead Scientists'),
    (350, 'Demonic Arm'),
    (546, 'Devilish Bust'),
    (854, 'Gore Decorations'),
    (446, 'Gore Pack'),
    (358, 'Half Cut Soldier Carcass'),
    (464, 'Hanged Bloody Skeleton'),
    (359, 'Hanged Imps'),
    (455, 'Hanged Marines'),
    (431, 'Hanged Player'),
    (584, 'Hanging Corpse Pack'),
    (729, 'Hanging Duke'),
    (785, 'Hanging Marine Meat'),
    (531, 'Hanging Marines'),
    (781, 'Hanging Marines 2'),
    (919, 'Hanging Wizard Corpse'),
    (360, 'Head Sticks'),
    (366, 'Imp Stick'),
    (547, 'Impaled Corpses'),
    (906, 'Impaled Dog Heads'),
    (504, 'Impaled Marines'),
    (405, 'Impaled Rocket Guy'),
    (822, 'Impaled Scientists'),
    (441, 'Marine Corpses'),
    (538, 'Marine Victim'),
    (440, 'Monster Head'),
    (681, 'Radioactive Corpses'),
    (361, 'Shirtless Beheaded Marine'),
    (362, 'Shirtless Marine Carcass'),
    (818, 'Shootable Impaled Humans'),
    (420, 'Sitting Corpses'),
    (463, 'Skeleton'),
    (564, 'Skewered Corpses'),
    (786, 'Skulltag Gore'),
    (525, 'Torn Corpse'),
    (424, 'Tortured Baron'),
    (548, 'Upside Down Corpses'),
    (727, 'Wolfenstein Gore'),
)

_PROPSTOP_HELL_MAGIC = (
    (  0, 'Prop Stop: Hell & Magic'),
    (728, 'Banners'),
    (345, 'Bible'),
    (346, 'Bloody Chalice'),
    (677, 'Ceramic Pottery'),
    (959, 'Chaos Sphere'),
    (882, 'Crow'),
    (616, 'D\'Sparil Statue'),
    (583, 'Doom Statues'),
    (462, 'Evil Eye Variations'),
    (734, 'Fire Pillars (Doom)'),
    (735, 'Fire Pillars (Hexen)'),
    (645, 'Flesh Pillar'),
    (905, 'Flesh Pods'),
    (617, 'Gold Stand Gizmos'),
    (474, 'Hell Gizmos'),
    (418, 'Hell Growth'),
    (660, 'Hell Pillars'),
    (475, 'Heretic Gizmos'),
    (698, 'Marble Columns'),
    (883, 'Marble Urn'),
    (833, 'Necrodome Tombstones'),
    (737, 'Pillar Gizmos'),
    (856, 'Rune Skull Pillars'),
    (651, 'Skull Candle'),
    (872, 'Small Key Gizmos'),
    (680, 'Stone Heads'),
    (702, 'Strife Bloody Columns'),
    (354, 'Tentacle Barrier'),
    (861, 'Warrior Statue'),
)


# ==============================================================================


_SFX_SHOPPE_ELEMENTALFX = (
    (  0, 'SFX Shoppe: Elemental Effects'),
    (335, 'Bubble Boiling'),
    (306, 'Clouds'),
    (-847, 'Doom Terrain Splashes'), # no standalone actors
    (278, 'Ember'),
    (280, 'Fire'),
    (791, 'Fog'),
    (708, 'Lavaball'),
    (279, 'Sparks'),
    (276, 'Steam'),
    (303, 'Thunder FX'),
    (665, 'Thunder Portal'),
    (904, 'Toxic Clouds'),
    (667, 'Underwater Bubbles'),
)

_SFX_SHOPPE_PARTICLES = (
    (  0, 'SFX Shoppe: Particle Spawners'),
    (668, 'Casing Spawners'),
    (662, 'Forcefield Laserbeams'),
    (925, 'Fountain of Rejuvenation'),
    (664, 'Magic Sparkle'),
    (889, 'Pond Frogs'),
    (663, 'PowerRing Pads'),
    (703, 'Scurrying Rats'),
    (721, 'Soul Spawners'),
    (277, 'Sparkle Spawners'),
    (197, 'Stronghold PowerPad'),
    (799, 'Swarm Spawner'),
    (870, 'Teleport Smoke Spawner'),
)

_SFX_SHOPPE_WEATHER = (
    (  0, 'SFX Shoppe: Weather Generators'),
    (666, 'Ash Spawner'),
    (707, 'Cinder'),
    (275, 'Rain Simple'),
    (198, 'Snow Simple'),
)

# ==============================================================================


def content():
    # the following notation allows simple repository customization
    result = []

    result += _ARMORY_DOOM
    result += _ARMORY_HERETIC_HEXEN
    result += _ARMORY_OTHER

    result += _BEASTIARY_DOOM
    result += _BEASTIARY_HERETIC_HEXEN
    result += _BEASTIARY_STRIFE
    result += _BEASTIARY_OTHER

    result += _ITEMSTORE_POWERUP_ARTIFACTS
    result += _ITEMSTORE_KEYS_PUZZLE if utils.is_aaa() else ()
    result += _ITEMSTORE_OTHER

    if utils.is_aaa():
        result += _PROPSTOP_TECHNICAL
        result += _PROPSTOP_VEGETATION
        result += _PROPSTOP_LIGHT_SOURCES
        result += _PROPSTOP_GORE_CORPSES
        result += _PROPSTOP_HELL_MAGIC

        result += _SFX_SHOPPE_ELEMENTALFX
        result += _SFX_SHOPPE_PARTICLES
        result += _SFX_SHOPPE_WEATHER

    return result


# ==============================================================================


def _cis(*args):
    return case_insensitive.CaseInsensitiveSet(args)


def excluded_wads():
    return {
        143: _cis('InfernalSpider (Jumping).wad'),
        243: _cis('UnmakerCentered.wad'),
        258: _cis('PolyMorph (old version).wad'),
        645: _cis('FleshPillarTestMap01.wad'),
        662: _cis('Demo.wad'),
        663: _cis('Demo.wad'),
        664: _cis('Demo.wad', 'SparkleFX_heretic.wad'), # or SparkleFX_doom.wad
        667: _cis('BubbleTestMap.wad'),
        703: _cis('ratTest.wad'),
        711: _cis('BrightBook.pk3'), # TODO: merge brightmaps with asset WAD
        716: _cis('StrobeTest.wad'),
        717: _cis('StrifeLandMine.wad'),
        721: _cis('testmap01.wad'),
        799: _cis('Swarm Test.wad'),
        816: _cis('CryoPal.wad'),
        825: _cis('SkullOrbsDemoMap.wad'),
        826: _cis('SupplyChestKeyDemoMap.wad'),
        827: _cis('AnkhOfLife (Upgradeable).wad'), # or 'AnkhOfLife (Map Duration).wad'
        867: _cis('Crosses.wad', 'Crosses3.wad'),  # or 'Crosses2.wad'
        897: _cis('FamiliarSummon (Sphere).wad'),  # or 'FamiliarSummon (Scroll).wad'
        925: _cis('demomaps.wad'),
        955: _cis('PowerCubeDemoMap.wad'),
    }
