setMode -bs
setCable -port auto
Identify -inferir
identifyMPM
assignFile -p 1 -file "${BITSTREAM_FILE}"
Program -p 1
exit
