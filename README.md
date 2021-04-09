# ms_codeutils
A collection of scripts for Python driven MS

### Useful libraries

- [pymzml](https://github.com/pymzml/pymzML) - Read mzML files 📖 
- [psims](https://github.com/mobiusklein/psims) - Write mzML files 📝

Both these libraries are only available from PyPi.
i.e. Install them with `pip`

You should also be able to install them straight from GitHub using pip if you need an updated version not in PyPi:

```bash
pip install git+https://github.com/pymzml/pymzML.git
```

This should be equivalent to downloading the git repo and running `python setup.py install`.

### Scripts

- `generate_mzml.py` - useful example for how to generate a fake mzML file, can be adopted for testing 🧪
- `mzml_to_csv.py` - example for reading mzML file into pandas DataFrame while skipping lock-mass scans 🔐

Outputs for these two scripts are located in the `samples` directory.