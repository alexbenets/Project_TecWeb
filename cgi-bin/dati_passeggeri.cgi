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

my $create=gestione_sessione::createSession();
gestione_sessione::setParam("location","/cgi-bin/dati_passeggeri.cgi");

my %form;


foreach my $p (param()) {
    $form{$p} = param($p);
    #print "$p = $form{$p}<br>\n";
}

my $errori=0;
my $passeggeri=gestione_sessione::getParam("passeggeri");
my @dati;
for(my $i=1; $i<=$passeggeri; $i++){
	my $errore=0;
	my $nome="Nome";
	if (defined ($form{"Nome$i"})){
		$nome=$form{"Nome$i"};
		gestione_sessione::setParam("Nome$i", $nome);
	}else{
		my $temp=gestione_sessione::getParam("Nome$i");
		if(defined($temp)){
			$nome=$temp;
		}
	}
	if((check_form::valida_nominativo($nome)==0) & defined ($form{"Nome$i"})){
		#errore
		$errori++;
		$errore=1;
	}
	
	my $cognome="Cognome";
	if (defined ($form{"Cognome$i"})){
		$cognome=$form{"Cognome$i"};
		gestione_sessione::setParam("Cognome$i", $cognome);
	}else{
		my $temp=gestione_sessione::getParam("Cognome$i");
		if(defined($temp)){
			$cognome=$temp;
		}
	}
	if((check_form::valida_nominativo($cognome)==0) & defined ($form{"Cognome$i"})){
		#errore
		$errori++;
		$errore|=2;
	}
	
	my $cf="Codice fiscale";
	if (defined ($form{"CF$i"})){
		$cf=$form{"CF$i"};
		gestione_sessione::setParam("CF$i", $cf);
	}else{
		my $temp=gestione_sessione::getParam("CF$i");
		if(defined($temp)){
			$cf=$temp;
		}
	}
	if((check_form::valida_codice_fiscale($form{"CF$i"})==0) & defined ($form{"CF$i"})){
		#errore
		$errori++;
		$errore|=4;
	}
	my $nascita="32/02/1900";
	if (defined ($form{"nascita$i"})){
		$nascita=$form{"nascita$i"};
		gestione_sessione::setParam("nascita$i", $nascita);
	}else{
		my $temp=gestione_sessione::getParam("nascita$i");
		if(defined($temp)){
			$nascita=$temp;
		}
	}
	if((check_form::controlla_data_passeggero($form{"nascita$i"})==0) & defined ($form{"nascita$i"})){
		#errore
		$errori++;
		$errore|=8;
	}
	my @dati_temp=(	$nome,
					$cognome,
					$cf,
					$nascita, 
					$errore);
	push  @dati,\@dati_temp; 
}


if((($errori==0)&defined($form{"avanti"})| $passeggeri==0)){
 #passo successivo	
 print "Location: servizi_aggiuntivi.cgi\n\n";
 exit;
}

my $titolo="Dati dei passeggeri";

print "Content-type: text/html\n\n";

print "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Strict//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd\">
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
print "		<div id=\"main\"><!-- div che contiene tutto il contenuto statico e/o dinamico-->"; #mega div
my $messaggio="";
if($errori>0){
	$messaggio="<div>
					<h3 class=\"errore\">Attenzione: alcuni dati non sono corretti!</h3>
				</div>";
}
my $testo="
		<div class=\"sezione\">
			<form action=\"dati_passeggeri.cgi\" method=\"post\">
				<fieldset>
						<div>
							<h3>Dati passeggeri</h3>
						</div>$messaggio";
					for (my $i=1; $i<=$passeggeri; $i++){
					$testo.="
						<div>
							<h4>Passeggero $i</h3>
						</div>
						<div>
							<label for=\"Nome$i\">Nome: </label>
							<input type=\"text\" id=\"Nome$i\" name=\"Nome$i\" value=\"";
							$testo.=@dati[$i-1]->[0];
							$testo.="\" class=\"";
							if(((@dati[$i-1]->[4])&1)>0){
								$testo.="errore";
							}
							$testo.="\"></input>
							<div class=\"clearer\"></div>
						</div>
						<div>
							<label for=\"Cognome$i\">Cognome: </label>
							<input type=\"text\" id=\"Cognome$i\" name=\"Cognome$i\" value=\"";
							$testo.=@dati[$i-1]->[1];
							$testo.="\" class=\"";
							if(((@dati[$i-1]->[4])&2)>0){
								$testo.="errore";
							}
							$testo.="\"></input>
							<div class=\"clearer\"></div>
						</div>
						<div>
							<label for=\"CF$i\">Codice Fiscale: </label>
							<input type=\"text\" id=\"CF$i\" name=\"CF$i\" value=\"";
							$testo.=@dati[$i-1]->[2];
							$testo.="\" class=\"";
							if(((@dati[$i-1]->[4])&4)>0){
								$testo.="errore";
							}
							$testo.="\"></input>
							<div class=\"clearer\"></div>
						</div>
						<div>
							<label for=\"nascita$i\">Data di nascita: </label>
							<input type=\"text\" id=\"nascita$i\" name=\"nascita$i\" value=\"";
							$testo.=@dati[$i-1]->[3];
							$testo.="\" class=\"";
							if(((@dati[$i-1]->[4])&8)>0){
								$testo.="errore";
							}
							$testo.="\"></input>
							<div class=\"clearer\"></div>
						</div>
						
						";
					}
				$testo.="
					<div>
							<button type=\"submit\" id=\"avanti\" name=\"avanti\" value=\"1\">
								<span>Procedi</span>
							</button>
						</div>
				</fieldset>
			</form>
		</div><!-- chiudo sezione-->
";

print print_content::print("$testo");
print "		</div> <!-- chiudo main -->"; #chiudo il div main
print print_footer::print();
print "	</body>
</html>";