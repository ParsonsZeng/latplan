#!/usr/bin/env python3

import importlib
import numpy as np

import latplan
import latplan.puzzles.hanoi as p

# importlib.reload(p)

import itertools
c = [ c for c in itertools.islice(p.generate_configs(3,3), 10000) ]

from colors import color
from functools import partial

style = partial(color, fg='black', bg='white')

from latplan.util.timer import Timer

with Timer(style("************************* states on cpu ***************************")):
    s = p.generate(c,3,3)

print(s[:3])

with Timer(style("************************* validate_states ***************************")):
    print("results:", np.all(p.validate_states(s)), "(should be True)")


with Timer(style("************************* to_configs on gpu, batch=100 ***************************")):
    p.to_configs(s,batch_size=100)
    

with Timer(style("************************* to_configs on gpu, batch=1000 ***************************")):
    p.to_configs(s,batch_size=1000)

c = c[:10]

with Timer(style("************************* transitions ***************************")):
    transitions = p.transitions(3,3,configs=c)

with Timer(style("************************* transitions one_per_state ***************************")):
    transitions = p.transitions(3,3,configs=c,one_per_state=True)

with Timer(style("************************* validate_transitions ***************************")):
    results = p.validate_transitions(transitions,batch_size=1000)

print("all transitions valid?:",np.all(results))
print("if not, how many invalid?:",len(results)-np.count_nonzero(results), "/", len(results))
