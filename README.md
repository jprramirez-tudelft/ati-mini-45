# ATI Mini45 Sensor Documentation 

## Background

[Manufacturer Landing Page](https://www.ati-ia.com/products/ft/ft_models.aspx?id=Mini45)

[Calibration Files](https://www.ati-ia.com/library/software/ftdigitaldownload/getcalfiles.aspx)

### Electronics


## Windows Setup

### Software

#### USB-RS485

[Bought from Farnell](https://nl.farnell.com/en-NL/ftdi/usb-rs485-we-1800-bt/cable-usb-rs485-serial-converter/dp/1740357)

[Datasheet](https://www.farnell.com/datasheets/652302.pdf)

[Install Driver from FTDI](https://ftdichip.com/drivers/vcp-drivers/)

#### ATI Demo Program 
1. Download and install [Digital F/T Demo Software] https://www.ati-ia.com/library/download.aspx
2. Edit > Options >
   See COM Port in Device Manager
   **Tested Baud Rate** 115200
   Edit File Destination to Write
4. Data > Calibrations > FT 144185
5. Click **Bias** to tare
6. **Collect to File? **

## Linux Setup
No need for driver installation. 
