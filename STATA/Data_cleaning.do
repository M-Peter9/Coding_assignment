*******************************************************
* STATA DATA CLEANING SCRIPT
* Dataset: Penn World Table 11.0
* Author: [Péter Márton]
*******************************************************

* 1. Set working directory
cd "C:/Users/User/OneDrive/Dokumentumok/suli/Egyetem/CEU/coding/Assignment"
* Define absolute paths for your subfolders
global raw     "C:/Users/User/OneDrive/Dokumentumok/suli/Egyetem/CEU/coding/Assignment/data/raw"
global cleaned "C:/Users/User/OneDrive/Dokumentumok/suli/Egyetem/CEU/coding/Assignment/data/cleaned"


* 2. Import CSV data
cd "$raw"
import delimited "pwt110.csv", clear


* 3. Inspect the data
describe
summarize
list in 1/5


* 4. Fix data types
* Convert Expenditure-side real GDP at chained PPPs (in mil. 2021US$), Output-side real GDP at chained PPPs (in mil. 2021US$), Population (in millions), Number of persons engaged (in millions), Average annual hours worked by persons engaged, and year to numeric if stored as strings
destring rgdpe rgdpo pop emp avh year, replace ignore(",")

* 5. Handle missing values
drop if missing(rgdpe)
drop if missing(rgdpo)
drop if missing(pop)
drop if missing(emp)
drop if missing(avh)
drop if missing(year)

* 6a. Filter observations
* Keep only data after year 2000
keep if year >= 2000

count if pop == 0
count if emp == 0
* 6b. Filter variables
* Keep only relevant columns
keep country year rgdpe rgdpo pop emp avh

* 6c. Create transformed variables
gen log_rgdpe = log(rgdpe)
gen rgdpe_real = rgdpe * 1000000
gen log_rgdpo = log(rgdpo)
gen rgdpo_real = rgdpo * 1000000
gen rgdpe_per_capita = rgdpe / pop
gen rgdpo_per_worker = rgdpo / emp


drop if missing(rgdpe_per_capita)
drop if missing(rgdpo_per_worker)

* --- Step 6d: Label variables ---
label var rgdpe "Expenditure-side real GDP (in millions 2021 USD)"
label var rgdpo "Output-side real GDP (in millions 2021 USD)"
label var pop "Population (millions)"
label var emp "Persons engaged (millions)"
label var avh "Average annual hours worked"
label var rgdpe_real "Expenditure-side real GDP (in USD)"
label var rgdpo_real "Output-side real GDP (in USD)"
label var log_rgdpe "Log of Expenditure-side real GDP"
label var log_rgdpo "Log of Output-side real GDP"
label var rgdpe_per_capita "Expenditure-side GDP per capita (USD)"
label var rgdpo_per_worker "Output-side GDP per worker (USD)"



* --- Step 7: Save cleaned data ---
capture mkdir "$cleaned"
cd "$cleaned"
save "country_data_cleaned.dta", replace
