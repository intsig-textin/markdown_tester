## 3.4重复值处理

对数据进行检查后发现第1322和第3518个样本完全一致，部分特征如表4所示。为了最大化程度减小过拟合风险，对后面重复的样本进行删除处理，删除后数据集中共计15999个样本。

###### 表4重复值检验


<table border="1" ><tr>
<td colspan="1" rowspan="1">#</td>
<td colspan="1" rowspan="1">一天去两家医院的天数</td>
<td colspan="1" rowspan="1">就诊的月数</td>
<td colspan="1" rowspan="1">月统筹金额＿MAX</td>
<td colspan="1" rowspan="1">个人账户金额＿SUM</td>
<td colspan="1" rowspan="1">ALL_SUM</td>
<td colspan="1" rowspan="1">可用账户报销金额SUM</td>
<td colspan="1" rowspan="1">治疗费用在总金额占比</td>
<td colspan="1" rowspan="1">是否挂号</td>
<td colspan="1" rowspan="1">RES</td>
</tr><tr>
<td colspan="1" rowspan="1">1322</td>
<td colspan="1" rowspan="1">0</td>
<td colspan="1" rowspan="1">1</td>
<td colspan="1" rowspan="1">248.9</td>
<td colspan="1" rowspan="1">27.66</td>
<td colspan="1" rowspan="1">276.56</td>
<td colspan="1" rowspan="1">27.66</td>
<td colspan="1" rowspan="1">0.061469</td>
<td colspan="1" rowspan="1">0</td>
<td colspan="1" rowspan="1">0</td>
</tr><tr>
<td colspan="1" rowspan="1">3518</td>
<td colspan="1" rowspan="1">0</td>
<td colspan="1" rowspan="1">1</td>
<td colspan="1" rowspan="1">248.9</td>
<td colspan="1" rowspan="1">27.66</td>
<td colspan="1" rowspan="1">276.56</td>
<td colspan="1" rowspan="1">27.66</td>
<td colspan="1" rowspan="1">0.061469</td>
<td colspan="1" rowspan="1">0</td>
<td colspan="1" rowspan="1">0</td>
</tr></table>

## 3.5归一化处理

分析原始数据集特征可以发现，不同类型的特征变量取值范围相差很大，例如就诊天数的取值范围一般不会超过100，比例甚至不会超过1，但是各类就诊费用却高达几千甚至上万，如果直接使用这些特征数据进行建模会导致模型偏好数值较高的这些特征，从而造成结果的误差。因此为了减小变量取值范围相差较大的影响，需要对特征变量进行无量纲化处理。

常用的无量纲化方法主要有Min-Max归一化和Z-score 标准化：

### （1）Min-Max归一化

该方法是对原始的特征变量进行归一化，将所有的数值映射到［0,1］之间，具体转化方法如公式1所示。

$x^{*}=\frac{x-\min(x)}{\max(x)-\min(x)}$

### （2）Z-score 标准化

该方法主要是对数据进行标准化，使得数据服从标准正态分布，具体转化方法如公式2所示。

$x^{*}=\frac{x-\mu}{\sigma}$

在本文中，由于分类变量进行独热编码后全部为0或1，故选用第一种方法对除了医院编码NN、出院诊断病种名称NN、BZ＿民政救助、BZ＿城乡优抚、是否挂号等分类变量和RES标签之外的所有数值型数据进行归一化处理，使得所有的医保变量数值都处于［0,1］之间。并且由中心极限定理得，当样本数据量足够大时，独立随机变量的均值趋于正态分布。

归一化之后的部分数据如表5所示

