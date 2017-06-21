setPreference -pref ConfigOnFailure:Continue
setMode -bs
setCable -port usb21 -baud 12000000
addDevice -p 1 -file "${SFV_FILE}"
Play
exit
