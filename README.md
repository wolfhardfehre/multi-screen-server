# multi-screen-server

Server to directly control a multi screen Raspberry Pi cluster.

## Installation [Ubuntu 18.04]

* Install Python3 

        $ sudo apt install python3
        
* Install Pip 

        $ sudo apt install python3-pip
        
* Install libraries (from inside project folder)

        $ pip install -r requirements.txt

## Run Server

        $ FLASK_APP=app.py flask run


## UDP Communication Protocol
 
Description | First Byte | Second
---|:---:|:---:
Screen Off | 0 | 0
Screen On | 0 | 1
Select Shader | 1 | 0...∞
Reset Time | 2 | 
Use Local Span | 3 | 0
Use Global Span | 3 | 1

## Control Virtual Env

* Activate Virtual Env

        $ source venv/bin/activate
        
* Deactivate Virtual Env 

        $ deactivate
