# SecurityPatch

    Security Patch Group: Data Cleaning Task.
    Developer: Shu Wang
    Date: 2020-04-03
    File Structure:
    Patch
        |-- candidates              # found samples need to be judged.
        |-- judged                  # already judged samples.
                |-- negatives
                |-- positives
        |-- matlab                  # matlab program.
        |-- random_commit           # unknown patches.
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
        |-- feature.csv             # feature file.
        |-- main.py                 # main entrance.
    Usage:
        python main.py
