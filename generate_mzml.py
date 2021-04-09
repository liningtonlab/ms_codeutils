from collections import namedtuple

import numpy as np
from psims.mzml.writer import MzMLWriter

Scan = namedtuple("Scan", "id mz_array intensity_array")


fake_array = lambda n: np.linspace(1.0, 50.0, num=n)


def get_scan_data():
    scans = [
        (
            Scan(
                **{
                    "id": "function=1 process=0 scan=1",
                    "mz_array": fake_array(20),
                    "intensity_array": fake_array(20),
                }
            ),
            [],
        ),
        (
            Scan(
                **{
                    "id": "function=5 process=0 scan=2", # fake lock-spray
                    "mz_array": fake_array(5),
                    "intensity_array": fake_array(5),
                }
            ),
            [],
        ),
        (
            Scan(
                **{
                    "id": "function=1 process=0 scan=3",
                    "mz_array": fake_array(40),
                    "intensity_array": fake_array(40),
                }
            ),
            [],
        ),
    ]

    return scans


def main():
    # Load the data to write
    scans = get_scan_data()

    with MzMLWriter(open("out.mzML", "wb"), close=True) as out:
        # Add default controlled vocabularies
        out.controlled_vocabularies()
        # Open the run and spectrum list sections
        i = 0
        with out.run(id="my_analysis"):
            spectrum_count = len(scans) + sum([len(products) for _, products in scans])
            with out.spectrum_list(count=spectrum_count):
                for scan, products in scans:
                    i += 1
                    scan_time = 0.23 * i
                    # Write Precursor scan
                    out.write_spectrum(
                        scan.mz_array,
                        scan.intensity_array,
                        id=scan.id,
                        centroided=True,
                        scan_start_time=scan_time,
                        params=[
                            "MS1 Spectrum",
                            {"ms level": 1},
                            {"total ion current": sum(scan.intensity_array)},
                        ],
                    )
                    # Write MSn scans
                    for prod in products:
                        out.write_spectrum(
                            prod.mz_array,
                            prod.intensity_array,
                            id=prod.id,
                            params=[
                                "MSn Spectrum",
                                {"ms level": 2},
                                {"total ion current": sum(prod.intensity_array)},
                            ],
                            # Include precursor information
                            precursor_information={
                                "mz": prod.precursor_mz,
                                "intensity": prod.precursor_intensity,
                                "charge": prod.precursor_charge,
                                "scan_id": prod.precursor_scan_id,
                                "activation": [
                                    "beam-type collisional dissociation",
                                    {"collision energy": 25},
                                ],
                                "isolation_window": [
                                    prod.precursor_mz - 1,
                                    prod.precursor_mz,
                                    prod.precursor_mz + 1,
                                ],
                            },
                        )


if __name__ == "__main__":
    main()
