open_hw
connect_hw_server
create_hw_target flash_afcv3
open_hw_target

create_hw_device -part xc7a200t
set_property PROGRAM.FILE {${BITSTREAM_FILE}} [lindex [get_hw_devices] 0]
program_hw_devices [lindex [get_hw_devices] 0]
write_hw_svf "${OUTPUT_SVF_FILE}"

close_hw_target
exit
