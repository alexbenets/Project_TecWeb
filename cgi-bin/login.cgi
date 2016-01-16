#!/usr/bin/perl


package index_page;

use strict;

use CGI qw(:standard);
use CGI;



require "common_functions/print_header.cgi";
require "common_functions/print_search.cgi";
require "common_functions/print_content.cgi";
require "common_functions/print_footer.cgi";
require "common_functions/Session.cgi";

my %form;


foreach my $p (param()) {
    $form{$p} = param($p);
    #print "$p = $form{$p}<br>\n";
}

my $email=$form{"email"};
my $password=$form{"password"};

my $titolo="Login";

my $create=gestione_sessione::createSession();

my $location=gestione_sessione::getParam("location"); #variabile che contiene la pagina a cui ero prima (per esempio, se mi chiede il login durante la registrazione, allora tornerò là.
if(!defined($location)){#se la variabile di sessione non è definita
	$location="index.cgi";
}
if (gestione_sessione::getParam("logged") == 1){
		print "Location: $location\n\n";
		exit;
}
if(defined($email) and defined($password)){
	if(0){ #se la combinazione di nome utente e password esistono o l'utente ha già effettuato l'accesso
		gestione_sessione::setParam("logged","1");
		print "Location: $location\n\n";
		exit;
	}
}

my $session_cookie = CGI::Cookie->new(-name=>'SESSION',-value=>$create,-expires =>  '+2h',);

print CGI::header(-cookie=>$session_cookie);#imposto il cookie di sessione

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

my $testo="
	<div class=\"sezione\">
		<form action=\"login.cgi\" method=\"post\">
			<fieldset>";
			if(defined($email) or defined($password)){
				$testo.="
					<div>
						<p class=\"errore\">E-MAIL O PASSWORD NON VALIDI</p>
					</div>
				";
			}
$testo.="		<div>
					<label for=\"email\">E-mail</label>
					<input type=\"text\" id=\"email\" name=\"email\" ";
					if(defined($email)){# email non valida
						$testo.="class=\"errore\"";
					}else{
						$email="Email\@example.org";
					}
					$testo.=" value=\"$email\"></input>
					<div class=\"clearer\"></div>
				</div>
				<div>
					<label for=\"password\">Password</label>
					<input type=\"password\" id=\"password\" name=\"password\" ";
					if(defined($password)){# email non valida
						$testo.="class=\"errore\"";
					}else {
						$password="password";
					}
					$testo.=" value=\"$password\"></input>
					<div class=\"clearer\"></div>
				</div>
				<div>
					<button type=\"submit\">
									<span>Login</span>
					</button>
				</div>
				<div>
					<p>
						<span>Non sei ancora registrato?</span>
						<a href=\"registrati.cgi\">Registrati!</a>
					</p>
				</div>
			</fieldset>
		</form>
	</div>
";

print print_content::print($testo);
print "		</div>"; #chiudo il div main
print print_footer::print();
print "	</body>
</html>";