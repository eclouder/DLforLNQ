import os
from enum import unique

import numpy as np
import pydicom
import nibabel as nib
import shutil


def dicom_to_nifti(dcm_folder, nifti_file):
    """
    dicom_to_nifti('path_to_dicom_folder', 'output_file.nii.gz')
    :param dcm_folder:
    :param nifti_file:
    :return:
    """
    # Get all DICOM files in the folder
    dicom_files = [os.path.join(dcm_folder, f) for f in os.listdir(dcm_folder) if f.endswith('.dcm')]

    # Read the first DICOM file to get metadata
    pixel_array = np.stack([pydicom.dcmread(f).pixel_array for f in dicom_files], axis=-1)

    # Create NIfTI image
    nifti_img = nib.Nifti1Image(pixel_array, np.eye(4))  # Identity matrix for affine

    # Save as .nii.gz
    nib.save(nifti_img, nifti_file)


def split_dataset2nnunet(dataset_name, feature_path, label_path):
    def _check_folder_exists(folder_path):
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            return True
        else:
            return False

    def _copy_file(source, destination):
        try:
            shutil.copy(source, destination)
            print(f"file '{source}' copied 2 '{destination}'。")
        except FileNotFoundError:
            print(f"file '{source}' don't exist。")
        except Exception as e:
            print(f"copy false {e}")

    assert isinstance(feature_path, list) & isinstance(label_path, list), "paths must be a list"
    if not _check_folder_exists("nnUNet_raw"):
        os.makedirs("nnUNet_raw")
    dataset_name = "nnUNet_raw" + "\\" + dataset_name
    if not _check_folder_exists(dataset_name):
        os.makedirs(dataset_name)
    nnunet_train_path = os.path.join(dataset_name, "imagesTr")
    nnunet_label_path = os.path.join(dataset_name, "labelsTr")
    if not _check_folder_exists(nnunet_train_path):
        os.makedirs(nnunet_train_path)
        for path in feature_path:
            _copy_file(path, nnunet_train_path + "\\" + os.path.basename(path))
    if not _check_folder_exists(nnunet_label_path):
        os.makedirs(nnunet_label_path)
        for path in label_path:
            _copy_file(path, nnunet_label_path + "\\" + os.path.basename(path))
    dataset_json_path = os.path.join(dataset_name, "dataset.json")
    dataset_json = \
        """{ 
         "channel_names": {
           "0": "CT"
         }, 
         "labels": {
           "background": 0,
           "LN": 1
         }, 
         "numTraining": 32, 
         "file_ending": ".nii.gz",
         "overwrite_image_reader_writer": "SimpleITKIO"
         }"""
    if not os.path.exists(dataset_json_path):
        with open(dataset_json_path, "w") as f:
            f.write(dataset_json)


# from Path import LyNoS_feature_path, LyNoS_ln_label_path
#
# split_dataset2nnunet("Dataset001_lynosNiigz", LyNoS_feature_path, LyNoS_ln_label_path)


def read_niigz(file_path):
    img = nib.load(file_path)
    data = img.get_fdata()
    return data
