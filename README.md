# CartesianToSphericalMRI
 Spherical coordinates transformation pre-processing in MRI

Source code used to apply transformation from Cartesian to Spherical coordinates as a pre-processing step in Deep Learning for MRI automatic tumor segmentation.

This python code is part of the code used to train Deep Learning model in the Original Article [Spherical coordinates transformation pre-processing in Deep Convolution Neural Networks for brain tumor segmentation in MRI](https://link.springer.com/article/10.1007%2Fs11517-021-02464-1) by C. Russo et al.


```
Usage: python cartesian2spherical.py <input nifti file> <output nifti file>
example: python cartesian2spherical.py mri_demo.nii.gz sph_mri_demo.nii.gz
```


## Example of output transformed volume
![Example of transformed volume](https://github.com/doc78/CartesianToSphericalMRI/blob/main/imgs/VolumePolarCoordinatesExample.PNG?raw=true)
