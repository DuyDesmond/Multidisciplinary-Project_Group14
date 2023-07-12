# Multidisciplinary Project - Watering System

A smart plant watering system based on the AIoT Kit.  
This is a demo for the Multidisciplinary Project Lab.  

## Key Features

- **Automatic Watering**: Watering is done automatically based on soil moisture.
- **Plant Detection**: Watering is only done if a plant is detected at the plot.
- **Reservoir Monitoring**: Automatically monitor pump reservoir and warns if it gets empty.

## Getting Started
### Prerequisites

Before you proceed, ensure that you have Python 3.8 installed with these libraries:

- adafruit-io
- tensorflow
- keras
- Pillow
- opencv-python
- pyserial

A free account on [Adafruit IO](https://io.adafruit.com/) as well as the AIoT Kit is also required.  

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