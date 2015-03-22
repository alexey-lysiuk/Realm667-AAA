![Realm667 Logo](http://realm667.com/images/modules/header/header_general.jpg)
## Realm667 - An Awesome Awesomeness
##### Weapons/monsters/powerups/props/effects collection for (G)ZDoom
#### About

This project is an attempt to _automatically_ combine all assets from www.realm667.com repository in a single package.  
Almost all actors (weapons, monsters, powerups, props, effects) are included.

#### How to play

Load `realm667-aaa.pk3` (or `realm667-aaa.pk7`, if available) in the recent build of ZDoom ([Windows](http://devbuilds.drdteam.org/zdoom/) / [OS X](http://devbuilds.drdteam.org/zdoom-mac/)) or GZDoom ([Windows](http://devbuilds.drdteam.org/gzdoom/) / [OS X](https://github.com/alexey-lysiuk/gzdoom/releases)):  
`zdoom -iwad doom2 -file realm667-aaa.pk3`  
There is no restriction on IWAD, but most of assets are designed to work with Doom II.  
  
Open **Realm667 - Armory** menu ('H' button by default) to summon weapons.  
Open **Realm667 - Beastiary** menu ('J' button by default) to summon monsters. Here you can change your affiliation with monsters.  
Open **Realm667 - Item Store** menu ('N' button by default) to summon power-up, keys and other inventory items.  
Open **Realm667 - Prop Stop / SFX Shoppe** menu ('B' button by default) to summon various decorations and effects (on the second page).  
Use 'U' button (by default) to summon the last summoned actor again.
The key bindings can be changed in **Customize Controls** menu. Look for **Realm667 - An Awesome Awesomeness** at the bottom of the controls list.

**Note:** Do not expect that all assets will work in any game supported by (G)ZDoom. Use Doom II for maximum compatibility. Also, check `issues.md` file for the list of known issues.


#### How to build

You need [Python 2.7](https://www.python.org/downloads/release/python-279/) to run `build.py` script. The recent versions of Linux and OS X come with Python pre-installed. Make sure that you have version 2.7.x and not 3.x by executing `python --version` command in the terminal.  
The script will create `realm667-aaa.pk3` (or `realm667-aaa.pk7`, depending on command line options) in the repository's root directory.  
The script will download and cache all resources during the first run. Generation process will be much faster next time.  
  
Also, you can clone [an accompanied repository](https://github.com/alexey-lysiuk/Realm667-AAA-Cache) into `cache` directory to avoid downloading. In this case, the whole process will look like:
```
git clone https://github.com/alexey-lysiuk/Realm667-AAA.git
cd Realm667-AAA
git clone https://github.com/alexey-lysiuk/Realm667-AAA-Cache.git cache
python build.py
```
Use `--help` command line switch for the list of available options.  
Intel-based Windows, Linux and OS X are supported at full extent. Compression via 7-Zip and handling of assets packed with RAR are not available on other platforms.
