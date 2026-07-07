#!/usr/bin/env python3

import sys
import argparse
from pathlib import Path
import pympi
import pandas as pd

def parse_arguments():
    """Converts from SayMore ELAN TSV file to SayMore ELAN EAF file"""
    parser = argparse.ArgumentParser()
    parser.add_argument("saymore_tsv_file", nargs='?', 
                        type=argparse.FileType('r'), default=sys.stdin, 
                        help="the input SayMore TSV file, if not specifed or a hyphen is given then standard input will be used. " 
                             "The first line of the TSV file should follow the ELAN conventions of "
                             "showing the four column titles: "
                             "Begin Time - ss.msec End Time - ss.msec Transcription Phrase Free Translation.")
    parser.add_argument('saymore_eaf_output_file', nargs='?', 
                        type=argparse.FileType('w'), default=sys.stdout,
                        help="the output SayMore EAF file, if not specified or a hyphen is given then standard output will be used.")
    parser.add_argument('--media-file',
                        help="optional media file to link in the generated EAF. "
                             "Absolute paths start with '/'. Relative paths are resolved from the current working directory.")
    args = parser.parse_args()

    if args.media_file:
        media_input = Path(args.media_file)
        media_abs = media_input if media_input.is_absolute() else (Path.cwd() / media_input).resolve()
        if not media_abs.is_file():
            parser.error(f"media file not found: {args.media_file}")

        if media_input.is_absolute():
            media_rel = f"./{media_abs.name}"
        else:
            media_rel = media_input.as_posix()
            if not media_rel.startswith("./") and not media_rel.startswith("../"):
                media_rel = f"./{media_rel}"

        args.media_file_abs = media_abs
        args.media_file_rel = media_rel
    else:
        args.media_file_abs = None
        args.media_file_rel = None

    return args
    
    
def main():
    tsv_file_path = args.saymore_tsv_file
    saymore_df = pd.read_csv(tsv_file_path,sep='\t',keep_default_na=False)
    # create a new Elan EAF object
    new_eaf = pympi.Elan.Eaf()

    if args.media_file_abs is not None:
        new_eaf.add_linked_file(
            str(args.media_file_abs),
            relpath=args.media_file_rel,
        )

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
    # Write directly to the requested destination; pympi handles stdout when given "-".
    output_path = (
        "-" if args.saymore_eaf_output_file is sys.stdout else args.saymore_eaf_output_file.name
    )
    pympi.Elan.to_eaf(output_path, new_eaf, pretty=True)

if __name__ == '__main__':
    args = parse_arguments()
    main()
