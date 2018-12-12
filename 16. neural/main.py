from typing import Any, Iterable, List

import matplotlib.pyplot as plt
import numpy as np
import theano
import theano.tensor as tf

from lasagne.updates import adam

from nn import ConvLayer, HiddenLayer, StandardConvSetup


BATCH_SIZE = 512
MESSAGE_SIZE = 8
KEY_SIZE = 8
COMMON_SIZE = 8


def get_all_params(layers: Iterable) -> List[Any]:
    out = []

    for l in layers:
        for p in l.params:
            out.append(p)

    return out


def gen_data(n=BATCH_SIZE, msg_len=MESSAGE_SIZE, key_len=KEY_SIZE):
    return (np.random.randint(0, 2, size=(n, msg_len)) * 2 - 1). \
               astype(theano.config.floatX), \
           (np.random.randint(0, 2, size=(n, key_len)) * 2 - 1). \
               astype(theano.config.floatX)


def assess(pred_fn, n=BATCH_SIZE, msg_len=MESSAGE_SIZE, key_len=KEY_SIZE):
    msg_in_val, key_val = gen_data(n, msg_len, key_len)
    return np.round(np.abs(msg_in_val[0:n] - \
                           pred_fn(msg_in_val[0:n], key_val[0:n])), 0)


def err_over_samples(err_fn, n=BATCH_SIZE):
    msg_in_val, key_val = gen_data(n)
    return err_fn(msg_in_val[0:n], key_val[0:n])


def main():
    msg_in = tf.matrix('msg_in')
    key = tf.matrix('key')

    alice_in = tf.concatenate([msg_in, key], axis=1)

    alice_hid = HiddenLayer(alice_in,
                            input_size=MESSAGE_SIZE + KEY_SIZE,
                            hidden_size=MESSAGE_SIZE + KEY_SIZE,
                            name='alice_to_hid',
                            act_fn='relu')

    alice_conv_in = alice_hid.output.reshape((BATCH_SIZE, 1, MESSAGE_SIZE + KEY_SIZE, 1))
    alice_conv = StandardConvSetup(alice_conv_in, 'alice')
    alice_comm = alice_conv.output.reshape((BATCH_SIZE, MESSAGE_SIZE))

    bob_in = tf.concatenate([alice_comm, key], axis=1)
    bob_hid = HiddenLayer(bob_in,
                          input_size=COMMON_SIZE + KEY_SIZE,
                          hidden_size=COMMON_SIZE + KEY_SIZE,
                          name='bob_to_hid',
                          act_fn='relu')

    bob_conv_in = bob_hid.output.reshape((BATCH_SIZE, 1, COMMON_SIZE + KEY_SIZE, 1))
    bob_conv = StandardConvSetup(bob_conv_in, 'bob')
    bob_msg = bob_conv.output.reshape((BATCH_SIZE, MESSAGE_SIZE))

    eve_hid1 = HiddenLayer(alice_comm,
                           input_size=COMMON_SIZE,
                           hidden_size=COMMON_SIZE + KEY_SIZE,
                           name='eve_to_hid1',
                           act_fn='relu')

    eve_hid2 = HiddenLayer(eve_hid1,
                           input_size=COMMON_SIZE + KEY_SIZE,
                           hidden_size=COMMON_SIZE + KEY_SIZE,
                           name='eve_to_hid2',
                           act_fn='relu')


    eve_conv_in = eve_hid2.output.reshape((BATCH_SIZE, 1, COMMON_SIZE + KEY_SIZE, 1))
    eve_conv = StandardConvSetup(eve_conv_in, 'eve')
    eve_msg = eve_conv.output.reshape((BATCH_SIZE, MESSAGE_SIZE))

    decrypt_err_eve = tf.mean(tf.abs_(msg_in - eve_msg))

    decrypt_err_bob = tf.mean(tf.abs_(msg_in - bob_msg))
    loss_bob = decrypt_err_bob + (1. - decrypt_err_eve) ** 2.

    params = {'bob': get_all_params([bob_conv, bob_hid,
                                     alice_conv, alice_hid])}
    updates = {'bob': adam(loss_bob, params['bob'])}
    err_fn = {'bob': theano.function(inputs=[msg_in, key],
                                     outputs=decrypt_err_bob)}
    train_fn = {'bob': theano.function(inputs=[msg_in, key],
                                       outputs=loss_bob,
                                       updates=updates['bob'])}
    pred_fn = {'bob': theano.function(inputs=[msg_in, key], outputs=bob_msg)}

    params['eve'] = get_all_params([eve_hid1, eve_hid2, eve_conv])
    updates['eve'] = adam(decrypt_err_eve, params['eve'])
    err_fn['eve'] = theano.function(inputs=[msg_in, key],
                                    outputs=decrypt_err_eve)
    train_fn['eve'] = theano.function(inputs=[msg_in, key],
                                      outputs=decrypt_err_eve,
                                      updates=updates['eve'])
    pred_fn['eve'] = theano.function(inputs=[msg_in, key], outputs=eve_msg)

    def train(bob_or_eve, results, max_iters, print_every, es=0., es_limit=100):
        count = 0
        for i in range(max_iters):
            msg_in_val, key_val = gen_data()
            loss = train_fn[bob_or_eve](msg_in_val, key_val)
            results = np.hstack((results,
                                 err_fn[bob_or_eve](msg_in_val, key_val).sum()))
            if i % print_every == 0:
                print('Функция потери:', loss)
            if es and loss < es:
                count += 1
                if count > es_limit:
                    break
        return np.hstack((results, np.repeat(results[-1], max_iters - i - 1)))

    results_bob, results_eve = [], []
    adversarial_iterations = 60

    for i in range(adversarial_iterations):
        n = 2000
        print_every = 100
        print('Обучаем Алису и Боба, запуск №' + str(i + 1))
        results_bob = train('bob', results_bob, n, print_every, es=0.01)
        print('Обучаем Еву, запуск №' + str(i + 1))
        results_eve = train('eve', results_eve, n, print_every, es=0.01)

    plt.plot([np.min(results_bob[i:i + n]) for i in np.arange(0,
                                                              len(results_bob), n)])
    plt.plot([np.min(results_eve[i:i + n]) for i in np.arange(0,
                                                              len(results_eve), n)])
    plt.legend(['bob', 'eve'])
    plt.xlabel('Конкурентное обучение')
    plt.ylabel('Наименьшая ошибка расшифровки')
    plt.show()


if __name__ == '__main__':
    main()
