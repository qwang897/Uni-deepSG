from turtle import forward
import numpy as np
import torch 
import torch.nn as nn 
import torch.nn.functional as F
from torch.utils.data import Dataset
import torch.utils.data as Data
import data_loader as dl
import train as tt
#torch.manual_seed(3047)

net=tt.sgrna_net().cuda()

lossf = nn.MSELoss()
print(net)

train=dl.data_loader(dic="./data/train",state="prepared")
test=dl.data_loader(dic="./data/test",state="prepared")

trloader=Data.DataLoader(dataset=train,batch_size=10000,shuffle=True)
valoader=Data.DataLoader(dataset=test ,batch_size=10000,shuffle=True)


opt=torch.optim.Adam(filter(lambda p : p.requires_grad, net.parameters()),lr=0.0001)
she=torch.optim.lr_scheduler.CosineAnnealingWarmRestarts(opt,T_0=5)   
steps=20000
wt1=open("./generate_data/traj/trloss","w+")
wt2=open("./generate_data/traj/valoss","w+")

for _ in range(steps+1):
    net.train()
    for seq,typ,eff in trloader:
        seq=seq.cuda()
        typ=typ.cuda()
        eff=eff.cuda()
        pre=net(seq,typ)
        loss=lossf(pre,eff)
        opt.zero_grad()
        loss.backward()
        opt.step()
        she.step()
    print(loss.detach().cpu().numpy(),file=wt1,flush=True)

    net.eval()
    for seq,typ,eff in valoader:
        seq=seq.cuda()
        typ=typ.cuda()
        eff=eff.cuda()
        pre=net(seq,typ)
        loss=lossf(pre,eff)
    print(loss.detach().cpu().numpy(),file=wt2,flush=True)

    if _%100 ==0:
        presave=[]
        effsave=[]
        for seq,typ,eff in trloader:
            seq=seq.cuda()
            typ=typ.cuda()
            eff=eff.cuda()
            pre=net(seq,typ)
            pre=pre.detach().cpu().numpy()
            eff=eff.detach().cpu().numpy()
            if len(presave)==0:
                presave=np.copy(pre)
                effsave=np.copy(eff)
            else:
                presave=np.concatenate((presave,pre))
                effsave=np.concatenate((effsave,eff))
            
        np.save("./generate_data/out/effv"+"_"+str(_),effsave)
        np.save("./generate_data/out/prev"+"_"+str(_),presave)

        presave=[]
        effsave=[]
        for seq,typ,eff in valoader:
            seq=seq.cuda()
            typ=typ.cuda()
            eff=eff.cuda()
            pre=net(seq,typ)
            pre=pre.detach().cpu().numpy()
            eff=eff.detach().cpu().numpy()
            if len(presave)==0:
                presave=np.copy(pre)
                effsave=np.copy(eff)
            else:
                presave=np.concatenate((presave,pre))
                effsave=np.concatenate((effsave,eff))
            
        np.save("./generate_data/out/eff"+"_"+str(_),effsave)
        np.save("./generate_data/out/pre"+"_"+str(_),presave)

        torch.save(net,"./generate_data/model/"+str(_)+".pt")

        
