# ILASセミナー: 量子コンピュータを動かしてみよう

これは2018年度前期に京都大学の全額共通科目の一つである『ILASセミナー: 量子コンピュータを動かしてみよう』
での最終課題をまとめたものである。

僕自身は潜りで受けていたのだが、一回生のMくんと一緒にチームを組んで今回の課題を完成させた。
感謝します。

# 加算器(Full Adder)

加算器の作成には
https://github.com/Qiskit/openqasm/blob/master/examples/generic/adder.qasm
を大いに参考にした。このコードは4bitの足し算をRipple-Carry adderで実装したものである。
(さらに8bitの足し算は[ここ](https://github.com/Qiskit/openqasm/blob/master/examples/generic/bigadder.qasm)に載っている。)
この足し算方式は[この論文](https://arxiv.org/abs/quant-ph/0410184)で詳しく解説がなされている。

今回は4bit、8bitの足し算がすでに実装されているのでそれを16bitに拡張することを試みた。
このコードを動かすためには[IBM Q](https://quantumexperience.ng.bluemix.net/qx/editor)でAPIのキーを取得し、
[Qconfig.py](/Qconfig.py)の保存する。そうすれば足し算ができるようになる。例えば、`300+400`の足し算をしたければ、
```
python adder.py 300 400
```
とすれば良い。それなりに待てば(ものによっては7分くらい)、`700`と出力する。

# 回路図

今回作成した加算器の回路図をtexで生成した。量子回路を作成するのに
`qcircuit`というパッケージを用いた。
~~非常に書くのがめんどくさい。。。~~

加算器の回路は`majority`ゲートと`unmajority`ゲートからなっている。

- `majority`ゲート
![majority](/figure/maj.jpg)

- `unmajority`ゲート
![unmajority](/figure/unmaj.jpg)

この２つのゲートを組み合わせることで今回の加算器が完成する。
![adder](/figure/adder.jpg)
なぜこの回路に至ったのかについては[論文](https://arxiv.org/abs/quant-ph/0410184)を読むべきだったが、
今回はそこまで回らなかった。

# 結論と今後の展望

今回は https://github.com/Qiskit/openqasm/blob/master/examples/generic/adder.qasm
を参考に加算器を作成し、15bit+15bitの足し算回路を作成することに成功した。

ただ、やはり時間がかかる、という問題点はどうしても避けられない。
今回用いたRipple-Carry adderの他にも、
Carry-lookahead adderというものがあるらしく、この加算器は非常に高速に動くらしい。
今後時間があれば、Carry-lookahead adderの実装も行ってみたいと思う。

