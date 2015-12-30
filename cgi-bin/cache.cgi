#!/usr/bin/perl


package cache_page;

use strict;
use warnings;


require "common_functions/print_header.cgi";
require "common_functions/print_search.cgi";
require "common_functions/print_content.cgi";
require "common_functions/print_footer.cgi";

my $titolo="N/D";

sub getTitle{
	my ($testo)=@_;
	#<!-- title=\"Registrati\" -->
	$testo =~/(<!--)+([ ]*)(title=")+([ ]*)([A-Za-z0-9]+)([ ]*)/;
	$titolo=$5;
}

sub generate {
	my ($testo)=@_;
		
	if(defined($testo)){
		getTitle($testo);
		my $output.= "
<!-- GENERATO DA CACHE.CGI-->
<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Strict//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd\">
<html xmlns=\"http://www.w3.org/1999/xhtml\">
	<head>
		<link rel=\"stylesheet\" href=\"style/main.css\" type=\"text/css\" media=\"screen\" charset=\"utf-8\"/>
		<title>$titolo</title>
	</head>
	
	<body>
";

	my @menu_temp;
	my @menu=("Home", "index.html", "1");
	push @menu_temp, \@menu; 
	my @menu=("Home1", "index1.html", "0");
	push @menu_temp, \@menu;
	my @menu=("Home2", "index2.html", "0");
	push @menu_temp, \@menu;

	#funzionamento: la funzione riceve un riferimento ad un array di riferimenti di array.
	# esempio: RIF_MENU_1=array("Home", "pagina.html", "1"); //Il pulsante avrà il nome "Home", il riferimento a "pagina.html" e sarà selezionato sul CSS.
	#          RIF_MENU_1=array("404", "404.html", "0"); //Il pulsante avrà il nome "404", il riferimento a "404.html" e NON sarà selezionato sul CSS.
	#
	print_header::setMenu(\@menu_temp);

	my @path_temp;
	my @path=("Home", "index.html");
	push @path_temp, \@path;
	my @path=("Pagina principale", "index.html");
	push @path_temp, \@path;
	print_header::setPath(\@path_temp);

	$output.= print_header::print();
	$output.= "		<div id=\"main\"><!-- div che contiene tutto il contenuto statico e/o dinamico-->"; #mega div
	#$output.= print_search::print();
	$output.=print_content::print($testo);
	$output.= "		</div>"; #chiudo il div main
	$output.= print_footer::print();
	$output.= "	</body>
</html>";
	return $output;
		
	}
	
}
my $testo="";
my $directory = 'pages';
my $html_directory = '../htdocs';

opendir (DIR, $directory) or die $!;	
while (my $file = readdir(DIR)) {
		if($file =~/([A-Za-z0-9_-].txt)/){#ricavo il nome del file corrente. evito files con caratteri strani.
        	my $content;
    		open(my $fh, '<', $directory."/".$file) or die "cannot open file $file";
    		{
        		local $/;
        		$content = <$fh>;
        		$file=~ /([A-Za-z0-9_-]+)/;
        		my $filename= $1.".html";
        		my $cnt= generate( $content);
        		open(my $o_fh, '>', $html_directory."/".$filename) or die "cannot open file $filename";
        		print $o_fh $cnt;
        		close $o_fh;
        		
    		}
    		close($fh);
		}

}
exit(0);