### Known issues
|ID |Name | Issue |
|---|-----|-------|
|143|Infernal Spider|Various conficts between Regular and Jumping versions. The latter was excluded|
|243|Unmaker|Various conficts between Angled and Centered versions. The latter was excluded|
|258|Poly Morph|Various conficts between New and Old versions. The latter was excluded|
|664|Magic Sparkle|Various conficts (including usage of Heretic palette) between WADs for Doom and for Heretic. Heretic version was excluded|
|717|LandMine Layer|Various conficts between WADs for Doom and for Strife. Strife version was excluded|
|816|CryoBow|Custom palette is used, stored in separate WAD file. It's excluded from generated .pk3|
|827|Ankh of Life|Various conflicts between Map Duration and Upgradeable version. The latter was excluded|
|847|Doom Terrain Splashes|No standalone actors, excluded|
|867|Cross Keys|Various conflicts between three key sets. Only one is kept|
|897|Familiar Summon|Various conflicts between Scroll and Sphere WADs. Sphere version was excluded|

### Lump names collisions
|Lump|WAD Files|Comments|
|---|---|---|
|BURN|HERETIC.WAD, Lavademon.wad|The same sound|
|GNTPOW|HERETIC.WAD, HEXEN.WAD, LighteningRod.wad|The same sound|
|SORRISE|HERETIC.WAD, ApprenticeOfDsparil.wad|The same sound|
|TLMPE0|DOOM2.WAD, TNT.WAD, PLUTONIA.WAD, Switchable Tech Lamp.wad|Intentional extension of sprite from Doom II and Final Doom IWADs|

### Clearing of player classes
|ID|Name|
|---|----|
|465|Salvation Sphere|
|509|Prox Launcher|
|536|Jackbomb|
|539|Blood Lich|
|552|Hierophant|
The assets from the table above contain `KEYCONF` lump with `clearplayerclasses` command. This command causes an issue when player class added after it doesn't match the current game, e.g. Doom player class in Heretic. Such `KEYCONF` lumps are removed during package generation.  
_**TODO:** actors may depend on new player classes and may work incorrectly without it._
