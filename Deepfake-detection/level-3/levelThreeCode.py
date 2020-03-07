import math
import torch
import torch.nn as nn
from torch.nn import init

class Xception(nn.Module):
    """
    Xception optimized for the ImageNet dataset, as specified in
    https://arxiv.org/pdf/1610.02357.pdf
    """
    def __init__(self, num_classes=1000):
        """ Constructor
        Args:
            num_classes: number of classes
        """
        super(Xception, self).__init__()
        self.num_classes = num_classes

        # First convolution layer
        self.conv1 = nn.Conv2d(3, 32, 3,2, 0, bias=False)
        # First pooling layer
        self.bn1 = nn.BatchNorm2d(32)
        # First activation layer: RELU 
        self.relu = nn.ReLU(inplace=True)

        # Second set of layers
        self.conv2 = nn.Conv2d(32,64,3,bias=False)
        self.bn2 = nn.BatchNorm2d(64)
        
        # Specifying padding blocks, which are hard coded in PyTorch 
        # A block specifies the amount of pixels from the image added to the CNN
        # This is the implementation of the separable convolution from the Xception architecture with RELU activations
        self.block1=Block(64,128,2,2,start_with_relu=False,grow_first=True)
        self.block2=Block(128,256,2,2,start_with_relu=True,grow_first=True)
        self.block3=Block(256,728,2,2,start_with_relu=True,grow_first=True)

        self.block4=Block(728,728,3,1,start_with_relu=True,grow_first=True)
        self.block5=Block(728,728,3,1,start_with_relu=True,grow_first=True)
        self.block6=Block(728,728,3,1,start_with_relu=True,grow_first=True)
        self.block7=Block(728,728,3,1,start_with_relu=True,grow_first=True)

        self.block8=Block(728,728,3,1,start_with_relu=True,grow_first=True)
        self.block9=Block(728,728,3,1,start_with_relu=True,grow_first=True)
        self.block10=Block(728,728,3,1,start_with_relu=True,grow_first=True)
        self.block11=Block(728,728,3,1,start_with_relu=True,grow_first=True)
        self.block12=Block(728,1024,2,2,start_with_relu=True,grow_first=False)

        # Third set of layers  
        self.conv3 = SeparableConv2d(1024,1536,3,1,1)
        self.bn3 = nn.BatchNorm2d(1536)

        # Fourth set of layers
        self.conv4 = SeparableConv2d(1536,2048,3,1,1)
        self.bn4 = nn.BatchNorm2d(2048)

        # Linear output layer with num_classes as the number of output neurons (prediction classes)
        # With a binary classification task, num_classes = 2
        self.fc = nn.Linear(2048, num_classes)