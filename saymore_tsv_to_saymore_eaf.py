#!/usr/bin/env python3

import os
import sys
import argparse
import pympi
import pandas as pd

def parse_arguments():
    """Converts from SayMore ELAN TSV file to SayMore ELAN EAF file"""
    parser = argparse.ArgumentParser()
    parser.add_argument("saymore_tsv_file", nargs='?', 
                        type=argparse.FileType('r'), default=sys.stdin, 
                        help="the input SayMore TSV file, if not specifed or a hyphen is given then standard input will be used." 
                             "The first line of the TSV file should follow the ELAN conventions of "
                             "showing the four column titles: "
                             "Begin Time - ss.msec End Time - ss.msec Transcription Phrase Free Translation.")
    parser.add_argument('saymore_eaf_output_file', nargs='?', 
                        type=argparse.FileType('w'), default=sys.stdout,
                        help="the output SayMore EAF file, if not specifed or a hyphen is given then standard output will be used.")
    args = parser.parse_args()
    return args
    
    
def main():
    tsv_file_path = args.saymore_tsv_file
    saymore_df = pd.read_csv(tsv_file_path,sep='\t',keep_default_na=False)
    # create a new Elan EAF object
    new_eaf = pympi.Elan.Eaf()
    # Define linguistic types, locales, and the tiers; to match SayMore template
    new_eaf.add_linguistic_type("Transcription", constraints=None, timealignable=True)
    new_eaf.add_linguistic_type("Translation", constraints='Symbolic_Association', timealignable=False)
    new_eaf.add_locale("ipa-ext",variant="IPA Extended")
    new_eaf.add_tier("Transcription",ling="Transcription",locale="ipa-ext")
    new_eaf.add_tier("Phrase Free Translation",ling="Translation",parent="Transcription",locale="ipa-ext")
    # Copy across each interval to the transcription and translation tier
    for index,row in saymore_df.iterrows():
        start = round(row.get("Begin Time - ss.msec") * 1000) # convert to ms
        end = round(row.get("End Time - ss.msec") * 1000) # convert to ms
        mid_point = start + (end-start)/2
        ipa = row.get("Transcription")
        gloss = row.get("Phrase Free Translation")
        new_eaf.add_annotation("Transcription",start,end,value=ipa)
        new_eaf.add_ref_annotation("Phrase Free Translation","Transcription",mid_point,value=gloss)
    # remove ELAN default data structures
    new_eaf.remove_tier("default")
    new_eaf.remove_linguistic_type("default-lt")
    # the pympy output to EAF file is a bit idiosyncratic so I'm saving it to 
    # a temporary file first
    unique_temp_filename = "saymore_tsv_to_saymore_eaf_out_73137.tmp"
    new_eaf.to_file(unique_temp_filename) 
    ###pympi.Elan.to_eaf("-", new_eaf,pretty=True) # documentation says you can use this but it 
    ##gives error "TypeError: write() argument must be str, not bytes"
    ###new_eaf.to_file("/dev/stdout") # doesn't work because it tries to back up /dev/stdout first!
    # open up the temporary file just created
    with open(unique_temp_filename) as f:   
        data = f.read()
    # delete the temporary file
    os.remove(unique_temp_filename)
    # now write it in just a standard way
    # note that we don't need an open command because 
    # args.saymore_eaf_output_file is already an IO object / stream
    with args.saymore_eaf_output_file as text_file:
        print(data, file=text_file)

if __name__ == '__main__':
    args = parse_arguments()
    main()
