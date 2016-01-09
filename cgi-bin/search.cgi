#!/usr/bin/perl


package index_page;

use strict;
use CGI::Carp qw(fatalsToBrowser);
use CGI qw(:standard);
use CGI;
#use warnings;


require "common_functions/print_header.cgi";
require "common_functions/print_search.cgi";
require "common_functions/print_content.cgi";
require "common_functions/print_footer.cgi";
require "common_functions/check_form.cgi";


my %form;


foreach my $p (param()) {
    $form{$p} = param($p);
    #print "$p = $form{$p}<br>\n";
}

my $andata_ritorno=$form{"AR"};
my $select_partenza=$form{"partenza"};
my $select_arrivo=$form{"arrivo"};
my $data_partenza=check_form::leggi_data($form{"data_partenza"});
my $data_ritorno=check_form::leggi_data($form{"data_ritorno"});
my $select_passeggeri=check_form::leggi_numeri($form{"passeggeri"});

my $andata=0; #booleana: se non è andata, allora è con ritorno.

if($andata_ritorno eq "andata"){
	$andata=1;
}
my $errori=0;
if($data_partenza==0){
	$errori=1;
}
if($data_ritorno==0){
	$errori+=2;
}

my $titolo="Ricerca voli";

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

my @menu_temp;
my @menu=("Home", "../index.html", "1");
push @menu_temp, \@menu; 
my @menu=("Home1", "index1.html", "0");
push @menu_temp, \@menu;
my @menu=("Contatti", "../contatti.html", "0");
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

print print_header::print();
if($errori>0){
	print print_search::print($errori, $andata, $select_partenza, $select_arrivo, $data_partenza, $data_ritorno, $select_passeggeri);
}
print "		<div id=\"main\"><!-- div che contiene tutto il contenuto statico e/o dinamico-->"; #mega div
print print_content::print(" $errori $andata_ritorno, $select_partenza, $select_arrivo, $data_partenza, $data_ritorno, $select_passeggeri");
print "		</div>"; #chiudo il div main
print print_footer::print();
print "	</body>
</html>";