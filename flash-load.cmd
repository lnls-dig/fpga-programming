setMode -bs
setPreference -pref ConfigOnFailure:Stop
setCable -port auto
setCableSpeed -speed 12000000
Identify -inferir
identifyMPM
attachflash -position 1 -spi "M25P128"
assignfiletoattachedflash -position 1 -file "${MCS_FILE}"
Program -p 1 -dataWidth 1 -spionly -e -loadfpga
exit
