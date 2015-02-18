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

### Lump names collisions
|Name|WAD Files|Comments|
|---|---|---|
|BATCRASH|Eyes.wad, ImpWarlord.wad||
|BATDIE|Eyes.wad, ImpWarlord.wad||
|BATIDLE1|Eyes.wad, ImpWarlord.wad||
|BATIDLE2|Eyes.wad, ImpWarlord.wad||
|BATPAIN|Eyes.wad, ImpWarlord.wad||
|BMSAR2A1|BloodFiend.wad, NightmareDemon.wad||
|BMSAR2A2|BloodFiend.wad, NightmareDemon.wad||
|BMSAR2A3|BloodFiend.wad, NightmareDemon.wad||
|BMSAR2B1|BloodFiend.wad, NightmareDemon.wad||
|BMSAR2B2|BloodFiend.wad, NightmareDemon.wad||
|BMSAR2B3|BloodFiend.wad, NightmareDemon.wad||
|BMSAR2C1|BloodFiend.wad, NightmareDemon.wad||
|BMSAR2C2|BloodFiend.wad, NightmareDemon.wad||
|BMSAR2C3|BloodFiend.wad, NightmareDemon.wad||
|BMSAR2D1|BloodFiend.wad, NightmareDemon.wad||
|BMSAR2D2|BloodFiend.wad, NightmareDemon.wad||
|BMSAR2D3|BloodFiend.wad, NightmareDemon.wad||
|BMSAR2E1|BloodFiend.wad, NightmareDemon.wad||
|BMSAR2E2|BloodFiend.wad, NightmareDemon.wad||
|BMSAR2E8|BloodFiend.wad, NightmareDemon.wad||
|BMSAR2F1|BloodFiend.wad, NightmareDemon.wad||
|BMSAR2F2|BloodFiend.wad, NightmareDemon.wad||
|BMSAR2F8|BloodFiend.wad, NightmareDemon.wad||
|BMSAR2G1|BloodFiend.wad, NightmareDemon.wad||
|BMSAR2G2|BloodFiend.wad, NightmareDemon.wad||
|BMSAR2G8|BloodFiend.wad, NightmareDemon.wad||
|BMSAR2H1|BloodFiend.wad, NightmareDemon.wad||
|BMSAR2H2|BloodFiend.wad, NightmareDemon.wad||
|BMSAR2H3|BloodFiend.wad, NightmareDemon.wad||
|BMSAR2H4|BloodFiend.wad, NightmareDemon.wad||
|BMSAR2H8|BloodFiend.wad, NightmareDemon.wad||
|BMSAR2I0|BloodFiend.wad, NightmareDemon.wad||
|BOUNCE|40mmGrenadeLauncher.wad, ChainmailEttin.wad, SourceGuardian.wad||
|BUILD|Phantom.wad, Thor.wad||
|COMETEXP|InfernoDemon.wad, Thamuz.wad||
|DEATH|Gatekeeper.wad, LesserMutant.wad, Maephisto.wad||
|DFATTACK|ImpWarlord.wad, InfernoDemon.wad||
|DOOMDEFS|Incubus.wad, PhaseImp.wad||
|DSBGACT|!DOOM.WAD, !DOOM2.WAD, !PLUTONIA.WAD, !TNT.WAD, ImpWarlord.wad||
|DSBGDTH1|!DOOM.WAD, !DOOM2.WAD, !PLUTONIA.WAD, !TNT.WAD, ImpWarlord.wad||
|DSBGDTH2|!DOOM.WAD, !DOOM2.WAD, !PLUTONIA.WAD, !TNT.WAD, ImpWarlord.wad||
|DSBGSIT1|!DOOM.WAD, !DOOM2.WAD, !PLUTONIA.WAD, !TNT.WAD, ImpWarlord.wad||
|DSBGSIT2|!DOOM.WAD, !DOOM2.WAD, !PLUTONIA.WAD, !TNT.WAD, ImpWarlord.wad||
|DSBIGBRN|HellApprentice.WAD, HellHound.wad, Hellsmith.WAD, Sentinel.wad||
|DSBLOODX|BloodFiend.wad, Ghoul.wad, PlaugeImp.wad||
|DSBLUR|Acolyte.wad, Disciple.wad, Vampire.wad||
|DSBOLTFI|DeathKnight.wad, Sentinel.wad||
|DSBRUFIR|Cybruiser.wad, Terminator.wad||
|DSCMTEXP|Avatar.wad, Phantom.wad, PyroDemon.wad||
|DSDASH|HellApprentice.WAD, Hellsmith.WAD||
|DSDEMBIT|Helemental.wad, Inferno.wad||
|DSDEVEXP|Avatar.wad, DevastatorZombie.wad, Overlord.wad||
|DSDEVZAP|Avatar.wad, DevastatorZombie.wad, Helemental.wad||
|DSDIASHT|Diabolist.wad, HellApprentice.WAD, Hellsmith.WAD, Zardaz.wad||
|DSDISHT1|Disciple.wad, Sentinel.wad||
|DSDMACT|!DOOM.WAD, !DOOM2.WAD, !PLUTONIA.WAD, !TNT.WAD, Banshee.wad, PlasmaDemon.wad||
|DSDMPAIN|!DOOM.WAD, !DOOM2.WAD, !PLUTONIA.WAD, !TNT.WAD, Banshee.wad, HellsGuard.wad, PlasmaDemon.wad||
|DSDOGATK|HellHound.wad, Rottweiler.wad||
|DSFIRBFI|ArchonOfHell.wad, Diabolist.wad, HellstormArchon.wad, InfernoDemon.wad||
|DSFIREX2|Avatar.wad, DeathKnight.wad||
|DSFIREX3|Diabolist.wad, HellApprentice.WAD, Hellsmith.WAD, Inferno.wad, InfernoDemon.wad, Sentinel.wad||
|DSFIREX4|DeathKnight.wad, Diabolist.wad||
|DSFIREX5|Diabolist.wad, Fallen.wad, Hierophant.wad, Wicked.wad||
|DSFIRMFI|Diabolist.wad, Fallen.wad, Hierophant.wad, Inferno.wad, InfernoDemon.wad, Wicked.wad||
|DSFIRSFI|GuardianCube.wad, Sentinel.wad||
|DSFIRSHT|!DOOM.WAD, !DOOM2.WAD, !PLUTONIA.WAD, !TNT.WAD, DarkClink.wad, PlasmaDemon.wad||
|DSFIRXPL|!DOOM.WAD, !DOOM2.WAD, !PLUTONIA.WAD, !TNT.WAD, Banshee.wad, DarkClink.wad, PlasmaDemon.wad||
|DSFLAMER|FlamerZombie.wad, PyroDemon.wad, SpellBinder.wad||
|DSHADSIT|Avatar.wad, DeathIncarnate.wad||
|DSHAMFLR|HellApprentice.WAD, Hellsmith.WAD||
|DSHAMHIT|HellApprentice.WAD, Hellsmith.WAD||
|DSHAMSHT|HellApprentice.WAD, Hellsmith.WAD||
|DSHAMSWG|HellApprentice.WAD, Hellsmith.WAD||
|DSHELLEX|ApprenticeOfDsparil.wad, ArchonOfHell.wad, Cybruiser.wad, Diabolist.wad, HellApprentice.WAD, Hellsmith.WAD, HellstormArchon.wad, InfernoDemon.wad, Terminator.wad||
|DSHELLFI|Diabolist.wad, HellApprentice.WAD, Hellsmith.WAD||
|DSINCACT|DeathIncarnate.wad, Incubus.wad||
|DSINCDTH|DeathIncarnate.wad, Incubus.wad||
|DSINCHIT|DeathIncarnate.wad, Incubus.wad||
|DSINCSIT|DeathIncarnate.wad, Incubus.wad||
|DSJUSTFI|Avatar.wad, InfernoDemon.wad||
|DSKNIFE|FemaleScientist.wad, Knife.wad||
|DSMINIGN|Minigunner.wad, UberMinigun.wad||
|DSNBBEXP|NailBorg.wad, NailBorgCommando.wad||
|DSNBBNC1|NailBorg.wad, NailBorgCommando.wad||
|DSNBBNC2|NailBorg.wad, NailBorgCommando.wad||
|DSNBDTH1|NailBorg.wad, NailBorgCommando.wad||
|DSNBDTH2|NailBorg.wad, NailBorgCommando.wad||
|DSNBDTH3|NailBorg.wad, NailBorgCommando.wad||
|DSNBMBLC|NailBorg.wad, NailBorgCommando.wad||
|DSNBPAIN|NailBorg.wad, NailBorgCommando.wad||
|DSNBSACT|NailBorg.wad, NailBorgCommando.wad||
|DSNBSIT1|NailBorg.wad, NailBorgCommando.wad||
|DSNBSIT2|NailBorg.wad, NailBorgCommando.wad||
|DSNBSIT3|NailBorg.wad, NailBorgCommando.wad||
|DSNBWALK|NailBorg.wad, NailBorgCommando.wad||
|DSNLFIRE|NailBorg.wad, NailBorgCommando.wad||
|DSNLFLIT|NailBorg.wad, NailBorgCommando.wad||
|DSNLIMPD|NailBorg.wad, NailBorgCommando.wad||
|DSNLIMPL|NailBorg.wad, NailBorgCommando.wad||
|DSPIPEX1|InfernoDemon.wad, Pipebombs.wad, PyroDemon.wad||
|DSPOPAIN|!DOOM.WAD, !DOOM2.WAD, !PLUTONIA.WAD, !TNT.WAD, ImpWarlord.wad||
|DSSGTATK|!DOOM.WAD, !DOOM2.WAD, !PLUTONIA.WAD, !TNT.WAD, PlasmaDemon.wad||
|DSSGTDTH|!DOOM.WAD, !DOOM2.WAD, !PLUTONIA.WAD, !TNT.WAD, PlasmaDemon.wad||
|DSSGTSIT|!DOOM.WAD, !DOOM2.WAD, !PLUTONIA.WAD, !TNT.WAD, PlasmaDemon.wad||
|DSSKLATK|!DOOM.WAD, !DOOM2.WAD, !PLUTONIA.WAD, !TNT.WAD, Banshee.wad||
|DSSLSHDT|Catharsi.wad, DuneWarrior.wad, SourceGuardian.wad||
|DSSLSHOT|Catharsi.wad, DuneWarrior.wad, SourceGuardian.wad||
|DSSLTHTI|Catharsi.wad, DuneWarrior.wad, SourceGuardian.wad||
|DSSMITHA|HellApprentice.WAD, Hellsmith.WAD||
|DSSMITHD|HellApprentice.WAD, Hellsmith.WAD||
|DSSMITHP|HellApprentice.WAD, Hellsmith.WAD||
|DSSMITHR|HellApprentice.WAD, Hellsmith.WAD||
|DSSMITHS|HellApprentice.WAD, Hellsmith.WAD||
|DSSMITHT|HellApprentice.WAD, Hellsmith.WAD||
|DSSPIDTH|!DOOM.WAD, !DOOM2.WAD, !PLUTONIA.WAD, !TNT.WAD, Eyes.wad||
|DSSPIRT1|Necronomicon.wad, Phantom.wad||
|DSSPISIT|!DOOM.WAD, !DOOM2.WAD, !PLUTONIA.WAD, !TNT.WAD, Eyes.wad||
|DSSULDTH|HellApprentice.WAD, Hellsmith.WAD||
|DSTENPN1|CoreTentacles.wad, Wicked.wad||
|DSTENPN2|CoreTentacles.wad, Wicked.wad||
|DSTRTPSN|PoisonSoul.wad, TorturedSoul.wad||
|DSUNMKER|Unmaker.wad, UnMakerZombie.wad||
|DSUNMKPO|Unmaker.wad, UnMakerZombie.wad||
|DSVULHIT|Grell.wad, Vulgar.wad||
|DSZTANK1|ZombieMissileTank.wad, ZombiePlasmaTank.wad||
|DSZTANK2|ZombieMissileTank.wad, ZombiePlasmaTank.wad||
|DSZTANKD|ZombieMissileTank.wad, ZombiePlasmaTank.wad||
|DSZTANKP|ZombieMissileTank.wad, ZombiePlasmaTank.wad||
|DSZTANKX|ZombieMissileTank.wad, ZombiePlasmaTank.wad||
|FEMZDHT|femaleplasma.wad, FemaleScientist.wad, FemaleScientist3.wad||
|FEMZPAIN|femaleplasma.wad, FemaleScientist.wad||
|FIREBALL|Avatar.wad, InfernoDemon.wad, Phantom.wad, Thor.wad||
|FIRE|Gatekeeper.wad, NetherworldQueen.wad, SourceGuardian.wad||
|IMPACT3|BloodLich.wad, FamiliarSummon (Scroll).wad, Rictus.wad||
|IMPFIRE2|BloodLich.wad, InfernoDemon.wad, Rictus.wad||
|PAIN|Gatekeeper.wad, LesserMutant.wad, Maephisto.wad||
|SCRIPTS|Hangman.wad, OxygenCanister.wad||
|SEE|Gatekeeper.wad, LesserMutant.wad||
|STEP2|!DOOM.WAD, !DOOM2.WAD, !PLUTONIA.WAD, !TNT.WAD, DarkInquisitor.wad||
|STRIKE1|Bormereth.wad, Horn Beast.wad, Rictus.wad||

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
