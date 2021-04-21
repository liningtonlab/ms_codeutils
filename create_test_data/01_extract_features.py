from pathlib import Path
import pandas as pd

HERE = Path(__file__).parent
RTTOL = 0.06
MZTOL = 20

df = pd.read_csv(HERE / "RLUS1353_test_features.csv")
print(df.head())

scan_files = HERE.glob("201804*.csv")

for f in scan_files:
    sdf = pd.read_csv(f)
    keep = set()
    for _, row in df.iterrows():
        print(row)
        idxs = sdf[
            sdf.rettime.between(row.RetTime - RTTOL, row.RetTime + RTTOL)
            & sdf.mz.between(row.PrecMz - MZTOL, row.PrecMz + MZTOL)
        ].index
        # print(len(idxs))
        keep.update(set(idxs))
    sdf1 = sdf.loc[idxs]
    print(sdf.shape)
    print(sdf1.shape)
    sdf1.to_csv(HERE / f"{f.stem}_seen.csv")