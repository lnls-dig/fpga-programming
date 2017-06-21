setMode -bs
setCable -port auto
setCableSpeed -speed 12000000
Identify -inferir
identifyMPM
assignFile -p 1 -file "${BITSTREAM_FILE}"
Program -p 1
exit
