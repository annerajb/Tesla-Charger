# Tesla-Charger
Reverse Engineering of the Tesla 10Kw charger and development of an open source control board

19/10/17 : Uploaded two files : 
ph_frames.csv this file contains the 3 messages required to run phase module 1 in the Gen 2 charger
power_run_ph1.csv this is a capture of phase 1 starting up , ramping up to 8.5A DC 320VDC, 15.5A AC, 230v 50hz
Mains switched manually around message number 700 in ph_frames.csv


21/10/17 : Uploaded two files : 
power_run_ph1_arduino_2a_365vdc.csv
Tesla_chg1_1.ino
Crude arduino sketch to run one power module in the gen2 charger. Runs on an arduino due on CAN1


01/11/17 : Uploaded design files for Version 1 open source logic board for the Tesla Gen 2 charger. As of this date this design is totally unchecked and untested. Do not build this. It could blow up your house , car or cat. Based on the Arduino Due SAM3X8E microcontroller. Stay tuned.


05/11/17 : Updated Design files and PCBs ordered for prototype builds.

17/11/17 : BOM uploaded for the V1 board.


08/12/17 : Added Tesla_charger_Tom_v2_test.ino source file. Should run all 3 phases with the V1 logic board. Untested.

20/12/17 : Added design files for V2 Charger control board. Major changes :

Added 2M Serial EEPROM for parameter storage

Changed to a Vertical type B USB socket.

27/02/18 : Error found on the V2 board. Missing grounds on Q1 and D5. Affects EVSE control only. Will ammend in a rev3 board asap.

28/02/18 : V3 design files released with grounds fixed. Also new S/W thanks to Tom DeBree released but untested as of today. Also pictures of mod required on V1 and V2 boards.

Enjoy!
