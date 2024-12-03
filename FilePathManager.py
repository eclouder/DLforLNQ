from glob import glob
from typing import List, Dict, Optional
import shutil
from tqdm import tqdm
###
# .
# ├── ...
# ├── data
# │   ├── brats_patch
# │       ├── flair
#             ├── flair
#                 ├── training
#                     ├── normal
#                     ├── tumor
#                     ├── seg # label mask
#                 ├── validation
###
print(glob(r"F:\Y\weak_diff_seg\datasetB\*flair.nii.gz"))


class FilePathManager:
    def __init__(self, data_path: str, file_sorting: List[int], file_postfix: Dict[int, List[str]],
                 input_postfix: str,
                 mask_postfix: str):
        """

        """
        self.data_path = data_path
        self.file_sorting = file_sorting
        self.file_sorting_num = len(file_sorting)
        self.file_postfix = file_postfix
        self.input_postfix = input_postfix
        self.mask_postfix = mask_postfix
        if self.file_sorting[-1] != 1:
            self.input_path = data_path + "\\"
            self.mask_path = data_path + "\\"
        self.input_files = []
        self.mask_files = []
        self._find_files()

    def _find_files(self):
        for file_index, file_num in enumerate(self.file_sorting):
            if not file_index == self.file_sorting_num - 1:
                self.input_path += self.file_postfix[file_index + 1][0] + "\\"
                self.mask_path += self.file_postfix[file_index + 1][0] + "\\"
            else:
                self.input_path = self.input_path + self.input_postfix
                self.mask_path = self.mask_path + self.mask_postfix
        self.input_files = glob(self.input_path)
        self.mask_files = glob(self.mask_path)

    def get_path_info(self):
        assert len(self.input_files) != 0
        print(f"the first input file:{self.input_files[0]}")
        print(f"the first mask file:{self.mask_files[0]}")

    def move2fitcode(self, input_path: str, mask_path: str, delete: Optional[bool] = False):
        """
        TODO:
            1:async
            2:judge path exist , if not exist then create it.
            3: control tqdm (enable hidden)
        """
        assert len(self.input_files) != 0
        for input_file,mask_file in tqdm(zip(self.input_files,self.mask_files)):
            shutil.copy(input_file, input_path)
            shutil.copy(mask_file, mask_path)


filemanager = FilePathManager(
    r"F:\Y\weak_diff_seg\dataset",
    [1, 2],
    {1: ["BraTS2021_0*"],
     2: ["*flair.nii.gz", "*seg.nii.gz"]},
    input_postfix="*flair.nii.gz",
    mask_postfix="*seg.nii.gz"
)
filemanager.get_path_info()
filemanager.move2fitcode(r"F:\Y\weak_diff_seg\cond_ddpm_wsss\data\brats_patch\flair\flair\training\tumor",
                         r"F:\Y\weak_diff_seg\cond_ddpm_wsss\data\brats_patch\flair\flair\training\seg")