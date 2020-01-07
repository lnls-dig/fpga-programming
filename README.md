# Description

Automated scripts to program bitstreams into AFC's Xilinx Virtex 7 FPGA

## Serial Programming

This is used to program a bitstream through Serial mode:

    ./vivado-prog.py --svf=<svf_to_be executed_prior_to_programming> --prog_serial --host_url=<remote_ip>:<remote_port> --bit=<bitstream_filename>

## Flash Programming

This is used to program a bitstream through Indirect Flash mode:

    ./vivado-prog.py --svf=<svf_to_be executed_prior_to_programming> --prog_flash --mcs=<bitstream_filename_with_mcs_extension> --bit_to_mcs --host_url=<remote_ip>:<remote_port> --bit=<bitstream_filename>

## nSVF Programming

If using NAT MCH with nSVF + CURL support you can use the following:

    ./curl-prog.py <nsvf_to_be_programmed> <host> <slot_to_be_programmed (see NAT JSM manual)>

Be advised that you need to generate a .svf file from a .bit file and
then convert it to the .nsvf file using the NAT provided binary.

To generate a .svf file for either serial of flash programming, see below.

## Generation of .svf file from bitstream for Flash programming

This is used to generate a .svf file from a given bitstream file. This
is intended to be run with a JTAG tool for indirect Flash programming,
such as the one available inside Vivado

    ./vivado-prog.py --svf=<svf_to_be executed_prior_to_programming> --bit_to_mcs --mcs_to_svf=<output_svf_filename> --bit=<bitstream_filename>

## Generation of .svf file from bitstream for Serial programming

This is used to generate a .svf file from a given bitstream file. This
is intended to be run with a JTAG tool for Serial programming,
such as the one available inside Vivado

    ./vivado-prog.py --svf=<svf_to_be executed_prior_to_programming> --bit_to_svf=<output_svf_filename> --bit=<bitstream_filename>

## Calling multiple instances

One can run this script multiple times in parallel, setting a different port for the hw_server.
To program the FPGA Flash:

    ./vivado-prog.py --svf=<svf_to_be executed_prior_to_programming> --prog_flash --mcs=<bitstream_filename_with_mcs_extension> --bit_to_mcs --host_url=<remote_ip1>:<remote_port1> --hw_server_url <hw_server_ip>:<port1> --bit=<bitstream_filename> &
    ./vivado-prog.py --svf=<svf_to_be executed_prior_to_programming> --prog_flash --mcs=<bitstream_filename_with_mcs_extension> --bit_to_mcs --host_url=<remote_ip2>:<remote_port2> --hw_server_url <hw_server_ip>:<port2> --bit=<bitstream_filename> &

Note that port1 and port2 must be different. Their values are arbitrary, but the safer option is to use values greater than 2000, avoiding conflict with other open ports
