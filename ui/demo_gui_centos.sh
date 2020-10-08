#!/bin/bash  --login     

# Include libraries into library path.
# export LD_LIBRARY_PATH=../_opilib/linux_x86_64
# Include plugin libraries 
# export QT_PLUGIN_PATH=../gui/qeframework/lib/linux_x86_64
# export QT_PLUGIN_PATH=${QT_PLUGIN_PATH}:../gui/qtfsm/lib/linux_x86_64
   
export QE_UI_PATH="."
qegui -o -m "P=CAPROTO_DEMO" demo_top.ui &

 
# end
