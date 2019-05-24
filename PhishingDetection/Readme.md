# PhishingDetection-using-Logistic-Regression
Detects whether a given URL is malicious or safe one 
(Still model has to be refined by choosing the right set of attributes, It detects the phishing websites with approx. 100% accuracy but thr few of the safe ones are treated as malicious too. IF you can find out, Do let me know ,Thanks)


Data set: https://archive.ics.uci.edu/ml/datasets/Phishing+Websites

Machine learning algorithm used : Logistic regression

Total attributes from Dataset: 31

Attributes selected and used : 20 (Using Recursive Feature Elimination(RFE))

Feature extraction from URL(as refernce): https://github.com/rewanth1997/Detect-phishing-websites-using-ML
https://github.com/rishipalyadav/Phishing-Website-Detection-Using-ML/blob/master/features.py
