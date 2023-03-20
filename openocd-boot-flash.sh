#!/bin/sh

board="$1"
interface="$2"

if [ -z "$board" -o -z "$interface" ]; then
	echo "Usage: $0 board interface"
	exit 1
fi

scansta_cmd=""
sfp_jtag=""
if [ "$board" = "afcv3" ]; then
	scansta_cmd="svf afc-scansta.svf -quiet"
elif [ "$board" = "afcv4" ]; then
	sfp_jtag=""
elif [ "$board" = "afcv4_sfp" ]; then
	sfp_jtag="jtag newtap auto0 tap -irlen 8 -ignore-version -expected-id 0x16d4a093"
else
	echo "Board '${board}' not supported!"
	exit 1
fi

if [ "$interface" = "ftdi" ]; then
	openocd -f afcv4-ftdi-jtag.cfg \
			-c "init" \
			-c "exit" \
			-c "${scansta_cmd}" \
			-c "svf boot-from-flash.svf -quiet" \
			-c "ftdi_set_signal JEN 0"
elif [ "$interface" = "xvc" ]; then
	xvc_host="$3"
	xvc_port="$4"

	if [ -z "$xvc_host" -o -z "$xvc_port" ]; then
		echo "Usage: $0 board xvc hostname port"
		exit 1
	fi

	openocd -c "adapter driver xvc" \
			-c "adapter speed 3000" \
			-c "xvc_host ${xvc_host}" \
			-c "xvc_port ${xvc_port}" \
			-c "reset_config none" \
			-c "${sfp_jtag}" \
			-c "jtag newtap xc7 tap -irlen 6 -ignore-version -expected-id 0x03636093" \
			-c "pld device virtex2 xc7.tap 1" \
			-c "init" \
			-c "${scansta_cmd}" \
			-c "svf boot-from-flash.svf -quiet" \
			-c "exit"
else
	echo "Interface '${interface}' not supported!"
	exit 1
fi
