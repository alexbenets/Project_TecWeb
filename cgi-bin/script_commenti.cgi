#!/usr/bin/perl
package commenti;
use strict;
use DateTime;  #utilizzato per validare la data inserita
use Time::Piece;
use CGI::Carp qw(fatalsToBrowser);
use CGI qw(:standard);
use CGI;
my $q = new CGI; #parte maria, forse userò l'altro metodo wait


#require "common_functions/print_header.cgi";
#require "common_functions/print_search.cgi"; #inutile: non viene sfruttato in questa pagina.
#require "common_functions/print_content.cgi";
#require "common_functions/print_footer.cgi";
#require "common_functions/Session.cgi";
#require "common_functions/check_form.cgi";
#require "common_functions/database.cgi";
#require "common_functions/menu.cgi";

#parte iniziale per la corretta visualizzazione della pagina

# NB !!! %form dovrebbe essere inutile xke non viene passato niente mediante il link
#my %form;


#foreach my $p (param()) {
#    $form{$p} = param($p);
    #print "$p = $form{$p}<br>\n";
# 

#my $id_prenotazione=int($form{"idP"}); 
#my $idUR=gestione_sessione::getParam("id");
#my $titolo="Area utente";


#my $create=gestione_sessione::createSession();

#if(gestione_sessione::getParam("logged")!=1){
#	print "location: index.cgi\n\n";
#	exit;
#}

#gestione_sessione::setParam("location","utente.cgi");


#my $session_cookie = CGI::Cookie->new(-name=>'SESSION',-value=>$create,-expires =>  '+2h',);

#print CGI::header(-cookie=>$session_cookie);#imposto il cookie di sessione

print "
<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Strict//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd\">
<html xmlns=\"http://www.w3.org/1999/xhtml\" xml:lang=\"it\" lang=\"it\">
	<head>
		
		<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\"/>
		
		<style type=\"text/css\" media=\"screen\">
			\@import url(\"../style/main.css\");
		</style>
		
		<title>Commenti sul volo</title>
		
		<meta name=\"title\" content=\"Compagnia Aerea A-ir - Commenti untente\"/>
		<meta name=\"description\" content=\"script per la manipolazione dei commenti effettuati dall'utente\"/>
		<meta name=\"robots\" content=\"noindex, nofollow\"/> <!--contiene info che non devono venir indicizzate da google quindi credo di dover usare questo giusto????-->
		<meta name=\"language\" content=\"italian it\"/>
		<meta name=\"author\" content=\"MarAlFraMar\"/>
		
	</head>
	
	<body>
		<div id=\"header\">
			<div id=\"logo\">
				
			</div>
			<div id=\"banner\">
				<h1>The A<span>-IR &copy;</span></h1>
				<h2>Si alza il vento, vola con Noi!</h2>
				
				<div id=\"description\">
					<span>Sito web adibito alla prenotazione di un volo aereo low cost</span>
				</div>
			</div><!-- chiudo banner-->
			
			<div id=\"menu\">
				<a href=\"index.html\" >Home</a>
				<a href=\"compagnia.html\">Compagnia</a>
				<a href=\"servizi.html\" >Servizi</a>
				<a href=\"cgi-bin/login.cgi\" class=\"selected\" >Area utente</a>
			</div><!-- chiudo menu -->
			<div class=\"clearer\"></div>
			
			<div id=\"path\">
				<span>Ti trovi in: </span>
				<!-- span class separatore_path &gt sara la stringa aggiunta dal codice perl per la creazione
				del path -->
				<a href=\"index.html\">Home</a>
				<span class=\"separatore_path\"> &gt;</span>
				<a href=\"index.html\">Area Utente</a>
				<span class=\"separatore_path\"> &gt;</span>
				<a href=\"index.html\">Commenti</a>
				<span class=\"separatore_path\"> &gt;</span>
				<span>Manipola Commenti</span>
			</div><!-- chiudo path-->
		</div><!-- chiudo header-->
		
		<div id=\"main\"><!-- div che contiene tutto il contenuto statico e/o dinamico-->
		<div id=\"contenuto\">	
			<div id=\"secondo_menu\">
				<ul>
					<li><a href=\"utente.cgi?dati=1\">Dati personali</a></li>
					<li><a href=\"utente.cgi?prenotazioni=1\">Prenotazioni</a></li>
					<li><a href=\"utente.cgi\" class=\"selected\">Commenti</a></li>
				</ul>
			</div><!-- chiudo secondo menu -->
		<div id=\"contenitore_sezioni\"><!-- apro maxi contenitore per le sezioni -->
			<div class=\"sezione\" id=\"S1\"><!-- inizio div che contiene titolo e sezione dell\'articolo -->
";
#print_header::setMenu(menu::get());
#my @path_temp;
#my @path=("Home", "index.cgi");
#push @path_temp, \@path;
#my @path=("Area utente", "utente.cgi");
#push @path_temp, \@path;
#print_header::setPath(\@path_temp);

#print print_header::print();
#print "		<div id=\"main\"><!-- div che contiene tutto il contenuto statico e/o dinamico-->"; #mega div
#print '<div id="secondo_menu">
#					<ul>
#						<li><a href="utente.cgi?dati=1">Dati personali</a></li>
#						<li><a href="utente.cgi?prenotazioni=1">Prenotazioni</a></li>
#						<li><a href="utente.cgi">Commenti</a></li>
#					</ul>
#				</div><!-- chiudo secondo menu -->';
#my $testo='<div id="contenitore_sezioni"><!-- apro maxi contenitore per le sezioni -->
					
#					<div class="sezione" id="S1"><!-- inizio div che contiene titolo e sezione dell\'articolo -->
#						<h3>Benvenuto!</h3>
#						<p>In questa pagina potrai manipolare il commento espresso sul volo prenotato mediante la prenotazione che hai selezionato.</p>
#					</div><!-- chiudo sezione -->
					
#					<div id="torna_su">
#						<a href="#header">Torna su</a>
#					</div>
#				';

#done parte iniziale di visualizzazione pagina 

#form da manipolare NB SERVE UNA FUNZIONE PER VALIDARLA
#SE la form deve essere SALVATA
#la funzione controllerà se esistono campi vuoti:
#se il select valutazione è vuoto ""=>$errore.=non è stata  impostata una valutazione
#se il titolo è ""=>$errore.=non si è dato titolo al commento
#se il testo è""=>$errore.=il commento è vuoto
#puo esseci solo voto o solo commento con titolo MA l'utente deve dare conferma che è proprio quello che vuole inserire(!!! troppo complicato?)
#SE INVECE la form va ELIMINATA
#chiedo conferma e chiudo

my $error_count=0;
my $idC = $q->param('idC');
my $idV = $q->param('idV');
my $idUR=$q->param('idUR');
my $cittaP= $q->param('cittaP');
my $cittaA= $q->param('cittaA');
my $valutazione = $q->param('valutazione');
my $titolo = $q->param('titolo');
my $testoC= $q->param('testo');

#local ($buffer, @pairs, $pair, $name, $value, %FORM);
    # Read in text
#   $ENV{'REQUEST_METHOD'} =~ tr/a-z/A-Z/;
#  if ($ENV{'REQUEST_METHOD'} eq "POST")
#   {
#       read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
#   }else {
#	$buffer = $ENV{'QUERY_STRING'};
#   }
    # Split information into name/value pairs
#   @pairs = split(/&/, $buffer);
#   foreach $pair (@pairs)
#   {
#	($name, $value) = split(/=/, $pair);
#	$value =~ tr/+/ /;
#	$value =~ s/%(..)/pack("C", hex($1))/eg;
#	$FORM{$name} = $value;
#   }

my $form_control="
				<h3>Il Commento sul volo $idV da $cittaP a $cittaA non è stato salvato perchè poco informativo</h3>
				<p>per essere considerato valido il commento deve contenere almeno il campo \"testo compilato\"</p>	
				<div class=\"commento\">
					<form action=\"script_commenti.cgi\" method=\"post\"> 
						<fieldset>
							<legend>commento</legend>
							<input type=\"hidden\" name=\"idC\" value=\"$idC\"></input><
							<input type=\"hidden\" name=\"idV\" value=\"$idV\"></input>
							<input type=\"hidden\" name=\"idUR\" value=\"$idUR\"></input>
							<input type=\"hidden\" name=\"cittaP\" value=\"$cittaP\"></input>
							<input type=\"hidden\" name=\"cittaA\" value=\"$cittaA\"></input>
							<label for=\"valutazione\">Valutazione:</label>
							<select name=\"valutazione\">
								<option value=\"0\" checked=\"checked\">non valutato</option>
								<option value=\"1\">1</option>
								<option value=\"2\">2</option>
								<option value=\"3\">3</option>
								<option value=\"4\">4</option>
								<option value=\"5\">5</option>
							</select>
							</br>
							</br>
							<label for=\"titolo\">Titolo:</label>
								<input type=\"text\" name=\"titolo\" id=\"titolo\">$titolo</input></br>
							<label for=\"testo\">Testo:</label>
								<textarea name=\"testo\" rows=\"5\" cols=\"30\">$testoC</input></br>
							<input type=\"hidden\" name=\"action\" value=\"salva\"></input>	
							<input type=\"submit\" value=\"Salva\"></input>
						</fieldset>
					</form>
					</div>
				</div><!-- chiudo sezione -->
					";
  
if ($testoC=~m\ \){#$testoC==NULL
	print $form_control;
}
else{
	print "<h3>Commento sul volo $idV da $cittaP a $cittaA</h3>
				<p>Il commento è stato salvato</p>
				<div class=\"commento\">
					<p class=\"nomeA\">perlIsaBICH</p>
					<p class=\"dataC\">14/5/16</p>
					<h2 class=\"titoloC\">to BE free IS my ONLY desire</h2>
					<p class=\"valutazioneC\">valutazione: 4</p> 
					<p class=\"testoC\">let it END</p>
				</div>
			</div>";
}
print "<div id=\"torna_su\">
						<a href=\"#header\">Torna su</a>
					</div>
				</div><!-- chiudo contenitore_sezioni -->	
				
				<div class=\"clearer\"></div>
			</div><!-- chiudo contenuto-->
		</div><!-- chiudo main-->
		
		<div id=\"footer\">
			<div id=\"sitemap\">
				<a href=\"#\">Mappa del sito</a>
			</div> <!-- chiudo sitemap -->
			<div id=\"dati_aziendali\">
				<p>Si alza il vento, vola con Noi!</p>
				<p>P.IVA: Zanicchi</p>
			</div><!-- chiudo dati aziendali -->
			<div id=\"gruppo\">
				<p>An project by: MarAlFraMar</p>
			</div><!-- chiudo div del gruppo -->
			<div id=\"validazione\">
				<p class=\"html_valido\">
    				<a href=\"http://validator.w3.org/check?uri=referer\">
						<img src=\"http://www.w3.org/Icons/valid-xhtml10\" alt=\"Valid XHTML 1.0 Strict\" height=\"31\" width=\"88\" />
					</a>
	  			</p>
				<p class=\"css_valido\">
					<a href=\"http://jigsaw.w3.org/css-validator/check/referer\">
    					<img style=\"border:0;width:88px;height:31px\" src=\"http://jigsaw.w3.org/css-validator/images/vcss-blue\" alt=\"CSS Valido!\" />
    				</a>
				</p>
				<div class=\"clearer\"></div> <!-- chiudo i float -->
			</div><!-- chiudo div validazione -->
		</div><!-- chiudo footer-->
	</body>
</html>";
