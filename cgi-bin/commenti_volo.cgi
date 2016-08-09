#!/usr/bin/perl

#la pagina otterrà dalla precedente otterrà id volo; SE si dovessero visualizzare i commenti di + voli... basterebbe fare un ciclo, ma non so come passare tutti i voli

package seleziona_voli_page;

use strict;
use CGI::Carp qw(fatalsToBrowser);
use CGI qw(:standard);
use CGI;
#use warnings;


#require "common_functions/print_header.cgi";
#require "common_functions/print_search.cgi"; #inutile: non viene sfruttato in questa pagina.
#require "common_functions/print_content.cgi";
#require "common_functions/print_footer.cgi";
#require "common_functions/check_form.cgi";
#require "common_functions/Session.cgi";
#require "common_functions/database.cgi";
#require "common_functions/menu.cgi";

#my %form;
#foreach my $p (param()) {
#    $form{$p} = param($p);
    #print "$p = $form{$p}<br>\n";
#}

#my $idV=int($form{"idV"});


#my $create=gestione_sessione::createSession();
#gestione_sessione::setParam("location","commenti_volo.cgi");#right????

my $titolo="commenti sul volo scelto"; 

#my $session_cookie = CGI::Cookie->new(-name=>'SESSION',-value=>$create,-expires =>  '+2h',);

#print CGI::header(-cookie=>$session_cookie);#imposto il cookie di sessione

print "
<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Strict//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd\">
	<html xmlns=\"http://www.w3.org/1999/xhtml\" xml:lang=\"it\" lang=\"it\">
	<head>
		<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\"/>
			<style type=\"text/css\" media=\"screen\">
				\@import url(\"../style/main.css\"); <!--è corretto? altrimenti qui può venir usato <link rel=\"stylesheet\" href=\"../style/main.css\" type=\"text/css\" media=\"screen\" charset=\"utf-8\"/> -->
			</style>
		
		<title>Commenti sul volo</title>
		
		<meta name=\"title\" content=\"Compagnia Aerea A-ir - Commenti volo\"/>
		<meta name=\"description\" content=\"commenti effettuati dai nostri clienti sul volo richiesto\"/>
		<meta name=\"robots\" content=\"noindex, nofollow\"/> <!--contiene info che non devono venir indicizzate da google quindi credo di dover usare questo giusto????-->
		<meta name=\"language\" content=\"italian it\"/>
		<meta name=\"author\" content=\"MarAlFraMar\"/>
	</head>
	<body>
	<!-- L'ORIGINALE ERA
	<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Strict//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd\">
		<html xmlns=\"http://www.w3.org/1999/xhtml\" lang=\"it\" xml:lang=\"it\">
		<head>
			<link rel=\"stylesheet\" href=\"../style/main.css\" type=\"text/css\" media=\"screen\" charset=\"utf-8\"/>
			<title>$titolo</title>
		</head>
		<body>
	-->
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
					<a href=\"cgi-bin/login.cgi\" >Area utente</a>
				</div><!-- chiudo menu -->
				<div class=\"clearer\"></div>
			
				<div id=\"path\">
					<span>Ti trovi in: </span>
					<!-- span class separatore_path &gt sara la stringa aggiunta dal codice perl per la creazione del path -->
					<a href=\"index.html\">Home</a>
					<span class=\"separatore_path\"> &gt;</span>
					<a href=\"search.cgi\">ricerca voli</a>
					<span class=\"separatore_path\"> &gt;</span>
					<a href=\"seleziona_voli.cgi\">Seleziona i voli disponibili</a>
					<span class=\"separatore_path\"> &gt;</span>
					<span>commenti sul volo</span> <!--ANDRà MODIFICATO NELLE PAGINE SUCCESSIVE X INCLUDERLO-->
				</div><!-- chiudo path-->
			</div><!-- chiudo header-->
			<div id=\"main\">
			<div id=\"contenuto\">
			<div id=\"contenitore_sezioni\"><!-- apro maxi contenitore per le sezioni -->
				<div class=\"sezione\" id=\"S1\"><!-- inizio div che contiene titolo e sezione dell articolo -->
					<h3>La compagnia The A-ir</h3>
					<p>qui potete vedere i commenti eseguiti dai nostri clienti sul volo che avete selezionato</p>
				</div><!-- chiudo sezione -->		
";

my $c1={
	idC=>"1",
	idV=>"1",
	idUR=>"1",
	nick=>"perlHater",
	data=>"14/3/16",
	titolo=>"let it end",
	valutazione=>"5",
	testo=>"just LOVE perl, but keep calm and prorgram on"
};
my $c2={
	idC=>"2",
	idV=>"1",
	idUR=>"2",
	nick=>"perlLoveerr",
	data=>"14/3/16",
	titolo=>"les't stay for EVER",
	valutazione=>"3",
	testo=>"let's run away together my love, you can stay in my hart forever"
};
my $c3={
	idC=>"3",
	idV=>"1",
	idUR=>"1",
	nick=>"perlEndurer",
	data=>"14/3/16",
	titolo=>"i will survive",
	valutazione=> "5",
	testo=>"asd asd asd asd asd asd asd aswd asd asd asd wtfiU"
};
my $c4={
	idC=>"3",
	idV=>"2",
	idUR=>"1",
	nick=>"perlHater",
	data=>"14/3/16",
	titolo=>"i should not be here",
	valutazione=>"0",
	testo=>"ignore me"
};
#print_header::setMenu(menu::get());

#my @path_temp;
#my @path=("Home", "index.cgi");
#push @path_temp, \@path;
#my @path=("Ricerca voli", "search.cgi");
#push @path_temp, \@path;
#my @path=("Seleziona i voli disponibili", "seleziona_voli.cgi", "commenti sul volo");#modificabile nn mi ricordo dove andava esattamente
#push @path_temp, \@path;
#print_header::setPath(\@path_temp);

my $idV=1;
my $numero_C=0;
my @commenti;#={};#(c1=>\%c1, c2=>\%c2, c3=>\%c3, c4=>\%c4);#cimtiene TUTTi i commenti che abbiamo, NO ci mettiamo solo quelli utili
my $testo="";
my $i=0;
push(@commenti, $c1);
push(@commenti, $c2);
push(@commenti, $c3);
push(@commenti, $c4);
foreach my $commento (@commenti){
		my %item=%{$commento};
		$testo.="<div class=\"commento\">
					<p class=\"nomeA\">".$item{"nick"}."</p>
					<p class=\"dataC\">".$item{"data"}."</p>
					<h2 class=\"titoloC\">".$item{"titolo"}."</h2>
					<p class=\"valutazioneC\">valutazione:".$item{"valutazione"}."</p> 
					<pclass=\"testoC\">".$item{"testo"}."</p>
				</div>
				";
}

print $testo;
#print print_header::print();
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


