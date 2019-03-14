#!/usr/bin/env python

from subprocess import call, Popen
import os
import argparse
import signal

def get_hw_server_pids(hw_server_url):
    pids = []
    for dirname in os.listdir('/proc'):
        if dirname == 'curproc':
            continue
        try:
            with open('/proc/{}/cmdline'.format(dirname), mode='rb') as fd:
                content = fd.read().decode().split('\x00')
        except Exception:
            continue
        if ('tcp:'+hw_server_url) in content:
            pids.append(dirname)
    return pids

def kill_hw_server_procs(hw_server_url):
    pids = get_hw_server_pids(hw_server_url)
    for proc in pids:
        os.kill(int(proc), signal.SIGKILL)

curpid = str(os.getpid())

parser = argparse.ArgumentParser(description='Program Xilinx FPGA routed with SCANSTA JTAG switch using Vivado tool')
parser.add_argument('--bit', type=str, help='Bitstream path')
parser.add_argument('--prog_serial', action='store_true', help='Program FPGA via FPGA serial', default=False)
parser.add_argument('--prog_flash', action='store_true', help='Program Flash via Indirect programming', default=False)
parser.add_argument('--mcs', type=str, help='Path to MCS formatted that will be written to FLASH')
parser.add_argument('--svf', type=str, help='SVF configuration file to run before the FPGA programming')
parser.add_argument('--vivado', type=str, help='Vivado binary path', default='/opt/Xilinx/Vivado/2016.3/bin/vivado')
parser.add_argument('--hw_server', type=str, help='HW Server binary path', default='/opt/Xilinx/Vivado/2016.3/bin/hw_server')
parser.add_argument('--host_url', type=str, help='Host URL in format <ip>:<port>', default='localhost:3121')
parser.add_argument('--hw_server_url', type=str, help='HW Server Host URL in format <ip>:<port>', default='localhost:3121')
parser.add_argument('--bit_to_mcs', action='store_true', help='Generate .mcs from given .bit file and write to FLASH',  default=False)
parser.add_argument('--mcs_to_svf', type=str, help='Generate .svf from given .mcs file')
parser.add_argument('--bit_to_svf', type=str, help='Generate .svf from given .bit file')
parser.add_argument('-r', '--repetitions', type=int, help='Number of times to repeat the configuration proccess', default=1)

args = parser.parse_args()

if (args.prog_serial and args.prog_flash):
    print( 'WARNING: This script will write both FLASH and FPGA RAM in this specific order, so the actual bitstream running will be in the FPGA RAM until the FPGA is power cycled.' )

#Create MCS file from given bitstream
if (args.bit and args.bit_to_mcs):
    with open('mcs-vivado-gen.cmd','r') as mcs_script_template, open(curpid+'temp-mcs-vivado-gen.cmd','w') as mcs_script_new:
        for line in mcs_script_template:
            mcs_script_new.write(line.replace('${BITSTREAM_FILE}', args.bit).replace('${MCS_NAME}', args.bit.replace('.bit','.mcs')))
    call([args.vivado, '-mode', 'batch', '-source', curpid+'temp-mcs-vivado-gen.cmd'])
    os.remove(curpid+'temp-mcs-vivado-gen.cmd')

#Create SVF file from given MCS
if (args.bit and args.mcs_to_svf):
    if not (args.svf):
        print( '\n\nWhen generating SVF from BIT an SVF file must be selected!\n')
        quit()
    with open('svf-vivado-gen.cmd','r') as svf_script_template, open(curpid+'temp-svf-vivado-gen.cmd','w') as svf_script_new:
        for line in svf_script_template:
            svf_script_new.write(line.replace('${SVF_FILE}', args.svf).replace('${MCS_FILE}', args.bit.replace('.bit','.mcs')).replace('${HW_SERVER_URL}', args.hw_server_url).replace('${BITSTREAM_FILE}', args.bit).replace('${OUTPUT_SVF_FILE}', args.mcs_to_svf))
    call([args.vivado, '-mode', 'batch', '-source', curpid+'temp-svf-vivado-gen.cmd'])
    os.remove(curpid+'temp-svf-vivado-gen.cmd')
    # Now, prepend the input SVF with the generated one
    with open(args.mcs_to_svf, 'r') as original: data = original.read()
    with open(args.svf, 'r') as svf_prepend: svf_data = svf_prepend.read()
    with open(args.mcs_to_svf, 'w') as modified: modified.write(svf_data + data)

#Create SVF file from given BIT
if (args.bit and args.bit_to_svf):
    if not (args.svf):
        print( '\n\nWhen generating SVF from BIT an SVF file must be selected!\n')
        quit()
    with open('svf-serial-vivado-gen.cmd','r') as svf_script_template, open(curpid+'temp-svf-serial-vivado-gen.cmd','w') as svf_script_new:
        for line in svf_script_template:
            svf_script_new.write(line.replace('${SVF_FILE}', args.svf).replace('${BITSTREAM_FILE}', args.bit).replace('${HW_SERVER_URL}', args.hw_server_url).replace('${OUTPUT_SVF_FILE}', args.bit_to_svf))
    call([args.vivado, '-mode', 'batch', '-source', curpid+'temp-svf-serial-vivado-gen.cmd'])
    os.remove(curpid+'temp-svf-serial-vivado-gen.cmd')
    # Now, prepend the input SVF with the generated one
    with open(args.bit_to_svf, 'r') as original: data = original.read()
    with open(args.svf, 'r') as svf_prepend: svf_data = svf_prepend.read()
    with open(args.bit_to_svf, 'w') as modified: modified.write(svf_data + data)

#Write new impact batch command files based on templates
if (args.svf and not args.mcs_to_svf and not args.bit_to_svf):
    with open('scansta-vivado-cfg.cmd','r') as svf_script_template, open(curpid+'temp-scansta-vivado.cmd','w') as svf_script_new:
        for line in svf_script_template:
            svf_script_new.write(line.replace('${HOST_URL}', args.host_url).replace('${SVF_FILE}', args.svf).replace('${HW_SERVER_URL}', args.hw_server_url))
    hw_server_p = Popen([args.hw_server, '-s', 'tcp:'+args.hw_server_url])
    call([args.vivado, '-mode', 'batch', '-source', curpid+'temp-scansta-vivado.cmd'])
    kill_hw_server_procs(args.hw_server_url)
    os.remove(curpid+'temp-scansta-vivado.cmd')

for i in range(0, args.repetitions) :
    #Program MCS file to FPGA FLASH
    if (args.prog_flash):
        print( '\n\nProgramming Flash!\n')
        with open('flash-vivado-load.cmd','r') as flash_script_template, open(curpid+'temp-flash-vivado-load.cmd','w') as flash_script_new:
            for line in flash_script_template:
                flash_script_new.write(line.replace('${HOST_URL}', args.host_url).replace('${MCS_FILE}', args.mcs).replace('${HW_SERVER_URL}', args.hw_server_url))
        hw_server_p = Popen([args.hw_server, '-s', 'tcp:'+args.hw_server_url])
        call([args.vivado, '-mode', 'batch', '-source', curpid+'temp-flash-vivado-load.cmd'])
        kill_hw_server_procs(args.hw_server_url)
        os.remove(curpid+'temp-flash-vivado-load.cmd')

    #Program bit file to FPGA RAM
    if (args.prog_serial):
        print( '\n\nDownloading bitstream!\n')
        with open('fpga-vivado-load.cmd','r') as bit_script_template, open(curpid+'temp-fpga-vivado-load.cmd','w') as bit_script_new:
            for line in bit_script_template:
                bit_script_new.write(line.replace('${HOST_URL}', args.host_url).replace('${BITSTREAM_FILE}', args.bit).replace('${HW_SERVER_URL}', args.hw_server_url))
        hw_server_p = Popen([args.hw_server, '-s', 'tcp:'+args.hw_server_url])
        call([args.vivado, '-mode', 'batch', '-source', curpid+'temp-fpga-vivado-load.cmd'])
        kill_hw_server_procs(args.hw_server_url)
        os.remove(curpid+'temp-fpga-vivado-load.cmd')

