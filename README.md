# multi-screen-server

Server to directly control a multi screen Raspberry Pi cluster.

## Installation [Ubuntu 18.04]

* Install Python3 

        $ sudo apt install python3
        
* Install Pip 

        $ sudo apt install python3-pip
        
* Install libraries (from inside project folder)

        $ pip install -r requirements.txt
        
        
## Save Dependencies

        pip freeze --local | grep -v myapp > requirements.txt

## Run Server

        $ python3 app.py

## UDP Communication Protocol
 
Description | First Byte | Second
---|:---:|:---:
Screen Off | 0 | 0
Screen On | 0 | 1
Select Shader | 1 | 0...∞
Reset Time | 2 | 
Use Local Span | 3 | 0
Use Global Span | 3 | 1

## API Documentation

### Change Shader
Example

        192.168.1.9:5000/change_shader?shader=3
        
Possible Shader

| Shader | Name |
| ---|--- |
| 0 | Ren |
| 1 | Stimpy | 
| 2 | Pinky |
| 3 | Brain |

### Change Screen Span
Example

        192.168.1.9:5000/screen_span?mode=1
        
Possible Modes

Mode | Name
---|---
0 | Local
1 | Global 
> 1 | Random

### Single Time Reset
Example

        192.168.1.9:5000/reset_time?screen=2
        
Possible Screens

Screen | Name
---|---
0 | All
1...∞ | Specific Screen 

### Reset Times
Example

        192.168.1.9:5000/reset_times?synced=1
        
Possible Modes

Resets | Name
---|---
0 | Random
1 | Synchronize 

### Manual/Preset Mode
Example

        192.168.1.9:5000/manual?mode=1
        
Possible Modes

Mode | Name
---|---
0 | manual mode
1 | preset mode

## Control Virtual Env

* Activate Virtual Env

        $ source venv/bin/activate
        
* Deactivate Virtual Env 

        $ deactivate
