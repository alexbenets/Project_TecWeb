#!/usr/bin/perl


package index_page;

use strict;

use CGI qw(:standard);
use CGI;



require "common_functions/print_header.cgi";
require "common_functions/print_search.cgi";
require "common_functions/print_content.cgi";
require "common_functions/print_footer.cgi";


my %form;


foreach my $p (param()) {
    $form{$p} = param($p);
    #print "$p = $form{$p}<br>\n";
}

my $nome=$form{"Nome"};
my $cognome=$form{"Cognome"};
my $codice_fiscale=$form{"CF"};
my $nascita=$form{"nascita"};
my $email=$form{"email"};
my $password=$form{"password"};


sub registrati {

}

my $titolo="Home";

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

my $errore= (($nome eq "" & defined ($nome))?1:0)+
			(($cognome eq "" & defined ($cognome))?2:0)+
			(($codice_fiscale eq "" & defined ($codice_fiscale))?4:0)+
			(($nascita eq "" & defined ($nascita))?8:0)+
			(($email eq "" & defined ($email))?16:0)+
			(($password eq "" & defined ($password))?32:0);
if($errore==0){#se il campo non è ancora stato compilato...
	$nome="Nome";
	$cognome="Cognome";
	$codice_fiscale="CODICE FISCALE";
	$nascita="32/02/1920";
	$email="info\@example.org";
	$password="password";
}
print print_header::print();
print "	<div id=\"main\"><!-- div che contiene tutto il contenuto statico e/o dinamico-->"; #mega div
my $testo="<div class=\"sezione\">
					<form action=\"registrati.cgi\" method=\"post\">
						<fieldset>";
if($errore>0){
	$testo.="<p class=\"errore\">Errore: devi compilare correttamente tutti i campi!</p>";
}						
$testo.="							<div>
								<h3>Per acquistare i biglietti, registrati inserendo i tuoi dati!</h3>
							</div>
							<div>
								<label for=\"Nome\">Nome: </label>
								<input type=\"text\" id=\"Nome\" name=\"Nome\" class=\"";
if($errore & 1>0){
	$testo.="errore";
}
$testo.="\" value=\"$nome\"></input>
								<div class=\"clearer\"></div>
							</div>
							<div>
								<label for=\"Cognome\">Cognome: </label>
								<input type=\"text\" id=\"Cognome\" name=\"Cognome\" class=\"";
if($errore & 2>0){
	$testo.="errore";
}
$testo.="\" value=\"$cognome\"></input>
								<div class=\"clearer\"></div>
							</div>
							<div>
								<label for=\"CF\">Codice Fiscale: </label>
								<input type=\"text\" id=\"CF\" name=\"CF\" class=\"";
if($errore & 4>0){
	$testo.="errore";
}
$testo.="\" value=\"$codice_fiscale\"></input>
								<div class=\"clearer\"></div>
							</div>
							<div>
								<label for=\"nascita\">Data di nascita: </label>
								<input type=\"text\" id=\"nascita\" name=\"nascita\" class=\"";
if($errore & 8>0){
	$testo.="errore";
}
$testo.="\" value=\"$nascita\"></input>
								<div class=\"clearer\"></div>
							</div>
							<div>
								<label for=\"email\">E-mail: </label>
								<input type=\"text\" id=\"email\" name=\"email\" class=\"";
if($errore & 16>0){
	$testo.="errore";
}
$testo.="\" value=\"$email\"></input>
								<div class=\"clearer\"></div>
							</div>
							<div>
								<label for=\"password\">Password: </label>
								<input type=\"password\" id=\"password\" name=\"password\" class=\"";
if($errore & 32>0){
	$testo.="errore";
}
$testo.="\" value=\"$password\"></input>
								<div class=\"clearer\"></div>
							</div>
							<div>
								<button type=\"submit\">
									<span>Registrati</span>
								</button>
							</div>
						</fieldset>
					</form>
				</div>
				<div class=\"clearer\"></div></div><!-- chiudo contenuto-->";
print print_content::print($testo);
print "		"; #chiudo il div main
print print_footer::print();
print "	</body>
</html>";