#!/bin/sh

BITSTREAM="$1"

if [ -z "${BITSTREAM}" ]; then
	echo "Usage: $0 bitstream.bit"
	exit 1
fi

openocd -f interface/ftdi/digilent_jtag_hs3.cfg \
        -c "transport select jtag" \
        -f cpld/xilinx-xc6v.cfg \
        -f cpld/xilinx-xcf-p.cfg \
        -c "adapter speed 3000" \
        -c "init" \
        -c "virtex2 program xc6v.pld" \
        -c "pld load xc6v.pld \"${BITSTREAM}\"" \
        -c "exit"
