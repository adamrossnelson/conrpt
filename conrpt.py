# 1.0.0(py) Adam Ross Nelson May2018 ported to Python
# Original author : Adam Ross Nelson
# Description     : Python routine that provides confusion matrix statistics.
# Maintained at   : https://github.com/adamrossnelson/conrpt

def conrpt(rvar, tvar):
    from pandas import DataFrame
    import pandas
    import math

    df = pandas.concat([rvar.to_frame(), tvar.to_frame()], 
       axis=1, ignore_index=True)
    df.columns = ['rvar','tvar']

    df_xtab = pandas.crosstab(df['rvar'], df['tvar'])

    # Test that arguments are binary
    if not (df['rvar'].isin([1,0]).all()) or not (df['tvar'].isin([1,0]).all()):    
        raise ValueError('Variables must be binary.')

    # Count number of observed positive
    ObservedPos = sum(rvar)
    # Count number of observed negative
    ObservedNeg = len(rvar) - sum(rvar)
    # Count number of total observations
    ObseredTot = len(rvar)
    # Count number that tested positive
    TestedPos = sum(tvar)
    # Count number that tested negative
    TestedNeg = len(tvar) - sum(tvar)
    # Count number of all tested
    TestedTot = len(tvar)
    # Count true positive results
    TruePos = df_xtab.ix[1][1]
    # Count true negative results
    TrueNeg = df_xtab.ix[0][0]
    # Count false positive
    FalsePos = df_xtab.ix[1][0]
    # Count false negative
    FalseNeg = df_xtab.ix[0][1]
    # Calculate sensitivity
    Sensitivity = TruePos / ObservedPos
    # Calculate specitivity
    Specitivity = TrueNeg / ObservedNeg
    # Calculate positive predictive value
    PosPredVal = TruePos / (TruePos + FalsePos)
    # Calculate negative predictive value
    NegPredVal = TrueNeg / (TrueNeg + FalseNeg)
    # Calculate false positive rate
    FalsePosRt = FalsePos / ObservedNeg
    # Calculate false negative rate
    FalseNegRt = FalseNeg / (FalseNeg + TruePos)
    # Calculate correct rate
    CorrectRt = (TruePos + TrueNeg) / TestedTot
    # Calculate incorrect rate
    IncorrectRt = (FalsePos + FalseNeg) / TestedTot
    # Calculate ROC area
    
    # Calculate f1 Score
    F1Score = (2 * TruePos / (2 * TruePos + FalsePos + FalseNeg))
    # Calculate Matthes corr coefficient
    MattCorCoef = (((TruePos * TrueNeg) - (FalsePos * FalseNeg)) /
                  math.sqrt(
                      (TruePos + FalsePos) * (TruePos + FalseNeg)
                      (TrueNeg + FalsePos) * (TrueNeg + FalseNeg)))

    # TODO: Concatenate each column into a DataFrame
    # Pseudo-code:
    # pandas.concat([perfect,reference,test,p25coin,p50coin,p75coin], axis=1)

'''
Referenced / Observed Variable : reference_var

             |   perfect  fst_pre~t  scd_pre~t    p25coin    p50coin    p75coin 
-------------+------------------------------------------------------------------
   TestedPos |       487        604        555        247        509        751 
   TestedNeg |       513        396        445        753        491        249 
   TestedTot |      1000       1000       1000       1000       1000       1000 
     TruePos |       487        487        438        117        252        363 
     TrueNeg |       513        396        396        383        256        125 
    FalsePos |         0        117        117        130        257        388 
    FalseNeg |         0          0         49        370        235        124 
 Sensitivity |       100        100      89.94      24.02      51.75      74.54 
 Specificity |       100      77.19      77.19      74.66       49.9      24.37 
  PosPredVal |       100      80.63      78.92      47.37      49.51      48.34 
  NegPredVal |       100        100      88.99      50.86      52.14       50.2 
  FalsePosRt |         0      22.81      22.81      25.34       50.1      75.63 
  FalseNegRt |         0          0      10.06      75.98      48.25      25.46 
   CorrectRt |       100       88.3       83.4         50       50.8       48.8 
 IncorrectRt |         0       11.7       16.6         50       49.2       51.2 
     ROCArea |         1       .886      .8357      .4934      .5082      .4945 
     F1Score |         1      .8928      .8407      .3188       .506      .5864 
 MattCorCoef |         1      .7889      .6752     -.0153      .0165     -.0127 

   Notes: ObservedPos: 487, ObservedNeg: 513, & ObservedTot: 1000, Prevalence: 48.7     

   Keywords, Terminology, & Calculations - Quick References

   Prevalence  = ObservedPos/ObservedTot
   Specificity = TrueNeg/ObservedNeg           Sensitivity = TruePos/ObservedPos
   PosPredVal  = TruePos/(TruePos+FalsePos)    NegPredVal  = TrueNeg/(TrueNeg+FalseNeg)
   FalsePosRt  = FalsePos/ObservedNeg          FalseNegRt  = (FalseNeg/(FalseNeg+TruePos))
   CorrectRt   = (TruePos+TrueNeg)/TestedTot   IncorrectRt = (FalsePos+FalseNeg)/TestedTot

   FalsePos    = Type I Error                  FalseNeg    = Type II Error
   FalsePosRt  = Inverse Specificity           FalseNegRt  = Inverse Sensitivity

- conrpt - Command was a success.

'''