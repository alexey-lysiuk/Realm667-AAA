### Known issues

|ID |Name | Issue |
|---|-----|-------|
|143|Infernal Spider|Various conficts between Regular and Jumping versions. The latter was excluded|
|243|Unmaker|Various conficts between Angled and Centered versions. The latter was excluded|
|258|Poly Morph|Various conficts between New and Old versions. The latter was excluded|
|510|Vile Staff|The weapon doesn't spawn projectile nor cause any damage. Is it broken?|
|511|Lightbringer|Missing actor reference in `GLDEFS`. Causes _Warning: dynamic lights attached to non-existent actor SunProjectile1_ warning|
|536|Jackbomb|Missing actor references in `GLDEFS`. Causes multiple _Warning: dynamic lights attached to non-existent actor ..._ warnings|
|717|LandMine Layer|Various conficts between WADs for Doom and for Strife. Strife version was excluded|
|816|CryoBow|Custom palette is used, stored in separate WAD file. It's excluded from generated .pk3|
|827|Ankh of Life|Various conflicts between Map Duration and Upgradeable version. The latter was excluded|
|867|Cross Keys|Various conflicts between three key sets. Only one is kept|
|897|Familiar Summon|Various conflicts between Scroll and Sphere WADs. Sphere version was excluded|

### Lump names collisions
|Name|WAD Files|Comments|
|---|---|---|
|DSDASH|HellApprentice.WAD, Hellsmith.WAD||
|DSFIRSHT|!DOOM.WAD, !DOOM2.WAD, !PLUTONIA.WAD, !TNT.WAD, PlasmaDemon.wad||
|DSFIRXPL|!DOOM.WAD, !DOOM2.WAD, !PLUTONIA.WAD, !TNT.WAD, PlasmaDemon.wad||
|SCRIPTS|Hangman.wad, OxygenCanister.wad|ACS source code, unused by engine|
|STEP2|!DOOM.WAD, !DOOM2.WAD, !PLUTONIA.WAD, !TNT.WAD, DarkInquisitor.wad|Works fine, lumps are from different namespaces|

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
