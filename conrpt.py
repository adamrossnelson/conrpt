# 1.0.0(py) Adam Ross Nelson May2018 ported to Python
# Original author : Adam Ross Nelson
# Description     : Python routine that provides confusion matrix statistics.
# Maintained at   : https://github.com/adamrossnelson/conrpt

# Pass into this function :
#      First argument, a series that represents observed references.
#      Second argument, a list of series that represents one or more test results.
def conrpt(df):
    from pandas import DataFrame
    import pandas
    import math

    for df_col in df.columns:
        if not (df[df_col].isin([1,0]).all):
            raise ValueError('Vriables must be binary')
    
    grand_list = [['TestedPos', 'TestedNeg', 'TestedTot',
                'TruePos', 'TrueNeg', 'FalesPos', 'FalseNeg',
                'Sensitivity', 'Specificity',
                'PosPredVal', 'NegPredVal',
                'FalsePosRt', 'FalseNegRt',
                'CorrectRt', 'IncorrectRt',
                'ROCArea', 'F1Score', 'MattCorCoef']]
    for df_col in df.columns:
        grand_list.append(return_column(df[df.columns[0]], df[df_col]))
    
    grand_columns = ['Results']
    for item in df.columns:
        grand_columns.append(item)

    grand_frame = pandas.DataFrame(grand_list)
    grand_frame = grand_frame.transpose()
    grand_frame.columns = grand_columns
    return grand_frame

def return_column(rvar, tvar):
    from pandas import DataFrame
    import pandas
    import math

    df = pandas.concat([rvar.to_frame(), tvar.to_frame()], 
       axis=1, ignore_index=True)
    df.columns = ['rvar','tvar']
    df_xtab = pandas.crosstab(df['rvar'], df['tvar'])

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
    ROCArea = 0
    # Calculate f1 Score
    F1Score = (2 * TruePos / (2 * TruePos + FalsePos + FalseNeg))
    # Calculate Matthes corr coefficient
    MattCorCoef = (((TruePos * TrueNeg) - (FalsePos * FalseNeg)) / 
        math.sqrt((TruePos + FalsePos) * (TruePos + FalseNeg) * 
        (TrueNeg + FalsePos) * (TrueNeg + FalseNeg)))
    
    column = [int(TestedPos), int(TestedNeg), int(TestedTot), 
              int(TruePos), int(TrueNeg), int(FalsePos), int(FalseNeg), 
              Sensitivity, Specitivity, PosPredVal, NegPredVal, 
              FalsePosRt, FalseNegRt,CorrectRt, IncorrectRt, 
              ROCArea, F1Score, MattCorCoef]
    return(column)
