# Uni-deepSG
If you use any code in this repository, please kindly cite our paper: "Z. C. Zhong, Z. Y. Li, J. Yang and Qian Wang, Unified Model to Predict gRNA Efficiency across Diverse Cell Lines and CRISPR-Cas9 Systems, Journal of Chemical Information and Modeling". Thank you.

![uni-deepSG](./topic.png)<br>
**Model Introduction**  
Uni-deepSG is a sgRNA efficiency prediction tool. In our paper, we proved that:
1) SgRNA efficiency, eff, can be modeled as  $eff=\frac{1}{1+\cdot e^{(a*E+b)}}$. E is solely determined by sgRNA sequence. a and b are two constants representing the uniqueness of each dataset
2) For identical sgRNA sequence, the editing efficiency measured in two different experiments can be expressed as $eff2=\frac{1}{1+A*((1/$eff1 -1))^B}}$
Based on these two conclusions, we can integrate data from different sources (labs, cell lines, Cas9 variants...) together to train a unified model.

**Requirments**
python==3.8.0  
numpy==1.23.5  
pytorch==2.0.1+cu117    

**Source Data**
All training and testing data can be found in ./main/source_data  

**Model Training**  
If you want to train the model, in ./main/TrainModel/ run temtrain.py.  
If you want to add new items, please check the format in ./main/TrainModel/data/ remeber to add the scaffold. the scaffold format is in "./main/TrainModel/AddScarfford.ipynb"<br>
the model is showing as follow:  
![MODEL](./model.png)
 

**predict tools**  
to make sgrna format correctly, choosing "normal" for normal scarfford, "abnormal" for scarfford using in Kim et al 2020.
if you want to predict one sgrna eff, in ./main/PredictionTools run predict.ipynb. change the sgrna variable in "cell 2" 23bp is need.

if you want to predict batches of sgrna in ./main/BatchPrediction/ run predict.ipynb. input file example is at ./main/BatchPredition/data/esp_format_23bp_eff.npy
In this model, if you want to predict multiple sequences and want to minimize the mean squared error (MSE), you can adjust the parameters A and B with input a small number of template sequence(10 for example) within your cas9 variants or laboratory. This adjustment can help improve the prediction results. It's important to note that this process will not affect the Spearman correlation.
