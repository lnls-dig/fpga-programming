#!/bin/bash

# This is a simple example to show how to program multiple boards
# using the vivado-prog.py script. It does not aim to be generic,
# but to provide a starting point for more complex scripts

set -eoxo pipefail

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

for port in ${PORT[*]}; do
    echo "Programming AFC located in port: "${port}
    bitstream=
    if [ "${port}" == "2544" ]; then
        bitstream="../../rack_test/v1.0.0-rc2/afcv3-bpm-gw-fmc250m-bo-sirius-v1.0.0-rc2-20170628-2fe9e3a8be.bit"
    elif [ "${port}" == "2545" ]; then
        bitstream="../../rack_test/v1.0.0-rc2/afcv3-bpm-gw-fmc250m-sr-sirius-v1.0.0-rc2-20170628-2fe9e3a8be.bit"
    else
        bitstream="../../rack_test/v1.0.0-rc2/afcv3-bpm-gw-fmc250m-sr-uvx-v1.0.0-rc2-20170628-2fe9e3a8be.bit"
    fi

    echo "Using bitstream: " ${bitstream}

    command="time ../vivado-prog.py --bit_to_mcs \
        --bit=${bitstream} \
        --svf=../afc-scansta.svf \
        --mcs=dbe_bpm2.mcs --host_url=10.2.118.36:${port}"
    eval ${command}
    echo "Programming AFC completed at: "
    date
done
