#!/usr/bin/perl


package index_page;

use strict;
use warnings;


require "common_functions/print_header.cgi";
require "common_functions/print_search.cgi";
require "common_functions/print_content.cgi";
require "common_functions/print_footer.cgi";


my $titolo="Home";

print "Content-type: text/html\n\n";

print "
<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Strict//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd\">
<html xmlns=\"http://www.w3.org/1999/xhtml\">
	<head>
		<link rel=\"stylesheet\" href=\"../style/main.css\" type=\"text/css\" media=\"screen\" charset=\"utf-8\"/>
		<title>$titolo</title>
	</head>
	
	<body>
";

my @tmp;
my @menu=("Home", "index.html", "1");
push @tmp, \@menu; 
my @menu=("Home1", "index1.html", "0");
push @tmp, \@menu;
my @menu=("Home2", "index2.html", "0");
push @tmp, \@menu;
my $ref=\@tmp;
print scalar(@tmp);
print_header::setMenu(\@tmp);
print print_header::print();
print "		<div id=\"main\"><!-- div che contiene tutto il contenuto statico e/o dinamico-->"; #mega div
print print_search::print();
print print_content::print();
print "		</div>"; #chiudo il div main
print print_footer::print();
print "	</body>
</html>";