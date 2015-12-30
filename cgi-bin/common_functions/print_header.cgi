#!/usr/bin/perl
package print_header;
require      Exporter;

our @ISA       = qw(Exporter);
our $VERSION   = 1.00;         # Version number

my $menu; #(Titolo, pagina.html, selezionato:0/1)
my $path; #(Titolo, pagina.html)

#menu[x]: array (Titolo, pagina, selezionato)

sub setMenu {#@m: array contenente i vari riferimenti ai menu
	 my ($m) = @_;
	$menu=$m;
}
sub setPath {#@p: array contenente i vari riferimenti al path
	my ($p)=@_;
	$path=$p;
}

sub print { 
		$temp= "
		<div id=\"header\">
			<div id=\"banner\">
				<h1>Vola con noi &copy;</h1>
				<h2>Prenota il tuo volo per la destinazione che ti pare e piace :(</h2>
			</div><!-- chiudo banner-->
			
			<div id=\"menu\">\n";
				
				for( my $i=0; $i<scalar(@{$menu}); $i++){
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
			</div><!-- chiudo path-->
		</div><!-- chiudo header-->

" ;
	return $temp;
}


1;