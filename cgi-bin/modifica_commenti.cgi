#div main chiuso prima del dovuto!
#!/usr/bin/perl

#package commenti;
use strict;
use CGI::Carp qw(fatalsToBrowser);
use CGI qw(:standard);
use CGI;
use DateTime;  #utilizzato per validare la data inserita

#require "common_functions/print_header.cgi";
#require "common_functions/print_search.cgi"; #inutile: non viene sfruttato in questa pagina.
#require "common_functions/print_content.cgi";
#require "common_functions/print_footer.cgi";
#require "common_functions/Session.cgi";
#require "common_functions/check_form.cgi";
#require "common_functions/database.cgi";
#require "common_functions/menu.cgi";

#pagina per la creazione di nuovi commenti o la modifica/eliminazione
#deve ricevere dei parametri dalla pagina di visualizzazione: idP dal quale ricavare idUR, idV ( e se serve idCommento, datacommento, titolo, contenuto, voto(se esiste, zero altrimenti))

#my %form;
#foreach my $p (param()) {
#    $form{$p} = param($p);
    #print "$p = $form{$p}<br>\n";
#}

#my $idPrenotazione=int($form{"idP"}); 
#my $titolo="Area utente";
#my $idUR=gestione_sessione::getParam("id");  

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
		
		<meta http-equiv=\"Content-Type\" content=\"text/html; charset=\"utf-8\"/>
		
		<style type=\"text/css\" media=\"screen\">
			\@import url(\"style/main.css\");
		</style>
		
		<title>Manipolazione Commento</title>
		
		<meta name=\"title\" content=\"Compagnia Aerea A-ir - Salva Commenti\"/>
		<meta name=\"description\" content=\"form per la manipolazione dei commenti effettuati dall'utente\"/>
		<meta name=\"robots\" content=\"noindex, nofollow\"/> <!--contiene info che non devono venir indicizzate da google quindi credo di dover usare questo giusto???? ma validatore nn approva-->
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
		
		<div id=\"main\"><!-- divisore che contiene tutto il contenuto statico e/o dinamico-->
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
				<h3>Benvenuto!</h3>
				<p>In questa pagina potrai manipolare il commento espresso sul volo prenotato mediante la prenotazione che hai selezionato.</p>
			</div><!-- chiudo sezione -->
			<div class=\"commento\">
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
#						<p>In questa pagina potrai scrivere, modificare, eliminare commenti che vuoi esprimere sulla tua esperienza di volo con noi.</p>
#				</div><!-- chiudo sezione -->
					
#					<div id="torna_su">
#						<a href="#header">Torna su</a>
#					</div>';

#fine di parte copiata che dovrebbe formare la parte comune a tutte le pagine del sito
#i dati di questa dovrebbero essere presi dal database

my $idC=1;
my $idV=1;
my $idUR=1;
my $cittaP="uno";
my $cittaA="due";

my %c1={
	idC=> $idC,
	idV=>$idV,
	idUR=>$idUR,
	cittaP=>$cittaP,
	cittaA=>$cittaA,
	nick=>"perlHater",
	data=>"14/3/16",
	titolo=>"let it end",
	valutazione=>"5",
	testo=>"just LOVE perl, but keep calm and prorgram on"
};
my $today=Time::Piece->new();
my $form_comm="";
if(1){#se esiste 1 commento gia eseguito su quel volo qui dato x scontato, in azione dovremo eseguire 1 chiamata al database x saperlo
	$form_comm="<form action=\"script_commenti.cgi\" method=\"post\">  <!--modifica così che passi i dati da utente-->
	<fieldset>
		<legend>commento sul volo da $c1{cittaP} a $c1{cittaA}</legend>
			<input type=\"hidden\" name=\"idC\" value=\"$c1{idC}\"></input> <!--DUBBIO INFAME COSì CONTIENE I DATI CHE DEVE CONTENERE? -->
			<input type=\"hidden\" name=\"idV\" value=\"$c1{idV}\"></input>
			<input type=\"hidden\" name=\"idUR\" value=\"$c1{idUR}\"></input>
			<input type=\"hidden\" name=\"cittaP\" value=\"$c1{cittaP}\"></input>
			<input type=\"hidden\" name=\"cittaP\" value=\"$c1{cittaA}\"></input>
			</br>
				<label for=\"titolo\">Titolo:</label>
					<input type=\"text\" name=\"titolo\" id=\"titolo\" value=\"$c1{\"titolo\"}\"></input>#come assicurarsi che sia visibile la cosa giusta?
			</br>
			<label for=\"valutazione\">Valutazione:</label>
				<select name=\"valutazione\">";
	for(my $i=1;$i<5; $i++){
		if($i==$c1{"valutazione"}){#potrei dover usare un match? ma è un semplice intero... sarebbe $i=~m/$commento{"valutazione"}/?
				$form_comm.="<option value=\"$i\" selected=\"selected\">$i</option>";
			}
			else{
				$form_comm.="<option value=\"$i\">$i</option>";
			}
		}
	}
	$form_comm.="</select>
				</br>
				</br>
				<label for=\"testo\">Testo:</label>
					<textarea name=\"testo\" rows=\"5\" cols=\"30\"></textarea></br>
					<input type=\"submit\" value=\"submit\"></input>
			</fieldset>
		</form>";
}
else{
	$form_comm="<form>
				<fieldset action=\"script_commenti.cgi\" method=\"post\">
					<legend>nuovo commento sul volo da $cittaP a $cittaA</legend>
					<input type=\"hidden\" name=\"idC\" value=\"0\"></input>
					<input type=\"hidden\" name=\"idV\" value=\"$idV\"></input>
					<input type=\"hidden\" name=\"idUR\" value=\"$idUR\"></input>
					<input type=\"hidden\" name=\"cittaP\" value=\"$cittaP\"></input>
					<input type=\"hidden\" name=\"cittaA\" value=\"$cittaA\"></input>
				</br>
				<label for=\"titolo\">Titolo:</label>
				<input type=\"text\" name=\"titolo\"></input></br>
				</br>
				<label for=\"valutazione\">Valutazione:</label>
				<select name=\"valutazione\">
					<option value=\"0\" selected=\"selected\"></option>
					<option value=\"1\">1</option>
					<option value=\"2\">2</option>
					<option value=\"3\">3</option>
					<option value=\"4\">4</option>
					<option value=\"5\">5</option>
				</select>
				</br>
				<label for=\"testo\">Testo:</label>
				<textarea name=\"testo\" rows=\"5\" cols=\"30\"></textarea></br>
				<input type=\"submit\" value=\"Salva\"></input>
				</fieldset>
			</form>";
}
print $form_comm;
print "
</div>
	<div id=\"torna_su\">
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
			</div><!-- chiudo divisore validazione -->
		</div><!-- chiudo footer-->
	</body>
</html>";


#form da manipolare NB SERVE UNA FUNZIONE PER VALIDARLA
#SE la form deve essere SALVATA
#la funzione controllerà se esistono campi vuoti:
#se il select valutazione è vuoto ""=>$errore.=non è stata  impostata una valutazione
#se il titolo è ""=>$errore.=non si è dato titolo al commento
#se il testo è""=>$errore.=il commento è vuoto
#puo esseci solo voto o solo commento con titolo MA l'utente deve dare conferma che è proprio quello che vuole inserire(!!! troppo complicato?)
#SE INVECE la form va ELIMINATA
#chiedo conferma e chiudo

#$testo.= '</div>	
#		<div class="clearer"></div>';

#print print_content::print($testo);
#print "		</div>"; #chiudo il div main
#print print_footer::print();
#print "	</body>
#</html>";
