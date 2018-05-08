*! 1.0.2 Adam Ross Nelson April2018 // Added pdx option
*! 1.0.0 Adam Ross Nelson March2018 // Original version
*! Original author : Adam Ross Nelson
*! Description     : Stata package that provides confusion matrix statistics.
*! Maintained at   : https://github.com/adamrossnelson/conrpt

capture program drop conrpt
program define conrpt, rclass byable(recall)
	// Version control
	version 15
	preserve
	
	// Syntax statement limits first argument to variable name which 
	// must be binary. Subsequent vars in varlist must be binary.
	syntax varlist(min=2 numeric) [if] [in] ///
	[,noPRINT noCOIN noLEGEND perfect ///
	title(string) PROBs(string asis) ///
	MATrix(string) PDX]
	
	local spp char(10)
	local sp char(13) char(10)      // Define double spacer.
	local sl char(13)               // Define line return.
	
	// Test number of arguments. Must be at least two.
	local nvar : word count `varlist'
	if `nvar' < 2 {
		di as error "ERROR: Too few arguments specified."
		error 102
	}
	// Test that arguments are binary.
	foreach v of varlist `varlist' {
		capture assert `v' == 1 | `v' == 0
		if _rc {
			di as error "ERROR: Variable `v' not binary. Values must be 0 or 1."
			error 452
		}
	}
	// Test that coin and probs not both specified.
	if "`coin'" == "nocoin" & "`probs'" != ""{
		di as error "ERROR: Nocoin option may not be combined with probs option."
		error 198
	}
	// If pdx option given, test if there is an active putdocx.
	if "`pdx'" == "pdx" {
		capture putdocx describe
		if _rc {
			di in smcl as error "ERROR: No active docx, pdx option must be in the"
			di in smcl as error "       context of an active putdocx."
			exit = 119
		}
	}

	// Tag subsample with temp var touse & test if empty.
	marksample touse
	quietly count if `touse'
	if `r(N)' == 0 {
		di as error "ERROR: No observations after if or in qualifier."
		error 2000
	}
	// Test that sample large enough for coins.
	if `r(N)' < 99 {
		di as result "WARNING: Coin option less reliable when sample size is low."
		di as result "         Current sample size is `r(N)'."
	}

	// Build Matricies
	local varlist2 = substr("`varlist'",strpos("`varlist'"," "),strlen("`varlist'") - strpos("`thelist'"," "))
	local varlist3 = "`varlist2'"
	if "`coin'" != "nocoin" {
		set seed 1000
		gen _srtr = runiform(1,100)
		local totcoins = 0
		if "`probs'" == "" {
			local probs 25 50 75
		}
		foreach prob in `probs' {
			qui {
				gen p`prob'coin = 0
				replace p`prob'coin = 1 if _srtr < `prob'
				local varlist3 = "`varlist3' p`prob'coin"
				local ++totcoins
			}
		}
	}
	if "`perfect'" == "perfect" {
		qui {
			gen perfect = `1' if `touse'
			local varlist3 = "perfect `varlist3'"
			local nvar = `nvar' + 1
		}
	}
	tempname rmat
	matrix `rmat' = J(18, `nvar' + `totcoins' - 1,.)
	local i = 1
	foreach v of varlist `varlist3' {
		qui {
			
			// ObservedPos   (number of) positive samples (P)
			count if `1' == 1 & `touse'		
			local ObservedPos = r(N)
			// ObservedNeg   (number of) negative samples (N)
			count if `1' == 0 & `touse'
			local ObservedNeg = r(N)
			// ObservedTot
			local ObservedTot = `ObservedPos' + `ObservedNeg'
			// Prevalence                                       // (ObservedPos/ObservedTot)
			local Prevalence : di %-9.6g (`ObservedPos' / `ObservedTot')                * 100

			// TestedPos
			count if `v' == 1 & `touse'
			matrix `rmat'[1,`i'] = r(N)
			local TestedPos = r(N)
			// TestedNeg
			count if `v' == 0 & `touse'
			matrix `rmat'[2,`i'] = r(N)
			local TestedNeg = r(N)
			// TestedTot
			local TestedTot = `TestedPos' + `TestedNeg'
			matrix `rmat'[3,`i'] = `TestedTot'

			// TruePos        // (TP) eqv. with hit
			count if `v' == 1 & `1' == 1 & `touse'
			matrix `rmat'[4,`i'] = r(N)
			local TruePos = r(N)
			// TrueNeg        // (TN) eqv. with correct rejection
			count if `v' == 0 & `1' == 0 & `touse'
			matrix `rmat'[5,`i'] = r(N)
			local TrueNeg = r(N)
			// FalsePos       // (FP) eqv. with false alarm, Type I error
			count if `v' == 1 & `1' == 0 & `touse'
			matrix `rmat'[6,`i'] = r(N)
			local FalsePos = r(N)
			// FalseNeg      // (FN) eqv. with miss, Type II error
			count if `v' == 0 & `1' == 1 & `touse'
			matrix `rmat'[7,`i'] = r(N)
			local FalseNeg = r(N)
			
			// Sensitivity aka true positive rate (TPR)         // (TruePos/ObservedPos)
			local Sensitivity : di %-6.2f (`TruePos' / `ObservedPos')              * 100
			matrix `rmat'[8,`i'] = `Sensitivity'
			// Specificity aka true negative rate (TNR)         // (TrueNeg/ObservedNeg)
			local Specificity : di %-6.2f (`TrueNeg' / `ObservedNeg')              * 100
			matrix `rmat'[9,`i'] = `Specificity'

			// PosPredVal aka precision                         // (TruePos/(TruePos+FalsePos))
			local PosPredVal : di %-6.2f (`TruePos' / (`TruePos' + `FalsePos'))    * 100
			matrix `rmat'[10,`i'] = `PosPredVal'
			// NegPredVal aka ...                               // (TrueNeg/(TrueNeg+FalseNeg))
			local NegPredVal : di %-6.2f (`TrueNeg' / (`TrueNeg' + `FalseNeg'))    * 100
			matrix `rmat'[11,`i'] = `NegPredVal'
			// FalsePosRt aka Inverse Specificity or fall-out   // (FalsePos/ObservedNeg)
			local FalsePosRt : di %-6.2f (`FalsePos' / `ObservedNeg')              * 100
			matrix `rmat'[12,`i'] = `FalsePosRt'
			// FalseNegRt aka Inverse Sensitivity               // (FalseNeg/(FalseNeg+TruePos))
			local FalseNegRt : di %-8.2f (`FalseNeg' / `ObservedPos')              * 100
			matrix `rmat'[13,`i'] = `FalseNegRt'

			// CorrectRt aka Accuracy                           // (TruePos+TrueNeg)/TestedTot
			local CorrectRt : di %-6.2f (`TruePos' + `TrueNeg') / `TestedTot'      * 100
			matrix `rmat'[14,`i'] = `CorrectRt'
			// IncorrectRt                                      // (FalsePos+FalseNeg)/TestedTot
			local IncorrectRt : di %-6.2f (`FalsePos' + `FalseNeg') / `TestedTot'  * 100
			matrix `rmat'[15,`i'] = `IncorrectRt'
			
			// ROCArea
			roctab `1' `v'
			local rocarea r(area)
			local rocarea : di %-6.4f `rocarea'
			matrix `rmat'[16,`i'] = `rocarea'
			
			// F1 Score aka harmonic mean of precision and sensitivity
			// 2TruePos / (2TruePos + FalsePos + FalseNeg)
			local F1Score : di %-6.4f (2 * `TruePos' / (2 * `TruePos' + `FalsePos' + `FalseNeg'))
			matrix `rmat'[17,`i'] = `F1Score'

			// Matthews correlation coefficient (MattCorCoef)
			local MattCorCoef : di %-6.4f  ///
			((`TruePos' * `TrueNeg') - (`FalsePos' * `FalseNeg')) / ///
			sqrt( (`TruePos' + `FalsePos') * ///
			      (`TruePos' + `FalseNeg') * ///
				  (`TrueNeg' + `FalsePos') * ///
				  (`TrueNeg' + `FalseNeg') )
			matrix `rmat'[18,`i'] = `MattCorCoef'
			// For reference: https://en.wikipedia.org/wiki/Sensitivity_and_specificity
		}
		local ++i
	}

	matrix colnames `rmat' = `varlist3'
	matrix rownames `rmat' = TestedPos TestedNeg TestedTot ///
	TruePos TrueNeg FalsePos FalseNeg ///
	Sensitivity Specificity PosPredVal NegPredVal ///
	FalsePosRt FalseNegRt CorrectRt IncorrectRt ROCArea F1Score MattCorCoef
	if "`print'" != "noprint" {
		if "`title'" == "" {
			di ""
			di in smcl in gr "{ul:Referenced / Observed Variable : `1'}"
		}
		else {
			di ""
			di in smcl in gr "{ul:`title'}"
		}
		matlist `rmat'
		di ""

		// Define the notes line as a local for later display to screen and/or to putdocx.
		if strlen("`varlist3'") * 2 > 81 {
			local observed_results "   Notes: ObservedPos: `ObservedPos', ObservedNeg: `ObservedNeg', & ObservedTot: `ObservedTot', Prevalence: `Prevalence'`spp'" ///
			""
		}
		else if strlen("`varlist3'") * 2 < 82 & strlen("`varlist3'") * 2 > 34 {
			local observed_results "   Notes: ObservedPos: `ObservedPos', ObservedNeg: `ObservedNeg', & `spp'" ///
			"   ObservedTot: `ObservedTot', Prevalence: `Prevalence'`spp'" ///
			""
		}
		else if strlen("`varlist3'") * 2 < 35 {
			local observed_results "   Notes: ObservedPos: `ObservedPos',`spp'" ///
			"   ObservedNeg: `ObservedNeg', & `spp'" ///
			"   ObservedTot: `ObservedTot',`spp'" ///
			"   Prevalence: `Prevalence'`spp'" ///
			""
		}

		// Print the observed results
		foreach line in "`observed_results'" {
			di as result subinstr("`line'","`spp'","",.)
		}

		// Build legend text.
		local legtext "   Prevalence  = ObservedPos/ObservedTot`spp'" ///
		"   Specificity = TrueNeg/ObservedNeg           Sensitivity = TruePos/ObservedPos`spp'" ///
		"   PosPredVal  = TruePos/(TruePos+FalsePos)    NegPredVal  = TrueNeg/(TrueNeg+FalseNeg)`spp'" ///
		"   FalsePosRt  = FalsePos/ObservedNeg          FalseNegRt  = (FalseNeg/(FalseNeg+TruePos))`spp'" ///
		"   CorrectRt   = (TruePos+TrueNeg)/TestedTot   IncorrectRt = (FalsePos+FalseNeg)/TestedTot`spp'" ///
		"`spp'" ///
		"   FalsePos    = Type I Error                  FalseNeg    = Type II Error`spp'" ///
		"   FalsePosRt  = Inverse Specificity           FalseNegRt  = Inverse Sensitivity`spp'" ///
		""
		
		local legtext_sc_header = "   {ul:Keywords, Terminology, & Calculations - Quick References}"
		scalar legtext_fl_header = "Keywords, Terminology, & Calculations - Quick References"
		
		if "`legend'" != "nolegend" {
			di as text "`legtext_sc_header'" `spp'
			foreach line in "`legtext'" {
				di subinstr("`line'","`spp'","",.)
			}
		}
	}
	
	// If matrix option not specified let the matrix name be rmat.
	if "`matrix'" != "" {
		matrix `matrix' = `rmat'
	}
	
	if "`pdx'" == "pdx" {
		putdocx table tablename = matrix(`rmat'), nformat(%6.5g) rownames colnames
		putdocx paragraph, font(Consolas, 8)
		foreach line in "`observed_results'" {
			putdocx text (subinstr(subinstr("`line'","`spp'","",.),"   ","",.)), linebreak
		}
		if "`legend'" != "nolegend" {
			// putdocx paragraph, font(Consolas, 8)
			putdocx text ("`=legtext_fl_header'"), linebreak underline
			foreach line in "`legtext'" {
				putdocx text (subinstr("`line'","`spp'","",.)), linebreak
			}
		}
	}
	
	return matrix rmat = `rmat'              // Return matrix
	return local varnames `varlist'          // Return full varlist
	return local testnames `varlist2'        // Return test variables
	return local obsvar `1'                  // Return observed variable
	restore

	di as result "{it:- conrpt - }Command was a success."
end

