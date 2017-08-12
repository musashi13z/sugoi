#! -*- coding: utf-8 -*-
import cv2
import numpy as np

class Croped():
    """切り出された画像を扱うクラス."""

    dets = None # 矩形情報
    img = None # 切り出した画像情報
    analysis = [] # 算出した情報

    def __init__(self, original, dets):
        """initial."""
        self.dets = self._fit_to_img(original, dets)
        #元画像から切り出して画像を生成
        self.img = original[
            self.dets['top']:self.dets['bottom'],
            self.dets['left']:self.dets['right']
        ]

    def _resize(self, size):
        """画像をリサイズしてものを返す."""
        return cv2.resize(self.img, (size, size))

    def _fit_to_img(self, original, dets):
        """渡された画像からはみ出る場合は小さくする."""
        height, width, _ = original.shape
        return {
            'top': max(dets.top(), 0),
            'bottom': min(dets.bottom(), height),
            'left': max(dets.left(), 0),
            'right': min(dets.right(), width),
        }

    def fromat_4_tf(self):
        """tfで扱いやすい形式に変換."""
        # リサイズ
        img = self._resize(28)
        # 画像情報を一列にした後、0-1のfloat値にする
        image = []
        image.append(img.flatten().astype(np.float32)/255.0)
        # numpy形式に変換し、TensorFlowで処理できるようにする
        return np.asarray(image)

    def format_4_res(self):
        """レスポンスで扱いやすい形式に変換."""
        return {
            'analysis': self.analysis[0],
            'rect': self.dets,
        }
