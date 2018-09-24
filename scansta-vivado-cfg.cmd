open_hw
connect_hw_server -url "${HW_SERVER_URL}"
open_hw_target -quiet -xvc_url "${HOST_URL}"
execute_hw_svf "${SVF_FILE}"
