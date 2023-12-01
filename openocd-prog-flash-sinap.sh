#!/bin/sh

FLASHBIN="$1"

if [ -z "${FLASHBIN}" ]; then
	echo "Usage: $0 flash.bin"
	exit 1
fi

openocd -f interface/ftdi/digilent_jtag_hs3.cfg \
        -c "transport select jtag" \
        -f cpld/xilinx-xc6v.cfg \
        -f cpld/xilinx-xcf-p.cfg \
        -c "adapter speed 3000" \
        -c "program \"${FLASHBIN}\" reset" \
        -c "xcf configure 0" \
        -c "exit"
