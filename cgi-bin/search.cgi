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
require "common_functions/Session.cgi";

my %form;


foreach my $p (param()) {
    $form{$p} = param($p);
    #print "$p = $form{$p}<br>\n";
}

my $create=gestione_sessione::createSession();
gestione_sessione::setParam("location","/cgi-bin/search.cgi");

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
if(($data_ritorno==0)&($andata==0)){
	$errori+=2;
}
#controllo se la data di ritorno è inferiore alla data di partenza
if(($data_partenza>=$data_ritorno)&($andata==0)){
	$errori=3;
}
#non posso atterrare nello stesso aeroporto!
if($select_partenza eq $select_arrivo){
	$errori|=8;
}

if(defined($form{"cerca"})){ #se non è stato premuto il pulsante "cerca"
	gestione_sessione::setParam("Defined",undef($form{"cerca"}));
	gestione_sessione::setParam("AR",$andata);
	gestione_sessione::setParam("partenza",$select_partenza);
	gestione_sessione::setParam("arrivo",$select_arrivo);
	gestione_sessione::setParam("data_partenza",$data_partenza);
	gestione_sessione::setParam("data_ritorno",$data_ritorno);
	gestione_sessione::setParam("passeggeri",$select_passeggeri);
}else{
	if((gestione_sessione::getParam("AR")==1)){
		$andata_ritorno="andata";
	}
	$select_partenza=gestione_sessione::getParam("partenza");
	$select_arrivo=gestione_sessione::getParam("arrivo");
	$data_partenza=gestione_sessione::getParam("data_partenza");
	$data_ritorno=gestione_sessione::getParam("data_ritorno");
	$select_passeggeri=gestione_sessione::getParam("passeggeri");
	#recupero i dati dalle variabili di sessione
}






my $titolo="Ricerca voli";



my $session_cookie = CGI::Cookie->new(-name=>'SESSION',-value=>$create,-expires =>  '+2h',);

print CGI::header(-cookie=>$session_cookie);#imposto il cookie di sessione

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
print gestione_sessione::getParam("partenza")." $errori, $andata, $select_partenza, $select_arrivo, $data_partenza, $data_ritorno, $select_passeggeri		<div id=\"main\"><!-- div che contiene tutto il contenuto statico e/o dinamico-->"; #mega div


print "		</div>"; #chiudo il div main
print print_footer::print();
print "	</body>
</html>";