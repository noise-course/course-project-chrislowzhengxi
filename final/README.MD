# Mobile App Country-of-Origin Classification

This project reproduces results from the **Mobile App Country of Origin** task in the nPrint benchmark. The goal is to predict whether a mobile application originated in **China**, **India**, or the **United States** using only its network traffic features.

The original benchmark uses AutoGluon, but here I focus on a traditional machine-learning baseline (Random Forest) and compare it with other common models. (I did include AutoGluon partially in the end.) 

---

## Files in this repository

```
final_notebook.ipynb          ← main notebook (runs end-to-end)
final_dataset_with_labels.csv ← dataset used for training/testing
offline_processing/           ← preprocessing scripts & intermediate files
   traffic.pcapng
   traffic_fixed.pcap
   traffic_features.csv
   extract_labels_tshark.py
   fix_pcap_safe.py
requirements.txt              ← packages needed to run the notebook
report/ ← the report folder. The html is under report/build/html/index.html
```

The notebook only depends on the CSV file and the Python packages listed. Nothing in the offline folder needs to be executed to reproduce the results.

---

## How to run

Open a terminal in the project directory and install dependencies:

```bash
pip install -r requirements.txt
```

Then open:

```bash
jupyter notebook final_notebook.ipynb
```

Inside Jupyter, use **Kernel → Restart & Run All**. The notebook should run start-to-finish and produce the same results.

---

## What the notebook does

1. Loads the cleaned feature dataset
2. Performs basic exploratory checks
3. Trains a Random Forest baseline
4. Evaluates accuracy and balanced accuracy
5. Displays confusion matrices and per-class results
6. Compares several additional models

   * Logistic Regression
   * SVM (linear + RBF)
   * Gradient Boosting
   * KNN
   * AutoGluon (simplified)
7. Performs simple cross-validation
8. Reports interpretation and conclusions

---

## Summary of results

Random Forest achieves:

* Accuracy around **93–94 percent**
* Balanced accuracy around **93 percent**

Performance is consistent across CV folds.

Gradient Boosting is close. Logistic Regression and linear SVM are slightly below. RBF SVM performs poorly on this dataset.

AutoGluon is decent as well, with slightly higher balanced accuracy (~94%) than random forest.

---

## Offline preprocessing (short note)

The original `.pcapng` file needed conversion and feature extraction using **nPrint**, and labels were extracted using **tshark**. These steps were completed once and are summarized in the Appendix of the notebook. The full scripts are included in `offline_processing/`.

This preprocessing is **not required** to run the notebook, since the dataset is already provided.
