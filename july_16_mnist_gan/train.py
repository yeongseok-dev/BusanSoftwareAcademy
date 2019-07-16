import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader

import data_loader

import model

if __name__=='__main__':
    batch_size=100
    
    # 트레이닝 데이터 로드

    train_data=data_loader.read_dataset('./training/')
    train_set=DataLoader(train_data,batch_size,True)

    # 트레이닝

    learning_rate=0.001
    training_epochs=10

    d_net=model.Discriminator()
    g_net=model.Generator()

    criterion=nn.BCELoss()
    
    d_optimizer=optim.Adam(d_net.parameters(),learning_rate)
    g_optimizer=optim.Adam(g_net.parameters(),learning_rate)

    print('Learning started. It takes sometime.')

    for epoch in range(training_epochs):
        for X,Y in train_set:
            d_optimizer.zero_grad()
            g_optimizer.zero_grad()

            hypothesis=d_net(X)
            d_cost_real=criterion(hypothesis,Y)

            z=torch.randn(batch_size,64)
            fake_images=g_net(z)
            hypothesis=d_net(fake_images)
            d_cost_fake=criterion(hypothesis,torch.zeros(batch_size))

            d_cost=d_cost_real+d_cost_fake
            d_cost.backward()
            d_optimizer.step()

            z=torch.randn(batch_size,64)
            fake_images=g_net(z)
            hypothesis=d_net(fake_images)
            g_cost=criterion(hypothesis,Y)
            g_cost.backward()
            g_optimizer.step()

        # 트레이닝 데이터 저장

        torch.save(g_net.state_dict(),'./g_net_epoch_%d.pth'%(epoch+1))
    
    print('Learning Finished!')