setMode -bs
setCable -port usb21 -baud 12000000
Identify -inferir
identifyMPM
assignFile -p 1 -file "${BITSTREAM_FILE}"
Program -p 1
exit
