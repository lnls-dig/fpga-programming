from subprocess import call
import argparse

parser = argparse.ArgumentParser(description='Program Xilinx FPGA routed with SCANSTA JTAG switch using IMPACT tool')
parser.add_argument('bit', type=str, help='Bitstream path')
parser.add_argument('--svf', type=str, help='SVF configuration file to run before the FPGA programming')
parser.add_argument('--impact', type=str, help='Impact binary path', default='/opt/Xilinx/14.7/LabTools/LabTools/bin/lin/impact')
#TODO: Add FLASH programming option

args = parser.parse_args()

svf_script_template = open('scansta-cfg.cmd','r')
bit_script_template = open('fpga-load.cmd','r')

#Write new impact batch command files based on templates
if (args.svf):
    with open('temp-scansta.cmd','w') as svf_script_new:
        for line in svf_script_template:
            svf_script_new.write(line.replace('${SFV_FILE}', args.svf))

with open('temp-fpga-load.cmd','w') as bit_script_new:
    for line in bit_script_template:
        bit_script_new.write(line.replace('${BITSTREAM_FILE}', args.bit))

svf_script_template.close()
bit_script_template.close()

if (args.svf):
    call( [args.impact, '-batch', 'temp-scansta.cmd'])

call( [args.impact, '-batch', 'temp-fpga-load.cmd'])

os.remove('temp-scansta.cmd')
os.remove('temp-fpga-load.cmd')
