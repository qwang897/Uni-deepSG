import numpy as np
import torch 
import torch.nn as nn 
import torch.nn.functional as F
from torch.utils.data import Dataset
import torch.utils.data as Data
import matplotlib.pyplot as plt
import data_loader as dl


class sgrna_net(nn.Module):
    def __init__(self,type=11):
        super().__init__()
        self.embed1=nn.Embedding(5,16)
        self.embed3=nn.Sequential(nn.Embedding(type,100),nn.ReLU(),nn.Linear(100,100),nn.ReLU(),nn.Linear(100,2),nn.Sigmoid())
        self.conv1=nn.Conv1d(in_channels=16,out_channels=64,kernel_size=5,padding=2)
        self.conv2=nn.Conv1d(in_channels=64,out_channels=64,kernel_size=5,padding=2)
        self.conv3=nn.Conv1d(in_channels=64,out_channels=64,kernel_size=5,padding=2)
        self.conv4=nn.Conv1d(in_channels=16,out_channels=64,kernel_size=5,padding=2)
        self.lin1=nn.Linear(64*59*2,2048)
        self.lin2=nn.Linear(2048,2048)
        self.lin3=nn.Linear(2048,1)
    
    def forward(self,seq,typ,s1=False,train=True):
        bt=10*(self.embed3(typ)-0.5)
        out=self.embed1(seq)
        out=out.transpose(-1,-2)
        si =self.conv1(out)
        be =self.conv4(out)
        out=F.relu(si)
        if train:
            out=F.dropout(out,p=0.5)
        out=self.conv2(out)
        out=F.relu(out)
        if train:
            out=F.dropout(out,p=0.5)
        out=self.conv3(out)
        out=F.relu(out)
        if train:
            out=F.dropout(out,p=0.5)
        out=out.view(out.size(0),out.size(1)*out.size(2))
        be4=be.view(be.size(0),be.size(1)*be.size(2))
        out = torch.cat((out,be4),dim=-1)
        out=self.lin1(out)
        out=F.relu(out)
        if train:
            out=F.dropout(out,p=0.5)
        out=self.lin2(out)
        out=F.relu(out)
        if train:
            out=F.dropout(out,p=0.5)
        out=self.lin3(out)
        out = torch.cat((out,torch.ones(size=(out.size(0),1),device="cuda")),dim=-1).unsqueeze(1)
        out = torch.mul(out,bt)
        out= torch.sigmoid(torch.sum(out,dim=-1))
        return out
        
