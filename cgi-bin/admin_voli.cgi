#!/usr/bin/perl


package pagina_utente;

use strict;
use CGI::Carp qw(fatalsToBrowser);
use CGI qw(:standard);
use CGI;


require "common_functions/print_header.cgi";
require "common_functions/print_search.cgi";
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


my $titolo="Area Amministrativa";


my $create=gestione_sessione::createSession();

if((gestione_sessione::getParam("logged")!=1) or (gestione_sessione::getParam("admin")!=1)){
	print "location: index.cgi\n\n";
	exit;
}

my $errore="";
#my ($tratta, $orario_partenza, $prezzo, $attivo,$id)=@_;
my $tratta=$form{"tratta"};
my $orario_partenza=$form{"partenza"};
my $prezzo=$form{"prezzo"};
my $attivo=$form{"attivo"};
my $volo=$form{"volo"};
if (!($form{"salva"} eq "")){
	$tratta =~/([0-9]+)([\s:\s])([a-zA-Z\s]+)([\s-\s])([a-zA-Z\s]+)([,])([\s]*)([0-9]+)/;
	my $id_tratta=$1;
	if($attivo eq ""){
			$attivo=0;
		}else{
			$attivo=1;
	}
	if(!($volo eq "")){
		$volo =~/([0-9]+)/;
		my $id_volo=$1;
		#$errore="$id_volo $orario_partenza $prezzo $attivo";
		$errore=database::addVolo($id_tratta, $orario_partenza, $prezzo, $attivo, $id_volo); 
	}else{
		#$errore="$id_tratta $orario_partenza $prezzo $attivo";
		$errore=database::addVolo($id_tratta, $orario_partenza, $prezzo, $attivo); 
	}
}
gestione_sessione::setParam("location","admin_voli.cgi");


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
my @path=("Gestione voli", "admin_voli.cgi");
push @path_temp, \@path;
print_header::setPath(\@path_temp);

print print_header::print();
print "		<div id=\"main\"><!-- div che contiene tutto il contenuto statico e/o dinamico-->"; #mega div
print '<div id="secondo_menu">
					<ul>
						<li><span>Gestione voli</span></li>
					</ul>
				</div><!-- chiudo secondo menu -->';
my $testo='<div id="contenitore_sezioni"><!-- apro maxi contenitore per le sezioni -->
					
					<div class="sezione" id="S1"><!-- inizio div che contiene titolo e sezione dell\'articolo -->
						<h3>Benvenuto!</h3>
						<p>In questa pagina modificare i vari parametri inerenti agli aereoporti, citt&agrave; ecc...</p>
					</div><!-- chiudo sezione -->
					<div class="sezione">
						<form action="admin_voli.cgi" method="post">
							<fieldset>
								<h3>Modifica un volo</h3>'.$errore.'
								<div>
									<label for="volo">Volo:</label>
									<select id="volo" name="volo">
										<option>-</option>';
										my @voli=@{database::getVoli_totali()};
										foreach my $volo (@voli){
											my @v=@{$volo};
											$testo.= "<option>@v[0]: ora partenza: @v[1], partenza: @v[2] arrivo: @v[3], @v[4]&euro;</option>";
									}
								$testo.='	</select>
								</div>
								<div class="clearer"></div>
								<div>
									<label for="tratta">Tratta:</label>
									<select id="tratta" name="tratta">
										<option>-</option>';
										my @tratte=@{database::getTratta()};
								foreach my $tratta (@tratte){
									my @tmp=@{$tratta};
										$testo.="<option>@tmp[0]: @tmp[1] - @tmp[2], @tmp[3] minuti</option>";
								
								}
								$testo.='	</select>
								</div>
								<div class="clearer"></div>	
								<div>
									<label for="partenza">Partenza:</label>
									<input type="text" id="partenza" name="partenza" value="08:00"></input>
								</div>
								<div class="clearer"></div>
								<div>
									<label for="prezzo">Prezzo &euro;:</label>
									<input type="text" id="prezzo" name="prezzo" value="12"></input>
								</div>
								<div class="clearer"></div>
								<div>
									<label for="attivo">Attivo </label>
									<input type="checkbox" id="attivo" name="attivo" value="1"></input>
								</div>
								<div class="clearer"></div>
								
								<div>
									<button type="submit" id="salva" name="salva" value="salva">
										<span>modifica</span>
									</button>
								</div>
							</fieldset>
						</form>
					</div>
					<div class="clearer"></div>
					<!-- fine sezione -->
					<div class="sezione">
						<form action="admin_voli.cgi" method="post">
							<fieldset>
								<h3>Aggiungi un volo</h3>'.$errore.'';
								
								$testo.='
								<div class="clearer"></div>
								<div>
									<label for="tratta">Tratta:</label>
									<select id="tratta" name="tratta">
										<option>-</option>';
										my @tratte=@{database::getTratta()};
										foreach my $tratta (@tratte){
											my @tmp=@{$tratta};
										$testo.="<option>@tmp[0]: @tmp[1] - @tmp[2], @tmp[3] minuti</option>";
								
								}
								$testo.='	</select>
								</div>
								<div class="clearer"></div>	
								<div>
									<label for="partenza">Partenza:</label>
									<input type="text" id="partenza" name="partenza" value="08:00"></input>
								</div>
								<div class="clearer"></div>
								<div>
									<label for="prezzo">Prezzo &euro;:</label>
									<input type="text" id="prezzo" name="prezzo" value="12"></input>
								</div>
								<div class="clearer"></div>
								<div>
									<label for="attivo">Attivo </label>
									<input type="checkbox" id="attivo" name="attivo" value="1"></input>
								</div>
								<div class="clearer"></div>
								
								<div>
									<button type="submit" id="salva" name="salva" value="salva">
										<span>aggiungi</span>
									</button>
								</div>
							</fieldset>
						</form>
					</div>
					<div class="clearer"></div>
					<!-- fine sezione -->
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