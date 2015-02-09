### Known issues

|ID |Name | Issue |
|---|-----|-------|
|~~243~~|~~Unmaker~~|~~DECORATE classes and sprite names confict between centered and angled versions WADs~~ Centered version was excluded|
|236, 266|Flare Gun, Napalm Launcher|The same `actor NapalmDebris` is used by both weapons. Causes _Tried to register class 'NapalmDebris' more than once_ error|
|313, 659|Plasma Bolter, Pulse Rifle UAC|The same `actor PlasmaBolterShot1` and `actor PlasmaBolterShot1Trail` are used by both weapons. Causes _Tried to register class '...' more than once_ errors|
|444, 510|Necronomicon, Vile Staff|The same `actor Darkmana` is used by both weapons. Causes _Tried to register class 'Darkmana' more than once_ error|
|496, 560|Nailgun (MG), Nailgun (SG)|The same `actor Nail` is used by both weapons. Causes _Tried to register class 'Nails' more than once_ error|
|510|Vile Staff|The weapon doesn't spawn projectile nor cause any damage. Is it broken?|
|511|Lightbringer|Missing actor reference in `GLDEFS`. Causes _Warning: dynamic lights attached to non-existent actor SunProjectile1_|
|522, 659|Pulse Rifle, Pulse Rifle UAC|Both assets share the same filename `PulseRifle.wad`, although they work correctly. Python warning is issued during `.pk3` generation|
|536|Jackbomb|Missing actor references in `GLDEFS`. Causes multiple _Warning: dynamic lights attached to non-existent actor ..._|
|541, 543|Flamethrower, UTNT Pyro-Cannon|The same `actor Gas` and `actor BigGas` are used by both weapons. Causes _Tried to register class '...' more than once_ errors|
|~~717~~|~~LandMine Layer~~|~~DECORATE classes and sprite names confict between WADs for Doom and for Strife. Causes multiple _Tried to register class '...' more than once_ errors~~ Strife version was excluded|
|874, 876|BFG 2704, Spray Cannon|_Almost_ the same `actor 2704Ball` and `actor 2704Ball2` are used by both weapons, different by obituary message only. Causes _Tried to register class '...' more than once_ errors and wrong obituary message for one of the weapons|
|926|Shield Spells|DECORATE classes and sprite names confict between Scroll and Sphere WADs|

### Duplicate lump names, weapons only
|Name|WAD Files|Comments|
|---|---|---|
|~~AGASA0~~|~~Flamethrower.wad, UTNTPyroCannon.wad~~|The same sprite saved with different PNG settings|
|~~AGASB0~~|~~Flamethrower.wad, UTNTPyroCannon.wad~~|_same as above_|
|~~ANIME0~~|~~SawedOff.wad, SawedOff.wad~~|Sprites with different weapon shift in firing state|
|~~ANIMF0~~|~~SawedOff.wad, SawedOff.wad~~|_same as above_|
|~~ANIMG0~~|~~SawedOff.wad, SawedOff.wad~~|_same as above_|
|~~AXE~~|~~Axe.wad, Axe.wad~~|Compiled ACS and its source code in different namespaces|
|~~BOLTA0~~|~~PlasmaBolter.wad, TeslaCannon.wad~~|Renamed Tesla Cannon ammo sprite|
|~~BXPLL0~~|~~CryoBow.wad, PlasmaBallista.wad~~|The same sprite with different PNG binary layout|
|~~BXPLM0~~|~~CryoBow.wad, PlasmaBallista.wad~~|_same as above_|
|~~COLTA0~~|~~Colt45.wad, Reaper.wad~~|Renamed Reaper sprite|
|~~COLTB0~~|~~Colt45.wad, Reaper.wad~~|_same as above_|
|~~COLTC0~~|~~Colt45.wad, Reaper.wad~~|_same as above_|
|~~COTSFPO~~|~~CultStaff.WAD, CultStaff.WAD~~|Similar sounds with the same name|
|~~CREDIT~~|~~!DOOM.WAD, !DOOM2.WAD, !PLUTONIA.WAD, !TNT.WAD, SuperCrossbow.wad~~|Informational text, lump removed|
|~~DEVGN0~~|~~Devastators.wad, Devastators.wad~~|Sprites with different weapon shift in firing state|
|DSDBCLS|!DOOM2.WAD, !PLUTONIA.WAD, !TNT.WAD, Doom3SSG.wad||
|DSDBLOAD|!DOOM2.WAD, !PLUTONIA.WAD, !TNT.WAD, Doom3SSG.wad||
|DSDBOPN|!DOOM2.WAD, !PLUTONIA.WAD, !TNT.WAD, Doom3SSG.wad||
|DSDSHTGN|!DOOM2.WAD, !PLUTONIA.WAD, !TNT.WAD, Doom3SSG.wad||
|~~DSMINIGN~~|~~Minigun.wad, UberMinigun.wad~~|Renamed Minigun sound|
|~~EXP2A0~~|~~Deviation.wad, SeekerBazooka.wad~~|Renamed Seeker Bazooka and Napalm Launcher sprites|
|~~EXP2B0~~|~~Deviation.wad, SeekerBazooka.wad~~|_same as above_|
|~~EXP2C0~~|~~Deviation.wad, SeekerBazooka.wad~~|_same as above_|
|~~EXP2D0~~|~~Deviation.wad, SeekerBazooka.wad~~|_same as above_|
|~~EXP2E0~~|~~Deviation.wad, SeekerBazooka.wad~~|_same as above_|
|~~EXP2F0~~|~~Deviation.wad, SeekerBazooka.wad~~|_same as above_|
|~~EXP2G0~~|~~Deviation.wad, SeekerBazooka.wad~~|_same as above_|
|~~EXP2H0~~|~~Deviation.wad, SeekerBazooka.wad~~|_same as above_|
|~~EXP2I0~~|~~Deviation.wad, SeekerBazooka.wad~~|_same as above_|
|~~EXP2J0~~|~~Deviation.wad, SeekerBazooka.wad~~|_same as above_|
|~~EXP2K0~~|~~Deviation.wad, SeekerBazooka.wad~~|_same as above_|
|~~EXP2L0~~|~~Deviation.wad, SeekerBazooka.wad~~|_same as above_|
|~~EXP2M0~~|~~Deviation.wad, SeekerBazooka.wad~~|_same as above_|
|~~EXP2N0~~|~~Deviation.wad, SeekerBazooka.wad~~|_same as above_|
|~~EXP3A0~~|~~jackbomb.wad, SeekerBazooka.wad~~|Renamed Seeker Bazooka Launcher sprite|
|~~EXP3B0~~|~~jackbomb.wad, SeekerBazooka.wad~~|_same as above_|
|~~EXP3C0~~|~~jackbomb.wad, SeekerBazooka.wad~~|_same as above_|
|~~EXP3D0~~|~~jackbomb.wad, SeekerBazooka.wad~~|_same as above_|
|~~EXP3E0~~|~~jackbomb.wad, SeekerBazooka.wad~~|_same as above_|
|~~EXP3F0~~|~~jackbomb.wad, SeekerBazooka.wad~~|_same as above_|
|~~EXP3G0~~|~~jackbomb.wad, SeekerBazooka.wad~~|_same as above_|
|~~EXP3H0~~|~~jackbomb.wad, SeekerBazooka.wad~~|_same as above_|
|~~EXP3I0~~|~~jackbomb.wad, SeekerBazooka.wad~~|_same as above_|
|~~EXP3J0~~|~~jackbomb.wad, SeekerBazooka.wad~~|_same as above_|
|~~EXP3K0~~|~~jackbomb.wad, SeekerBazooka.wad~~|_same as above_|
|~~EXP3L0~~|~~jackbomb.wad, SeekerBazooka.wad~~|_same as above_|
|~~EXP3M0~~|~~jackbomb.wad, SeekerBazooka.wad~~|_same as above_|
|~~EXP3N0~~|~~jackbomb.wad, SeekerBazooka.wad~~|_same as above_|
|~~EXP3O0~~|~~jackbomb.wad, SeekerBazooka.wad~~|_same as above_|
|~~EXP3P0~~|~~jackbomb.wad, SeekerBazooka.wad~~|_same as above_|
|~~EXP3Q0~~|~~jackbomb.wad, SeekerBazooka.wad~~|_same as above_|
|~~EXP3R0~~|~~jackbomb.wad, SeekerBazooka.wad~~|_same as above_|
|~~EXP3S0~~|~~jackbomb.wad, SeekerBazooka.wad~~|_same as above_|
|~~EXP3T0~~|~~jackbomb.wad, SeekerBazooka.wad~~|_same as above_|
|~~EXP3U0~~|~~jackbomb.wad, SeekerBazooka.wad~~|_same as above_|
|~~EXP3V0~~|~~jackbomb.wad, SeekerBazooka.wad~~|_same as above_|
|~~EXP3W0~~|~~jackbomb.wad, SeekerBazooka.wad~~|_same as above_|
|~~EXP3X0~~|~~jackbomb.wad, SeekerBazooka.wad~~|_same as above_|
|~~EXP3Y0~~|~~jackbomb.wad, SeekerBazooka.wad~~|_same as above_|
|~~EXP3Z0~~|~~jackbomb.wad, SeekerBazooka.wad~~|_same as above_|
|~~FLMEA0~~|~~Flamethrower.wad, UTNTPyroCannon.wad~~|The same sprite saved with different PNG settings|
|~~FLMEB0~~|~~Flamethrower.wad, UTNTPyroCannon.wad~~|_same as above_|
|~~FLMEC0~~|~~Flamethrower.wad, UTNTPyroCannon.wad~~|_same as above_|
|~~FLMED0~~|~~Flamethrower.wad, UTNTPyroCannon.wad~~|_same as above_|
|~~FLMEE0~~|~~Flamethrower.wad, UTNTPyroCannon.wad~~|_same as above_|
|~~FLMEF0~~|~~Flamethrower.wad, UTNTPyroCannon.wad~~|_same as above_|
|~~FLMEG0~~|~~Flamethrower.wad, UTNTPyroCannon.wad~~|_same as above_|
|~~FLMEH0~~|~~Flamethrower.wad, UTNTPyroCannon.wad~~|_same as above_|
|~~FLMEI0~~|~~Flamethrower.wad, UTNTPyroCannon.wad~~|_same as above_|
|~~FLMEJ0~~|~~Flamethrower.wad, UTNTPyroCannon.wad~~|_same as above_|
|~~FLMEK0~~|~~Flamethrower.wad, UTNTPyroCannon.wad~~|_same as above_|
|~~FLMEL0~~|~~Flamethrower.wad, UTNTPyroCannon.wad~~|_same as above_|
|~~FLMEM0~~|~~Flamethrower.wad, UTNTPyroCannon.wad~~|_same as above_|
|~~FLMEN0~~|~~Flamethrower.wad, UTNTPyroCannon.wad~~|_same as above_|
|~~FRFXA0~~|~~Flamethrower.wad, UTNTPyroCannon.wad~~|_same as above_|
|~~FRFXB0~~|~~Flamethrower.wad, UTNTPyroCannon.wad~~|_same as above_|
|~~FRFXC0~~|~~Flamethrower.wad, UTNTPyroCannon.wad~~|_same as above_|
|~~FRFXD0~~|~~Flamethrower.wad, UTNTPyroCannon.wad~~|_same as above_|
|~~FRFXE0~~|~~Flamethrower.wad, UTNTPyroCannon.wad~~|_same as above_|
|~~FRFXF0~~|~~Flamethrower.wad, UTNTPyroCannon.wad~~|_same as above_|
|~~FRFXG0~~|~~Flamethrower.wad, UTNTPyroCannon.wad~~|_same as above_|
|~~FRFXH0~~|~~Flamethrower.wad, UTNTPyroCannon.wad~~|_same as above_|
|~~FRFXI0~~|~~Flamethrower.wad, UTNTPyroCannon.wad~~|_same as above_|
|~~FRFXJ0~~|~~Flamethrower.wad, UTNTPyroCannon.wad~~|_same as above_|
|~~FRFXK0~~|~~Flamethrower.wad, UTNTPyroCannon.wad~~|_same as above_|
|~~FRFXL0~~|~~Flamethrower.wad, UTNTPyroCannon.wad~~|_same as above_|
|~~FRFXM0~~|~~Flamethrower.wad, UTNTPyroCannon.wad~~|_same as above_|
|~~FRFXN0~~|~~Flamethrower.wad, UTNTPyroCannon.wad~~|_same as above_|
|~~FRFXO0~~|~~Flamethrower.wad, UTNTPyroCannon.wad~~|_same as above_|
|GLAUA0|GrenadeLauncher(KDiZD).wad, GrenadeLauncher.wad||
|GRNDA1|GrenadeLauncher(KDiZD).wad, M79.wad||
|GRNDA5|GrenadeLauncher(KDiZD).wad, M79.wad||
|GRNDA6A4|GrenadeLauncher(KDiZD).wad, M79.wad||
|GRNDA7A3|GrenadeLauncher(KDiZD).wad, M79.wad||
|GRNDA8A2|GrenadeLauncher(KDiZD).wad, M79.wad||
|HNDGI0|Ammo satchels.wad, HandGrenade.wad||
|HNDGJ0|Ammo satchels.wad, HandGrenade.wad||
|HNDGK0|Ammo satchels.wad, HandGrenade.wad||
|HNDGL0|Ammo satchels.wad, HandGrenade.wad||
|HNDGM0|Ammo satchels.wad, HandGrenade.wad||
|HNDGN0|Ammo satchels.wad, HandGrenade.wad||
|HNDGO0|Ammo satchels.wad, HandGrenade.wad||
|HNDGP0|Ammo satchels.wad, HandGrenade.wad||
|LANGUAGE|Arbalest.wad, CryoBow.wad||
|MISLA1|!DOOM.WAD, !DOOM2.WAD, !PLUTONIA.WAD, !TNT.WAD, Deviation.wad||
|MISLA5|!DOOM.WAD, !DOOM2.WAD, !PLUTONIA.WAD, !TNT.WAD, Deviation.wad||
|MISLA6A4|!DOOM.WAD, !DOOM2.WAD, !PLUTONIA.WAD, !TNT.WAD, Deviation.wad||
|MISLA7A3|!DOOM.WAD, !DOOM2.WAD, !PLUTONIA.WAD, !TNT.WAD, Deviation.wad||
|MISLA8A2|!DOOM.WAD, !DOOM2.WAD, !PLUTONIA.WAD, !TNT.WAD, Deviation.wad||
|~~NBOXA0~~|~~Nailgun(SG).wad, PulseNailgun.wad~~|Renamed Pulse Nailgun sprite|
|~~PYXPO0~~|~~UTNTPyroCannon.wad, UTNTPyroCannon.wad~~|Different frame of explosion animation with the same name|
|~~RELOADIN~~|~~Drummle.wad, Enforcer(Pistol).wad~~|Alternative DECORATE lump, unused by engine|
|~~REVII0~~|~~Necronomicon.wad, VileStaff.wad~~|The same sprite saved with different PNG settings|
|SGN2A0|!DOOM2.WAD, !PLUTONIA.WAD, !TNT.WAD, Doom3SSG.wad||
|SMRTA0|!DOOM.WAD, !DOOM2.WAD, !PLUTONIA.WAD, !TNT.WAD, SmartGun.wad||
|SMRTB0|!DOOM.WAD, !DOOM2.WAD, !PLUTONIA.WAD, !TNT.WAD, SmartGun.wad||
|SMRTC0|!DOOM.WAD, !DOOM2.WAD, !PLUTONIA.WAD, !TNT.WAD, SmartGun.wad||
|SMRTD0|!DOOM.WAD, !DOOM2.WAD, !PLUTONIA.WAD, !TNT.WAD, SmartGun.wad||
|SPAFA0|SPAS-12.wad, SwatShotgun.wad||
|SPASA0|SPAS-12.wad, SwatShotgun.wad||
|SPIKB0|NailGun.wad, SkullStaff.wad||
|~~UPDATES~~|~~BioPipebombLauncher.wad, Glock18.wad~~|Informational text, unused by engine|
