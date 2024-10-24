import os
import numpy as np
import pydicom
import nibabel as nib


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
    dcm_data = pydicom.dcmread(dicom_files[0])
    pixel_array = np.stack([pydicom.dcmread(f).pixel_array for f in dicom_files], axis=-1)

    # Create NIfTI image
    nifti_img = nib.Nifti1Image(pixel_array, np.eye(4))  # Identity matrix for affine

    # Save as .nii.gz
    nib.save(nifti_img, nifti_file)



