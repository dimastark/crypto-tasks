from typing import Any

import numpy as np
import theano
import theano.tensor as tf


def get_source(source: Any) -> str:
    if 'Layer' in source.__class__.__name__:
        return source.output
    return source


def get_activation(x: Any, act: str) -> Any:
    if act == 'tanh':
        return tf.tanh(x)
    elif act == 'relu':
        return tf.nnet.relu(x)
    elif act == 'sigmoid':
        return tf.nnet.sigmoid(x)

    return x


def get_weights(in_d: int, out_d: int, name: str) -> Any:
    return theano.shared(name=name, borrow=True, value=np.asarray(
        np.random.uniform(
            low=-np.sqrt(6. / (in_d + out_d)),
            high=np.sqrt(6. / (in_d + out_d)),
            size=(in_d, out_d)
        ),
        dtype=theano.config.floatX
    ))


def get_bias(d: int, name: str) -> Any:
    return theano.shared(
        name=name, borrow=True,
        value=np.zeros((d,), dtype=theano.config.floatX),
    )


class ConvLayer:
    def __init__(self, source, filter_shape, image_shape, stride,
                 act_fn, border_mode='full', name='conv'):
        self.image_shape = image_shape
        self.filter_shape = filter_shape
        self.stride = stride
        self.border_mode = border_mode
        self.name = name
        self.act_fn = act_fn

        self.parent = source
        self.source = get_source(source)

        fan_in = np.prod(filter_shape[1:])
        fan_out = (filter_shape[0] * np.prod(filter_shape[2:]))
        W_bound = np.sqrt(6. / (fan_in + fan_out))
        self.W = theano.shared(
            np.asarray(
                np.random.uniform(low=-W_bound, high=W_bound, size=filter_shape),
                dtype=theano.config.floatX
            ),
            borrow=True,
            name=name + '_W'
        )

        b_values = np.zeros((filter_shape[0],), dtype=theano.config.floatX)
        self.b = theano.shared(value=b_values, borrow=True, name=name + '_b')
        conv_out = tf.nnet.conv2d(
            input=self.source,
            filters=self.W,
            filter_shape=self.filter_shape,
            input_shape=self.image_shape,
            border_mode=self.border_mode,
            subsample=self.stride
        )

        self.output_pre_activ = conv_out + self.b.dimshuffle('x', 0, 'x', 'x')
        self.output = get_activation(self.output_pre_activ,
                                     act=self.act_fn)

        self.params = [self.W, self.b]


class HiddenLayer:
    def __init__(self, source, input_size, hidden_size, name, act_fn):
        self.parent = source
        self.source = get_source(source)
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.name = name
        self.act_fn = act_fn
        self.W = get_weights(self.input_size, self.hidden_size, 'W_' + name)
        self.b = get_bias(self.hidden_size, 'b_' + name)
        self.output_pre_activ = tf.dot(self.source, self.W) + \
                                self.b.dimshuffle('x', 0)
        self.output = get_activation(self.output_pre_activ,
                                     act=self.act_fn)
        self.params = [self.W, self.b]


class StandardConvSetup:
    def __init__(self, reshaped_input, name='unnamed'):
        self.name = name
        self.conv_layer1 = ConvLayer(reshaped_input,
                                     filter_shape=(2, 1, 4, 1),
                                     image_shape=(None, 1, None, 1),
                                     stride=(1, 1),
                                     name=self.name + '_conv1',
                                     border_mode=(2, 0),
                                     act_fn='relu')

        self.conv_layer2 = ConvLayer(self.conv_layer1,
                                     filter_shape=(4, 2, 2, 1),
                                     image_shape=(None, 2, None, 1),
                                     stride=(2, 1),
                                     name=self.name + '_conv2',
                                     border_mode=(0, 0),
                                     act_fn='relu')

        self.conv_layer3 = ConvLayer(self.conv_layer2,
                                     filter_shape=(4, 4, 1, 1),
                                     image_shape=(None, 4, None, 1),
                                     stride=(1, 1),
                                     name=self.name + '_conv3',
                                     border_mode=(0, 0),
                                     act_fn='relu')

        self.conv_layer4 = ConvLayer(self.conv_layer3,
                                     filter_shape=(1, 4, 1, 1),
                                     image_shape=(None, 4, None, 1),
                                     stride=(1, 1),
                                     name=self.name + '_conv4',
                                     border_mode=(0, 0),
                                     act_fn='tanh')

        self.output = self.conv_layer4.output
        self.layers = [self.conv_layer1, self.conv_layer2,
                       self.conv_layer3, self.conv_layer4]
        self.params = []
        for l in self.layers:
            self.params += l.params
