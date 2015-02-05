### Known issues

|ID |Name | Issue |
|---|-----|-------|
|~~243~~|~~Unmaker~~|~~DECORATE classes and sprite names confict between centered and angled versions WADs~~ Centered version was excluded|
|308|Doom 3 SSG|Sprite `SGN2A0` replaces original one from `doom2.wad`|
|313, 659|Plasma Bolter, Pulse Rifle UAC|The same `actor PlasmaBolterShot1` and `actor PlasmaBolterShot1Trail` are used by both weapons. Causes _Tried to register class '...' more than once_ errors|
|496, 560|Nailgun (MG), Nailgun (SG)|The same `actor Nail` is used by both weapons. Causes _Tried to register class 'Nails' more than once_ error|
|522, 659|Pulse Rifle, Pulse Rifle UAC|Both assets share the same filename `PulseRifle.wad`, although they work correctly. Python warning is issued during `.pk3` generation|
|541, 543|Flamethrower, UTNT Pyro-Cannon|The same `actor Gas` and `actor BigGas` are used by both weapons. Causes _Tried to register class '...' more than once_ errors|
|~~717~~|~~LandMine Layer~~|~~DECORATE classes and sprite names confict between WADs for Doom and for Strife. Causes multiple _Tried to register class '...' more than once_ errors~~ Strife version was excluded|
|874, 876|BFG 2704, Spray Cannon|_Almost_ the same `actor 2704Ball` and `actor 2704Ball2` are used by both weapons, different by obituary message only. Causes _Tried to register class '...' more than once_ errors and wrong obituary message for one of the weapons|
|926|Shield Spells|DECORATE classes and sprite names confict between Scroll and Sphere WADs|
