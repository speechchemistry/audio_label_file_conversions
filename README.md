# audio_label_file_conversions

Script `saymore_eaf_to_saymore_tsv.py` converts from the standard SayMore EAF (ELAN) file format to the Tab-separated values (TSV) file format. It should be identical to using ELAN to load up the original EAF file and exporting as Tab-delimited Text. This script allows you do the same but with a batch of files. It is mainly just a wrapper around the excellent [pympi](https://github.com/dopefishh/pympi) python module. 

Script `saymore_tsv_to_saymore_eaf.py` converts in the other direction.
