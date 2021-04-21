from pathlib import Path
import pandas as pd
from psims.mzml.writer import MzMLWriter

HERE = Path(__file__).parent

scan_files = HERE.glob("*seen.csv")


def id_str(scan_index, fn=1):
    return f"function={fn} process=0 scan={scan_index}"


def write_mzml(df, fname):
    with MzMLWriter(open(fname, "wb"), close=True) as out:
        # Add default controlled vocabularies
        out.controlled_vocabularies()

        scount = len(df.scanindex.unique())
        with out.run(id="selected_ions"):
            with out.spectrum_list(count=scount):
                for sidx, g in df.groupby("scanindex"):
                    mz = g["mz"].values
                    intens = g["intensity"].values
                    rt = g.iloc[0]["rettime"]
                    # print(sidx, rt, mz, intens)
                    out.write_spectrum(
                        mz,
                        intens,
                        id=id_str(sidx),
                        centroided=True,
                        scan_start_time=rt,
                        params=[
                            "MS1 Spectrum",
                            {"ms level": 1},
                        ],
                    )


for f in scan_files:
    df = pd.read_csv(f)
    fname = f.with_suffix(".mzml")
    write_mzml(df, fname)