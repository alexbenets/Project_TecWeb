#la pagina otterrà dalla precedente otterrà id volo; SE si dovessero visualizzare i commenti di + voli... basterebbe fare un ciclo, ma non so come passare tutti i voli
#!/usr/bin/perl


package seleziona_voli_page;

use strict;
use CGI::Carp qw(fatalsToBrowser);
use CGI qw(:standard);
use CGI;
#use warnings;


require "common_functions/print_header.cgi";
#require "common_functions/print_search.cgi"; #inutile: non viene sfruttato in questa pagina.
require "common_functions/print_content.cgi";
require "common_functions/print_footer.cgi";
require "common_functions/check_form.cgi";
require "common_functions/Session.cgi";
require "common_functions/database.cgi";
require "common_functions/menu.cgi";

my %form;
foreach my $p (param()) {
    $form{$p} = param($p);
    #print "$p = $form{$p}<br>\n";
}

my $idV=int($form{"idV"});

#subroutines

sub find_comm($idV, $arr_ref){	#secondo par contiene rif a array dove mettere i dati
	($idV, $arr_ref)=_@;
	open (comm, "file_commenti.txt") or die "could not open file";
	my 
	while(<comm>){
		$line=_$;
		chomp ($line);
		my $temp.=$line;
		my $ok=NULL;
		if($line=~m/idV=$idV/){
			$ok=1;
		}
		if($line!=~m/;/){
			$temp.=$line;
		}
		else{
			if($ok){
				push($arr_comm, $temp);
			}
			else{
				$temp=NULL;
			}
		}
	}
	return arr_comm;
}

#subroutines end

my $create=gestione_sessione::createSession();
gestione_sessione::setParam("location","commenti_volo.cgi");#right????

my $titolo="commenti sul volo scelto"; 

my $session_cookie = CGI::Cookie->new(-name=>'SESSION',-value=>$create,-expires =>  '+2h',);

print CGI::header(-cookie=>$session_cookie);#imposto il cookie di sessione

print "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Strict//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd\">
<html xmlns=\"http://www.w3.org/1999/xhtml\" lang=\"it\" xml:lang=\"it\">
	<head>
		<link rel=\"stylesheet\" href=\"../style/main.css\" type=\"text/css\" media=\"screen\" charset=\"utf-8\"/>
		<title>$titolo</title>
	</head>
	
	<body>
";


print_header::setMenu(menu::get());

my @path_temp;
my @path=("Home", "index.cgi");
push @path_temp, \@path;
my @path=("Ricerca voli", "search.cgi");
push @path_temp, \@path;
my @path=("Seleziona i voli disponibili", "seleziona_voli.cgi", "commenti sul volo");#modificabile nn mi ricordo dove andava esattamente
push @path_temp, \@path;
print_header::setPath(\@path_temp);



print print_header::print();
print "		<div id=\"main\"><!-- div che contiene tutto il contenuto statico e/o dinamico-->"; #mega div


print_header::setMenu(menu::get());

my @path_temp;
my @path=("Home", "index.cgi");
push @path_temp, \@path;
my @path=("Ricerca voli", "search.cgi");
push @path_temp, \@path;
my @path=("Seleziona i voli disponibili", "seleziona_voli.cgi");
push @path_temp, \@path;
my @path=("Inserisci i dati dei passeggeri", "dati_passeggeri.cgi");
push @path_temp, \@path;
my @path=("Seleziona i servizi aggiuntivi", "servizi_aggiuntivi.cgi");
push @path_temp, \@path;
print_header::setPath(\@path_temp);



print print_header::print();
print "		<div id=\"main\"><!-- div che contiene tutto il contenuto statico e/o dinamico-->"; #mega div
my $testo="<div class=\"sezione\">";

#here's the fun
my @arr_comm=NULL;
my $arr_ref=\@arr_comm;
$arr_ref=&find_comm($idV, $arr_ref);
foreach $el (@arr_comm){#cosi si trova il numero di elementi in un array giusto?
#argh spacchetta 1 elemento e stampalo x volta
$el=~s\&\ \ \;
$testo.="<p>$el</p>" #sorry too sleepy to think anymoore 
}

print print_content::print($testo);
print "		</div>"; #chiudo il div main
print print_footer::print();
print "	</body>
</html>";




