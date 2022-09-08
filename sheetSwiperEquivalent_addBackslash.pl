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
   chomp($line);
   @lineArray = split(/\t/,$line); 
   #   $phone = shift @lineArray;
   if ($count==0)
   {
      @labelArray = @lineArray;      
   }
   else
   {
       print "\n";
       $countElement = 0;
       for $lineArrayElement (@lineArray)
       {
	  print "\\$labelArray[$countElement] $lineArrayElement\n";
          $countElement++;
       }
   } 
   $count++;
}
