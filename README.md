# Description

Automated scripts to program bitstreams into AFC's Xilinx Virtex 7 FPGA

## Generation of .svf file from bitstream

This is used to generate a .svf file from a given bitstream file. This
is intended to be run with a JTAG tool, such as the one available inside
Vivado

./vivado-prog.py --svf=<svf_to_be executed_prior_to_programming> --bit_to_mcs --mcs_to_svf=<output_svf_filename> --bit=<bitstream_filename>
