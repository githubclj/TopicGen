# -*- coding:utf-8 -*-
"""
Brief:

Authors: zhangruqing(@software.ict.ac.cn)
Date:    2017/12/02 01:44:06
File:    predict.py
"""
import os
import math
import tensorflow as tf
import time
import logging
import numpy as np
import sys
from en_de import EncodeDecodeModel
from process_data import ProcessData
import config as cf

max_length_decoder = 17
model_dir = cf.model_dir
batch_size = cf.batch_size
vocab_dir = cf.vocab_dir

processed = ProcessData(vocab_dir, 20, 50)
news_with_chn = processed.extract_chn_with_symbols(cf.news_file)
word_num, sent_num, news, vocab = processed._process_data(news_with_chn)


model = EncodeDecodeModel(cell_type = 'gru',
                              num_hidden = 512,
                              num_layers = 1,
                              embedding_size = 128,
                              max_vocab_size = 60004,
                              learning_rate = 0.0005,
                              batch_size = batch_size,
                              decay_rate = 0.99,
                              decay_steps = 100000,
                              grad_clip = 5.0,
                              num_samples = 512,
                              max_length_decoder = max_length_decoder)


def train():
    '''
    config = tf.ConfigProto(log_device_placement=True)
    config.gpu_options.allow_growth = True
    '''
    decode_list = []
    with tf.Session() as sess:
        init = tf.global_variables_initializer()
        sess.run(init)
        saver = tf.train.Saver(tf.global_variables(), max_to_keep=20)
        ckpt = tf.train.get_checkpoint_state(model_dir)

        fw = open(cf.decode_file,'w')
        if ckpt and tf.train.checkpoint_exists(ckpt.model_checkpoint_path):
            print("Reading model parameters from %s" % ckpt.model_checkpoint_path)
            saver.restore(sess, ckpt.model_checkpoint_path)
            for f in range(news.shape[0]/batch_size):
                encoder_inputs = news[f*batch_size:(f+1)*batch_size]
                encoder_word_num = np.reshape(word_num[f*batch_size:(f+1)*batch_size,:], -1)
                encoder_sent_num = sent_num[f*batch_size:(f+1)*batch_size]

                decode_predict, feed_dict = model.predict(encoder_inputs, encoder_word_num, encoder_sent_num)
                predict = sess.run(decode_predict, feed_dict=feed_dict)

                pre = np.array(predict).transpose()
                for i in range(batch_size):
                    tmp = []
                    for j in range(max_length_decoder):
                        if pre[i][j] == 60001:
                            break
                        else:
                            tmp.append(list(vocab.keys())[list(vocab.values()).index(str(pre[i][j]))].encode('utf8'))
                            #fw.write(list(vocab.keys())[list(vocab.values()).index(str(pre[i][j]))].encode('utf8'))
                    fw.write(''.join(tmp))
                    decode_list.append(''.join(tmp))
                    fw.write('\n')
    return decode_list


# if __name__ == '__main__':
#     train()
