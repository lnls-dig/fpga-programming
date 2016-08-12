from subprocess import call
import os
import argparse

parser = argparse.ArgumentParser(description='Program Xilinx FPGA routed with SCANSTA JTAG switch using IMPACT tool')
parser.add_argument('--bit', type=str, help='Bitstream path')
parser.add_argument('--mcs', type=str, help='Path to MCS formatted that will be written to FLASH')
parser.add_argument('--svf', type=str, help='SVF configuration file to run before the FPGA programming')
parser.add_argument('--impact', type=str, help='Impact binary path', default='/opt/Xilinx/14.7/LabTools/LabTools/bin/lin/impact')
parser.add_argument('--bit_to_mcs', action='store_true', help='Generate .mcs from given .bit file and write to FLASH',  default=False)

args = parser.parse_args()

if (args.bit and args.mcs):
    print( 'WARNING: This script will write both FLASH and FPGA RAM in this specific order, so the actual bitstream running will be in the FPGA RAM' )

#Create MCS file from given bitstream
if (args.bit and args.bit_to_mcs):
    with open('mcs-gen.cmd','r') as mcs_script_template, open('temp-mcs-gen.cmd','w') as mcs_script_new:
        for line in mcs_script_template:
            mcs_script_new.write(line.replace('${BITSTREAM_FILE}', args.bit).replace('${MCS_NAME}', os.path.basename(args.bit).replace('.bit','.mcs')))
    call([args.impact, '-batch', 'temp-mcs-gen.cmd'])
    args.mcs = args.bit.replace('.bit','.mcs')
    args.bit = ''
    os.remove('temp-mcs-gen.cmd')

#Write new impact batch command files based on templates
if (args.svf):
    with open('scansta-cfg.cmd','r') as svf_script_template, open('temp-scansta.cmd','w') as svf_script_new:
        for line in svf_script_template:
            svf_script_new.write(line.replace('${SFV_FILE}', args.svf))
    call( [args.impact, '-batch', 'temp-scansta.cmd'])
    os.remove('temp-scansta.cmd')

if (args.mcs):
    print( '\n\nProgramming Flash!\n')
    with open('flash-load.cmd','r') as flash_script_template, open('temp-flash-load.cmd','w') as flash_script_new:
        for line in flash_script_template:
            flash_script_new.write(line.replace('${MCS_FILE}', args.mcs))
    call( [args.impact, '-batch', 'temp-flash-load.cmd'])
    os.remove('temp-flash-load.cmd')

if (args.bit):
    print( '\n\nDownloading bitstream!\n')
    with open('fpga-load.cmd','r') as bit_script_template, open('temp-fpga-load.cmd','w') as bit_script_new:
        for line in bit_script_template:
            bit_script_new.write(line.replace('${BITSTREAM_FILE}', args.bit))
    call( [args.impact, '-batch', 'temp-fpga-load.cmd'])
    os.remove('temp-fpga-load.cmd')

