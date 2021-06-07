open_hw
connect_hw_server -url "${HW_SERVER_URL}"
open_hw_target -quiet -xvc_url "${HOST_URL}"
close_hw_target
disconnect_hw_server
open_hw
connect_hw_server -url "${HW_SERVER_URL}"
open_hw_target -quiet -xvc_url "${HOST_URL}"
get_hw_targets
current_hw_target [get_hw_targets */xilinx_tcf/Xilinx/${HOST_URL}]
open_hw_target

set_property PROGRAM.FILE {${BITSTREAM_FILE}} [lindex [get_hw_devices] 0]
program_hw_devices [lindex [get_hw_devices] 0]
