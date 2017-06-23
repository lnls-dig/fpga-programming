write_cfgmem -force -format mcs -size 32 -interface SPIx4 -loadbit {up 0x00000000 ${BITSTREAM_FILE} } -file ${MCS_NAME}
