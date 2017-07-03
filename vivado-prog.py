#!/usr/bin/env python

from subprocess import call
import os
import argparse

parser = argparse.ArgumentParser(description='Program Xilinx FPGA routed with SCANSTA JTAG switch using Vivado tool')
parser.add_argument('--bit', type=str, help='Bitstream path')
parser.add_argument('--mcs', type=str, help='Path to MCS formatted that will be written to FLASH')
parser.add_argument('--svf', type=str, help='SVF configuration file to run before the FPGA programming')
parser.add_argument('--vivado', type=str, help='Vivado binary path', default='/opt/Xilinx/Vivado/2016.3/bin/vivado')
parser.add_argument('--host_url', type=str, help='Host URL in format <ip>:<port>', default='localhost:3121')
parser.add_argument('--bit_to_mcs', action='store_true', help='Generate .mcs from given .bit file and write to FLASH',  default=False)
parser.add_argument('-r', '--repetitions', type=int, help='Number of times to repeat the configuration proccess', default=1)

args = parser.parse_args()

if (args.bit and args.mcs):
    print( 'WARNING: This script will write both FLASH and FPGA RAM in this specific order, so the actual bitstream running will be in the FPGA RAM until the FPGA is power cycled.' )

#Create MCS file from given bitstream
if (args.bit and args.bit_to_mcs):
    with open('mcs-vivado-gen.cmd','r') as mcs_script_template, open('temp-mcs-vivado-gen.cmd','w') as mcs_script_new:
        for line in mcs_script_template:
            mcs_script_new.write(line.replace('${BITSTREAM_FILE}', args.bit).replace('${MCS_NAME}', os.path.basename(args.bit).replace('.bit','.mcs')))
    call([args.vivado, '-mode', 'batch', '-source', 'temp-mcs-vivado-gen.cmd'])
    args.bit = ''
    os.remove('temp-mcs-vivado-gen.cmd')

#Write new impact batch command files based on templates
if (args.svf):
    with open('scansta-vivado-cfg.cmd','r') as svf_script_template, open('temp-scansta-vivado.cmd','w') as svf_script_new:
        for line in svf_script_template:
            svf_script_new.write(line.replace('${HOST_URL}', args.host_url).replace('${SVF_FILE}', args.svf))
    call([args.vivado, '-mode', 'batch', '-source', 'temp-scansta-vivado.cmd'])
#    os.remove('temp-scansta-vivado.cmd')

for i in range(0, args.repetitions) :
    #Program MCS file to FPGA FLASH
    if (args.mcs):
        print( '\n\nProgramming Flash!\n')
        with open('flash-vivado-load.cmd','r') as flash_script_template, open('temp-flash-vivado-load.cmd','w') as flash_script_new:
            for line in flash_script_template:
                flash_script_new.write(line.replace('${HOST_URL}', args.host_url).replace('${MCS_FILE}', args.mcs))
        call([args.vivado, '-mode', 'batch', '-source', 'temp-flash-vivado-load.cmd'])
        os.remove('temp-flash-vivado-load.cmd')

    #Program bit file to FPGA RAM
    if (args.bit):
        print( '\n\nDownloading bitstream!\n')
        with open('fpga-vivado-load.cmd','r') as bit_script_template, open('temp-fpga-vivado-load.cmd','w') as bit_script_new:
            for line in bit_script_template:
                bit_script_new.write(line.replace('${HOST_URL}', args.host_url).replace('${BITSTREAM_FILE}', args.bit))
        call([args.vivado, '-mode', 'batch', '-source', 'temp-fpga-vivado-load.cmd'])
        os.remove('temp-fpga-vivado-load.cmd')

