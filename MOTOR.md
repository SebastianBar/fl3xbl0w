<p align="center">
  <img height="100" src="logo.png">
</p>

## Treadmill Motor Controller | fl3xbl0w

*This mostly applies to Treadmill 22 & Treadmill 56.*

The motor control board is manufactured by [Electronics Way Industry](https://www.ewayindustry.com/ew-dc-b017.html).

![Motor Control Board Controller B017D](assets/b017d.jpg)

Given the [service manual](https://download.nautilus.com/supportdocs/AM_OM/Bowflex/BFX.T10.T22.T25.T56.SM.EN.pdf) provided by Nautilus Inc. ([backup on archive.org](https://web.archive.org/web/20220409140737/https://download.nautilus.com/supportdocs/AM_OM/Bowflex/BFX.T10.T22.T25.T56.SM.EN.pdf)):

![Treadmill electrical diagram](assets/treadmill-electrical.png)

And focusing specifically on this part:

![Treadmill communication path](assets/treadmill-comm.png)

We can identify the "communication cable" connecting the motor controller as being of 5 pins. There's only one 5-pin connector.
I've labeled the wires with their corresponding colors (data & switch are optoisolated):

| cable color | label |
|-------------|-------|
| red         | GND   |
| white       | RXD   |
| black       | TXD   |
| yellow      | +12   |
| green       | SW    |


The board is not directly connected to the Android console.

The only 5-pin connector is of Molex brand. A Google search for "small Molex connectors" led me to a picture of a so-called `Molex Micro-Fit 3.0 Single Row (5-Pin)`, which is used to connect the motor controller board:

![Molex Micro-Fit 3.0 Connector](assets/molex.jpg)

[AliExpress Link](https://es.aliexpress.com/item/32902205579.html)

By peeking on `NautilusLauncher.apk` through `jadx-gui`, I can see that they communicate with the Android tablet with their "Universal Console" by using Serial at 230400 Baud (using `/dev/ttyS4`). That's NOT what we're analyzing here. That refers to the communication between Android and the "Universal Console". We investigate the comms between the "Universal Console" and the "Motor Control Board".

Trying to hook an ESP32 or a CH340-based serial bridge directly to the wires between the Treadmill base & Bowflex controller board caused the treadmill base to not properly initialize, so I started to guess they're using RS232.

Note: Attaching only to GND and RXD, we can "see" some apparent garbage hex information at 9600 baud. Hooking to TXD makes the treadmill base not initialize.

-- To be continued, a logic analyzer would be convenient at this time --
