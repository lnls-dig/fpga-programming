setMode -pff
setSubmode -pffspi
addConfigDevice  -name "${MCS_NAME}" -path "./"
setAttribute -configdevice -attr multibootBpiType -value ""
setAttribute -configdevice -attr compressed -value "FALSE"
setAttribute -configdevice -attr autoSize -value "FALSE"
setAttribute -configdevice -attr fileFormat -value "mcs"
setAttribute -configdevice -attr fillValue -value "FF"
setAttribute -configdevice -attr swapBit -value "FALSE"
setAttribute -configdevice -attr dir -value "UP"
setAttribute -configdevice -attr multiboot -value "FALSE"
setAttribute -configdevice -attr spiSelected -value "TRUE"
addDesign -version 0 -name "0"
addDeviceChain -index 0
addPromDevice -p 1 -size 16384 -name 16M
setAttribute -design -attr name -value "0000"
addDevice -p 1 -file "${BITSTREAM_FILE}"
generate

exit
