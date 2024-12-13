# -*- coding: utf-8 -*-
"""Building  a simple CNN using Pytorch.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ZgD1mEu1b14JxaUNkl_ZlFuIxjgXTjPD
"""

#importing libraries
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

#Defining a CNN model
# The model i am defining here is a simple CNN
# Simple CNN is a straightforward convolutional neural network designed for image classification tasks, such as the MNIST dataset.
class SimpleCNN(nn.Module):
    def __init__(self):
        super(SimpleCNN, self).__init__()
        self.conv1 = nn.Conv2d(1, 16, kernel_size=3, stride=1, padding=1)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, stride=1, padding=1)
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
        self.fc1 = nn.Linear(32 * 7 * 7, 128)
        self.fc2 = nn.Linear(128, 10)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.relu(self.conv1(x))
        x = self.pool(x)
        x = self.relu(self.conv2(x))
        x = self.pool(x)
        x = x.view(-1, 32 * 7 * 7)  # Flatten
        x = self.relu(self.fc1(x))
        x = self.fc2(x)
        return x

# preparing data
# we are giving MNIST data
transform = transforms.Compose([
    transforms.Resize((28, 28)),
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))  # Normalize grayscale images
])

train_dataset = datasets.MNIST(root='data', train=True, transform=transform, download=True)# training model
train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)

test_dataset = datasets.MNIST(root='data', train=False, transform=transform, download=True)# testing the model
test_loader = DataLoader(test_dataset, batch_size=64, shuffle=False)

# Initialize Model, Loss, and Optimizer
model = SimpleCNN()
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training the model
epochs = 5 #epochs represent the number of times(5) the model sees the entire dataset during training.
for epoch in range(epochs):
    model.train()
    running_loss = 0.0
    for images, labels in train_loader:
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        running_loss += loss.item()

    print(f"Epoch {epoch+1}, Loss: {running_loss/len(train_loader):.4f}")

# Evaluating the model
model.eval() # It is used  to inform PyTorch that the model is in evaluation mode.
correct = 0
total = 0
with torch.no_grad(): # It is used to turn off gradient calculations.
    for images, labels in test_loader:
        outputs = model(images)
        _, predicted = torch.max(outputs, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

print(f"Accuracy: {100 * correct / total:.2f}%")