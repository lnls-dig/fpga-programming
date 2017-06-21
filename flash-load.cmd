setMode -bs
setPreference -pref ConfigOnFailure:Stop
setCable -port auto
setCableSpeed -speed 12000000
Identify -inferir
identifyMPM
attachflash -position 1 -spi "N25Q256"
assignfiletoattachedflash -position 1 -file "${MCS_FILE}"
Program -p 1 -dataWidth 4 -spionly -e -loadfpga -v
exit
