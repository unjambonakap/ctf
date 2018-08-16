#!/usr/bin/perl 

while(<>){
	s/#([a-fA-F0-9]{2})/chr(hex($1))/ge;
	s/\\([0-9]{3})/chr(oct($1))/ge;
	s/\\\r\n//g;
	print $_;

}
