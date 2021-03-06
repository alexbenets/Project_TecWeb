#!/usr/bin/perl


package pagina_utente;

use strict;
use CGI::Carp qw(fatalsToBrowser);
use CGI qw(:standard);
use CGI;


require "common_functions/print_header.cgi";
#require "common_functions/print_search.cgi"; #inutile: non viene sfruttato in questa pagina.
require "common_functions/print_content.cgi";
require "common_functions/print_footer.cgi";
require "common_functions/Session.cgi";
require "common_functions/check_form.cgi";
require "common_functions/database.cgi";
require "common_functions/menu.cgi";
require "common_functions/aggiorna_index.cgi";

my %form;


foreach my $p (param()) {
    $form{$p} = param($p);
    #print "$p = $form{$p}<br>\n";
}


my $titolo="Area Amministrativa";


my $create=gestione_sessione::createSession();

if((gestione_sessione::getParam("logged")!=1) or (gestione_sessione::getParam("admin")!=1)){
	print "location: index.cgi\n\n";
	exit;
}

my $errore="";

my $nuova_citta=int($form{"nuova_citta"});
my $modifica_citta=int($form{"modifica_citta"});

my $nazione=$form{"nazione"};
my $citta=$form{"citta"};
my $nuovo_nome=$form{"nuovo_nome"};
if (!($form{"salva"} eq "")){
	if(!($citta eq "")){
		if(!($citta eq "")){
			$citta=~/([0-9]+)-([a-zA-Z]+)/;
			#print $2;
			$errore=database::addCitta($nuovo_nome,$nazione,$1); 
		}
	}else{
		$errore=database::addCitta($nuovo_nome, $nazione); 
	}
	if($errore!=1){
		$errore='<p class="errore">Attenzione: non ho potuto modificare la citt&agrave;!</p>';
	}else{
		$errore="";
		aggiorna_index::aggiorna();
	}
}
gestione_sessione::setParam("location","admin_citta.cgi");


my $session_cookie = CGI::Cookie->new(-name=>'SESSION',-value=>$create,-expires =>  '+2h',);

print CGI::header(-cookie=>$session_cookie);#imposto il cookie di sessione

print "
<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Strict//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd\">
<html xmlns=\"http://www.w3.org/1999/xhtml\" lang=\"it\" xml:lang=\"it\">
	<head>
		<link rel=\"stylesheet\" href=\"../style/main.css\" type=\"text/css\" media=\"screen\" charset=\"utf-8\"/>
		<title>$titolo</title>
	</head>
	
	<body>
";



#funzionamento: la funzione riceve un riferimento ad un array di riferimenti di array.
# esempio: RIF_MENU_1=array("Home", "pagina.html", "1"); //Il pulsante avrà il nome "Home", il riferimento a "pagina.html" e sarà selezionato sul CSS.
#          RIF_MENU_1=array("404", "404.html", "0"); //Il pulsante avrà il nome "404", il riferimento a "404.html" e NON sarà selezionato sul CSS.
#
print_header::setMenu(menu::get());

my %tratte=database::listTratte();
print_search::set_tratte(%tratte);

my @path_temp;
my @path=("Home", "index.cgi");
push @path_temp, \@path;
my @path=("Area amministratore", "admin.cgi");
push @path_temp, \@path;
my @path=("Gestione citt&agrave;", "admin_citta.cgi");
push @path_temp, \@path;
print_header::setPath(\@path_temp);

print print_header::print();
print "		<div id=\"main\"><!-- div che contiene tutto il contenuto statico e/o dinamico-->"; #mega div
print '<div id="secondo_menu">
					<ul>
						<li><a href="admin_nazioni.cgi" >Gestione Nazioni</a></li>
						<li><a href="admin_citta.cgi" class="selected">Gestione Citt&agrave;</a></li>
						<li><a href="admin_aereoporti.cgi" >Gestione Aereoporti</a></li>
						<li><a href="admin_tratte.cgi">Gestione Tratte</a></li>
						<li><a href="admin_voli.cgi">Gestione Voli</a></li>
						<li><a href="admin_servizi.cgi">Gestione Servizi</a></li>
					</ul>
				</div><!-- chiudo secondo menu -->';
my $testo='<div id="contenitore_sezioni"><!-- apro maxi contenitore per le sezioni -->
					
					<div class="sezione" id="S1"><!-- inizio div che contiene titolo e sezione dell\'articolo -->
						<h3>Benvenuto!</h3>';
if ($nuova_citta==0 and $modifica_citta==0){
				$testo.='<p>Per favore, scegli quale azione desideri effettuare</p>
						</div><!-- chiudo sezione -->
					<div class="sezione">
						<a href="admin_citta.cgi?modifica_citta=1">Modifica una citt&agrave; esistente</a>
					</div>
					<div class="clearer"></div>
					<!-- fine sezione -->	
					<div class="sezione">
						<a href="admin_citta.cgi?nuova_citta=1">Aggiungi una nuova citt&agrave;</a>
					</div>
					<div class="clearer"></div>
					<!-- fine sezione -->	';
}else{
			$testo.='
						<p>In questa pagina puoi modificare le citt&agrave; presenti nel database.</p>
					</div><!-- chiudo sezione -->';
	if($modifica_citta==1){
		$testo.='
					<div class="sezione">
						<form action="admin_citta.cgi" method="post">
							<fieldset>
								<h3>Modifica una citt&agrave;</h3>'.$errore.'
								<div>
									<label for="citta">citt&agrave;:</label>
									<select id="citta" name="citta">
										<option>-</option>';
								my @citta=@{database::listCitta()};
								foreach my $nazione (@citta){
										my @tmp=@{$nazione};
										$testo.='<option>'.@tmp[0]."-".@tmp[1].'</option>';
								
								}
								$testo.='	</select>
								</div>
								<div>
									<label for="nazione1">Nazione d\'appartenenza:</label>
									<select id="nazione1" name="nazione">
										<option>-</option>';
								my @citta=@{database::listStati()};
								foreach my $nazione (@citta){
										my @tmp=@{$nazione};
										$testo.='<option>'.@tmp[1].'</option>';
								
								}
								$testo.='	</select>
								</div>
								<div>
									<label for="nuovo_nome">Nuovo nome:</label>
									<input type="text" id="nuovo_nome" name="nuovo_nome" value="Milano"></input>
								</div>
								<div>
									<button type="submit" id="salva" name="salva" value="salva">
										<span>modifica</span>
									</button>
								</div>
							</fieldset>
						</form>
					</div>
					<div class="clearer"></div>
					<!-- fine sezione -->';
			}
		if($nuova_citta==1){
		$testo.='
					<div class="sezione">
						<form action="admin_citta.cgi" method="post">
							<fieldset>
								<h3>Aggiungi una citt&agrave;</h3>
								<div>
									<label for="nazione2">Nazione d\'appartenenza:</label>
									<select id="nazione2" name="nazione">
										<option>-</option>';
								my @citta=@{database::listStati()};
								foreach my $nazione (@citta){
										my @tmp=@{$nazione};
										$testo.='<option>'.@tmp[1].'</option>';
								
								}
								$testo.='	</select>
								</div>
								<div>
									<label for="nuovo_nome1">Nome della citt&agrave;:</label>
									<input type="text" id="nuovo_nome1" name="nuovo_nome" value="Milano"></input>
								</div>
								<div>
									<button type="submit" id="salva2" name="salva" value="salva">
										<span>Aggiungi</span>
									</button>
								</div>
							</fieldset>
						</form>
					</div>
					<div class="clearer"></div>
					<!-- fine sezione -->';
			}
		}
			$testo.='
					<div id="torna_su">
						<a href="#header">Torna su</a>
					</div>
			</div><!-- chiudo contenitore_sezioni -->	
			<div class="clearer"></div>
				';

print print_content::print($testo);
print "		</div>"; #chiudo il div main
print print_footer::print();
print "	</body>
</html>";