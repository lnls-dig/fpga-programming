open_hw
connect_hw_server -url "${HW_SERVER_URL}"
open_hw_target -xvc_url "${HOST_URL}"

set_property PROGRAM.FILE {${BITSTREAM_FILE}} [lindex [get_hw_devices] 0]
program_hw_devices [lindex [get_hw_devices] 0]
