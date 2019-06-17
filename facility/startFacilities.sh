#!/bin/bash

echo "Type help to view commands" 

HELP="help"
KILLALL="killall"
RUNALL="runall"
GENERATE="generate"
LIST_FACILITIES="lsfac"
DELETE_FACILITIES="rmfac"

PID_ARR=( )

while true; do
    echo
    echo "Ready"
    read USER_INPUT
    if [ "$USER_INPUT" = "$KILLALL" ]; then
        for i in "${PID_ARR[@]}"; do
            kill $i
        done
        PID_ARR=()
    fi
    if [ "$USER_INPUT" = "$RUNALL" ]; then
        for filename in facilities/*.json; do
            python3 facility.py "$filename" & PID_ARR+=($!)
        done   
    fi
    if [ "$USER_INPUT" = "$GENERATE" ]; then
        echo "How many facilities do you want?"
        read FAC_NMB
        echo "How many cycles do you want?"
        read CYCLE_NMB
        echo "How many messages do you want per cycle?"
        read UPDATE_NMB
        python3 generateFacilities.py $FAC_NMB $CYCLE_NMB $UPDATE_NMB
        ./../stateServices/loadDatabases.sh
    fi
    if [ "$USER_INPUT" = "$LIST_FACILITIES" ]; then
        for filename in facilities/*.json; do
            echo $filename
        done
    fi
    if [ "$USER_INPUT" = "$DELETE_FACILITIES" ]; then
        rm facilities/*.json
    fi
    if [ "$USER_INPUT" = "$HELP" ]; then
        echo "killall --Kill all facilities"
        echo "runall" --Run all facilities from port 8000
        echo "generate" --Generate facilities
        echo "lsfac" --List facility files
        echo "rmfac" --Remove all facilities
    fi
done
