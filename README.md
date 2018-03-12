# conrpt
Stata package that provides confusion matrix statistics.

## Introduction

This package was inspired by discussions on statalist.org. See for example:

[https://www.statalist.org/for...classtabi-now-available-for-download-from-ssc](https://www.statalist.org/forums/forum/general-stata-discussion/general/1321572-a-new-command-classtabi-now-available-for-download-from-ssc)

## Installation

```
net install conrpt, from(https://raw.githubusercontent.com/adamrossnelson/conrpt/master)
```

## Example & Test Script

To run a version from Stata's command line:
```
do https://raw.githubusercontent.com/adamrossnelson/conrpt/master/conrpttester.do
```

```
// Script to test conrpt.ado
// More information: https://github.com/adamrossnelson/conrpt

// First test, no options
clear all
set obs 100
gen var1 = round(runiform(0,1))
gen var2 = var1
replace var2 = 1 if _n > 80
conrpt var1 var2

// Second test, test options
clear all
set obs 1000
gen reference_var = round(runiform(0,1))
gen fst_predict = reference_var
replace fst_predict = 1 if _n > 800
gen scd_predict = reference_var
replace scd_predict = 1 if _n > 800
replace scd_predict = 0 if _n < 100

conrpt reference_var fst_predict scd_predict, noprint
conrpt reference_var fst_predict scd_predict, nocoin
conrpt reference_var fst_predict scd_predict, perfect nocoin
conrpt reference_var fst_predict scd_predict, perfect probs(10 20 80 90)
```

