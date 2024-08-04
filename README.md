This project contains a GUI and its associated driver compliant for MAX32660 microcontroller used for demonstrating various features and functionality of MAX77958 PD negotiator and MAX77986 single cell charger.

Hardware Requirements: 

a) MAX77958AEVKIT

b) MAX32660EVSYS

c) Single cell Li-ion battery (18650)

d) USB micro-b connector.

Block Diagram: 

![BlockDiagram1](https://github.com/user-attachments/assets/5fb63d4f-b7c9-4fa4-b469-2c377c283061)

Hardware Connections Required:

![MAX77986_DIAGRAM](https://github.com/user-attachments/assets/0e3fce38-fcb8-4798-8a76-902c5f1b6115)

a) Connect VDDIO, GND, SCL, SDA from MAX32660EVSYS to  MAX77986EVKIT
b) Remove jumper J7
c) Don't connect the USB micro-b cable to the PC
d) Toggle the switch SW1 to left to connect to SCLM and SDAM (master I2C port of MAX77958). This means that MAX77986 charger is configured using MAX32660 via MAX77986.
   Refer MAX77958 opcode command guide to understand the working.
   https://www.analog.com/media/en/technical-documentation/user-guides/max77958-customization-script-and-opcode-command-guide.pdf

GUI Operation:
1) Once the MAX32660EVSYS is connected to the PC, a USB drive named DAPLINK can be seen.
   Drag and drop the binary driver file "GUI_exe_Driver_bin/USB_PD_1_cell_Driver" to the DAPLINK to flash the driver to the microcontroller and press the reset button of MAX32660EVSYS for the program to take 
   effective.

2) Select the respective COMM port and select baud rate of 115200 and press connect. A window will pop up showing the connection status.
  ![Connection_tab](https://github.com/user-attachments/assets/a4fbd1e2-70f8-4ce7-b7ba-516583e7c312)

3) Now connect the PD compliant adapter and Go to Quick Run tab to understand the details of the adapter connected.
   Based on the available PDOs, the user can change the voltage and current on the fly from the "Choose from available PDOs" tab.
   The "Sink PDO Setting" allows user to set an initial plugin voltage like 5V,9V and so on. The "PPS mode" demonstrates the using of PPS option in MAX77958 if a PPS compliant adapter is plugged in.
   The "Charger Settings" tab allows the charger (MAX77986) configuration. The "OTG settings" tab allows enabling the Reverse OTG power mode.
   ![Quickrun](https://github.com/user-attachments/assets/2a050c33-12c4-4c8f-a9d2-95fdc4f8e16b)

4) Using the "Commands" tab, the user can issue various commands to control and monitor the various functionalities in binary values. Refer USB PD documentation in USB.org to understand the register format
   of source and sink PDOs.
   ![Screenshot 2024-08-04 131351](https://github.com/user-attachments/assets/dc8c716c-465f-4319-bf78-96deffdbc166)

5) If looking for an API for USB PD charging for MAX77958, MAX77986, MAX17262 controlled by MAX32660, please refer the Github link below:
   https://github.com/fahdfawa/USB-PD-1cell-sink-solution-API/tree/main


   



   







