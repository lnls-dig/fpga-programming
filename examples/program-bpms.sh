#!/bin/bash

# This is a simple example to show how to program multiple boards
# using the vivado-prog.py script. It does not aim to be generic,
# but to provide a starting point for more complex scripts

set -eoxo pipefail

SCRIPT_DIR=$(dirname "$0")
BIT_EXTENSION=.bit
MCS_EXTENSION=.mcs
PORT=(\
    "2544" \
    "2545" \
    "2546" \
    "2547" \
    "2548" \
    "2549" \
    "2550" \
    "2551" \
    "2552" \
    )

cd ${SCRIPT_DIR}/../
for port in ${PORT[*]}; do
    echo "Programming AFC located in port: "${port}
    bitstream_raw=
    bitstream_bit=
    bitstream_mcs=
    if [ "${port}" == "2544" ]; then
        bitstream_raw="../rack_test/v1.0.0-rc2/afcv3-bpm-gw-fmc250m-bo-sirius-v1.0.0-rc2-20170628-2fe9e3a8be"
    elif [ "${port}" == "2545" ]; then
        bitstream_raw="../rack_test/v1.0.0-rc2/afcv3-bpm-gw-fmc250m-sr-sirius-v1.0.0-rc2-20170628-2fe9e3a8be"
    else
        bitstream_raw="../rack_test/v1.0.0-rc2/afcv3-bpm-gw-fmc250m-sr-uvx-v1.0.0-rc2-20170628-2fe9e3a8be"
    fi
    bitstream_bit=${bitstream_raw}${BIT_EXTENSION}
    bitstream_mcs=${bitstream_raw}${MCS_EXTENSION}
    #bitstream="/home/lerwys/afcv3-bpm-gw-fmc250m-sr-sirius-v1.0.0-rc2-20170703-2fe9e3a8be.bit"

    echo "Using bitstream: " ${bitstream_bit}

    echo "Programming started at: "
    date
    ./vivado-prog.py --bit_to_mcs \
        --bit=${bitstream_bit} \
        --svf=./afc-scansta.svf \
        --mcs=${bitstream_mcs} \
        --host_url=10.0.18.33:${port}
    echo "Programming finished at: "
    date
done
