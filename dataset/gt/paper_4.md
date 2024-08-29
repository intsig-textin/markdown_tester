## A Scaling laws

We use 7 models to fit the scaling laws of Baichuan 2.The parameter details are shown in Table 10.

<table style="width: 61.9668%;" border="1" cellspacing="0" cellpadding="6" align="center">
<tbody>
<tr>
<td style="width: 26.2452%;">$N_{hidden}$</td>
<td style="width: 12.6437%;">$N_{FFN}$</td>
<td style="width: 14.1762%;">$N_{layer}$</td>
<td style="width: 14.5594%;">$N_{head}$</td>
<td style="width: 32.3755%;">$Nparams$ (Millions)</td>
</tr>
<tr>
<td style="text-align: center; width: 26.2452%;">384</td>
<td style="text-align: center; width: 12.6437%;">1,152</td>
<td style="text-align: center; width: 14.1762%;">6</td>
<td style="text-align: center; width: 14.5594%;">6</td>
<td style="text-align: center; width: 32.3755%;">11.51</td>
</tr>
<tr>
<td style="text-align: center; width: 26.2452%;">704</td>
<td style="text-align: center; width: 12.6437%;">2,112</td>
<td style="text-align: center; width: 14.1762%;">8</td>
<td style="text-align: center; width: 14.5594%;">8</td>
<td style="text-align: center; width: 32.3755%;">51.56</td>
</tr>
<tr>
<td style="text-align: center; width: 26.2452%;">832</td>
<td style="text-align: center; width: 12.6437%;">2,496</td>
<td style="text-align: center; width: 14.1762%;">12</td>
<td style="text-align: center; width: 14.5594%;">8</td>
<td style="text-align: center; width: 32.3755%;">108.01</td>
</tr>
<tr>
<td style="text-align: center; width: 26.2452%;">1,216</td>
<td style="text-align: center; width: 12.6437%;">3,648</td>
<td style="text-align: center; width: 14.1762%;">16</td>
<td style="text-align: center; width: 14.5594%;">8</td>
<td style="text-align: center; width: 32.3755%;">307.60</td>
</tr>
<tr>
<td style="text-align: center; width: 26.2452%;">1,792</td>
<td style="text-align: center; width: 12.6437%;">5,376</td>
<td style="text-align: center; width: 14.1762%;">20</td>
<td style="text-align: center; width: 14.5594%;">14</td>
<td style="text-align: center; width: 32.3755%;">835.00</td>
</tr>
<tr>
<td style="text-align: center; width: 26.2452%;">2,240</td>
<td style="text-align: center; width: 12.6437%;">6,720</td>
<td style="text-align: center; width: 14.1762%;">24</td>
<td style="text-align: center; width: 14.5594%;">14</td>
<td style="text-align: center; width: 32.3755%;">1,565.60</td>
</tr>
<tr>
<td style="text-align: center; width: 26.2452%;">2,880</td>
<td style="text-align: center; width: 12.6437%;">8,640</td>
<td style="text-align: center; width: 14.1762%;">28</td>
<td style="text-align: center; width: 14.5594%;">20</td>
<td style="text-align: center; width: 32.3755%;">3,019.33</td>
</tr>
</tbody>
</table>

###### Table 10:The model we choose for fitting scaling laws.

The losses of the 7 different models are shown in Figure 8.



###### Figure 8: The various training loss of small models for scaling law.

## B NormHead

By conducting a word embedding KNN retrieval task, where given a query word the nearest K words are retrieved. We found that the semantic information is mainly encoded by the cosine similarity of embedding rather than $L_{2}$ distance. i.e.,The KNN results of cosine similarity are words with semantic similarity while the KNN results of $L_{2}$ distance are meaningless in some way. Since the current linear classifier computes logits by dot product, which is a mixture of $L_{2}$ distance and cosine similarity. To alleviate the distraction of $L_{2}$ distance,We propose to compute the logits by the angle only. We normalized the output Embedding so that the dot product is not affected by the norm of embedding.

To validate this operation, we conduct an ablation experiment where we add or remove the normalization before softmax and train a 7B model for 12k steps. All the hyper-parameters and data are the same with Baichuan 2-7B. The training loss is shown in Figure 9. We can see that when removing the NormHead the training became very unstable at the beginning, on the contrary, after we normalized the head the training became very stable,which resulted in better performance.



###### Figure 9: The training loss with and without NormHead operation. The experiments are conducted on 7 billion parameters with the same hyper-parameters (torch random seeds, data flow, batch size, learning rate, etc.)

## C Training Dynamics

In this section, we analyze the training dynamics of our model. We save the checkpoints of Baichuan 2-7B and Baichuan 2-13B every 1000 steps. And evaluate those intermediate results on C-Eval development set (Huang et al., 2023), MMLU (Hendrycks et al., 2021a), CMMLU (Li et al., 2023),JEC-QA(Zhong et al.,2020),GSM8K(Shi et al., 2022) and HumanEval (Chen et al., 2021). The result is shown in Figure 10.

As shown, both the 7B and 13B models demonstrate substantial gains as training progresses. However, on general benchmarks such as MMLU (Hendrycks et al., 2021a) and C-Eval (Huang et al., 2023), improvements appear to plateau after 2 trillion tokens. In contrast, consistent gains are achieved on the GSM8K math tasks even beyond 2 trillion tokens. This suggests training FLOPs may strongly correlate with improvements in math problem solving, which may be further studied.

## D Baichuan Harmless Evaluation Dataset

WARNING: this section contains unsafe,offensive, or upsetting examples of text.

We proposed the Baichuan Harmless Evaluation Dataset (BHED) to evaluate the chat models, as

