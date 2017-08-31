#!/bin/bash

ulimit -v 16000000000

trap exit SIGINT

ncpu=$(cat /proc/cpuinfo | grep -c processor)
jobs=$((ncpu-1))

parallel -j $jobs --eta --timeout 180 --joblog problem-instances-salt/latplan.puzzles.puzzle_mnist.csv  \
         "./trivial-planner.py samples/{1} {2} {3} > {2}/{1}_{3}.log" \
         ::: puzzle_mnist_3_3_36_20000_conv \
         ::: problem-instances-salt/latplan.puzzles.puzzle_mnist/* \
         ::: Astar

parallel -j $jobs --eta --timeout 180 --joblog problem-instances-salt/latplan.puzzles.puzzle_mandrill.csv   \
         "./trivial-planner.py samples/{1} {2} {3} > {2}/{1}_{3}.log" \
         ::: puzzle_mandrill_3_3_36_20000_conv \
         ::: problem-instances-salt/latplan.puzzles.puzzle_mandrill/* \
         ::: Astar


parallel -j $jobs --eta --timeout 180 --joblog problem-instances-salt/latplan.puzzles.puzzle_spider.csv   \
         "./trivial-planner.py samples/{1} {2} {3} > {2}/{1}_{3}.log" \
         ::: puzzle_spider_3_3_36_20000_conv \
         ::: problem-instances-salt/latplan.puzzles.puzzle_spider/* \
         ::: Astar


parallel -j $jobs --eta --timeout 180 --joblog problem-instances-salt/latplan.puzzles.hanoi.csv   \
         "./trivial-planner.py samples/{1} {2} {3} > {2}/{1}_{3}.log" \
         ::: hanoi_7_4_36_10000_conv \
         ::: problem-instances-salt/latplan.puzzles.hanoi/* \
         ::: Astar


parallel -j $jobs --eta --timeout 180 --joblog problem-instances-salt/latplan.puzzles.lightsout_digital.csv   \
         "./trivial-planner.py samples/{1} {2} {3} > {2}/{1}_{3}.log" \
         ::: lightsout_digital_4_36_20000_conv \
         ::: problem-instances-salt/latplan.puzzles.lightsout_digital/* \
         ::: Astar


parallel -j $jobs --eta --timeout 180 --joblog problem-instances-salt/latplan.puzzles.lightsout_twisted.csv   \
         "./trivial-planner.py samples/{1} {2} {3} > {2}/{1}_{3}.log" \
         ::: lightsout_twisted_4_36_20000_conv \
         ::: problem-instances-salt/latplan.puzzles.lightsout_twisted/* \
         ::: Astar


