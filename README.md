# Description

Automated scripts to program bitstreams into AFC's Xilinx Virtex 7 FPGA

## Serial Programming

This is used to program a bitstream through Serial mode:

./vivado-prog.py --svf=<svf_to_be executed_prior_to_programming> --prog_serial --host_url=<remote_ip>:<remote_port> --bit=<bitstream_filename>

## Flash Programming

This is used to program a bitstream through Indirect Flash mode:

./vivado-prog.py --svf=<svf_to_be executed_prior_to_programming> --prog_flash --mcs=<bitstream_filename_with_mcs_extension> --bit_to_mcs --host_url=<remote_ip>:<remote_port> --bit=<bitstream_filename>

## Generation of .svf file from bitstream

This is used to generate a .svf file from a given bitstream file. This
is intended to be run with a JTAG tool, such as the one available inside
Vivado

./vivado-prog.py --svf=<svf_to_be executed_prior_to_programming> --bit_to_mcs --mcs_to_svf=<output_svf_filename> --bit=<bitstream_filename>
