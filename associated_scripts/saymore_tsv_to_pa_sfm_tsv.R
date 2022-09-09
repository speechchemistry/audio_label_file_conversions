#!/usr/bin/env Rscript
library(readr)
library(tidyr)
library(tibble)
suppressMessages(library(dplyr))
library(argparser)

p <- arg_parser("This script takes a file in the SayMore TSV format (i.e
that which ELAN outputs from opening a SayMore EAF file or the output 
of the script saymore_eaf_to_saymore_tsv.py, it then does a simple
rearrangement of the data so it's ready to be converted to SFM that
Phonology Assistant can read.")
# Add a positional argument
p <- add_argument(p, "saymore_tsv_file", 
                  help="a file in the SayMore TSV format")
# the following argument could be derived from the first argument in future
p <- add_argument(p, "corresponding_audio_filename", 
                  help="audio filename (script won't read the actual file)")
argv <- parse_args(p)

saymore_tsv <- read_tsv(argv$saymore_tsv_file)

sfm_tsv <- saymore_tsv %>%
  # interpret %ignore% as NA
  mutate(Transcription = na_if(Transcription, "%ignore%")) %>%
  # drop empty records
  drop_na(Transcription) %>% 
  # add a column that has the audio file (for later to be combined with start and end)
  add_column(audio_file = argv$corresponding_audio_file) %>% 
  # currently my convention is to put the word number and the gloss in the
  # SayMore translation field. We should now separate the number and the gloss
  separate(`Phrase Free Translation`,into=c("ref","ge"),sep=" ",extra="merge") %>%
  # Rename the transcription field to indicate lexeme form phonetic in SFM
  rename(lx_phonetic = Transcription) %>% 
  # Add start and end times to the audio file (Phonology Assistant accepts this
  # convention)
  unite(audio_file,`Begin Time - ss.msec`,`End Time - ss.msec`,col="lx_audio",sep=" ") %>% 
  # put the lexeme form phonetic field at the beginning of the SFM record
  relocate(lx_phonetic)

cat(format_tsv(sfm_tsv))
