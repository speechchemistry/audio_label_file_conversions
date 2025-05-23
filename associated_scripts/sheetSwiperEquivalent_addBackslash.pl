#!/usr/bin/env perl
# this script implements the equivalent of sheetswiper except
# that it adds the backslash prefix to column headings

# input: the tsv file (excel might have added quotes around text
#        containing commas which you probably should remove as
#        it leads to errors in silpa)
# output: the toolbox file

@ARGV = glob("@ARGV") if ($^O eq 'MSWin32');  

$count = 0;
while(<>) # go through the feature csv file and put into the arrays
{
   my $line = $_;
   $line =~ s/\r?\n$//; # chomp LF or CRLF terminators
   @lineArray = split(/\t/,$line); 
   if ($count==0)
   {
      @labelArray = @lineArray;      
   }
   else
   {
       print "\n";
       $countElement = 0;
       for my $lineArrayElement (@lineArray) {
          if ($lineArrayElement ne '') {
             print "\\$labelArray[$countElement] $lineArrayElement\n";
          }
          $countElement++;
       }
   } 
   $count++;
}
