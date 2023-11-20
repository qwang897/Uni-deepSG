# Uni-deepSG

Uni-deepSG is a sgRNA eff prediction tools.

using $eff=\frac{1}{1+A \cdot e^{(ener+B)}}$ to combine CAS9 variants together. so the model can train different CAS9 or in different labs 

requrments:

python==3.8.0

numpy==1.23.5

pytorch==2.0.1+cu117

source data path:./main/source_data

if you want to train the model, in ./main/TrainModel/ run temtrain.py. if you want to add new items, please check the format in ./TrainModel/data/

to make sgrna format correctly, choosing "normal" for normal scarfford, "abnormal" for scarfford using in Kim et al 2020. 

if you want to predict one sgrna eff, in ./PredictionTools run predict.ipynb . change the sgrna variable in cell2. 23bp is need.

if you want to predict batches of sgrna in ./BatchPrediction/ run predict.ipynb. input file example is at ./BatchPredition/data/esp_format_23bp_eff.npy
In this model, if you want to predict multiple sequences and want to minimize the mean squared error (MSE), you can adjust the parameters A and B with input a small number of template sequence(10 for example) within your cas9 variants or laboratory. This adjustment can help improve the prediction results. It's important to note that this process will not affect the Spearman correlation.
