#!/bin/bash

# This is a simple example to show how to program multiple boards
# using the vivado-prog.py script. It does not aim to be generic,
# but to provide a starting point for more complex scripts

set -eo pipefail

SCRIPT_DIR=$(dirname "$0")
BIT_EXTENSION=.bit
MCS_EXTENSION=.mcs
# This must follow the format "<port_number>,<bitstream_name_without_extension>"
PORT_BITSTREAM=(\
    "2541,bit1 " \
    "2542,bit2 " \
    "2543,bit3 " \
    "2544,bit4 " \
    "2545,bit5 " \
    "2546,bit6 " \
    "2547,bit7 " \
    "2548,bit8 " \
    "2549,bit9 " \
    "2550,bit10" \
    "2551,bit11" \
    "2552,bit12" \
    )

cd ${SCRIPT_DIR}/../
for portbit in ${PORT_BITSTREAM[*]}; do
    OLDIFS=$IFS; IFS=',';
    # Separate "tuple" arguments with positional notation
    set -- ${portbit};
    port=$1
    bitstream_raw=$2

    if [ "${bitstream_raw}" ]; then
        echo "Programming AFC located in port: "${port}

        # Bitstream/MCS names
        bitstream_bit=${bitstream_raw}${BIT_EXTENSION}
        bitstream_mcs=${bitstream_raw}${MCS_EXTENSION}

        echo "Using bitstream: " ${bitstream_bit}
        echo "Using mcs: " ${bitstream_mcs}

        echo "Programming started at: "
        date
        ./vivado-prog.py \
            --bit_to_mcs \
            --bit=${bitstream_bit} \
            --mcs=${bitstream_mcs} \
            --svf=./afc-scansta.svf \
            --prog_flash \
            --host_url=10.0.18.33:${port}
        echo "Programming finished at: "
        date
    fi

    IFS=$OLDIFS;
done;
