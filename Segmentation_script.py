#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 17 14:56:26 2022

@author: sriharsha.marupudi
"""

import numpy as np 
import numpy.ma as ma
import matplotlib.pyplot as plt
import nrrd 
from skimage import filters 
from skimage import measure
from skimage import exposure
from medpy import filter
# figDir = "/gpfs_projects_old/sriharsha.marupudi/ROI_Segmentations_otsu_grayscale_figs/"
figDir = "/gpfs_projects_old/sriharsha.marupudi/roi_figs_Segmentations_triplanar/"
sigma = .6


NAME = "1_761-67651-L45"

img1,header = nrrd.read(f"/gpfs_projects_old/sriharsha.marupudi/extract_rois_output_grayscale/ROI_{NAME}.nrrd")

val_marrow = 2e3
img1[img1<val_marrow] = val_marrow


img = filters.gaussian(img1, sigma)
image_slice = img[:,:,100]
# plt.imshow(image_slice)
filters.try_all_threshold(img[:,:,100], figsize=(8, 5), verbose=True)


# plt.imshow(img1[:,:,100])


img_otsu =filters.threshold_otsu(img[:,:,100])
plt.figure()
plt.imshow(img[:,:,100]>img_otsu)
# plt.imshow(img[:,:,100] > img_otsu)
# plt.show()
#img_ad = filter.smoothing.anisotropic_diffusion(img_otsu, niter=1, kappa=100, gamma=0.1, voxelspacing=None, option=2)



img_ad = filter.smoothing.anisotropic_diffusion(img, niter=10, kappa=100, gamma=0.1, voxelspacing=None, option=2)

def filter_otsu(img):
    thresh =filters.threshold_otsu(img)
    return img > thresh

img_otsu0 =filter_otsu(img)

img_otsu =filter_otsu(img_ad)

img_ad1 = img[:,:,100] > img_ad
img_otsu1 = img_ad1 > img_otsu

# plt.figure(figsize=(9, 4))
# plt.subplot(131)
# plt.imshow(image_slice, cmap='gray', interpolation='nearest')
# plt.axis('off')
# plt.subplot(132)
# plt.imshow(img_ad1[:,:,100], cmap='gray', interpolation='nearest')
# plt.axis('off')
# plt.subplot(133)
# plt.imshow(img_otsu1[:,:,100], cmap='gray', interpolation='nearest')
# plt.axis('off')
# plt.tight_layout()
# plt.show()

def plotall(img1,img2,img3,img4):
    plt.figure(figsize=(9, 4))
    plt.subplot(141)
    plt.imshow(img1[:,:,100], cmap='gray', interpolation='nearest')
    plt.axis('off')
    plt.subplot(142)
    plt.imshow(img2[:,:,100], cmap='gray', interpolation='nearest')
    plt.axis('off')
    plt.subplot(143)
    plt.imshow(img3[:,:,100], cmap='gray', interpolation='nearest')
    plt.axis('off')
    plt.subplot(144)
    plt.imshow(img4[:,:,100], cmap='gray', interpolation='nearest')
    plt.axis('off')
    plt.tight_layout()
    plt.show()

plotall(img, img_otsu0, img1, img_otsu)
nrrd.write(f"/gpfs_projects_old/sriharsha.marupudi/ROI_Segmentations_otsu_grayscales/Segmentation-{NAME}.nrrd",img_otsu.astype(np.uint8)

plt.figure(figsize=(9, 3.5))
plt.subplot(131)
plt.imshow(img1[:,:,100],cmap="gray")
plt.contour(img_otsu[:,:,100],level=0.5,linewidths=0.5)
plt.axis('off')
plt.subplot(132)
plt.imshow(img1[:,100,:],cmap="gray")
plt.contour(img_otsu[:,100,:],level=0.5,linewidths=0.5)
plt.axis('off')
plt.subplot(133)
plt.imshow(img1[100,:,:],cmap="gray")
plt.contour(img_otsu[100,:,:],level=0.5,linewidths=0.5)
plt.axis('off')
plt.savefig(figDir+f"{NAME}-Overlay")
