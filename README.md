# PatchClearance

    Security Patch Group: Data Cleaning Task.
    Developer: Shu Wang
    Date: 2020-06-18
    File Structure:
    PatchClearance
        |-- candidates              # found samples need to be judged.
        |-- csvfiles                # feature files.
                |-- feature00.csv   # positive feature file.
                |-- feature01.csv   # negative feature file.
        |-- judged                  # already judged samples.
                |-- negatives
                |-- positives
        |-- matlab                  # matlab program.
        |-- random_commit           # unknown patches.
                |-- commit01
        |-- security_patch          # positive patches.
        |-- temp                    # temporary stored variables.
                |-- distMatrix.npy
                |-- outIndex.npy
        |-- temp_judged             # temp folder for GUI annotation.
                |-- negatives
                |-- positives
                |-- judged.csv      # storage for annotation. DO NOT DELETE!
        |-- annotate_GUI.py         # GUI for annotate candidate patches.
        |-- extract_features.py     # extract features for random_commit and security_patch.
        |-- get_dataset.py          # get the 30-folder negative dataset.
        |-- main.py                 # main entrance.
        |-- README.md               # this file.
    Usage:
        python main.py

To get `extract_features.py`, please refer to [XindaW/PatchFEX](https://github.com/XindaW/PatchFEX/blob/main/extract_features.py).
