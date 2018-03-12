{smcl}

{title:Title}

{phang}
{bf:conrpt} {hline 2} Stata package that provides confusion matrix statistics.

{marker syntax}
{title:Syntax}

{p 8 17 2}
{cmdab:conrpt} [{it:varlist}] [if] [in] [, options]

{p 8 17 2} Where the first variable in [{it:varlist}] is a binary reference result. Subsequent variables in [{it:varlist}] are predictions. This command compares [{it:varlist}]'s 2nd throgh kth variable with [{it:varlist}]'s first variable and tabulates the results.

{synoptset 16 tabbed}{...}
{synopthdr}
{synoptline}
{syntab:Main}
{synopt:{opt no:print}}Suppress output. Default behavior is to produce table of statistics.{p_end}
{synopt:{opt no:legend}}Suppress output of legend which provides a quick reference.{p_end}
{synopt:{opt ti:tle}}Specify a title to be displayed with the output.{p_end}
{synopt:{opt no:coin}}Suppres production and output of comparison coins. Default behavior is to produce and display results for random coints which can be used for comparison purposes.{p_end}
{synopt:{opt prob:s(numlist)}}Where {it:numlist} is list of integers in the range of 1 through 100. This option modifies the random coins generated for comparison purposes.{p_end}
{synopt:{opt perfect}}Generates a column of statistics for a test that perfectly matches the reference variable. Intended for testing purposes.{p_end}
{synopt:{opt mat:rix}}Provide a name for the matrix.{p_end}

{marker description}
{title:Description}

{pstd}
{cmd:conrpt} Stata package that provides confusion matrix statistics. Example output:

. conrpt var1 var2

Referenced / Observed Variable : var1

             |      var2    p25coin    p50coin    p75coin 
-------------+--------------------------------------------
   TestedPos |        60         26         50         72 
   TestedNeg |        40         74         50         28 
   TestedTot |       100        100        100        100 
     TruePos |        47         11         22         33 
     TrueNeg |        40         38         25         14 
    FalsePos |        13         15         28         39 
    FalseNeg |         0         36         25         14 
 Sensitivity |       100       23.4      46.81      70.21 
 Specificity |     75.47       71.7      47.17      26.42 
  PosPredVal |     78.33      42.31         44      45.83 
  NegPredVal |       100      51.35         50         50 
  FalsePosRt |     24.53       28.3      52.83      73.58 
  FalseNegRt |         0       76.6      53.19      29.79 
   CorrectRt |        87         49         47         47 
 IncorrectRt |        13         51         53         53 
     ROCArea |     .8774      .4755      .4699      .4831 
     F1Score |     .8785      .3014      .4536      .5546 
 MattCorCoef |     .7689     -.0557     -.0601     -.0375 

   Notes: ObservedPos: 47, ObservedNeg: 53, & 
   ObservedTot: 100, Prevalence: 47    
  
{marker example}
{title:Example}

{phang}{cmd:. clear all}{p_end}
{phang}{cmd:. set obs 1000}{p_end}
{phang}{cmd:. gen reference_var = round(runiform(0,1))}{p_end}
{phang}{cmd:. gen fst_predict = reference_var}{p_end}
{phang}{cmd:. replace fst_predict = 1 if _n > 800}{p_end}
{phang}{cmd:. gen scd_predict = reference_var}{p_end}
{phang}{cmd:. replace scd_predict = 1 if _n > 800}{p_end}
{phang}{cmd:. replace scd_predict = 0 if _n < 100}{p_end}

{phang}{cmd:. conrpt reference_var fst_predict scd_predict, perfect}{p_end}

{marker author}
{title:Author}

{phang}     Adam Ross Nelson, JD PhD{p_end}
{phang}     {browse "https://github.com/adamrossnelson"}{p_end}