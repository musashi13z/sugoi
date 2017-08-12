#! -*- coding: utf-8 -*-
import numpy as np
import cv2
import tensorflow as tf
import dlib
import tensorflow.python.platform
from model import Croped

# 定数
SVM_DIR = 'lib/detector.svm'
CKPT_DIR = 'lib/model.ckpt'
CKPT_META_DIR = '{}.meta'.format(CKPT_DIR)
NUM_CLASSES = 5
IMAGE_SIZE = 28

def inference(images_placeholder, keep_prob):
    """"AIの学習モデル部分(ニューラルネットワーク)を作成する."""

    def weight_variable(shape):
        """重みを標準偏差0.1の正規分布で初期化する."""
        initial = tf.truncated_normal(shape, stddev=0.1)
        return tf.Variable(initial)

    def bias_variable(shape):
        """バイアスを標準偏差0.1の正規分布で初期化する."""
        initial = tf.constant(0.1, shape=shape)
        return tf.Variable(initial)

    def conv2d(x, W):
        """畳み込み層を作成する."""
        return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')

    def max_pool_2x2(x):
        """プーリング層を作成する."""
        return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

    # ベクトル形式で入力されてきた画像データを28px * 28pxの画像に戻す(?)。
    # 今回はカラー画像なので3(モノクロだと1)
    x_image = tf.reshape(images_placeholder, [-1, IMAGE_SIZE, IMAGE_SIZE, 3])

    # 畳み込み層第1レイヤーを作成
    with tf.name_scope('conv1') as scope:
        W_conv1 = weight_variable([5, 5, 3, 32])
        b_conv1 = bias_variable([32])
        h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)

    # プーリング層1の作成
    with tf.name_scope('pool1') as scope:
        h_pool1 = max_pool_2x2(h_conv1)

    # 畳み込み層第2レイヤーの作成
    with tf.name_scope('conv2') as scope:
        W_conv2 = weight_variable([5, 5, 32, 64])
        b_conv2 = bias_variable([64])
        h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)

    # プーリング層2の作成(ブーリング層1と同じ)
    with tf.name_scope('pool2') as scope:
        h_pool2 = max_pool_2x2(h_conv2)

    # 全結合層1の作成
    with tf.name_scope('fc1') as scope:
        W_fc1 = weight_variable([7*7*64, 1024])
        b_fc1 = bias_variable([1024])
        h_pool2_flat = tf.reshape(h_pool2, [-1, 7*7*64])
        h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)
        h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

    # 全結合層2の作成(読み出しレイヤー)
    with tf.name_scope('fc2') as scope:
        W_fc2 = weight_variable([1024, NUM_CLASSES])
        b_fc2 = bias_variable([NUM_CLASSES])

    # ソフトマックス関数による正規化
    # ここまでのニューラルネットワークの出力を各ラベルの確率へ変換する
    with tf.name_scope('softmax') as scope:
        y_conv=tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2) + b_fc2)

    # 各ラベルの確率(のようなもの?)を返す
    return y_conv

def detect_crop(img):
    """検出してCropedクラス生成."""
    detector = dlib.simple_object_detector(SVM_DIR)
    dets_list = detector(img)
    return [Croped(img, dets) for dets in dets_list]

def detect_friends(image):
    """切り出された画像からどのフレンズか判定."""
    logits = inference(image, 1.0)
    sess = tf.InteractiveSession()
    saver = tf.train.Saver()
    sess.run(tf.global_variables_initializer())
    saver = tf.train.import_meta_graph(CKPT_META_DIR)
    saver.restore(sess, CKPT_DIR)
    softmax = logits.eval()

    # 判定結果
    result = softmax[0]

    # 判定結果を%にして四捨五入
    rates = [round(n * 100.0, 1) for n in result]
    targets = [{'label': index, 'rate': rate} for index, rate in enumerate(rates)]
    # パーセンテージの高い順にソート
    rank = sorted(targets, key=lambda x: x['rate'], reverse=True)

    # よくわからないけどリセット
    tf.reset_default_graph()

    # 判定結果を返す
    return rank

def detect_img(file_data):
    # opencvのオブジェクトとして画像を読みこむ
    nparr = np.fromstring(file_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    out = img.copy()
    # 顔検出
    cropes = detect_crop(out)
    for crop in cropes:
        # 各顔を判定
        crop.analysis = detect_friends(crop.fromat_4_tf())
    return [c.format_4_res() for c in cropes]
