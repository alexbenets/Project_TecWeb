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


my %form;


foreach my $p (param()) {
    $form{$p} = param($p);
    #print "$p = $form{$p}<br>\n";
}

my $modifica_dati_utente=int($form{"dati"});
my $modifica_prenotazioni=int($form{"prenotazioni"});

my $titolo="Area utente";


my $create=gestione_sessione::createSession();

if(gestione_sessione::getParam("logged")!=1){
	print "location: index.cgi\n\n";
	exit;
}

gestione_sessione::setParam("location","utente.cgi");


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

#my %tratte=database::listTratte();
#print_search::set_tratte(%tratte);

my @path_temp;
my @path=("Home", "index.cgi");
push @path_temp, \@path;
my @path=("Area utente", "utente.cgi");
push @path_temp, \@path;
print_header::setPath(\@path_temp);

print print_header::print();
print "		<div id=\"main\"><!-- div che contiene tutto il contenuto statico e/o dinamico-->"; #mega div
print '<div id="secondo_menu">
					<ul>
						<li><a href="utente.cgi?dati=1">Dati personali</a></li>
						<li><a href="utente.cgi?prenotazioni=1">Prenotazioni</a></li>
					</ul>
				</div><!-- chiudo secondo menu -->';
my $testo='<div id="contenitore_sezioni"><!-- apro maxi contenitore per le sezioni -->
					
					<div class="sezione" id="S1"><!-- inizio div che contiene titolo e sezione dell\'articolo -->
						<h3>Benvenuto!</h3>
						<p>In questa pagina potrai modificare i tuoi dati e le tue prenotazioni (fino a 2 giorni prima della partenza).</p>
					</div><!-- chiudo sezione -->
					
					<div id="torna_su">
						<a href="#header">Torna su</a>
					</div>
			</div><!-- chiudo contenitore_sezioni -->	
			<div class="clearer"></div>
				';
if($modifica_dati_utente==1){
	my $id=gestione_sessione::getParam("id");
	my @dati=@{database::getUtente($id)};
	my $nome=@dati[0];
	my $nome_form=$form{"Nome"};
	my $errore=0;
	if((check_form::valida_nominativo($nome_form)==1) and !($nome_form eq "")){
		$nome=$nome_form;
	}else{
		if(!($nome_form eq "")){#se il nome non è validato
			$errore=1;
			$nome=$nome_form;
		}
	}
	my $cognome=@dati[1];
	my $cognome_form=$form{"Cognome"};
	if((check_form::valida_nominativo($cognome_form)==1) and !($cognome_form eq "")){
		$cognome=$cognome_form;
	}else{
		if(!($cognome_form eq "")){#se il nome non è validato
			$errore|=2;
			$cognome=$cognome_form;
		}
	}
	my $codice_fiscale=@dati[2];
	my $codice_fiscale_form=$form{"CF"};
	if((check_form::valida_codice_fiscale($codice_fiscale_form)==1) and !($codice_fiscale_form eq "")){
		$codice_fiscale=$codice_fiscale_form;
	}else{
		if(!($codice_fiscale_form eq "")){#se il nome non è validato
			$errore|=4;
			$codice_fiscale=$codice_fiscale_form;
		}
	}
	
	my $nascita=@dati[3];
	my $nascita_form=$form{"nascita"};
	
	if((check_form::valida_data($nascita_form)==1) and !($nascita_form eq "")){
		$nascita=$nascita_form;
	}else{
		if(!($nascita_form eq "")){#se il nome non è validato
			$errore|=8;
			$nascita=$nascita_form;
		}
	}
	
	my $password="**********";
	my $password_form=$form{"password_attuale"};
	
	my $nuova_password=$form{"nuova_password"};
	my $controllo_nuova_password=$form{"ripeti_nuova_password"};
	if(!($nuova_password eq $controllo_nuova_password)){
		$errore|=32;
	}
	my $messaggio;
	if($errore==0 and (int($form {"avanti"})==1)){
		#$id, $nome, $cognome, $cf, $nascita, $password, $nuova_password
		my $result=database::aggiornaUtente($id, $nome, $cognome, $codice_fiscale, $nascita, $password_form, $nuova_password);
		if($result==0){#se la password è errata
			$errore = 16;
		}
	}
	if(defined($form{"avanti"}) and ($errore==0)){
		$testo="<div class=\"sezione\"><!-- apro maxi contenitore per le sezioni -->
			<p>Dati aggiornati correttamente!</p>
			</div><!-- chiudo contenitore sezioni -->
		<div class=\"clearer\"></div>";
	}
	else{
	if(defined($form{"avanti"}) and ($errore >0)){
		$messaggio="<h3>Alcuni dati inseriti non sono corretti</h3>";
	}	
	$testo="
		<div class=\"sezione\"><!-- apro maxi contenitore per le sezioni -->
			<form action=\"utente.cgi\" method=\"post\">
				<fieldset>
						<div>
							<h3>Modifica i tuoi dati personali</h3>
						</div>
						
						<div>$messaggio</div>
						<div>
							<input type=\"hidden\" id=\"dati\" name=\"dati\" value=\"1\"/>
							<label for=\"Nome\">Nome: </label>
							<input type=\"text\" id=\"Nome\" name=\"Nome\" value=\"";
							$testo.=$nome;
							$testo.="\" class=\"";
							if(($errore &1)>0){
								$testo.="errore";
							}
							$testo.="\"></input>
							<div class=\"clearer\"></div>
						</div>
						<div>
							<label for=\"Cognome\">Cognome: </label>
							<input type=\"text\" id=\"Cognome\" name=\"Cognome\" value=\"";
							$testo.=$cognome;
							$testo.="\" class=\"";
							if(($errore&2)>0){
								$testo.="errore";
							}
							$testo.="\"></input>
							<div class=\"clearer\"></div>
						</div>
						<div>
							<label for=\"CF\">Codice Fiscale: </label>
							<input type=\"text\" id=\"CF\" name=\"CF\" value=\"";
							$testo.=$codice_fiscale;
							$testo.="\" class=\"";
							if(($errore&4)>0){
								$testo.="errore";
							}
							$testo.="\"></input>
							<div class=\"clearer\"></div>
						</div>
						<div>
							<label for=\"nascita\">Data di nascita: </label>
							<input type=\"text\" id=\"nascita\" name=\"nascita\" value=\"";
							$testo.=$nascita;
							$testo.="\" class=\"";
							if(($errore&8)>0){
								$testo.="errore";
							}
							$testo.="\"></input>
							<div class=\"clearer\"></div>
						</div>
						<div>
							<label for=\"password_attuale\">Password attuale: </label>
							<input type=\"password\" id=\"password_attuale\" name=\"password_attuale\" value=\"";
							$testo.="**********";
							$testo.="\" class=\"";
							if(($errore&16)>0){
								$testo.="errore";
							}
							$testo.="\"></input>
							<div class=\"clearer\"></div>
						</div>
						
						<div>
							<label for=\"nuova_password\">Nuova password: </label>
							<input type=\"password\" id=\"nuova_password\" name=\"nuova_password\" value=\"";
							$testo.="**********";
							$testo.="\" class=\"";
							if(($errore&32)>0){
								$testo.="errore";
							}
							$testo.="\"></input>
							<div class=\"clearer\"></div>
						</div>
						
						<div>
							<label for=\"ripeti_nuova_password\">Ripeti la nuova password: </label>
							<input type=\"password\" id=\"ripeti_nuova_password\" name=\"ripeti_nuova_password\" value=\"";
							$testo.="**********";
							$testo.="\" class=\"";
							if(($errore&32)>0){
								$testo.="errore";
							}
							$testo.="\"></input>
							<div class=\"clearer\"></div>
						</div>
						
						";
				$testo.="
					<div>
							<button type=\"submit\" id=\"avanti\" name=\"avanti\" value=\"1\">
								<span>Procedi</span>
							</button>
					</div>
				</fieldset>
			</form>
		</div><!-- chiudo contenitore sezioni -->
		<div class=\"clearer\"></div>
	";
	}
}

if($modifica_prenotazioni==1){
	print "prenotazioni";	
	$testo='<div id="contenitore_sezioni">';
	my @prenotazioni=@{database::getPrenotazioni(gestione_sessione::getParam("id"))};
	for (my $i=(scalar(@prenotazioni)-1); $i>=0; $i--)
	{
		$testo.="
		<div class=\"sezione\"><!-- apro maxi contenitore per le sezioni -->";
		my @prenotazione=@{@prenotazioni[$i]};
		@prenotazione[6]=~/([0-9]{4})-([0-9]{1,2})-([0-9]{1,2})/;
		my $giorno=int($3);
		if($giorno<10){
			$giorno="0".$giorno;
		}
		my $mese=int($2);
		if($mese<10){
			$mese="0".$mese;
		}
		my $anno=int($1);
		my $d_partenza="$giorno/$mese/$anno";
			$testo.='
			<a href="gestisci_prenotazione.cgi?id='.@prenotazione[0].'">
					<object>
						<fieldset>
							<p>Data: '.$d_partenza.'</p>
							<p>Partenza: '.@prenotazione[3].'</p>
							<p>Arrivo: '.@prenotazione[4].'</p>
							<p>Orario partenza: '.@prenotazione[7].'</p>
						</fieldset>
					</object>
				</a>';
		#my @temp=($id, $posti_occupati, "T$tratta"."V$id_volo", $aereoporto_partenza,$aereoporto_arrivo,$data_prenotazione, $data_partenza, $ora_partenza, $prezzo, $bagagli, \@servizi_prenotati); 
		$testo.="</div><!-- chiudo prenotazione -->
		<div class=\"clearer\"></div>";
	}
	$testo.='</div><!-- chiudo contenitore sezioni -->
				
			<div class="clearer"></div>';
}
print print_content::print($testo);
print "		</div>"; #chiudo il div main
print print_footer::print();
print "	</body>
</html>";