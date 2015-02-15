### Known issues

|ID |Name | Issue |
|---|-----|-------|
|243|Unmaker|DECORATE classes and sprite names confict between Angled and Centered versions. The latter was excluded|
|258|Poly Morph|DECORATE classes and sprite names confict between New and Old versions. The latter was excluded|
|236, 266|Flare Gun, Napalm Launcher|The same `actor NapalmDebris` is used by both weapons. Causes _Tried to register class 'NapalmDebris' more than once_ warning|
|313, 659|Plasma Bolter, Pulse Rifle UAC|The same `actor PlasmaBolterShot1` and `actor PlasmaBolterShot1Trail` are used by both weapons. Causes _Tried to register class '...' more than once_ warnings|
|444, 510|Necronomicon, Vile Staff|The same `actor Darkmana` is used by both weapons. Causes _Tried to register class 'Darkmana' more than once_ warning|
|496, 560|Nailgun (MG), Nailgun (SG)|The same `actor Nail` is used by both weapons. Causes _Tried to register class 'Nails' more than once_ warning|
|510|Vile Staff|The weapon doesn't spawn projectile nor cause any damage. Is it broken?|
|511|Lightbringer|Missing actor reference in `GLDEFS`. Causes _Warning: dynamic lights attached to non-existent actor SunProjectile1_ warning|
|536|Jackbomb|Missing actor references in `GLDEFS`. Causes multiple _Warning: dynamic lights attached to non-existent actor ..._ warnings|
|541, 543|Flamethrower, UTNT Pyro-Cannon|The same `actor Gas` and `actor BigGas` are used by both weapons. Causes _Tried to register class '...' more than once_ warnings|
|717|LandMine Layer|DECORATE classes and sprite names confict between WADs for Doom and for Strife. Strife version was excluded|
|874, 876|BFG 2704, Spray Cannon|_Almost_ the same `actor 2704Ball` and `actor 2704Ball2` are used by both weapons, different by obituary message only. Causes _Tried to register class '...' more than once_ warnings and wrong obituary message for one of the weapons|
|816|CryoBow|Custom palette is used. It's excluded from generated .pk3|
|827|Ankh of Life|Various conflicts between Map Duration and Upgradeable version. The latter was excluded|
|867|Cross Keys|DECORATE classes and sprite names confict between three key sets. Only one is kept|
|897|Familiar Summon|DECORATE classes and sprite names confict between Scroll and Sphere WADs. Sphere version was excluded|

### Duplicate lump names
|Name|WAD Files|Comments|
|---|---|---|
|BETAFIRE|BFG2704.wad, SprayCannon.wad|The same file|
|DSMCGUNF|Heavy Machinegun.wad, Light Machinegun.wad|The same file|
|FKITUSE|FieldKit.wad, MedicalBackpack.wad|The same file|
|FLECH4|Large Blood Container.wad, Small Blood Container.wad|The same file|
|FMTRFLAM|Flamethrower.wad, UTNTPyroCannon.wad|The same file|
|LANGUAGE|Arbalest.wad, CryoBow.wad, MorphCheddar.wad|It is correct to have LANGUAGE lumps in different WADs. Content from all files are used|
|LOCKDEFS|Crosses2.wad, d3keycards.wad, VariousKeysUpdated.wad|It is correct to have LANGUAGE lumps in different WADs. Content from all files are used. Although lock numbers must be adjusted to use these keys in levels|
|NAILFLY|Nailgun(MG).wad, Nailgun(SG).wad|The same file|
|NAILHIT|ImpalerXBow.wad, Nailgun(MG).wad, Nailgun(SG).wad|The same file|
|NAILHTBD|ImpalerXBow.wad, Nailgun(MG).wad, Nailgun(SG).wad|The same file|
|RELOADIN|Drummle.wad, Enforcer(Pistol).wad|Alternative DECORATE lumps, unused by engine|
|SCOLTFIR|Reaper.wad, SuppressedMP5.wad|The same file|
|UPDATES|BioPipebombLauncher.wad, Glock18.wad, PossessionSphere.wad|Informational text file, unused by engine|
