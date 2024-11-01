# audio_label_file_conversions

Script `saymore_eaf_to_saymore_tsv.py` converts from the standard SayMore EAF (ELAN) file format to the Tab-separated values (TSV) file format. It should be identical to using ELAN to load up the original EAF file and exporting as Tab-delimited Text. This script allows you do the same but with a batch of files. It is mainly just a wrapper around the excellent [pympi](https://github.com/dopefishh/pympi) python module. 

Script `saymore_tsv_to_saymore_eaf.py` converts in the other direction.

## Requirements

You need Python version 3 and the following python modules:

- pympi
- pandas (for `saymore_tsv_to_saymore_eaf.py` only)

## Installation

You can either clone this repository or just select the script you want and download the raw code. To use the script anywhere in your file directory you may need to add the script's location to your PATH environmental variable. 

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

## Known issues and workarounds
Note that the media filename is not explicitly mentioned in the .eaf output file. This may be fixed in the future. There are two workarounds:

1. Get SayMore to automatically add the link to the .eaf file:
   - Ensure that the .eaf file has the same filename as the .wav file but with the suffix `annoations.eaf`, for example `story_01.wav.annotations.eaf`
   - Place the .eaf and .wav files in the appropriate session folder e.g. `C:\Users\User\Documents\SayMore\Shang\Sessions\Story 01`
   - Start SayMore
   - When SayMore starts it will attempt to repair any .eaf files associated with media so that the media filename is explicitly added to the header of the .eaf file. You can check if this has worked by clicking on the .eaf file within SayMore. If it works the View tab should show the transcriptions. If it doesn't work the View tab will say "Open filename.eaf in it's associated program".

2. Link the media file manually through ELAN
   - Open the .eaf file with ELAN e.g. by clicking on the filename.eaf link mentioned in part 1 above.
   - Use menu Edit > Linked Files. You can then add or update a media file.
   - Save the .eaf file (e.g. using the naming convention mentinoned in part 1 above).
   - This linked .eaf file should now work for ELAN and hopefully for SayMore too. 
