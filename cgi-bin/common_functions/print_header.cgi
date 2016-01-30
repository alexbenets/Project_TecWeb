#!/usr/bin/perl
package print_header;
require      Exporter;

require "common_functions/Session.cgi";


our @ISA       = qw(Exporter);
our $VERSION   = 1.00;         # Version number

local $menu; #(Titolo, pagina.html, selezionato:0/1)
local $path; #(Titolo, pagina.html)

#menu[x]: array (Titolo, pagina, selezionato)

sub setMenu {#@m: array contenente i vari riferimenti ai menu
	 local ($m) = @_;
	$menu=$m;
}
sub setPath {#@p: array contenente i vari riferimenti al path
	local ($p)=@_;
	$path=$p;
}

sub print { 
		gestione_sessione::createSession();
		$temp= "
		<div id=\"header\">
			<div id=\"banner\">
				<h1>Vola con noi &copy;</h1>
				<h2>Prenota il tuo volo per la destinazione che ti pare e piace :(</h2>";
		if(gestione_sessione::getParam("logged")==1){
			$temp.="<h3>Benvenuto, ".gestione_sessione::getParam("nome").' (<a href="login.cgi?logout=1">esci</a>)</h3>';
		}		
		else
		{
			$temp.='<h3>Benvenuto, per prenotare devi <a href="login.cgi">effettuare il login</a> o <a href="registrati.cgi">la registrazione</a></h3>';
		}
		$temp.="	</div><!-- chiudo banner-->
			
			<div id=\"menu\">\n";
				
				for( local $i=0; $i<scalar(@{$menu}); $i++){
					my @arr_temp=@{$menu->[$i]};
					$temp.="				<a href=\"".@arr_temp[1]."\"";
						if(@arr_temp[2]>0){
							$temp.=" class=\"selected\"";
						}
					$temp.="  >".@arr_temp[0]."</a>\n";
				}
				
				
			$temp.="			</div><!-- chiudo menu -->
			<div class=\"clearer\"></div>
			
			<div id=\"path\">
				<span>Ti trovi in: </span>\n";
				
				for( my $i=0; $i<scalar(@{$path}); $i++){ #estraggo la dimensione dell'array dal riferimento dell'array
					my @arr_temp=@{$path->[$i]}; #estraggo l'array dal riferimento dell'array in posizione [$i]
					if($i<(scalar(@{$path})-1)){ #fino a quando non è il penultimo elemento
						$temp.="				<a href=\"".@arr_temp[1]."\">".@arr_temp[0]."</a>\n";
						
						$temp.="				<span class=\"separatore_path\"> &gt;</span>\n";
					}else { #se è l'ultimo elemento, allora è inutile che venga stampato il link alla pagina, visto che sono già lì!
						$temp.="				<span>".@arr_temp[0]."</span>";
					}
				}
				$temp.="
			</div><!-- chiudo path-->";
		
		$temp.="</div><!-- chiudo header-->

" ;
	return $temp;
}


1;