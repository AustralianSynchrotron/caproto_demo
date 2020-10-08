REM the UI_PATH is the path to the capmac module ui directory
REM you also need qegui to be in the PATH
SET UI_PATH=.
qegui.exe -a 90 -o -m "P=CAPROTO_DEMO"  %UI_PATH%/demo_top.ui &
PAUSE