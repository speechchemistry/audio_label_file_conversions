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
python saymore_eaf_to_saymore_tsv.py ZOOM0030_319-321.WAV.annotations.eaf > ZOOM0030_319-321.WAV.annotations.tsv

# A simple conversion from SayMore EAF to CSV in Linux (requires csvkit)
python saymore_eaf_to_saymore_tsv.py ZOOM0030_319-321.WAV.annotations.eaf | csvformat --tabs > ZOOM0030_319-321.WAV.annotations.csv

# Assuming you have the script in your path, and that you are using the bash shell e.g. in Ubuntu
# the following converts a batch of SayMore EAF files to TSV files
for file in *.annotations.eaf; do saymore_eaf_to_saymore_tsv.py "$file" > "${file%.eaf}.tsv"; done  
```

## Linking media when converting TSV to EAF

When converting TSV to EAF with `saymore_tsv_to_saymore_eaf.py`, you can link the media file in the generated EAF using `--media-file`:

```
python saymore_tsv_to_saymore_eaf.py input.annotations.tsv output.annotations.eaf --media-file story_01.wav
```

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
cat story_01_audacity_freeTranslation.txt |while IFS=$'\t' read -r start end label; do duration=$(printf "%.2f" "$(echo "$end - $start" | bc)"); echo ffmpeg -ss "$start" -t "$duration" -i "'story_01.wav'" -codec:a libopus "'${label}.webm'"; done
```

Finally these commands can be combined together to generate these individual audio files from the original EAF file:

```
python saymore_eaf_to_saymore_tsv.py story_01.wav.annotations.eaf |awk -F'\t' 'NR > 1 { print $1 "\t" $2 "\t" $4 }' |while IFS=$'\t' read -r start end label; do duration=$(printf "%.2f" "$(echo "$end - $start" | bc)"); echo ffmpeg -ss "$start" -t "$duration" -i "'story_01.wav'" -codec:a libopus "'${label}.webm'"; done
```
## Testing

The repository includes a `pytest` test for the `saymore_tsv_to_saymore_eaf.py` CLI.

Install the test dependency if needed:

```
python -m pip install pytest
```

Run the test suite from the repository root:

```
pytest
```

This test follows an approval-testing workflow:

- Input fixtures are in `tests/fixtures/tsv_to_eaf/inputs/*.tsv`
- Approved golden masters are in `tests/fixtures/tsv_to_eaf/approved/*.approved.eaf`
- On mismatch, the normalized actual output is written to `tests/fixtures/tsv_to_eaf/received/*.received.eaf`

To approve a new output, review the corresponding `.received.eaf` file and then replace the `.approved.eaf` file when the change is intentional.

The test performs light XML scrubbing before comparison to reduce brittleness from volatile metadata. These fields are replaced with stable dummy values (for example `DATE`, `AUTHOR`, `URN`, and last-used annotation ids) rather than removed.