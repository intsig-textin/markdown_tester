

图 13 PSO 流程图

$P S O$ 中每次迭代粒子 $\mathrm{i}$ 的速度 $v_{i}$ 和位置 $x_{i}$ 更新公式为:

$$
\begin{gathered}
v_{i}^{k}=w v_{i}^{k-1}+c_{1} r_{1} * \operatorname{rand}() *\left(\text { pbest }_{i}-x_{i}^{k-1}\right)+c_{2} r_{2} * \operatorname{rand}() *\left(\text { gbest }-x_{i}^{k-1}\right) \\
x_{i}^{k}=x_{i}^{k-1}+v_{i}^{k}
\end{gathered}
$$

其中, $w$ 为惯性权重 (inertia weight), $c_{1}$ 和 $c_{2}$ 为加速常数 (acceleration constants), $r a n d()$ 为在 $[0,1]$ 范围里变化的随机值, pbest 为粒子自身的最佳过去位置, gbest 为整个群或近邻的最佳过去位置。

采用粒子群算法优化随机森林模型的参数, 可以将模型返回预测结果计算得到的 F1 值作为目标函数，通过更新迭代得到最佳位置，即最优参数。

本项目中，在采用粒子群算法的基础上，还引入了惯性权重线性递减和多样性维护参数的概念，对算法加以改进。其中惯性权重 $w$ 线性递减，根据迭代进度，逐渐减小惯性权重, 可以在一定程度上优化粒子的寻优能力; 多样性维护参数 $c_{3}$ 可以确保种群中的粒子保持一定的多样性, 避免陷入局部最优解。

$$
\begin{gathered}
w=w_{\max }-\frac{t}{T}\left(w_{\max }-w_{\min }\right) \\
V=c_{3}^{*}(\operatorname{Rand}()-0.5) * \text { range } \\
v_{i}^{k}=v_{i}^{k}+V
\end{gathered}
$$

其中, $w_{\max }=0.9, w_{\min }=0.4, t$ 为当前迭代次数, $T$ 为最大迭代次数, $c_{3}=0.1, V$为多样性维护项, range 为各参数取值范围长度。

