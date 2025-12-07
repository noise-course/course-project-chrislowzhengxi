.. Mobile App Country of Origin Classification documentation master file, created by
   sphinx-quickstart on Sat Dec  6 21:36:21 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Mobile App Country of Origin Classification: A Leaderboard Reproduction
=======================================================================

Introduction
------------

In this report, I analyze the Mobile App Country of Origin dataset from the nPrint project. 
The goal is to predict whether a mobile app was developed in the United States, China, or India
based on its network traffic. The dataset in this project has already been processed using 
nPrint, so the features are ready for machine learning without the need to manually parse packet captures.

My main goal is to build a baseline model and compare the results against the published 
leaderboard. The official leaderboard reports a balanced accuracy of about 96.8 percent 
based on AutoGluon. I start with a Random Forest classifier as a simple baseline and examine
the results using balanced accuracy and confusion matrices. I also consider running AutoGluon 
and compare its results with the Random Forest model.

Project Structure and Data Preparation
--------------------------------------

This analysis uses a preprocessed dataset named ``final_dataset_with_labels.csv``. 
This file already contains the extracted nPrint features and the country label. 
This means the notebook can run end to end without installing nPrint or working 
with packet capture files.

The scripts and intermediate data used to convert the original packet traces, 
extract features, and attach labels are stored in the ``offline_processing`` folder. 
These steps are summarized in the Appendix. They are not required to run the notebook.


Data
----

The dataset in this project comes from the Mobile App Country of Origin benchmark 
in the nPrint project. Each row corresponds to one network flow produced by a 
mobile application, where a flow is a sequence of packets between two endpoints. 
All network traffic has already been processed by the nPrint tool, which converts 
each flow into a fixed length vector of binary and numeric features derived from 
low-level header fields and payload bit patterns.

There are about ten thousand rows in the final dataset and a little over one 
thousand feature columns. Most of the features are binary indicators produced by 
nPrint. The target label identifies the country where the mobile application was 
developed. In this benchmark the classes are the United States, China, and India. 
The class distribution is reasonably balanced, and there are no missing values 
in the preprocessed file.


Methods
-------

This analysis begins by forming a training set and a separate test set. I use a stratified
split so the proportions of China, India, and the United States remain close to the original
distribution. The feature matrix contains the nPrint binary and numeric fields, while the
label identifies the country of origin for each flow. I remove a small number of columns
that contain purely identifying information, such as the string representation of the IP
address. I do not apply other preprocessing steps inside the notebook because nPrint has
already produced a consistent feature space for supervised learning.

The first model I train is a Random Forest classifier. It usually performs well on high
dimensional feature spaces and requires very little additional preparation. I use accuracy
and balanced accuracy as the main evaluation metrics. Balanced accuracy gives a clearer
picture of performance here, since the label distribution is not perfectly even. Random Forest
reached about 93 percent in terms of balanced accuracy. The classification report in the notebook 
also provides precision, recall, and F1 scores for each class, which helps show whether the model
favors specific countries.

After building a baseline with Random Forest I train several other classifiers on exactly
the same training data. The idea is not to tune these models deeply or produce a perfect
leaderboard. The goal is to see whether a pattern that appears in Random Forest also shows
up in other supervised methods. The comparison uses common models that appear frequently
in introductory machine learning toolkits, such as Logistic Regression, Linear SVM,
Gradient Boosting, and a K Nearest Neighbors classifier. The results from this comparison
help show whether the performance is tied to a specific model family rather than something
that appears in a wider range of approaches.

I also run a short five fold cross validation on the Random Forest model. This step checks
whether the performance remains fairly stable across different partitions of the training
data. It gives a sense of how much the observed accuracy might depend on the particular
train and test split. The cross validation procedure evaluates balanced accuracy on each
fold and reports the mean and standard deviation across folds.


As a final experiment I also trained AutoGluon on the same feature table. 
This experiment follows the official nPrint benchmark, which uses AutoGluon to produce 
the published leaderboard scores. I only used the default tabular settings with 
the available backends in my environment. The intention was not to reproduce 
every component of the full AutoGluon pipeline, but rather to test whether 
automated ensembling can extract more signal from the same nPrint representation. 
This final experiment helps connect the results in this project with the 
leaderboard results that appear in the official nPrint benchmark.


Results
-------

The Random Forest baseline achieved an accuracy of approximately 93.63 percent and a 
balanced accuracy near 93.31 percent on the held out test set. The classification report 
indicates strong precision and recall for all three labels. The confusion matrix in 
the notebook shows that most predictions fall along the diagonal, which suggests that 
the model usually identifies the correct country. The largest block of correct 
predictions appears for the India flows. China shows a slightly larger number of 
mis-labeled samples compared to the other two classes.

Across the comparison models, Random Forest and Gradient Boosting reached the highest
and most stable performance. Logistic Regression and Linear SVM also delivered
reasonable results given the high dimensionality of the feature space. In contrast,
the RBF SVM model struggled (only about 33.34 percent balanced accuracy). This outcome
is expected because RBF kernels do not scale well to thousands of sparse binary features 
and often have difficulty finding a useful boundary in settings of this type. The 
comparison suggests that tree based approaches remain stronger models for the nPrint 
representation.

The five fold cross validation for Random Forest reported a mean balanced accuracy near
92.96 percent with a relatively small standard deviation across folds. This indicates that
the observed performance does not depend heavily on the particular train and test split
and that the model is fairly stable for this dataset.

The AutoGluon experiment produced a balanced accuracy near 93.95 percent using only the
available backends in this environment. This value is close to the manually tuned
Random Forest baseline. The remaining gap relative to the official leaderboard value
appears to come from additional model families inside the full AutoGluon installation.


Conclusion
----------

In this notebook I trained a set of baseline models on the packet-level features generated 
from the dataset. A Random Forest achieved the strongest performance among the manually 
selected models, reaching about 94 percent accuracy with balanced results across all three
classes. Cross-validation confirmed that this performance is stable across different train-test
splits. Simpler linear models (Logistic Regression) and Gradient Boosting also performed well, 
while models that rely on strong assumptions about the feature space, such as the RBF SVM, 
struggled with the high-dimensional sparse representation.

An additional experiment using AutoGluon showed that an automated ensemble of tree-based
methods can push the accuracy slightly higher on the same features, without any manual tuning. 
Overall, the results indicate that header-level structure alone contains enough signal to 
distinguish traffic from the United States, China, and India. More advanced modeling 
or richer payload features could be explored in future work, but for the purpose of a 
baseline reproduction this level of performance already compares favorably with the 
published results. Together these steps provide a complete and reproducible baseline 
for this benchmark.


Appendix
--------

Appendix A. Offline Processing Files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This project includes a folder named ``offline_processing``. It contains the
scripts and intermediate files that convert the original PcapNG capture into a
CSV with packet features and country labels. These steps were completed outside
this notebook, so a new user does not need to install nPrint or Tshark to run
the main analysis. The final combined dataset is called
``final_dataset_with_labels.csv`` and appears in the data folder of this
project.

Appendix B. Data Conversion and Feature Extraction
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The original capture for this benchmark was available in the PcapNG format.
An older version of nPrint was required for this project, and that tool expected
a regular ``.pcap`` file rather than a PcapNG file. To address this, I converted
the downloaded capture into a standard format using a short Python script. The
conversion rewrote timestamps and produced a file that nPrint could process.

After conversion, the nPrint command line tool parsed each packet and generated
a feature table with binary and numeric fields. The main flags requested IPv4,
TCP, and UDP header information along with a small region of payload bytes.
Because these steps were performed offline only once, the notebook simply loads
the resulting CSV and continues directly with the modeling tasks.

Appendix C. Attaching Country Labels
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The nPrint output did not contain the country of origin label. The country was
stored inside the original PcapNG file as a packet comment, so I extracted that
information before merging it with the feature table. Tshark was used to obtain
the packet comments and the source IP field. I then joined this information with
the nPrint features. The join used the original order of the packets in the
capture, since both files contained the same number of entries.

The packet comment contained both an identification string and the country. A
simple parsing step removed the identifier so that the resulting label column
contains only the country name. The combined feature table, now including a
``label`` column, was saved as ``final_dataset_with_labels.csv``. This is the
dataset used in the main notebook and the only file required to reproduce the
modeling results reported in this project.





