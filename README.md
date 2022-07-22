# Masked Loss based 1 D Convolution Neural Network (ML- ConvNet)

Masked Loss based 1 D Convolution Neural Network (ML- ConvNet) for  missing labels and applying mask for loss and metrics

Experimented with Mutli-label AMR datset with missing labels

Prerequists: Numpy, Pandas, Tensorflow, sklearn, matplotlib, Seaborn, tqdm

Steps

1. Follow step 1-4 from https://github.com/mukunthan/Rectified-Classifier-Chain
2. Dataset created from above steps is given in data/ folder
3. Run Default_Imptation_for_Missing_full_AMR.ipynb to get results with default loss function for 1D-CNN and ANN
4. Run Maskd_MEtrics_for_Missing_full_AMR.ipynb to get results with Masked loss function for 1D-CNN and ANN
5. Run Default_Imptation_for_Missing_full_AMR_Different_Missinglabel.ipynb to get results with different level of missingratio. 
6. Run Maskd_MEtrics_for_Missing_full_AMR_Different_Missinglabel.ipynb to get results with different level of missingratio.
7. Run Maskd_Metrics_for_Missing_Label_AMR _different models.ipynb to run different gradient based aproach and get significant features
8. Copy the Top featues saved in generated feature files in Step 7 and Run PrepareOutput.py to check the definition of features and known genes

