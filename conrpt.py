# 1.0.0(py) Adam Ross Nelson May2018 ported to Python
# Original author : Adam Ross Nelson
# Description     : Python routine that provides confusion matrix statistics.
# Maintained at   : https://github.com/adamrossnelson/conrpt

def conrpt(rvar, tvar):
    from pandas import DataFrame
    import pandas

    df = pandas.concat([rvar.to_frame(), tvar.to_frame()], 
       axis=1, ignore_index=True)
    df.columns = ['rvar','tvar']

    df_xtab = pandas.crosstab(df['rvar'], df['tvar'])

    # Test that arguments are binary
    if not (df['rvar'].isin([1,0]).all()) or not (df['tvar'].isin([1,0]).all()):    
        raise ValueError('Variables must be binary.')

    # Count true positive results
    TruePos = df_xtab.ix[1][1]
    # Count true negative results
    TrueNeg = df_xtab.ix[0][0]
    # Count false positive
    FalsePos = df_xtab.ix[1][0]
    # Count false negative
    FalseNeg = df_xtab.ix[0][1]

    print(TruePos)
    print(TrueNeg)
    print(FalsePos)
    print(FalseNeg)
    