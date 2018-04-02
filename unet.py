#! /usr/bin/python
# -*- coding: utf8 -*-

import tensorflow as tf
import tensorlayer as tl
import numpy as np
from tensorlayer.layers import *

'''
def UNet(t_image, is_train=False, reuse=False, scope = "UNet"):
    w_init1 = tf.random_normal_initializer(stddev=0.02)
    w_init2 = tf.random_normal_initializer(stddev=0.01)
    w_init3 = tf.random_normal_initializer(stddev=0.005)
    w_init4 = tf.random_normal_initializer(stddev=0.002)
    b_init = None # tf.constant_initializer(value=0.0)
    g_init = tf.random_normal_initializer(1., 0.02)
    hrg = t_image.get_shape()[1]
    wrg = t_image.get_shape()[2]
    with tf.variable_scope(scope, reuse=reuse) as vs:
        tl.layers.set_name_reuse(reuse)
        n = InputLayer(t_image, name='in')
        n_init = InputLayer(t_image, name='in2')
        n = Conv2d(n, 64, (3, 3), (1, 1), act=None, padding='SAME', W_init=w_init1, name='f0/c')
        #n = BatchNormLayer(n, is_train=is_train, gamma_init=g_init, name='f0/b')
        n = InstanceNormLayer(n, epsilon=1e-5, name='f0/b')
        f0 = n
        n = Conv2d(n, 64, (3, 3), (2, 2), act=None, padding='SAME', W_init=w_init2, name='d1/c1')
        #n = BatchNormLayer(n, act=tf.nn.relu, is_train=is_train, gamma_init=g_init, name='d1/b1')
        n = InstanceNormLayer(n, act=tf.nn.relu, epsilon=1e-5, name='d1/b1')
        n = Conv2d(n, 128, (3, 3), (1, 1), act=None, padding='SAME', W_init=w_init2, name='d1/c2')
        #n = BatchNormLayer(n, act=tf.nn.relu, is_train=is_train, gamma_init=g_init, name='d1/b2')
        n = InstanceNormLayer(n, act=tf.nn.relu, epsilon=1e-5, name='d1/b2')
        n = Conv2d(n, 128, (3, 3), (1, 1), act=None, padding='SAME', W_init=w_init2, name='d1/c3')
        #n = BatchNormLayer(n, is_train=is_train, gamma_init=g_init, name='d1/b3')
        n = InstanceNormLayer(n, epsilon=1e-5, name='d1/b3')
        f1_2 = n
        n = Conv2d(n, 256, (3, 3), (2, 2), act=None, padding='SAME', W_init=w_init3, name='d2/c1')
        #n = BatchNormLayer(n, act=tf.nn.relu, is_train=is_train, gamma_init=g_init, name='d2/b1')
        n = InstanceNormLayer(n, act=tf.nn.relu, epsilon=1e-5, name='d2/b1')
        n = Conv2d(n, 256, (3, 3), (1, 1), act=None, padding='SAME', W_init=w_init3, name='d2/c2')
        #n = BatchNormLayer(n, act=tf.nn.relu, is_train=is_train, gamma_init=g_init, name='d2/b2')
        n = InstanceNormLayer(n, act=tf.nn.relu, epsilon=1e-5, name='d2/b2')
        n = Conv2d(n, 256, (3, 3), (1, 1), act=None, padding='SAME', W_init=w_init3, name='d2/c3')
        #n = BatchNormLayer(n, act=tf.nn.relu, is_train=is_train, gamma_init=g_init, name='d2/b3')
        n = InstanceNormLayer(n, act=tf.nn.relu, epsilon=1e-5, name='d2/b3')
        n = Conv2d(n, 256, (3, 3), (1, 1), act=None, padding='SAME', W_init=w_init3, name='d2/c4')
        #n = BatchNormLayer(n, is_train=is_train, gamma_init=g_init, name='d2/b4')
        n = InstanceNormLayer(n, epsilon=1e-5, name='d2/b4')
        f2_3 = n
        n = Conv2d(n, 512, (3, 3), (2, 2), act=None, padding='SAME', W_init=w_init4, name='d3/c1')
        #n = BatchNormLayer(n, act=tf.nn.relu, is_train=is_train, gamma_init=g_init, name='d3/b1')
        n = InstanceNormLayer(n, act=tf.nn.relu, epsilon=1e-5, name='d3/b1')
        n = Conv2d(n, 512, (3, 3), (1, 1), act=None, padding='SAME', W_init=w_init4, name='d3/c2')
        #n = BatchNormLayer(n, act=tf.nn.relu, is_train=is_train, gamma_init=g_init, name='d3/b2')
        n = InstanceNormLayer(n, act=tf.nn.relu, epsilon=1e-5, name='d3/b2')
        n = Conv2d(n, 512, (3, 3), (1, 1), act=None, padding='SAME', W_init=w_init4, name='d3/c3')
        #n = BatchNormLayer(n, act=tf.nn.relu, is_train=is_train, gamma_init=g_init, name='d3/b3')
        n = InstanceNormLayer(n, act=tf.nn.relu, epsilon=1e-5, name='d3/b3')
        n = Conv2d(n, 512, (3, 3), (1, 1), act=None, padding='SAME', W_init=w_init4, name='d3/c4')
        #n = BatchNormLayer(n, act=tf.nn.relu, is_train=is_train, gamma_init=g_init, name='d3/b4')
        n = InstanceNormLayer(n, act=tf.nn.relu, epsilon=1e-5, name='d3/b4')

        n = DeConv2d(n, 256, (3, 3), (hrg/4, wrg/4), (2, 2), act=None, padding='SAME', W_init=w_init3, name='u3/d')
        #n = BatchNormLayer(n, is_train=is_train, gamma_init=g_init, name='u3/b')
        n = InstanceNormLayer(n, epsilon=1e-5, name='u3/b')
        n = ElementwiseLayer([n, f2_3], tf.add, name='s4')
        n.outputs = tf.nn.relu(n.outputs, name = 'relu4')

        n = Conv2d(n, 256, (3, 3), (1, 1), act=None, padding='SAME', W_init=w_init3, name='u3/c1')
        #n = BatchNormLayer(n, act=tf.nn.relu, is_train=is_train, gamma_init=g_init, name='u3/b1')
        n = InstanceNormLayer(n, act=tf.nn.relu, epsilon=1e-5, name='u3/b1')
        n = Conv2d(n, 256, (3, 3), (1, 1), act=None, padding='SAME', W_init=w_init3, name='u3/c2')
        #n = BatchNormLayer(n, act=tf.nn.relu, is_train=is_train, gamma_init=g_init, name='u3/b2')
        n = InstanceNormLayer(n, act=tf.nn.relu, epsilon=1e-5, name='u3/b2')
        n = Conv2d(n, 256, (3, 3), (1, 1), act=None, padding='SAME', W_init=w_init3, name='u3/c3')
        #n = BatchNormLayer(n, act=tf.nn.relu, is_train=is_train, gamma_init=g_init, name='u3/b3')
        n = InstanceNormLayer(n, act=tf.nn.relu, epsilon=1e-5, name='u3/b3')

        n = DeConv2d(n, 128, (3, 3), (hrg/2, wrg/2), (2, 2), act=None, padding='SAME', W_init=w_init2, name='u2/d')
        #n = BatchNormLayer(n, is_train=is_train, gamma_init=g_init, name='u2/b')
        n = InstanceNormLayer(n, epsilon=1e-5, name='u2/b')
        n = ElementwiseLayer([n, f1_2], tf.add, name='s3')
        n.outputs = tf.nn.relu(n.outputs, name = 'relu3')
        n = Conv2d(n, 128, (3, 3), (1, 1), act=None, padding='SAME', W_init=w_init2, name='u2/c1')
        #n = BatchNormLayer(n, act=tf.nn.relu, is_train=is_train, gamma_init=g_init, name='u2/b1')
        n = InstanceNormLayer(n, act=tf.nn.relu, epsilon=1e-5, name='u2/b1')
        n = Conv2d(n, 64, (3, 3), (1, 1), act=None, padding='SAME', W_init=w_init2, name='u2/c2')
        #n = BatchNormLayer(n, act=tf.nn.relu, is_train=is_train, gamma_init=g_init, name='u2/b2')
        n = InstanceNormLayer(n, act=tf.nn.relu, epsilon=1e-5, name='u2/b2')

        n = DeConv2d(n, 64, (3, 3), (hrg, wrg), (2, 2), act=None, padding='SAME', W_init=w_init1, name='u1/d')
        #n = BatchNormLayer(n, is_train=is_train, gamma_init=g_init, name='u1/b')
        n = InstanceNormLayer(n, epsilon=1e-5, name='u1/b')
        n = ElementwiseLayer([n, f0], tf.add, name='s2')
        n.outputs = tf.nn.relu(n.outputs, name = 'relu2')
        n = Conv2d(n, 15, (3, 3), (1, 1), act=None, padding='SAME', W_init=w_init1, name='u1/c1')
        #n = BatchNormLayer(n, act=tf.nn.relu, is_train=is_train, gamma_init=g_init, name='u1/b1')
        n = InstanceNormLayer(n, act=tf.nn.relu, epsilon=1e-5, name='u1/b1')
        n = Conv2d(n, 1, (3, 3), (1, 1), act=tf.nn.sigmoid, padding='SAME', W_init=w_init1, name='u1/c2')

        return n.outputs
'''
def UNet(t_image, is_train=False, reuse=False, scope = "UNet"):
    w_init1 = tf.random_normal_initializer(stddev=0.02)
    w_init2 = tf.random_normal_initializer(stddev=0.01)
    w_init3 = tf.random_normal_initializer(stddev=0.005)
    w_init4 = tf.random_normal_initializer(stddev=0.002)
    b_init = None # tf.constant_initializer(value=0.0)
    g_init = tf.random_normal_initializer(1., 0.02)
    hrg = t_image.get_shape()[1]
    wrg = t_image.get_shape()[2]
    with tf.variable_scope(scope, reuse=reuse) as vs:
        tl.layers.set_name_reuse(reuse)
        n = InputLayer(t_image, name='in')
        n_init = InputLayer(t_image, name='in2')
        n = Conv2d(n, 64, (3, 3), (1, 1), act=None, padding='SAME', W_init=w_init1, name='f0/c')
        n = BatchNormLayer(n, is_train=is_train, gamma_init=g_init, name='f0/b')
        f0 = n
        n = Conv2d(n, 64, (3, 3), (2, 2), act=None, padding='SAME', W_init=w_init2, name='d1/c1')
        n = BatchNormLayer(n, act=tf.nn.relu, is_train=is_train, gamma_init=g_init, name='d1/b1')
        n = Conv2d(n, 128, (3, 3), (1, 1), act=None, padding='SAME', W_init=w_init2, name='d1/c2')
        n = BatchNormLayer(n, act=tf.nn.relu, is_train=is_train, gamma_init=g_init, name='d1/b2')
        n = Conv2d(n, 128, (3, 3), (1, 1), act=None, padding='SAME', W_init=w_init2, name='d1/c3')
        n = BatchNormLayer(n, is_train=is_train, gamma_init=g_init, name='d1/b3')
        f1_2 = n
        n = Conv2d(n, 256, (3, 3), (2, 2), act=None, padding='SAME', W_init=w_init3, name='d2/c1')
        n = BatchNormLayer(n, act=tf.nn.relu, is_train=is_train, gamma_init=g_init, name='d2/b1')
        n = Conv2d(n, 256, (3, 3), (1, 1), act=None, padding='SAME', W_init=w_init3, name='d2/c2')
        n = BatchNormLayer(n, act=tf.nn.relu, is_train=is_train, gamma_init=g_init, name='d2/b2')
        n = Conv2d(n, 256, (3, 3), (1, 1), act=None, padding='SAME', W_init=w_init3, name='d2/c3')
        n = BatchNormLayer(n, act=tf.nn.relu, is_train=is_train, gamma_init=g_init, name='d2/b3')
        n = Conv2d(n, 256, (3, 3), (1, 1), act=None, padding='SAME', W_init=w_init3, name='d2/c4')
        n = BatchNormLayer(n, is_train=is_train, gamma_init=g_init, name='d2/b4')
        f2_3 = n
        n = Conv2d(n, 256, (3, 3), (2, 2), act=None, padding='SAME', W_init=w_init4, name='d3/c1')
        n = BatchNormLayer(n, act=tf.nn.relu, is_train=is_train, gamma_init=g_init, name='d3/b1')
        n = Conv2d(n, 256, (3, 3), (1, 1), act=None, padding='SAME', W_init=w_init4, name='d3/c2')
        n = BatchNormLayer(n, act=tf.nn.relu, is_train=is_train, gamma_init=g_init, name='d3/b2')
        n = Conv2d(n, 256, (3, 3), (1, 1), act=None, padding='SAME', W_init=w_init4, name='d3/c3')
        n = BatchNormLayer(n, act=tf.nn.relu, is_train=is_train, gamma_init=g_init, name='d3/b3')
        n = Conv2d(n, 256, (3, 3), (1, 1), act=None, padding='SAME', W_init=w_init4, name='d3/c4')
        n = BatchNormLayer(n, act=tf.nn.relu, is_train=is_train, gamma_init=g_init, name='d3/b4')
        
        f3_4 = n
        n = Conv2d(n, 512, (3, 3), (2, 2), act=None, padding='SAME', W_init=w_init4, name='d4/c1')
        n = BatchNormLayer(n, act=tf.nn.relu, is_train=is_train, gamma_init=g_init, name='d4/b1')
        n = Conv2d(n, 512, (3, 3), (1, 1), act=None, padding='SAME', W_init=w_init4, name='d4/c2')
        n = BatchNormLayer(n, act=tf.nn.relu, is_train=is_train, gamma_init=g_init, name='d4/b2')
        n = Conv2d(n, 512, (3, 3), (1, 1), act=None, padding='SAME', W_init=w_init4, name='d4/c3')
        n = BatchNormLayer(n, act=tf.nn.relu, is_train=is_train, gamma_init=g_init, name='d4/b3')
        n = Conv2d(n, 512, (3, 3), (1, 1), act=None, padding='SAME', W_init=w_init4, name='d4/c4')
        n = BatchNormLayer(n, act=tf.nn.relu, is_train=is_train, gamma_init=g_init, name='d4/b4')

        n = DeConv2d(n, 256, (3, 3), (hrg/8, wrg/8), (2, 2), act=None, padding='SAME', W_init=w_init3, name='u4/d')
        n = BatchNormLayer(n, is_train=is_train, gamma_init=g_init, name='u4/b')
        n = ElementwiseLayer([n, f3_4], tf.add, name='s5')
        n.outputs = tf.nn.relu(n.outputs, name = 'relu5')
        
        n = Conv2d(n, 256, (3, 3), (1, 1), act=None, padding='SAME', W_init=w_init3, name='u4/c1')
        n = BatchNormLayer(n, act=tf.nn.relu, is_train=is_train, gamma_init=g_init, name='u4/b1')
        n = Conv2d(n, 256, (3, 3), (1, 1), act=None, padding='SAME', W_init=w_init3, name='u4/c2')
        n = BatchNormLayer(n, act=tf.nn.relu, is_train=is_train, gamma_init=g_init, name='u4/b2')
        n = Conv2d(n, 256, (3, 3), (1, 1), act=None, padding='SAME', W_init=w_init3, name='u4/c3')
        n = BatchNormLayer(n, act=tf.nn.relu, is_train=is_train, gamma_init=g_init, name='u4/b3')
        
        n = DeConv2d(n, 256, (3, 3), (hrg/4, wrg/4), (2, 2), act=None, padding='SAME', W_init=w_init3, name='u3/d')
        n = BatchNormLayer(n, is_train=is_train, gamma_init=g_init, name='u3/b')
        n = ElementwiseLayer([n, f2_3], tf.add, name='s4')
        n.outputs = tf.nn.relu(n.outputs, name = 'relu4')

        n = Conv2d(n, 256, (3, 3), (1, 1), act=None, padding='SAME', W_init=w_init3, name='u3/c1')
        n = BatchNormLayer(n, act=tf.nn.relu, is_train=is_train, gamma_init=g_init, name='u3/b1')
        n = Conv2d(n, 256, (3, 3), (1, 1), act=None, padding='SAME', W_init=w_init3, name='u3/c2')
        n = BatchNormLayer(n, act=tf.nn.relu, is_train=is_train, gamma_init=g_init, name='u3/b2')
        n = Conv2d(n, 256, (3, 3), (1, 1), act=None, padding='SAME', W_init=w_init3, name='u3/c3')
        n = BatchNormLayer(n, act=tf.nn.relu, is_train=is_train, gamma_init=g_init, name='u3/b3')

        n = DeConv2d(n, 128, (3, 3), (hrg/2, wrg/2), (2, 2), act=None, padding='SAME', W_init=w_init2, name='u2/d')
        n = BatchNormLayer(n, is_train=is_train, gamma_init=g_init, name='u2/b')
        n = ElementwiseLayer([n, f1_2], tf.add, name='s3')
        n.outputs = tf.nn.relu(n.outputs, name = 'relu3')
        
        n = Conv2d(n, 128, (3, 3), (1, 1), act=None, padding='SAME', W_init=w_init2, name='u2/c1')
        n = BatchNormLayer(n, act=tf.nn.relu, is_train=is_train, gamma_init=g_init, name='u2/b1')
        n = Conv2d(n, 64, (3, 3), (1, 1), act=None, padding='SAME', W_init=w_init2, name='u2/c2')
        n = BatchNormLayer(n, act=tf.nn.relu, is_train=is_train, gamma_init=g_init, name='u2/b2')

        n = DeConv2d(n, 64, (3, 3), (hrg, wrg), (2, 2), act=None, padding='SAME', W_init=w_init1, name='u1/d')
        n = BatchNormLayer(n, is_train=is_train, gamma_init=g_init, name='u1/b')
        n = ElementwiseLayer([n, f0], tf.add, name='s2')
        n.outputs = tf.nn.relu(n.outputs, name = 'relu2')
        n = Conv2d(n, 15, (3, 3), (1, 1), act=None, padding='SAME', W_init=w_init1, name='u1/c1')
        n = BatchNormLayer(n, act=tf.nn.relu, is_train=is_train, gamma_init=g_init, name='u1/b1')
        n = Conv2d(n, 1, (3, 3), (1, 1), act=tf.nn.sigmoid, padding='SAME', W_init=w_init1, name='u1/c2')

        return n, n.outputs
