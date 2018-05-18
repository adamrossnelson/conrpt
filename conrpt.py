# 1.0.0(py) Adam Ross Nelson May2018 ported to Python
# Original author : Adam Ross Nelson
# Description     : Python routine that provides confusion matrix statistics.
# Maintained at   : https://github.com/adamrossnelson/conrpt

# Pass into this function :
#      First argument, a series that represents observed references.
#      Second argument, a list of series that represents one or more test results.
def conrpt(df, coins=[25,50,75]):
    from pandas import DataFrame
    import pandas
    import numpy
    import math
    
    numpy.random.seed(seed=1)
    
    if len(df) < 100:
        print('Warning: When there are less than 100 observations, random coins may be unreliable')
    
    # Count number of observed positive
    ObservedPos = sum(df[df.columns[0]])
    # Count number of observed negative
    ObservedNeg = len(df[df.columns[0]]) - sum(df[df.columns[0]])
    # Count number of total observations
    ObservedTot = len(df[df.columns[0]])
    # Calculate prevelance
    ObservedPrev = format((ObservedPos / ObservedTot) * 100, '.3f')
    print('{}Notes: ObservedPos: {}, ObservedNeg: {}, & ObservedTot: {}, Prevalence: {}'.format(
        '\n', ObservedPos, ObservedNeg, ObservedTot, ObservedPrev))
    
    for df_col in df.columns:
        if not (df[df_col].isin([1,0]).all):
            raise ValueError('Vriables must be binary')

    # df['50_coin'] = numpy.random.normal(.5, .00005, size=len(df))
    # df['50_coin'] = round(df['50_coin'])
            
    df['srtr'] = numpy.random.randint(1, 101, size=len(df))
    for coin in coins:
        new_col_name = str(coin) + 'coin'
        df[new_col_name] = numpy.where(df['srtr'] < coin, 1, 0)
    del df['srtr']
        
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
    grand_columns[1] = 'Perfect'

    grand_frame = pandas.DataFrame(grand_list)
    grand_frame = grand_frame.transpose()
    grand_frame.columns = grand_columns
    
    for coin in coins:
        new_col_name = str(coin) + 'coin'
        del df[new_col_name]
    
    return grand_frame

def return_column(rvar, tvar):
    from sklearn.metrics import roc_auc_score
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
    ObservedTot = len(rvar)
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
    Sensitivity = format(TruePos / ObservedPos, '.3f')
    # Calculate specitivity
    Specitivity = format(TrueNeg / ObservedNeg, '.3f')
    # Calculate positive predictive value
    PosPredVal = format(TruePos / (TruePos + FalsePos), '.3f')
    # Calculate negative predictive value
    NegPredVal = format(TrueNeg / (TrueNeg + FalseNeg), '.3f')
    # Calculate false positive rate
    FalsePosRt = format(FalsePos / ObservedNeg, '.3f')
    # Calculate false negative rate
    FalseNegRt = format(FalseNeg / (FalseNeg + TruePos), '.3f')
    # Calculate correct rate
    CorrectRt = format((TruePos + TrueNeg) / TestedTot, '.3f')
    # Calculate incorrect rate
    IncorrectRt = format((FalsePos + FalseNeg) / TestedTot, '.3f')
    # Calculate ROC area
    ROCArea = format(roc_auc_score(rvar, tvar), '.3f')
    # Calculate f1 Score
    F1Score = format((2 * TruePos / (2 * TruePos + FalsePos + FalseNeg)), '.3f')
    # Calculate Matthes corr coefficient
    MattCorCoef = format((((TruePos * TrueNeg) - (FalsePos * FalseNeg)) / 
        math.sqrt((TruePos + FalsePos) * (TruePos + FalseNeg) * 
        (TrueNeg + FalsePos) * (TrueNeg + FalseNeg))), '.3f')
    
    column = [int(TestedPos), int(TestedNeg), int(TestedTot), 
              int(TruePos), int(TrueNeg), int(FalsePos), int(FalseNeg), 
              Sensitivity, Specitivity, PosPredVal, NegPredVal, 
              FalsePosRt, FalseNegRt,CorrectRt, IncorrectRt, 
              ROCArea, F1Score, MattCorCoef]
    return(column)

def display_keywords():
    keywords = '''
    Keywords, Terminology, & Calculations - Quick References

    Prevalence  = ObservedPos/ObservedTot
    Specificity = TrueNeg/ObservedNeg           Sensitivity = TruePos/ObservedPos
    PosPredVal  = TruePos/(TruePos+FalsePos)    NegPredVal  = TrueNeg/(TrueNeg+FalseNeg)
    FalsePosRt  = FalsePos/ObservedNeg          FalseNegRt  = FalseNeg/(FalseNeg+TruePos)
    CorrectRt   = (TruePos+TrueNeg)/TestedTot   IncorrectRt = (FalsePos+FalseNeg)/TestedTot

    FalsePos    = Type I Error                  FalseNeg    = Type II Error
    FalsePosRt  = Inverse Specificity           FalseNegRt  = Inverse Sensitivity'''
    print(keywords)

