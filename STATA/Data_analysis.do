
*******************************************************
* STATA ANALYSIS SCRIPT
* Dataset: Cleaned Penn World Table 11.0
* Author: Péter Márton
*******************************************************

* 1. Set working directory
cd "C:/Users/User/OneDrive/Dokumentumok/suli/Egyetem/CEU/coding/Assignment"
global cleaned "C:/Users/User/OneDrive/Dokumentumok/suli/Egyetem/CEU/coding/Assignment/data/cleaned"
global graphs  "C:/Users/User/OneDrive/Dokumentumok/suli/Egyetem/CEU/coding/Assignment/graphs"

* 2. Load cleaned data
use "$cleaned/country_data_cleaned.dta", clear

* 3. Summary statistics for year 2023
display "Summary statistics for rgdpo and rgdpe in 2023"
summarize rgdpo rgdpe if year == 2023

* 4. Filter countries of interest
keep if inlist(country, "Hungary", "Austria", "Netherlands")

* 5. Create time series graphs
* --- Step 7: Save cleaned data ---
capture mkdir "$graphs"
cd "$graphs"
* Output per worker over time
twoway (line rgdpo_per_worker year if country == "Hungary", lcolor(blue)) ///
       (line rgdpo_per_worker year if country == "Austria", lcolor(red)) ///
       (line rgdpo_per_worker year if country == "Netherlands", lcolor(green)), ///
       title("Output per Worker Over Time") ///
       legend(label(1 "Hungary") label(2 "Austria") label(3 "Netherlands")) ///
       ytitle("USD") xtitle("Year")

* Save graph
graph export "$graphs/output_per_worker.png", replace

* Expenditure per capita over time
twoway (line rgdpe_per_capita year if country == "Hungary", lcolor(blue)) ///
       (line rgdpe_per_capita year if country == "Austria", lcolor(red)) ///
       (line rgdpe_per_capita year if country == "Netherlands", lcolor(green)), ///
       title("Expenditure per Capita Over Time") ///
       legend(label(1 "Hungary") label(2 "Austria") label(3 "Netherlands")) ///
       ytitle("USD") xtitle("Year")

* Save graph
graph export "$graphs/expenditure_per_capita.png", replace