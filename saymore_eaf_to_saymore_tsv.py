#!/usr/bin/env python3

import sys
import argparse
import pympi
import io
from contextlib import redirect_stdout

def parse_arguments():
    """Converts from SayMore ELAN EAF file to SayMore ELAN TSV file"""
    parser = argparse.ArgumentParser()
    parser.add_argument("saymore_eaf_file", 
                        help="the saymore eaf file i.e. with Transcription as "
                        "a parent tier of Phrase Free Translation (if you want"
                        " to use standard input you need to use a hyphen "
                        "instead of the filename due to the way Pympi works)")
    args = parser.parse_args()
    return args
    
def main():
    eaf_file_path = args.saymore_eaf_file
    # Initialize the elan file    
    # Pympi has an issue where it prints out a warning to standard output
    # so we need to catch this and print it out to standard error
    # I found help at https://stackoverflow.com/questions/16571150/how-to-capture-stdout-output-from-a-python-function-call
    f = io.StringIO()
    with redirect_stdout(f):
        new_eaf = pympi.Elan.Eaf(eaf_file_path)
    pympi_error = f.getvalue()
    print(pympi_error,file=sys.stderr)
    # print column headers
    print("Begin Time - ss.msec\tEnd Time - ss.msec\tTranscription\tPhrase Free Translation")
    translation_data1 = new_eaf.get_ref_annotation_data_for_tier("Phrase Free Translation")
    # Print each interval for both tiers (the translation tier points
    #  back to it's parent tier, transcription)
    for i in translation_data1: # i is each subsequent interval
        start = i[0]/1000 # calculate seconds from milliseconds
        end = i[1]/1000 # calculate seconds from milliseconds
        translation = i[2]
        transcription = i[3]
        print(start,end,transcription,translation,sep = '\t')
        #print(start,"\t",end,"\t",transcription,"\t",translation)

if __name__ == '__main__':
    args = parse_arguments()
    main()
