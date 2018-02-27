#!/usr/bin/env python

from subprocess import call
import os
import argparse

parser = argparse.ArgumentParser(description='Program Xilinx FPGA routed with SCANSTA JTAG switch using Vivado tool')
parser.add_argument('--bit', type=str, help='Bitstream path')
parser.add_argument('--prog_serial', action='store_true', help='Program FPGA via FPGA serial', default=False)
parser.add_argument('--prog_flash', action='store_true', help='Program Flash via Indirect programming', default=False)
parser.add_argument('--mcs', type=str, help='Path to MCS formatted that will be written to FLASH')
parser.add_argument('--svf', type=str, help='SVF configuration file to run before the FPGA programming')
parser.add_argument('--vivado', type=str, help='Vivado binary path', default='/opt/Xilinx/Vivado/2016.3/bin/vivado')
parser.add_argument('--host_url', type=str, help='Host URL in format <ip>:<port>', default='localhost:3121')
parser.add_argument('--bit_to_mcs', action='store_true', help='Generate .mcs from given .bit file and write to FLASH',  default=False)
parser.add_argument('--mcs_to_svf', type=str, help='Generate .svf from given .mcs file')
parser.add_argument('--bit_to_svf', type=str, help='Generate .svf from given .bit file')
parser.add_argument('-r', '--repetitions', type=int, help='Number of times to repeat the configuration proccess', default=1)

args = parser.parse_args()

if (args.prog_serial and args.prog_flash):
    print( 'WARNING: This script will write both FLASH and FPGA RAM in this specific order, so the actual bitstream running will be in the FPGA RAM until the FPGA is power cycled.' )

#Create MCS file from given bitstream
if (args.bit and args.bit_to_mcs):
    with open('mcs-vivado-gen.cmd','r') as mcs_script_template, open('temp-mcs-vivado-gen.cmd','w') as mcs_script_new:
        for line in mcs_script_template:
            mcs_script_new.write(line.replace('${BITSTREAM_FILE}', args.bit).replace('${MCS_NAME}', args.bit.replace('.bit','.mcs')))
    call([args.vivado, '-mode', 'batch', '-source', 'temp-mcs-vivado-gen.cmd'])
    os.remove('temp-mcs-vivado-gen.cmd')

#Create SVF file from given MCS
if (args.bit and args.mcs_to_svf):
    if not (args.svf):
        print( '\n\nWhen generating SVF from BIT an SVF file must be selected!\n')
        quit()
    with open('svf-vivado-gen.cmd','r') as svf_script_template, open('temp-svf-vivado-gen.cmd','w') as svf_script_new:
        for line in svf_script_template:
            svf_script_new.write(line.replace('${SVF_FILE}', args.svf).replace('${MCS_FILE}', args.bit.replace('.bit','.mcs')).replace('${BITSTREAM_FILE}', args.bit).replace('${OUTPUT_SVF_FILE}', args.mcs_to_svf))
    call([args.vivado, '-mode', 'batch', '-source', 'temp-svf-vivado-gen.cmd'])
    os.remove('temp-svf-vivado-gen.cmd')
    # Now, prepend the input SVF with the generated one
    with open(args.mcs_to_svf, 'r') as original: data = original.read()
    with open(args.svf, 'r') as svf_prepend: svf_data = svf_prepend.read()
    with open(args.mcs_to_svf, 'w') as modified: modified.write(svf_data + data)

#Create SVF file from given BIT
if (args.bit and args.bit_to_svf):
    if not (args.svf):
        print( '\n\nWhen generating SVF from BIT an SVF file must be selected!\n')
        quit()
    with open('svf-serial-vivado-gen.cmd','r') as svf_script_template, open('temp-svf-serial-vivado-gen.cmd','w') as svf_script_new:
        for line in svf_script_template:
            svf_script_new.write(line.replace('${SVF_FILE}', args.svf).replace('${BITSTREAM_FILE}', args.bit).replace('${OUTPUT_SVF_FILE}', args.bit_to_svf))
    call([args.vivado, '-mode', 'batch', '-source', 'temp-svf-serial-vivado-gen.cmd'])
    os.remove('temp-svf-serial-vivado-gen.cmd')
    # Now, prepend the input SVF with the generated one
    with open(args.mcs_to_svf, 'r') as original: data = original.read()
    with open(args.svf, 'r') as svf_prepend: svf_data = svf_prepend.read()
    with open(args.mcs_to_svf, 'w') as modified: modified.write(svf_data + data)

#Write new impact batch command files based on templates
if (args.svf and not args.mcs_to_svf and not args.bit_to_svf):
    with open('scansta-vivado-cfg.cmd','r') as svf_script_template, open('temp-scansta-vivado.cmd','w') as svf_script_new:
        for line in svf_script_template:
            svf_script_new.write(line.replace('${HOST_URL}', args.host_url).replace('${SVF_FILE}', args.svf))
    call([args.vivado, '-mode', 'batch', '-source', 'temp-scansta-vivado.cmd'])
    os.remove('temp-scansta-vivado.cmd')

for i in range(0, args.repetitions) :
    #Program MCS file to FPGA FLASH
    if (args.prog_flash):
        print( '\n\nProgramming Flash!\n')
        with open('flash-vivado-load.cmd','r') as flash_script_template, open('temp-flash-vivado-load.cmd','w') as flash_script_new:
            for line in flash_script_template:
                flash_script_new.write(line.replace('${HOST_URL}', args.host_url).replace('${MCS_FILE}', args.mcs))
        call([args.vivado, '-mode', 'batch', '-source', 'temp-flash-vivado-load.cmd'])
        os.remove('temp-flash-vivado-load.cmd')

    #Program bit file to FPGA RAM
    if (args.prog_serial):
        print( '\n\nDownloading bitstream!\n')
        with open('fpga-vivado-load.cmd','r') as bit_script_template, open('temp-fpga-vivado-load.cmd','w') as bit_script_new:
            for line in bit_script_template:
                bit_script_new.write(line.replace('${HOST_URL}', args.host_url).replace('${BITSTREAM_FILE}', args.bit))
        call([args.vivado, '-mode', 'batch', '-source', 'temp-fpga-vivado-load.cmd'])
        os.remove('temp-fpga-vivado-load.cmd')

