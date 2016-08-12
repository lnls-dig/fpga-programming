setPreference -pref ConfigOnFailure:Continue
setMode -bs
setCable -port auto
addDevice -p 1 -file "${SFV_FILE}"
Play
exit
