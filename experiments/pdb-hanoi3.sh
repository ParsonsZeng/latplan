#!/bin/bash
./plan.py pdb 'run_hanoi ( "samples/hanoi3_fc2" ,"fc2", import_module("puzzles.hanoi" ), 3)' |& tee $(dirname $0)/pdb-hanoi3.log
