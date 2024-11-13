#%%
import pandas as pd
import numpy as np
from glob import iglob
from tqdm import tqdm
import us
#%%
ncsl_csv_dir = "/mnt/c/Users/michg/Dropbox (MIT)/statelaws/2_data/1_raw/political_data/ncsl_statepartisancomposition/*.csv"
output_file = "/mnt/c/Users/michg/Dropbox (MIT)/statelaws/2_data/2_intermediate/political_data/post2009_statepartisancomposition.dta"
#%%
for i, file in enumerate(iglob(ncsl_csv_dir)):
    partisan_comp_year = pd.read_csv(file)
    year = int(file.split("/")[-1].split(".")[0])
    partisan_comp_year["year"] = year

    if i == 0:
        full_partisan_comp = partisan_comp_year
    else:
        full_partisan_comp = pd.concat([full_partisan_comp, partisan_comp_year], axis=0, ignore_index=True, verify_integrity=False)

#%%
full_partisan_comp["state"] = full_partisan_comp.state.apply(lambda x: us.states.lookup(x).abbr)
#%%
full_partisan_comp = full_partisan_comp.astype({"house_dem": float, "senate_dem": float, "house_rep": float, "senate_rep": float})
full_partisan_comp["dr_lowhse"] = full_partisan_comp["house_dem"] + full_partisan_comp["house_rep"]
full_partisan_comp["dr_upphse"] = full_partisan_comp["senate_dem"] + full_partisan_comp["senate_rep"]
full_partisan_comp["dem_lowhse"] = full_partisan_comp["house_dem"] / full_partisan_comp["dr_lowhse"]
full_partisan_comp["rep_lowhse"] = full_partisan_comp["house_rep"] / full_partisan_comp["dr_lowhse"]
full_partisan_comp["dem_upphse"] = full_partisan_comp["senate_dem"] / full_partisan_comp["dr_upphse"]
full_partisan_comp["rep_upphse"] = full_partisan_comp["senate_rep"] / full_partisan_comp["dr_upphse"]
full_partisan_comp["shr_dem_in_sess"] = full_partisan_comp.apply(lambda row: (row["dem_upphse"] + row["dem_lowhse"])/2, axis=1)
full_partisan_comp["shr_rep_in_sess"] = full_partisan_comp.apply(lambda row: (row["rep_upphse"] + row["rep_lowhse"])/2, axis=1)
# %%
full_partisan_comp[[
    "year",
    "state",
    "dem_upphse",
    "rep_upphse",
    "dem_lowhse",
    "rep_lowhse",
    "shr_dem_in_sess",
    "shr_rep_in_sess"
]].to_stata(output_file)