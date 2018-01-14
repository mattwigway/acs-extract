# ACS Extractor

This extracts variables from the [American Community Survey Summary Files](https://census.gov/programs-surveys/acs/data/summary-file.html). It is currently hardwired to extract 2016 5-year estimates for California, but will eventually be modified to handle data from all years and states.

To use it, you need to download and unzip the summary file from [here](https://census.gov/programs-surveys/acs/data/summary-file.html). You can then invoke the program like so:

    acs_extract.py [--tracts|--blockgroups] --readme readme.txt path/to/unzipped/extract VARIABLE [VARIABLE ...] out.csv

The options are largely self explanatory. The `--tracts` and `--blockgroups` options specify which geography to extract, and the `--readme` option specifies where to write a README giving explanations for the fields in the CSV output. You then pass in the path to the unzipped extract, the variables you want to extract, and the output CSV.

The variables are specified as `[table number]_[variable number]`, based on the lookup tables for the ACS (which ship with acs_extract). The table numbers can be more easily found through the search function of [American FactFinder](http://factfinder.census.gov). The variable numbers do not necessarily correspond to the variable numbers in American FactFinder, however.

You can specify a single variable as `[table_number]_[variable number]`, for instance the number of people with asked rent between $900 and $999 could be specified as `B25061_18`. It is also possible to specify a range, for example `B25061_2-18` for all the variables for rent between $0 and $999. Finally, it is possible to retrieve all variables from a table by specifying a variable number `*`, e.g. `B25061_*`.

The output CSV will contain a `geoid` (geographic ID) column, which is the FIPS tract or block group ID (which is itself the concatenation of the state, county, tract, and block group FIPS codes). This can be used to join with [TIGER/Line](https://www.census.gov/geo/maps-data/data/tiger-line.html) geographic data files.
