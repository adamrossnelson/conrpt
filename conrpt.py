# 1.0.0(py) Adam Ross Nelson May2018 ported to Python
# Original author : Adam Ross Nelson
# Description     : Python routine that provides confusion matrix statistics.
# Maintained at   : https://github.com/adamrossnelson/conrpt

def conrpt(rvar, tvar):
    from pandas import DataFrame

    df = DataFrame(rvar, tvar, columns=['rvar','tvar'])

    # print(df['rvar'].isin([1,0]).all())
    # print(df['tvar'].isin([1,0]).all())

    # Test that arguments are binary
    if not (df['rvar'].isin([1,0]).all() or not df['tvar'].isin([1,0]).all()):
        raise ValueError('Variables must be binary.')

    # Count true positive results
    TruePos = df[(df['rvar']==1) & (df['tvar']==1)].count()
    # Count true negative results
    TrueNeg = df[(df['rvar']==0) & (df['tvar']==0)].count()
    # Count false positive
    FalsePos = df[(df['rvar']==0) & (df['tvar']==1)].count()
    # Count false negative
    FalseNeg = df[(df['rvar']==1) & (df['tvar']==0)].count()

    print(TruePos)
    print(TrueNeg)
    print(FalsePos)
    print(FalseNeg)
    