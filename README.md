# ATC-Sim
ATC trainer + simulator, written in Python with pygame.


https://github.com/user-attachments/assets/9add3f23-b595-4874-8c25-ca6c4a63d2cb



## Quick Start
Run `main.py` to start the simulator.\
The simulation is controlled by the `System` by default, `LAlt` toggles User Controls on and off.\
User Controls enable manual aircraft guidance through commands (from the text bar).
\
\
Type instructions in the format 
```
<AircraftCallsign> <CommandType> <Heading/Alt/Speed/RwyNumber>
```

### Command Instructions
Commands follow OpenScope syntax.\
\
\
`t` - Turn to Heading\
`s` - Set Speed\
`c/a/d` - Climb / Ascend / Descent to Altitude\
`ils` - Capture ILS of Runway Number\
\
Pressing `↑` loads your last sent command into the Text Bar.\
\
_Using `t` Spawns a temporary Heading Guidance Wheel:_\
![image](https://github.com/user-attachments/assets/df997dd9-ea41-4bc0-b4fc-1a0ebe97d680)


## Simulation Speed
In `main.py`, under the `CONSTANTS` section, change the values of:\
`moveTimeInterval` : To change the simulation speed (how often aircraft positions update)\
`spawnTimeInterval` : To change the spawn rate of aircrafts into VOMM airspace from the entry fixes (this value is approximately 65000ms in real life)\
\
_Both values are in milliseconds_

## Supported Airports
As of now, only VOMM (Chennai Intl) is supported.\
Support for more airports coming soon! 
