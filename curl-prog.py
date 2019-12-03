#!/usr/bin/env python

from subprocess import call, Popen
import os
import argparse
import signal

parser = argparse.ArgumentParser(description='Program NAT AMC FPGA using CURL tool')
parser.add_argument('--nsvf', type=str, help='nSVF configuration file to program FPGA (need to use NAT nsvf tool)')
parser.add_argument('--host_ip', type=str, help='Host IP, either hostname or IP', default=False)
parser.add_argument('--slot', type=int, help='Crate slot number', default=False)
parser.add_argument('--curl_bin', type=str, help='CURL binary if not in PATH', default='curl')
parser.add_argument('--freq_target', type=int, help='Target frequency for the internal JTAG chain (see NAT JSM manual)', default='9')
parser.add_argument('--host_user', type=str, help='Host username', default='root')
parser.add_argument('--host_pass', type=str, help='Host password', default='nat')

args = parser.parse_args()

print('\nDownloading bitstream: {bitstream}, in Crate: {crate}, slot number: {slot}\n'.format(
    bitstream=args.nsvf, crate=args.host_ip, slot=args.slot))
call([args.curl_bin,
    '-H',
    '"Content-Type: multipart/form-data"',
    '-F',
    '"XsvfReqTarget=${SLOT_NSVF}"'.replace('${SLOT_NSVF}', str(args.slot)),
    '-F',
    '"XsvfReqFreq=${FREQ_TARGET}"'.replace('${FREQ_TARGET}', str(args.freq_target)),
    '-F',
    '"filename=@${BITSTREAM_NSVF}"'.replace('${BITSTREAM_NSVF}', args.nsvf),
    '-X',
    'POST',
    '-u',
    '"${HOST_USER}":"${HOST_PASS}"'.replace('${HOST_USER}', args.host_user).replace('${HOST_PASS}', args.host_pass),
    'http://${HOST_IP}/goform/ctrl_svf_proc'.replace('${HOST_IP}', args.host_ip)
    ])
