#!/bin/sh

bitstream="$1"
board="$2"
interface="$3"

if [ -z "$bitstream" -o -z "$board" -o -z "$interface" ]; then
	echo "Usage: $0 bitstream_file board interface"
	exit 1
fi

if [ "$board" = "afcv3" ]; then
	scansta_cmd="svf afc-scansta.svf -quiet"
elif [ "$board" = "afcv4" ]; then
	scansta_cmd=""
else
	echo "Board '${board}' not supported!"
	exit 1
fi

if [ "$interface" = "ftdi" ]; then
	openocd -f afcv4-ftdi-jtag.cfg \
			-c "init" \
			-c "xc7_program xc7.tap" \
			-c "pld load 0 \"${bitstream}\"" \
			-c "exit" \
			-c "ftdi_set_signal JEN 0"
elif [ "$interface" = "xvc" ]; then
	xvc_host="$4"
	xvc_port="$5"

	if [ -z "$xvc_host" -o -z "$xvc_port" ]; then
		echo "Usage: $0 bitstream_file board xvc hostname port"
		exit 1
	fi

	openocd -c "adapter driver xvc" \
			-c "adapter speed 3000" \
			-c "xvc_host ${xvc_host}" \
			-c "xvc_port ${xvc_port}" \
			-c "reset_config none" \
			-c "jtag newtap xc7 tap -irlen 6 -ignore-version -expected-id 0x03636093" \
			-c "pld device virtex2 xc7.tap 1" \
			-c "init" \
			-c "${scansta_cmd}" \
			-c "pld load 0 \"${bitstream}\"" \
			-c "exit"
else
	echo "Interface '${interface}' not supported!"
	exit 1
fi
