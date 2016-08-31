#!/usr/bin/perl
package aggiorna_index;

require      Exporter;
require "common_functions/print_header.cgi";
require "common_functions/print_search.cgi";
require "common_functions/print_content.cgi";
require "common_functions/print_footer.cgi";
require "common_functions/Session.cgi";
require "common_functions/check_form.cgi";
require "common_functions/database.cgi";
require "common_functions/menu.cgi";

my @ISA       = qw(Exporter);
my $VERSION   = 1.00;         # Version number

use Time::Piece;
use CGI::Carp qw(fatalsToBrowser);
use strict;


sub get{
my $ritorno;
my $titolo="Home";



#my $session_cookie = CGI::Cookie->new(-name=>'SESSION',-value=>$create,-expires =>  '+2h',);

#print CGI::header(-cookie=>$session_cookie);#imposto il cookie di sessione

$ritorno ="
<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Strict//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd\">
<html xmlns=\"http://www.w3.org/1999/xhtml\" lang=\"it\" xml:lang=\"it\">
	<head>
		<link rel=\"stylesheet\" href=\"style/main.css\" type=\"text/css\" media=\"screen\" charset=\"utf-8\"/>
		<title>$titolo</title>
	</head>
	
	<body>
";



#funzionamento: la funzione riceve un riferimento ad un array di riferimenti di array.
# esempio: RIF_MENU_1=array("Home", "pagina.html", "1"); //Il pulsante avrà il nome "Home", il riferimento a "pagina.html" e sarà selezionato sul CSS.
#          RIF_MENU_1=array("404", "404.html", "0"); //Il pulsante avrà il nome "404", il riferimento a "404.html" e NON sarà selezionato sul CSS.
#
print_header::setMenu(menu::get(1));

my %tratte=database::listTratte();
print_search::set_tratte(%tratte);

my @path_temp;
my @path=("Home", "index.html");
push @path_temp, \@path;
print_header::setPath(\@path_temp);

$ritorno .= print_header::print();
$ritorno .= "		<div id=\"main\"><!-- div che contiene tutto il contenuto statico e/o dinamico-->"; #mega div
$ritorno .= print_search::set_date(128);
my $testo='
				<div id="presentazione">
					
					<p>Benvenuto nel sito ufficiale della compagnia aerea low cost A-ir</p>
					<p>Qui potrai trovare tutte le informazioni riguardanti la nostra compagnia, il nostro personale, la nostra flotta e scoprire tutte le destinazioni che puoi scegliere per la tua vacanza o per il tuo viaggio di affari!</p>
					<p>Cosa stai aspettando? Prenota subito il tuo volo!!</p>
				</div>';
$ritorno .= print_content::print($testo);
$ritorno .= "		</div>"; #chiudo il div main
$ritorno .= print_footer::print();
$ritorno .= "	</body>
</html>";
return $ritorno;
}

#funzioni base
sub aggiorna{

	my $index;
	my $testo= get();
	#$testo =~ s/([a-zA-Z_.]+.cgi)/cgi-bin\/$1/g;
	#$testo =~ s/"..\//"/g;
	my $filename="../public_html/index.html";
	eval {
		open(my $fh, '>', $filename) or die "Could not open file '$filename' $!";
		print $fh $testo;
		close $fh;
	};	
    #my $ricerca=$p->getElementById("prenota");
    #print $ricerca;
   # my $ricerca=$p->get_tag('<div id="prenota">');
   # print $ricerca;
}
1;
