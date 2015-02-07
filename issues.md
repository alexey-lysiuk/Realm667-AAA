### Known issues

|ID |Name | Issue |
|---|-----|-------|
|~~243~~|~~Unmaker~~|~~DECORATE classes and sprite names confict between centered and angled versions WADs~~ Centered version was excluded|
|236, 266|Flare Gun, Napalm Launcher|The same `actor NapalmDebris` is used by both weapons. Causes _Tried to register class 'NapalmDebris' more than once_ error|
|308|Doom 3 SSG|Sprite `SGN2A0` replaces original one from `doom2.wad`|
|313, 659|Plasma Bolter, Pulse Rifle UAC|The same `actor PlasmaBolterShot1` and `actor PlasmaBolterShot1Trail` are used by both weapons. Causes _Tried to register class '...' more than once_ errors|
|444, 510|Necronomicon, Vile Staff|The same `actor Darkmana` is used by both weapons. Causes _Tried to register class 'Darkmana' more than once_ error|
|496, 560|Nailgun (MG), Nailgun (SG)|The same `actor Nail` is used by both weapons. Causes _Tried to register class 'Nails' more than once_ error|
|510|Vile Staff|The weapon doesn't spawn projectile nor cause any damage. Is it broken?|
|522, 659|Pulse Rifle, Pulse Rifle UAC|Both assets share the same filename `PulseRifle.wad`, although they work correctly. Python warning is issued during `.pk3` generation|
|541, 543|Flamethrower, UTNT Pyro-Cannon|The same `actor Gas` and `actor BigGas` are used by both weapons. Causes _Tried to register class '...' more than once_ errors|
|~~717~~|~~LandMine Layer~~|~~DECORATE classes and sprite names confict between WADs for Doom and for Strife. Causes multiple _Tried to register class '...' more than once_ errors~~ Strife version was excluded|
|874, 876|BFG 2704, Spray Cannon|_Almost_ the same `actor 2704Ball` and `actor 2704Ball2` are used by both weapons, different by obituary message only. Causes _Tried to register class '...' more than once_ errors and wrong obituary message for one of the weapons|
|926|Shield Spells|DECORATE classes and sprite names confict between Scroll and Sphere WADs|

### Duplicate lump names, weapons only
|Name|WAD Files|Comments|
|---|---|---|
|AGASA0|Flamethrower.wad, UTNTPyroCannon.wad||
|AGASB0|Flamethrower.wad, UTNTPyroCannon.wad||
|ANIME0|SawedOff.wad, SawedOff.wad||
|ANIMF0|SawedOff.wad, SawedOff.wad||
|ANIMG0|SawedOff.wad, SawedOff.wad||
|~~AXE~~|~~Axe.wad, Axe.wad~~|Compiled ACS and its source code in different namespaces|
|BOLTA0|PlasmaBolter.wad, TeslaCannon.wad||
|BXPLL0|CryoBow.wad, PlasmaBallista.wad||
|BXPLM0|CryoBow.wad, PlasmaBallista.wad||
|COLTA0|Colt45.wad, Reaper.wad||
|COLTB0|Colt45.wad, Reaper.wad||
|COLTC0|Colt45.wad, Reaper.wad||
|COTSFPO|CultStaff.WAD, CultStaff.WAD||
|DEVGN0|Devastators.wad, Devastators.wad||
|DSMINIGN|Minigun.wad, UberMinigun.wad||
|EXP2A0|Deviation.wad, SeekerBazooka.wad||
|EXP2B0|Deviation.wad, SeekerBazooka.wad||
|EXP2C0|Deviation.wad, SeekerBazooka.wad||
|EXP2D0|Deviation.wad, SeekerBazooka.wad||
|EXP2E0|Deviation.wad, SeekerBazooka.wad||
|EXP2F0|Deviation.wad, SeekerBazooka.wad||
|EXP2G0|Deviation.wad, SeekerBazooka.wad||
|EXP2H0|Deviation.wad, SeekerBazooka.wad||
|EXP2I0|Deviation.wad, SeekerBazooka.wad||
|EXP2J0|Deviation.wad, SeekerBazooka.wad||
|EXP2K0|Deviation.wad, SeekerBazooka.wad||
|EXP2L0|Deviation.wad, SeekerBazooka.wad||
|EXP2M0|Deviation.wad, SeekerBazooka.wad||
|EXP2N0|Deviation.wad, SeekerBazooka.wad||
|EXP3A0|jackbomb.wad, SeekerBazooka.wad||
|EXP3B0|jackbomb.wad, SeekerBazooka.wad||
|EXP3C0|jackbomb.wad, SeekerBazooka.wad||
|EXP3D0|jackbomb.wad, SeekerBazooka.wad||
|EXP3E0|jackbomb.wad, SeekerBazooka.wad||
|EXP3F0|jackbomb.wad, SeekerBazooka.wad||
|EXP3G0|jackbomb.wad, SeekerBazooka.wad||
|EXP3H0|jackbomb.wad, SeekerBazooka.wad||
|EXP3I0|jackbomb.wad, SeekerBazooka.wad||
|EXP3J0|jackbomb.wad, SeekerBazooka.wad||
|EXP3K0|jackbomb.wad, SeekerBazooka.wad||
|EXP3L0|jackbomb.wad, SeekerBazooka.wad||
|EXP3M0|jackbomb.wad, SeekerBazooka.wad||
|EXP3N0|jackbomb.wad, SeekerBazooka.wad||
|EXP3O0|jackbomb.wad, SeekerBazooka.wad||
|EXP3P0|jackbomb.wad, SeekerBazooka.wad||
|EXP3Q0|jackbomb.wad, SeekerBazooka.wad||
|EXP3R0|jackbomb.wad, SeekerBazooka.wad||
|EXP3S0|jackbomb.wad, SeekerBazooka.wad||
|EXP3T0|jackbomb.wad, SeekerBazooka.wad||
|EXP3U0|jackbomb.wad, SeekerBazooka.wad||
|EXP3V0|jackbomb.wad, SeekerBazooka.wad||
|EXP3W0|jackbomb.wad, SeekerBazooka.wad||
|EXP3X0|jackbomb.wad, SeekerBazooka.wad||
|EXP3Y0|jackbomb.wad, SeekerBazooka.wad||
|EXP3Z0|jackbomb.wad, SeekerBazooka.wad||
|FLMEA0|Flamethrower.wad, UTNTPyroCannon.wad||
|FLMEB0|Flamethrower.wad, UTNTPyroCannon.wad||
|FLMEC0|Flamethrower.wad, UTNTPyroCannon.wad||
|FLMED0|Flamethrower.wad, UTNTPyroCannon.wad||
|FLMEE0|Flamethrower.wad, UTNTPyroCannon.wad||
|FLMEF0|Flamethrower.wad, UTNTPyroCannon.wad||
|FLMEG0|Flamethrower.wad, UTNTPyroCannon.wad||
|FLMEH0|Flamethrower.wad, UTNTPyroCannon.wad||
|FLMEI0|Flamethrower.wad, UTNTPyroCannon.wad||
|FLMEJ0|Flamethrower.wad, UTNTPyroCannon.wad||
|FLMEK0|Flamethrower.wad, UTNTPyroCannon.wad||
|FLMEL0|Flamethrower.wad, UTNTPyroCannon.wad||
|FLMEM0|Flamethrower.wad, UTNTPyroCannon.wad||
|FLMEN0|Flamethrower.wad, UTNTPyroCannon.wad||
|FRFXA0|Flamethrower.wad, UTNTPyroCannon.wad||
|FRFXB0|Flamethrower.wad, UTNTPyroCannon.wad||
|FRFXC0|Flamethrower.wad, UTNTPyroCannon.wad||
|FRFXD0|Flamethrower.wad, UTNTPyroCannon.wad||
|FRFXE0|Flamethrower.wad, UTNTPyroCannon.wad||
|FRFXF0|Flamethrower.wad, UTNTPyroCannon.wad||
|FRFXG0|Flamethrower.wad, UTNTPyroCannon.wad||
|FRFXH0|Flamethrower.wad, UTNTPyroCannon.wad||
|FRFXI0|Flamethrower.wad, UTNTPyroCannon.wad||
|FRFXJ0|Flamethrower.wad, UTNTPyroCannon.wad||
|FRFXK0|Flamethrower.wad, UTNTPyroCannon.wad||
|FRFXL0|Flamethrower.wad, UTNTPyroCannon.wad||
|FRFXM0|Flamethrower.wad, UTNTPyroCannon.wad||
|FRFXN0|Flamethrower.wad, UTNTPyroCannon.wad||
|FRFXO0|Flamethrower.wad, UTNTPyroCannon.wad||
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
|NBOXA0|Nailgun(SG).wad, PulseNailgun.wad||
|PYXPO0|UTNTPyroCannon.wad, UTNTPyroCannon.wad||
|~~RELOADIN~~|~~Drummle.wad, Enforcer(Pistol).wad~~|Alternative DECORATE lump, unused by engine|
|REVII0|Necronomicon.wad, VileStaff.wad||
|SPAFA0|SPAS-12.wad, SwatShotgun.wad||
|SPASA0|SPAS-12.wad, SwatShotgun.wad||
|SPIKB0|NailGun.wad, SkullStaff.wad||
|~~UPDATES~~|~~BioPipebombLauncher.wad, Glock18.wad~~|Informational text, unused by engine|
