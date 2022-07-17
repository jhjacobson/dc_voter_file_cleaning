# dc_voter_file_cleaning
This helps ANCs find registered voters in their new district if they have the whole voter file and the boundaries of their ANC.

Steps:
1) Download this repo and add the voter file to "voter-list.xlsx".
2) Use get_addresses_from_df(<dataframe>,<min_street_number>,<max_street_number,<street_name_lowercase>,<street_type>,<city_quadrant>,<odd_even_both>). There are examples in process.py for my ANC.
3) Run the process and grab the file from "anc_voters.csv"