#!/usr/bin/perl


package seleziona_voli_page;

use strict;
use CGI::Carp qw(fatalsToBrowser);
use CGI qw(:standard);
use CGI;
#use warnings;


require "common_functions/print_header.cgi";
require "common_functions/print_search.cgi";
require "common_functions/print_content.cgi";
require "common_functions/print_footer.cgi";
require "common_functions/check_form.cgi";
require "common_functions/Session.cgi";


sub getVoli
{
	my ($giorno, $partenza, $arrivo, $passeggeri, $n)=@_;

	my @voli;
	for (my $i=0; $i<$n; $i++){
		my @volo=('AZ000'.$i, '8:00', '10:00', '160', '4.75', $giorno);
		push @voli, \@volo; 
	}
	return \@voli;
}

my %form;
foreach my $p (param()) {
    $form{$p} = param($p);
    #print "$p = $form{$p}<br>\n";
}

my $create=gestione_sessione::createSession();
gestione_sessione::setParam("location","/cgi-bin/seleziona_voli.cgi");


#dati recuperati dalle variabili di sessione

my $andata=gestione_sessione::getParam("AR");
my $select_partenza=gestione_sessione::getParam("partenza");
my $select_arrivo=gestione_sessione::getParam("arrivo");
my $data_partenza=gestione_sessione::getParam("data_partenza");
my $data_ritorno=gestione_sessione::getParam("data_ritorno");
my $select_passeggeri=gestione_sessione::getParam("passeggeri");

#$andata=0;
#$select_partenza="Milano - Linate";
#$select_arrivo="Roma - Fiumicino";
#$data_partenza="31/01/2016";
#$data_ritorno="28/02/2016";
#$select_passeggeri=2;



my $titolo="Seleziona il tuo volo";



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

my $date_tabella='';
for(my $dd=-3; $dd<=3; $dd++){
	#da -6 giorni a + 6 giorni
	my $gma=check_form::regexp_data($data_partenza);
	my $giorno=$gma->[0];
	my $mese=$gma->[1];
	my $anno=$gma->[2];
	my $dt2 = DateTime->new( 
					year       => $anno,
      				month      => $mese,
      				day        => $giorno
      				);
	$dt2=$dt2->add(days =>$dd);
	$date_tabella.="		<th class=\"data\">Data: ".$dt2->strftime('%d/%m/%y')."</th>\n";
}

my $testo='<div id="cerca_voli"><!-- sezione cerca voli -->
				<h1 id="voli_trovati">Ecco i voli per te!</h1>
				
				<h2 id="titolo_tabellaAndata">Andata &quot;'.$select_partenza.' &gt; '.$select_arrivo.'&quot;</h2>

					<table id="tabella_voliAndata" summary="In questa tabella vengono riportati i voli per il viaggio di ritorno">
						<caption class="intestazione_tabella">I voli in dettaglio per l\'andata del '.$data_partenza.'</caption>
							<thead>
								<tr>'.$date_tabella.'</tr>
							</thead>

							<tfoot>
									<tr>'.$date_tabella.'</tr>
							</tfoot>

							<tbody>';

#sub: inserisco i vari voli andata, iterativo.
#problema: ho una tabella, quindi il numero di elementi dev'essere costante!
#soluzione: array contenente i riferimenti ai voli.
#prima inserisco i riferimenti
my @voli_settimana;

my $max_altezza=0;# contiene il numero massimo di elementi presenti "in colonna"

for(my $dd=-3; $dd<=3; $dd++){
	#da -6 giorni a + 6 giorni
	my $gma=check_form::regexp_data($data_partenza);
	my $giorno=$gma->[0];
	my $mese=$gma->[1];
	my $anno=$gma->[2];
	my $dt2 = DateTime->new( 
					year       => $anno,
      				month      => $mese,
      				day        => $giorno
      				);
	$dt2=$dt2->add(days =>$dd);
	my $temp=\@{getVoli($dt2, $select_partenza, $select_arrivo, $select_passeggeri, $dd+4)};
	push @voli_settimana, $temp;
	if(scalar(@{$temp})>$max_altezza){
		$max_altezza=scalar(@{$temp});
	}
}

#poi scorro i vari elementi
for(my $altezza=0; $altezza<$max_altezza; $altezza++){
	$testo.='<tr>';
	for(my $giorno=0; $giorno<scalar(@voli_settimana); $giorno++){
		my @elemento=@{@voli_settimana[$giorno]};
		if($altezza<scalar(@elemento)){ #l'elemento è presente in questa "altezza" nel giorno
			my $classe="";
			if((($altezza+$giorno)%2)==0){
				$classe="scacchiera";
			}
			my $selected;
			if(((@elemento[$altezza]->[0]) eq $form{"volo_andata"}) and ((@elemento[$altezza]->[5]) eq $form{"giorno_partenza"})){
				$selected="volo_selected";
			}
			$testo.='<td class="'.$classe.' '.$selected.'">
									<a href="search.cgi?volo_andata='.@elemento[$altezza]->[0].'&giorno_partenza='.@elemento[$altezza]->[5].'">
										<object>
											<div class="seleziona_cella">
												<p>Volo n:'.@elemento[$altezza]->[0].'</p>
												<p>Partenza ore: '.@elemento[$altezza]->[1].'</p>
												<p>Arrivo ore: '.@elemento[$altezza]->[2].'</p> 
												<p>Prezzo: '.@elemento[$altezza]->[3].'</p>
												<p>Valutazione: '.@elemento[$altezza]->[4].'</p>
											</div>
										</object>
									</a>	
									</td>';
		}else{
			$testo.='<td>
										<div class="seleziona_cella">
											
										</div>	
									</td>';
		}

	}
	$testo.='</tr>';
}


$date_tabella='';
for(my $dd=-3; $dd<=3; $dd++){
	#da -6 giorni a + 6 giorni
	my $gma=check_form::regexp_data($data_ritorno);
	my $giorno=$gma->[0];
	my $mese=$gma->[1];
	my $anno=$gma->[2];
	my $dt2 = DateTime->new( 
					year       => $anno,
      				month      => $mese,
      				day        => $giorno
      				);
	$dt2=$dt2->add(days =>$dd);
	$date_tabella.='<th class="data">Data: '.$dt2->strftime('%d/%m/%y').'</th>';
}

$testo.='					</tbody>
					</table>';
if($andata!=1){
		
$testo.='					<h2 id="titolo_tabellaRitorno">Ritorno: &quot;'.$select_arrivo.' &gt; '.$select_partenza.'&quot;</h2>

					<table id="tabella_voliRitorno" summary="In questa tabella vengono riportati i voli per il viaggio di ritorno">
						<caption class="intestazione_tabella">I voli in dettaglio per il ritorno del '.$data_ritorno.'</caption>
							<thead>
								<tr>'.$date_tabella.'</tr>
							</thead>

							<tfoot>
								<tr>'.$date_tabella.'</tr>
							</tfoot>

							<tbody>
					';
#sub: inserisco i vari voli andata, iterativo.
#problema: ho una tabella, quindi il numero di elementi dev'essere costante!
#soluzione: array contenente i riferimenti ai voli.
#prima inserisco i riferimenti
my @voli_settimana;

my $max_altezza=0;# contiene il numero massimo di elementi presenti "in colonna"

for(my $dd=-3; $dd<=3; $dd++){
	#da -6 giorni a + 6 giorni
	my $gma=check_form::regexp_data($data_partenza);
	my $giorno=$gma->[0];
	my $mese=$gma->[1];
	my $anno=$gma->[2];
	my $dt2 = DateTime->new( 
					year       => $anno,
      				month      => $mese,
      				day        => $giorno
      				);
	$dt2=$dt2->add(days =>$dd);
	my $temp=\@{getVoli($dt2, $select_partenza, $select_arrivo, $select_passeggeri, 3)};
	push @voli_settimana, $temp;
	if(scalar(@{$temp})>$max_altezza){
		$max_altezza=scalar(@{$temp});
	}
}

#poi scorro i vari elementi
for(my $altezza=0; $altezza<$max_altezza; $altezza++){
	$testo.='<tr>';
	for(my $giorno=0; $giorno<scalar(@voli_settimana); $giorno++){
		my @elemento=@{@voli_settimana[$giorno]};
		if($altezza<scalar(@elemento)){ #l'elemento è presente in questa "altezza" nel giorno
			my $classe="";
			if((($altezza+$giorno)%2)==0){
				$classe="scacchiera";
			}
			$testo.='<td class="'.$classe.'">
									<a href="#">
										<object>
											<div class="seleziona_cella">
												<p>Volo n:'.@elemento[$altezza]->[0].'</p>
												<p>Partenza ore: '.@elemento[$altezza]->[1].'</p>
												<p>Arrivo ore: '.@elemento[$altezza]->[2].'</p> 
												<p>Prezzo: '.@elemento[$altezza]->[3].'</p>
												<p>Valutazione: '.@elemento[$altezza]->[4].'</p>
											</div>
										</object>
									</a>	
									</td>';
		}else{
			$testo.='<td >
										<div class="seleziona_cella">
											
										</div>	
									</td>';
		}

	}
	$testo.='</tr>';
}
$testo.='
							</tbody>
					</table>';
}
			
$testo.='			</div><!-- chiudo sezione visualizzazione voli -->';

print print_content::print($testo);
print "		</div>"; #chiudo il div main
print print_footer::print();
print "	</body>
</html>";