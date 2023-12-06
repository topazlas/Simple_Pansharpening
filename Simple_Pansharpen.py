import cv2
import gc
import numpy as np


def brovey_pansharpen(pan_path, ms_path, output_path, W=0.2):
    """
    Pansharpen a given multispectral image using its corresponding panchromatic image with brovey algorithm.

    Inputs:
    - pan_path: File path of panchromatic image (in .jpg or .png format)
    - ms_path: File path of multispectral image to be pansharpened (in .jpg or .png format)
    - output_path: File path of pansharpened multispectral image to be written to file (in .jpg or .png format)
    - W: Weight value to be used for brovey pansharpening

    Outputs:
    - img_psh: Pansharpened multispectral image
    """

    img_pan = cv2.imread(pan_path, cv2.IMREAD_GRAYSCALE)
    img_ms = cv2.imread(ms_path)

    ms_to_pan_ratio = img_ms.shape[1] / img_pan.shape[1]
    rescaled_ms = cv2.resize(img_ms, None, fx=ms_to_pan_ratio, fy=ms_to_pan_ratio, interpolation=cv2.INTER_CUBIC)

    if img_pan.shape[0] < rescaled_ms.shape[0]:
        rescaled_ms = rescaled_ms[:img_pan.shape[0], :, :]
    else:
        img_pan = img_pan[:rescaled_ms.shape[0], :]

    if img_pan.shape[1] < rescaled_ms.shape[1]:
        rescaled_ms = rescaled_ms[:, :img_pan.shape[1], :]
    else:
        img_pan = img_pan[:, :rescaled_ms.shape[1]]

    img_psh = np.zeros_like(rescaled_ms, dtype=np.uint8)

    DNF = (img_pan.astype(np.float32) - W * rescaled_ms[:, :, 0].astype(np.float32)) / (
                W * rescaled_ms[:, :, 0].astype(np.float32) + W * rescaled_ms[:, :, 1].astype(
            np.float32) + W * rescaled_ms[:, :, 2].astype(np.float32))

    for band in range(rescaled_ms.shape[2]):
        img_psh[:, :, band] = (rescaled_ms[:, :, band] * DNF).astype(np.uint8)

    del img_pan, rescaled_ms
    gc.collect()

    cv2.imwrite(output_path, img_psh)

    return img_psh


def esri_fusion(pan_path, ms_path, output_path):
    """
    Esri-style image fusion using mean subtraction.

    Inputs:
    - pan_path: File path of panchromatic image (in .jpg or .png format)
    - ms_path: File path of multispectral image to be fused (in .jpg or .png format)
    - output_path: File path of fused image to be written to file (in .jpg or .png format)

    Outputs:
    - fused_img: Fused image
    """

    img_pan = cv2.imread(pan_path, cv2.IMREAD_GRAYSCALE)
    img_ms = cv2.imread(ms_path)

    ms_to_pan_ratio = img_ms.shape[1] / img_pan.shape[1]
    rescaled_ms = cv2.resize(img_ms, None, fx=ms_to_pan_ratio, fy=ms_to_pan_ratio, interpolation=cv2.INTER_CUBIC)

    if img_pan.shape[0] < rescaled_ms.shape[0]:
        rescaled_ms = rescaled_ms[:img_pan.shape[0], :, :]
    else:
        img_pan = img_pan[:rescaled_ms.shape[0], :]

    if img_pan.shape[1] < rescaled_ms.shape[1]:
        rescaled_ms = rescaled_ms[:, :img_pan.shape[1], :]
    else:
        img_pan = img_pan[:, :rescaled_ms.shape[1]]

    fused_img = np.zeros_like(rescaled_ms, dtype=np.uint8)

    ADJ = img_pan - rescaled_ms.mean(axis=2)

    for band in range(rescaled_ms.shape[2]):
        fused_img[:, :, band] = rescaled_ms[:, :, band] + ADJ

    cv2.imwrite(output_path, fused_img)

    return fused_img


def simple_mean_fusion(pan_path, ms_path, output_path):
    """
    Simple mean transformation for image fusion.

    Inputs:
    - pan_path: File path of panchromatic image (in .jpg or .png format)
    - ms_path: File path of multispectral image to be fused (in .jpg or .png format)
    - output_path: File path of fused image to be written to file (in .jpg or .png format)

    Outputs:
    - fused_img: Fused image
    """

    img_pan = cv2.imread(pan_path, cv2.IMREAD_GRAYSCALE)
    img_ms = cv2.imread(ms_path)

    ms_to_pan_ratio = img_ms.shape[1] / img_pan.shape[1]
    rescaled_ms = cv2.resize(img_ms, None, fx=ms_to_pan_ratio, fy=ms_to_pan_ratio, interpolation=cv2.INTER_CUBIC)

    if img_pan.shape[0] < rescaled_ms.shape[0]:
        rescaled_ms = rescaled_ms[:img_pan.shape[0], :, :]
    else:
        img_pan = img_pan[:rescaled_ms.shape[0], :]

    if img_pan.shape[1] < rescaled_ms.shape[1]:
        rescaled_ms = rescaled_ms[:, :img_pan.shape[1], :]
    else:
        img_pan = img_pan[:, :rescaled_ms.shape[1]]

    fused_img = np.zeros_like(rescaled_ms, dtype=np.uint8)

    for band in range(rescaled_ms.shape[2]):
        fused_img[:, :, band] = 0.5 * (rescaled_ms[:, :, band] + img_pan)

    cv2.imwrite(output_path, fused_img)

    return fused_img


# Example usage:
pan_path = '1.jpg'
ms_path = '2.jpg'
output_path = 'results/1.jpg'

# Use the method you want for your purpose
#brovey_pansharpen(pan_path, ms_path, output_path)
#esri_fusion(pan_path, ms_path, output_path)
#simple_mean_fusion(pan_path, ms_path, output_path)
