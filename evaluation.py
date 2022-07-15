import SimpleITK as sitk
import matplotlib.pyplot as plt
import torch
from torchmetrics import MeanAbsoluteError

if __name__ == '__main__':
    # loading images
    reader = sitk.ImageFileReader()
    reader.SetFileName("C:/Users/pmilab/PycharmProjects/3D-CycleGan-Pytorch-MedImaging-main/Data_folder/train/images/0.nii") # ground truth
    true = reader.Execute()

    reader.SetFileName("C:/Users/pmilab/PycharmProjects/3D-CycleGan-Pytorch-MedImaging-main/Data_folder/train/images/0.nii") # output result
    # reader.SetFileName("C:/Users/pmilab/PycharmProjects/3D-CycleGan-Pytorch-MedImaging-main/Data_folder/test/labels/0.nii")
    result = reader.Execute()
    result = sitk.GetArrayFromImage(result)
    print("result shape", result.shape)

    true = sitk.GetArrayFromImage(true)
    print("true shape", true.shape)
    # print(true[0])
    print("true slice", true[0].shape, "\nresult slice", result[0].shape)

    # histogram
    histA = []
    histB = []

    print("length of his", true[:, 0, 0].size)

    for i in range(true[:, 0, 0].size):
        sliceA = true[i]
        sliceB = result[i]
        valA = plt.hist(sliceA.ravel(), bins=range(256))
        valB = plt.hist(sliceB.ravel(), bins=range(256))
        histA.append(valA[0])
        histB.append(valB[0])

    print(len(histB[0]))
    print(len(histA[0]))
    val = 0
    for i in range(len(histB[0])):
        val += histB[0][i]
    print("total histB", val)

    histC = []
    for i in range(len(histA)):
        histC.append(histB[i] - histA[i])

    histDiff = []
    for i in range(len(histC[0])):
        value = 0
        for j in range(len(histC)):
            value += histC[j][i]
        histDiff.append(value)
    print(histDiff)

    print("histDiff length", len(histDiff))
    plt.clf()

    plt.plot(histDiff)

    # print(histC)
    plt.show()

    # mean absolute error
    result_tensor = torch.from_numpy(result)
    true_tensor = torch.from_numpy(true)
    mae = MeanAbsoluteError()
    mae = mae(result_tensor.cpu(), true_tensor.cpu())
    print("mae from torch", mae.numpy())

    MAE = sum(sum(sum(abs(result - true)))) / result.size
    print("mae from numpy", MAE)