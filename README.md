# Uni-deepSG
If you use any code in this repository, please kindly cite our paper: "Z. C. Zhong, Z. Y. Li, J. Yang and Qian Wang, Unified Model to Predict gRNA Efficiency across Diverse Cell Lines and CRISPR-Cas9 Systems, Journal of Chemical Information and Modeling". Thank you.

![uni-deepSG](./topic.png)<br>
**Model Introduction**  
Uni-deepSG is a sgRNA efficiency prediction tool. We proved that:
1) SgRNA efficiency, eff, can be modeled as  $eff=\frac{1}{1+\cdot e^{(a*E+b)}}$. E is solely determined by sgRNA sequence. a and b are two constants representing the uniqueness of each dataset
2) For identical sgRNA sequence, the editing efficiency measured in two different experiments can be expressed as $eff2=\frac{1}{1+A*\cdot (1/eff1 - 1)^{B}}$  
Based on these two conclusions, we can integrate data from different sources (labs, cell lines, Cas9 variants...) together to train a unified model. Please see details in our original paper.

**Requirments**  
python==3.8.0  
numpy==1.23.5  
pytorch==2.0.1+cu117    

**Source Data**  
All training and testing data can be found in ./main/source_data  

**Model Training**  
If you want to train the model, in ./main/TrainModel/ run temtrain.py.  
If you want to add new training sets, please check the format in ./main/TrainModel/data/ remeber to add the scaffold. the scaffold format is in "./main/TrainModel/AddScarfford.ipynb"<br>
The architechture of the model is:  
![MODEL](./model.png)
 

**Model Prediction**  

1. Choosing "type 1" for the most common scaffold, "type 2" for scaffold used in Kim et al 2020  (Kim, N.; Kim, H. K.; Lee, S.; Seo, J. H.; Choi, J. W.; Park, J.; Min, S.; Yoon, S.; Cho, S. R.; Kim, H. H. Prediction of the Sequence- Specific Cleavage Activity of Cas9 Variants. Nat. Biotechnol. 2020, 38 (11), 1328−1336.).

2. If you want to predict the efficiency of a single sgRNA, go to the directory "./main/PredictionTools", run predict.ipynb. You need to input the sgRNA sequence (20+3PAM=23bp) in cell2 "sgrna=XXX".
3. If you want to predict the efficiencies of multiple sgRNA, go to the directory "./main/BatchPrediction/", run predict.ipynb. An input  example is: ./main/BatchPredition/data/esp_format_23bp_eff.npy
In this model, if you want to  minimize the mean squared error (MSE), you can adjust the parameters A and B, fitted by a small number of template sequences (10 for example). This adjustment can help improve the Pearson correlation. It's important to note that this process will not affect the Spearman correlation.
