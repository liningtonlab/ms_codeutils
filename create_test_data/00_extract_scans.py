from pathlib import Path
from typing import Union, List

import pandas as pd
import pymzml

HERE = Path(__file__).parent


def mzml(file_path: Union[str, Path], scan_low, scan_high, min_intensity: int = 600):
    """Import mzML files derived from applying MSConvert to .raw files."""
    headers = ["scanindex", "rettime", "mz", "intensity", "function"]

    # Borrowed and modified from https://github.com/rlinington/ms2analyte/blob/master/ms2analyte/converters/waters.py
    # Waters data includes the lockspray internal calibrant scans as 'MS1' data. These are differentiated from true
    # MS1 data by the 'function' attribute in the spectrum element. Data MS1 scans are function 1. Lockspray scans are
    # assigned the highest possible function number (floating, depends on how many DDA scans were permitted during
    # acquisition setup). Commonly lockspray function=5. This is always 3 for MSe (DIA) data.
    # NOTE: If MS2 functionality is added, this is not an issue, because all MS2 data have ms level = 2, and are
    # therefore all legitimate for inclusion.

    # Parse mzML file and format appropriate scan data as Dataframe
    run = pymzml.run.Reader(str(file_path))
    input_data = []
    for spec in run:
        # Skip over non-MS1 data
        if spec.ms_level != 1:
            continue
        # Skip lockspray or other functions if there are any!
        # If not, this is probably not Waters data and should be fine...
        fn = spec.id_dict.get("function")
        # if fn is not None:
        #     if fn != 1:
        #         continue
        scan_number = spec.ID
        # if scan_number < scan_low:
        #     continue
        # if scan_number > scan_high:
        #     print("End of useful scans")
        #     break
        retention_time = round(spec.scan_time_in_minutes(), 3)
        for peak in spec.peaks("raw"):
            mz = round(peak[0], 4)
            intensity = int(peak[1])
            if intensity < min_intensity:
                continue
            input_data.append([scan_number, retention_time, mz, intensity, fn])

        # Print import progress. Useful because importing large mzML files can be slow.
        if spec.index % 100 == 0 and spec.index > 0:
            print(f"{file_path.name} - Completed import of scan " + str(spec.ID))

    return pd.DataFrame(input_data, columns=headers)

# REPLACE THIS WITH THE PATH OF YOUR MZML FILES
mzml_dir = Path("Z:\Linington\working\isoanalyst_example\generalized\mzmls")

# REPLACE THIS WITH THE PATH OF TEST FEATURES CSV FILES
df = pd.read_csv(HERE / "RLUS1353_test_features.csv")
print(df.head())

scan_low = df.LowScan.min()
scan_high = df.HighScan.max()

for f in mzml_dir.glob("*.mzml"):
    if "BLANK" in f.name:
        continue
    mzdf = mzml(f, scan_low, scan_high, min_intensity=100)
    mzdf.to_csv(HERE / Path(f.stem).with_suffix(".csv"), index=False)