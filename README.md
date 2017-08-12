なんでも解析機
---

# 概要

[こちらの記事](http://orange634.hatenablog.com/entry/2017/08/12/153855)で作成したwebアプリを他のものでも流用できるように修正したものです。
顔の検出をdlib、判定をtensorflowで行います。
webフレームワークはflaskを用います。
ミドルウェアとしてgunicornとnginxを利用しています。

# 詳細

ブログ記事を書いたのでそちらを確認してください。

- http://orange634.hatenablog.com/entry/2017/08/12/131734
- http://orange634.hatenablog.com/entry/2017/08/12/153855

またサーバへのデプロイ方法は以下のリンクを確認してください。

- http://qiita.com/orange634/items/337061f3b0b5a8eaae0f
- http://qiita.com/orange634/items/8fb7667792a5b40f3752

使用する際はデータがなかったりするので、適宜調整が必要です。

- lib以下の学習データは入れていないので、利用する場合は作成する必要があります。
- faviconをダミーに差し替えています。
- 解析のラベルが５種類ある前提で作成されています。
