# audio_label_file_conversions

Script `saymore_eaf_to_saymore_tsv.py` converts from the standard SayMore EAF (ELAN) file format to the Tab-separated values (TSV) file format. It should be identical to using ELAN to load up the original EAF file and exporting as Tab-delimited Text. The advantage of the script is that it can be quickly run on multiple files and also chained together with other commands (see bottom for examples). It is mainly just a wrapper around the excellent [pympi](https://github.com/dopefishh/pympi) python module. 

Script `saymore_tsv_to_saymore_eaf.py` converts in the other direction. This should be identical to importing a TSV file into a [SayMore EAF template](https://github.com/speechchemistry/audio_label_file_conversions/blob/main/associated_scripts/say_more_template.etf) (selected in the import dialog box). 

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
When the script `saymore_tsv_to_saymore_eaf.py` produces the .eaf file, the media filename is not explicitly mentioned in the .eaf file. This may be fixed in the future. There are two workarounds:

1. Get SayMore to automatically add the link to the .eaf file:
   - Ensure that the .eaf file has the same filename as the .wav file but with the suffix `annoations.eaf`, for example `story_01.wav.annotations.eaf`
   - Place the .eaf and .wav files in the appropriate session folder e.g. `C:\Users\User\Documents\SayMore\Shang\Sessions\story_01`
   - Start SayMore
   - When SayMore starts it will attempt to repair any .eaf files associated with media so that the media filename is explicitly added to the header of the .eaf file. You can check if this has worked by clicking on the .eaf file within SayMore. If it works the View tab should show the transcriptions. If it doesn't work the View tab will say "Open filename.eaf in it's associated program".

2. Link the media file manually through ELAN
   - Open the .eaf file with ELAN e.g. by clicking on the filename.eaf link mentioned in part 1 above.
   - Use menu Edit > Linked Files. You can then add or update a media file.
   - Save the .eaf file (e.g. using the naming convention mentinoned in part 1 above).
   - This linked .eaf file should now work for ELAN and hopefully for SayMore too. 

## Converting to Audacity label files
SayMore allows you to convert the EAF files to Audacity label files. You can also do this using these scripts.

If you are using Linux you can easily convert the SayMore TSV file to an Audacity label file. Use the following command, substituting the filenames for your own: 

```
awk -F'\t' 'NR > 1 { print $1 "\t" $2 "\t" $4 }' story01.tsv > story_01_audacity_freeTranslation.txt
```
This will use the translation as the labels (which can be safer if you will subsequently use them for filenames where some tools insist on ASCII). To use the transcription as the labels use the following instead:
```
awk -F'\t' 'NR > 1 { print $1 "\t" $2 "\t" $3 }' story01.tsv > story_01_audacity_transcription.txt
```

## Extracting individual audio files
You may be familiar with using Audacity to extract individual audio files from the master audio file using the audacity labels. The following Linux command does something similar. It takes the audacity label file, and then generates the commands that call `ffmpeg`. Once you have `ffmpeg` installed you can just copy these resulting commands into the terminal.

```
cat story_01_audacity_freeTranslation.txt |while IFS=$'\t' read -r start end label; do duration=$(printf "%.2f" "$(echo "$end - $start" | bc)"); echo ffmpeg -i '"story_01.wav"' -ss "$start" -t "$duration" -codec:a libopus "${label}.webm"; done
```

Finally these commands can be combined together to generate these individual audio files from the original EAF file:

```
python3 saymore_eaf_to_saymore_tsv.py story_01.wav.annotations.eaf |awk -F'\t' 'NR > 1 { print $1 "\t" $2 "\t" $4 }' |while IFS=$'\t' read -r start end label; do duration=$(printf "%.2f" "$(echo "$end - $start" | bc)"); echo ffmpeg -i '"story_01.wav"' -ss "$start" -t "$duration" -codec:a libopus "${label}.webm"; done
```
