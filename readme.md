![Realm667 Logo](header.jpg)
## Realm667 - An Awesome Awesomeness
##### Weapons/monsters/powerups/props/effects collection for (G)ZDoom
#### About

This project is an attempt to _automatically_ combine all assets from www.realm667.com repository in a single package.  
Almost all actors (weapons, monsters, powerups, props, effects) are included.  
  
The single goal of this project is to showcase goodies available to creators of ZDoom-based projects.

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

Users of the alternative HUD can set **HUD options >> Alternative HUD >> Show ammo for** option to **Available weapons** in order to fit the ammo column into the screen.

#### How to build

You need [Python 2.7](https://www.python.org/downloads/release/python-279/) to run `build.py` script. Versions 3.2 and above are also supported but not recommended. The recent versions of Linux and OS X come with Python pre-installed. Make sure that you have required version by executing `python -V` command in the terminal.  
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

#### Credits

* Authors who contributed their work to the Realm667 Repository. Check individual asset's credits on the [web site](http://www.realm667.com)
* Realm667 staff and Daniel Gimmer (Tormentor667) in particular for collecting everything in one place
* Randy Heit et al. for ZDoom
* Christoph Oelckers (Graf Zahl) for GZDoom
* Guido van Rossum (BDFL) at al. for Python
* Jared Stafford (jspenguin) for doomwad module
* Marko Kreen for rarfile module
* David Jones (drj11) for PyPNG module
* Igor Pavlov for 7-Zip archiver and LZMA
* Alexander Roshal for RAR archiver

#### Links

###### Realm 667
* [Website](http://realm667.com)

###### ZDoom
* [Website](http://zdoom.org)
* [Development Builds](http://devbuilds.drdteam.org/zdoom)
* [Forums](http://forum.zdoom.org)
* [Wiki](http://zdoom.org/wiki)

###### GZDoom
* [Website](http://gzdoom.drdteam.org/)
* [Development Builds](http://devbuilds.drdteam.org/gzdoom)
* [Forums](http://forum.drdteam.org/viewforum.php?f=22)
* [Wiki](http://zdoom.org/wiki/Category:GZDoom_features)
