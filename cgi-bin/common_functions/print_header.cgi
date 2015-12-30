#!/usr/bin/perl
package print_header;
require      Exporter;

our @ISA       = qw(Exporter);
our $VERSION   = 1.00;         # Version number

my $menu;

#menu[x]: array (Titolo, pagina, selezionato)

sub setMenu {#@m: array contenente i vari riferimenti ai menu
	 my ($m) = @_;
	$menu=$m;
}

sub print { 
		$temp= "
		<div id=\"header\">
			<div id=\"banner\">
				<h1>Vola con noi &copy;</h1>
				<h2>Prenota il tuo volo per la destinazione che ti pare e piace :(</h2>
			</div><!-- chiudo banner-->
			
			<div id=\"menu\">
				";
				
				for( my $i=0; $i<scalar(@{$menu}); $i++){
					my @arr_temp=@{$menu->[$i]};
					$temp.="		<a href=\"".@arr_temp[1]."\"";
						if(@arr_temp[2]>0){
							$temp.=" class=\"selected\"";
						}
					$temp.="  >".@arr_temp[0]."</a>\n";
				}
				
				
			$temp.="</div><!-- chiudo menu -->
			<div class=\"clearer\"></div>
			
			<div id=\"path\">
				<span>Ti trovi in: </span>
				<!-- span class separatore_path &gt sara' la stringa aggiunta dal codice perl per la creazione
				del path -->
				<a href=\"index.html\">Home</a>
				<span class=\"separatore_path\"> &gt;</span>
				
				<a href=\"index.html\">Pagina boh</a>
				<span class=\"separatore_path\"> &gt;</span>
				
				<span>Pagina.bleah</span>
			</div><!-- chiudo path-->
		</div><!-- chiudo header-->

" ;
	return $temp;
}


1;