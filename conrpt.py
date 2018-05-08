# 1.0.0(py) Adam Ross Nelson May2018 ported to Python
# Original author : Adam Ross Nelson
# Description     : Python routine that provides confusion matrix statistics.
# Maintained at   : https://github.com/adamrossnelson/conrpt

def conrpt(rvar, tvar):
    from pandas import DataFrame
    import pandas

    print('Printing rvar')
    print(rvar)

    print('Printing tvar')
    print(tvar)

    # df = DataFrame(rvar, tvar, columns=['rvar','tvar'])
    # df = pandas.merge(rvar, tvar, how='outer')
    df = pandas.concat([rvar.to_frame(), tvar.to_frame()], 
       axis=1, ignore_index=True)
    df.columns = ['rvar','tvar']

    # df = DataFrame(rvar.to_frame(), tvar.to_frame(), columns=['rvar','tvar'])

    print('Printing df')
    print(df)

    df_xtab = pandas.crosstab(df['rvar'], df['tvar'])

    print('printing df_xtab')
    print(df_xtab)

    # print(df['rvar'].isin([1,0]).all())
    # print(df['tvar'].isin([1,0]).all())

    # Test that arguments are binary
    # if not (df['rvar'].isin([1,0]).all()) or not (df['tvar'].isin([1,0]).all()):
    # if ((df['rvar'].isin([1,0]).all() is not True) or (df['tvar'].isin([1,0]).all() is not True)):
    if 10 == 11:
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
    