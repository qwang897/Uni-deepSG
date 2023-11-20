import numpy as np
import torch 
import torch.nn as nn 
import torch.nn.functional as F
from torch.utils.data import Dataset
import torch.utils.data as Data
import os

basedir=["A","T","C","G","N"]
transdir={}
cout=0
for i in basedir:
    transdir[i]=cout
    cout+=1

print(transdir)

class data_loader(Dataset):
    def __init__(self,dic="./data",file=False,filetype=0,state="normal") -> None:
        super().__init__()
        if not file:
            item=os.listdir(dic)
        else:
            item=[file]
        self.allsgrna=[]
        self.alleff=[]
        self.alltype=[]
        type=0
        for i in item:
            print(i,type if not file else filetype)
            data=np.load(dic+"/"+i,allow_pickle=True)
            print(len(data))
            for psgrna,eff in data:
                line=[]
                try:
                    float(eff)
                except:
                    continue
                if state == "normal":
                    sgrna=psgrna+"gtttCagagctaTGCTGgaaaCAGCAtagcaagttGaaataaggctagtccgttatcaacttgaaaaagtggcaccgagtcggtgcttt"[:36].upper()
                elif state == "abnormal":
                    sgrna=psgrna+"gtttTagagctaNNNNNgaaaNNNNNtagcaagttAaaataaggctagtccgttatcaacttgaaaaagtggcaccgagtcggtgcttt"[:36].upper()
                elif state == "prepared":
                    sgrna = psgrna
                else:
                    print("part of the scar should in the input sequence. choose the state 'normal' for commen scar. 'abnormal' for scar in kim2020. prepared if you have used the sca.ipynb to add the scar. ")
                if len(sgrna) == 59 and float(eff) <=1000:
                    for j in range(59):
                        bb=sgrna[j:j+1].upper()
                        line.append(transdir[bb])
                    self.allsgrna.append(line)
                    self.alleff.append(eff)
                    self.alltype.append(type)
            type+=1
        self.alleff=np.array(self.alleff).astype(float)
        self.allsgrna=np.array(self.allsgrna).astype(float)
        self.alltype=np.array(self.alltype).astype(float)
        if not file:
            pass
        else:
            self.alltype=np.ones(shape=self.alleff.shape)*filetype
    
    def __len__(self):
        return(len(self.allsgrna))

    def __getitem__(self, index):
        return torch.LongTensor(self.allsgrna[index]),torch.LongTensor([self.alltype[index]]),torch.FloatTensor([self.alleff[index]])


if __name__=="__main__":
    test=data_loader()
    for i in range(len(test)):
        test[i]

def translateseq(sgrna):
    line=[]
    if len(sgrna) == 59:
        for j in range(59):
            bb=sgrna[j:j+1].upper()
            line.append(transdir[bb])
    return torch.LongTensor(line)