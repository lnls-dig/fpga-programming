#!/bin/sh

bitstream="$1"

if [ -z "$1" ]; then
	echo "Usage: $0 bitstream_file"
	exit 1
fi

openocd -f afcv4-ftdi-jtag.cfg -c "init; xc7_program xc7.tap; pld load 0 \"${bitstream}\"; exit; ftdi_set_signal JEN 0"
