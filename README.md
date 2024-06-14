# audio_label_file_conversions

Script `saymore_eaf_to_saymore_tsv.py` converts from the standard SayMore EAF (ELAN) file format to the Tab-separated values (TSV) file format. It should be identical to using ELAN to load up the original EAF file and exporting as Tab-delimited Text. This script allows you do the same but with a batch of files. It is mainly just a wrapper around the excellent [pympi](https://github.com/dopefishh/pympi) python module. 

Script `saymore_tsv_to_saymore_eaf.py` converts in the other direction.

## Requirements

You need Python version 3 and the following python modules:

- pympi
- pandas (for `saymore_tsv_to_saymore_eaf.py` only)

## Installation

You can either clone this repository or just select the script you want and download the raw code (e.g. in the Chrome browser on Windows right click on the "Raw" github button, and click "Save link as..."). To use the script anywhere in your file directory you may need to add the script's location to your PATH environmental variable. 

## Examples

```
# A simple conversion from SayMore EAF to TSV
python3 saymore_eaf_to_saymore_tsv.py ZOOM0030_319-321.WAV.annotations.eaf > ZOOM0030_319-321.WAV.annotations.tsv

# A simple conversion from SayMore EAF to CSV in Linux (requires csvkit)
python3 saymore_eaf_to_saymore_tsv.py ZOOM0030_319-321.WAV.annotations.eaf | csvformat --tabs > ZOOM0030_319-321.WAV.annotations.csv

# Assuming you have the script in your path, and that you are using the bash shell e.g. in Ubuntu
# the following converts a batch of SayMore EAF files to TSV files
for file in *.annotations.eaf; do saymore_eaf_to_saymore_tsv.py "$file" > "${file%.eaf}.tsv"; done  
```

## Usage
Note that the media file is not explicitly defined when using this script. When SayMore starts it will attempt to repair any EAF files associated with media so that the media filename is explicitly added to the header of the EAF file. 
