#!/usr/bin/env python3
import warnings
import config
import numpy as np
from latplan.model import ActionAE, default_networks
from latplan.util        import curry
from latplan.util.tuning import grid_search, nn_task

import keras.backend as K
import tensorflow as tf

float_formatter = lambda x: "%.3f" % x
np.set_printoptions(formatter={'float_kind':float_formatter})

################################################################

# default values
default_parameters = {
    'lr'              : 0.0001,
    'batch_size'      : 2000,
    'full_epoch'      : 1000,
    'epoch'           : 1000,
    'max_temperature' : 5.0,
    'min_temperature' : 0.1,
    'M'               : 2,
}

if __name__ == '__main__':
    import numpy.random as random

    import sys
    if len(sys.argv) == 1:
        sys.exit("{} [directory]".format(sys.argv[0]))

    directory = sys.argv[1]
    directory_aae = "{}/_aae/".format(directory)
    mode = sys.argv[2]
    
    data = np.loadtxt("{}/actions.csv".format(directory),dtype=np.int8)
    
    parameters = {
        'N'          :[1],
        'M'          :[128],
        'layer'      :[400],# 200,300,400,700,1000
        'encoder_layers' : [2], # 0,2,3
        'decoder_layers' : [2], # 0,1,3
        'dropout'    :[0.4], #[0.1,0.4],
        # 'dropout_z'  :[False],
        'batch_size' :[2000],
        'full_epoch' :[1000],
        'epoch'      :[1000],
        'encoder_activation' :['relu'], # 'tanh'
        'decoder_activation' :['relu'], # 'tanh',
        # quick eval
        'lr'         :[0.001],
    }
    print(data.shape)
    try:
        if 'learn' in mode:
            raise Exception('learn')
        aae = ActionAE(directory_aae).load()
    except:
        aae,_,_ = grid_search(curry(nn_task, ActionAE, directory_aae,
                                    data[:12000], data[:12000],
                                    data[12000:], data[12000:],),
                              default_parameters,
                              parameters)

    aae.plot(data[:8], "aae_train.png")
    aae.plot(data[12000:12008], "aae_test.png")

    from latplan.util import get_ae_type
    ae = default_networks[get_ae_type(directory)](directory).load()

    aae.plot(data[:8], "aae_train_decoded.png", ae=ae)
    aae.plot(data[12000:12008], "aae_test_decoded.png", ae=ae)
    
    
    actions = aae.encode_action(data, batch_size=1000)
    actions_r = actions.round()

    histogram = actions.sum(axis=0)
    print(histogram)
    histogram_r = actions_r.sum(axis=0,dtype=int)
    print(histogram_r)
    print (np.count_nonzero(histogram_r > 0))
        
"""* Summary:
Input: a subset of valid action pairs.

* Training:

* Evaluation:



If the number of actions are too large, they simply does not appear in the
training examples. This means those actions can be pruned, and you can lower the number of actions.

"""
