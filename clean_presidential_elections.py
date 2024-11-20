######################################
# Script: clean_presidential_elections.py
# Author: Michel Gutmann
# Purpose: Uses David Leip's dataset to generate a state-election year dataset with presidential election results by party.
######################################



##### REQUIRED IMPORTS #####
import pandas as pd
import argparse
import us


##### READ ARGUMENTS #####
if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(
        description="Uses David Leip's dataset to generate a state-election year dataset with presidential election results by party."
    )

    arg_parser.add_argument(
        '-d',
        '--data',
        action='store',
        nargs="?", 
        default="data/1_raw/political_data/StateLevelData.xlsx",
        type=str,
        help='The path of the David Leip state level election results excel file (default: data/1_raw/political_data/StateLevelData.xlsx)'
        )

    arg_parser.add_argument(
        '-o',
        '--output',
        action='store',
        nargs="?", 
        default="data/2_intermediate/political_data/statelevel_preselection_results.csv",
        type=str,
        help='The path where to output the produced dataset (default: data/2_intermediate/political_data/statelevel_preselection_results.csv)'
        )
    
    args= arg_parser.parse_args()



##### DEFINE MAIN CLEANING FUNCTION #####
def clean_election(df):
    # Standardize format by keeping only raw result columns
    i = 0
    cols_to_keep = ["Unnamed: 0"]
    for col in df.columns:
        if i == 1:
            cols_to_keep.append(col)
        elif col == "% Total Vote":
            i = 1
    cols_to_keep = cols_to_keep[:-2]
    df_filtered = df[cols_to_keep].copy()
    df_filtered.rename({"Unnamed: 0": "state"}, axis=1, inplace=True)

    # Rename columns to appropriate names
    col_names = ["state"]
    for col in df_filtered.columns:
        col_str = str(col)
        if col_str != "state" and not col_str.startswith("Unnamed: "):
            last_name = "".join(col_str.lower().split(" "))
            if last_name not in ["democratic", "republican"]:
                last_name = "thirdparties"
            elif last_name == "democratic":
                last_name = "dem"
            elif last_name == "republican":
                last_name = "rep"
            col_names.append("votes_" + last_name)
        elif col_str != "state":
            col_names.append("pct_" + last_name)
    df_filtered.columns = col_names
    
    # Sum over third party results
    cleaned_df = df_filtered.groupby(df_filtered.columns, axis=1).sum()
    return cleaned_df



##### LOAD DATA AND PUT IN FULL DATASET #####
if __name__ == "__main__":

    dfs = pd.read_excel(args.data, header=1, sheet_name=None)

    i = 0
    for key in dfs.keys():
        if key != "Copyright" and i == 0:
            new_df = clean_election(dfs[key])
            new_df["year"] = int(key)
            full_df = new_df
            i += 1
        elif key != "Copyright":
            new_df = clean_election(dfs[key])
            new_df["year"] = int(key)
            full_df = pd.concat([full_df, new_df], verify_integrity=True, axis=0, ignore_index=True)



##### PREPARE AND OUTPUT FULL DATASET #####
if __name__ == "__main__":

    full_df["state"] = full_df["state"].apply(lambda x: str(x)[:-1] if str(x).endswith("*") else str(x)) # Remove asterisks from state names
    full_df = full_df.loc[
        full_df["state"].isin([state.name for state in us.STATES])
    ].copy() # Only keep rows that contain states

    state_map = us.states.mapping("name", "fips")
    full_df["statefips"] = full_df["state"].apply(lambda x: state_map[x]) # Add state FIPS codes

    full_df.to_csv(args.output, index=False)