#!/usr/bin/env bash

TIMES=500
START=1

for (( n=$START; n<= $TIMES; n++ ))
do
    echo $n
    python3 Simulator/main-latest-all.py $n
done

python3 compute7.py $TIMES
