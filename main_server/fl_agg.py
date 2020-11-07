from __future__ import print_function

import glob
import tensorflow as tf
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense
import os

cwd = os.getcwd()
    
def scale_model_weights(weight, scalar):
    '''function for scaling a models weights'''
    weight_final = []
    steps = len(weight)
    for i in range(steps):
        weight_final.append(scalar * weight[i])
    return weight_final

def sum_scaled_weights(scaled_weight_list):
    '''Return the sum of the listed scaled weights. The is equivalent to scaled avg of the weights'''
    avg_grad = list()
    #get the average grad accross all client gradients
    for grad_list_tuple in zip(*scaled_weight_list):
        layer_mean = tf.math.reduce_sum(grad_list_tuple, axis=0)
        avg_grad.append(layer_mean)
        
    return avg_grad

def fl_average():
    client_models_path = os.listdir(cwd + "/client_models/")
       
    scaled_local_weight_list = []
    
    for path in client_models_path:
        print("Loading Model...")
        print(path)
       
        local_model = tf.keras.models.load_model(cwd + "/client_models/" + path)
        local_model.compile(Adam(lr=.0001), loss='categorical_crossentropy', metrics=['accuracy'])
        local_weights= local_model.get_weights()
        scaling_factor = 1/3
        scaled_weights = scale_model_weights(local_model.get_weights(), scaling_factor)
        
        print(len(local_weights))
        scaled_local_weight_list.append(scaled_weights)
        
    return scaled_local_weight_list


def build_model(weights):
    
    mobile = tf.keras.applications.mobilenet.MobileNet()   
    x = mobile.layers[-6].output
    output = Dense(units=2, activation='softmax')(x)
    global_model = Model(inputs=mobile.input, outputs=output)
    
    #to get the average over all the local model, we simply take the sum of the scaled weights
    average_weights = sum_scaled_weights(weights)
    print('Total models:',len(weights))
    print(len(average_weights))
    #update global model 
    global_model.compile(Adam(lr=.0001), loss='categorical_crossentropy', metrics=['accuracy'])
    global_model.set_weights(average_weights)
    return global_model

def save_agg_model(model):
    if os.path.isdir(cwd + '/agg_model') == False:
        os.mkdir(cwd + '/agg_model')
    model.save(cwd + "/agg_model/agg_model.h5")
    print("Model written to storage!")

def model_aggregation():
    weights = fl_average()
    model = build_model(weights)
    save_agg_model(model)
