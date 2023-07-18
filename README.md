# Multidisciplinary Project - Watering System

A smart plant watering system based on the AIoT Kit.  
This is a demo for the Multidisciplinary Project Lab.  

## Key Features

- **Automatic Watering**: Watering is done automatically based on soil moisture.
- **Plant Detection**: Watering is only done if a plant is detected at the plot.
- **Reservoir Monitoring**: Automatically monitor pump reservoir and warns if it gets empty.
- **(Optional) Notification**: Sends notification about various system event to your device.

## Getting Started
### Prerequisites

Before you proceed, ensure that you have Python 3.11 installed with these libraries:

- adafruit-io
- tensorflow
- keras
- opencv-python
- pyserial
- pushbullet.py

A free account on [Adafruit IO](https://io.adafruit.com/) as well as the AIoT Kit is also required. 

### Optional Dependencies
#### Pushbullet

[Pushbullet](https://www.pushbullet.com/) allows notification about various system events to be sent to your device.  
The pushbullet.py library is required to enable this feature as well as the Pushbullet application to be installed on your device.  
This feature can be disabled during setup.

### Installation
#### Connecting to the AIoT Kit

1. Connect the kit to the system via the USB cable.  
2. Locate the name of the port that the kit will be communicating through:

##### On Windows:
Check for the port name in `Device Manager/Ports`.  
The name should be something like `COM*`

##### On Linux:
Check for any new USB adapter in `/dev` directory.  
You can find it through the terminal: `ls /dev/ttyUSB*`.

#### Installation

1. Clone the repository.
2. Run `install.py` and follow the instruction.
3. Run `mqtt.py` to start the client.

## Contributors

- Dương Võ Thiên Bảo
- Nguyễn Duy
- Mai Thị Yến Nhi
- Lê Bỉnh Thanh
- Bùi Phạm Minh Tuấn