import numpy as np
import torch 
import torch.nn as nn 
import torch.nn.functional as F
from torch.utils.data import Dataset
import torch.utils.data as Data
import matplotlib.pyplot as plt
import data_loader as dl


class sgrna_net(nn.Module):
    def __init__(self):
        super().__init__()
        self.embed1=nn.Embedding(16,2)
        self.embed2 = nn.Embedding(4,1)
        self.embed3 = nn.Embedding(4,1)
        self.lin4 =nn.Linear(19*2,1)
    
    def forward(self,seq,typ):
        #ade=torch.tensor([[-3.087,-2.605,-1.964,-2.436,-1.4056,-1.621] for i in range(len(seq))]).cuda()
        #adt=torch.tensor([[1.183948427438736,1.6361907720565796,1.5788605213165283,1.9095913767814636,2.1990426778793335,0.8195111453533173]for i in range(len(seq))]).cuda()
        #de=torch.sum(F.one_hot(typ,num_classes=6).squeeze(1)*ade,dim=-1).unsqueeze(-1)
        #dt=torch.sum(F.one_hot(typ,num_classes=6).squeeze(1)*adt,dim=-1).unsqueeze(-1)
        out=self.embed1(seq)
        de =self.embed2(typ).squeeze(-1)
        dt =3*torch.sigmoid(self.embed3(typ).squeeze(-1))
        #print(de.size(),dt.size())
        out=out.view(out.size(0),out.size(1)*out.size(2))
        out=self.lin4(out)
        out= torch.sigmoid(dt*out+de)
        return out
        
