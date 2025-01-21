import subprocess

# Python scripts to process political data
notebooks = [
    "Cleaning_icpsr16_partisan_composition.ipynb",
    "cleaning_govData.ipynb",
    "merging_Klarner_and_ICPSR.ipynb",
    "cleanWikiFedData.ipynb",
    "partisanStateFedDataMerge.ipynb"
]

# Execute each notebook sequentially
for notebook in notebooks:
    print(f"Running {notebook}...")
    subprocess.run(
        ["jupyter", "nbconvert", "--to", "notebook", "--execute", "--inplace", notebook],
        check=True
    )
    print(f"Finished {notebook}.\n")

print("All notebooks executed successfully!")
