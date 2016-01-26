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
require "common_functions/database.cgi";


sub compareDate{
#controllo se la data "partenza" è inferiore o uguale alla data di "ritorno"
#questa funzione viene utilizzata per evitare di selezionare una data di ritorno inferiore o uguale ad una data di partenza.
	my($partenza, $ritorno)=@_;
	if($ritorno==''){
		return 1;
	}
	my $gma=check_form::regexp_data($partenza);
	my $giorno=int($gma->[0]);
	my $mese=int($gma->[1]);
	my $anno=int($gma->[2]);
	if($giorno+$mese+$anno==0){
		return 0; #non posso confrontare
	}
	my $dt1 = DateTime->new( 
					year       => $anno,
      				month      => $mese,
      				day        => $giorno
      				);
    my $gma=check_form::regexp_data($ritorno);
    if($gma==0){
    	return 0;
    }
	$giorno=$gma->[0];
	$mese=$gma->[1];
	$anno=$gma->[2];
	if($giorno+$mese+$anno==0){
		return 0; #non posso confrontare
	}
	my $dt2 = DateTime->new( 
					year       => $anno,
      				month      => $mese,
      				day        => $giorno
      				);
    my $cmp=DateTime->compare($dt1,$dt2);
    if($cmp>=0){
    	return 0;#no
    }
    return 1;#tutto ok
}



my %form;
foreach my $p (param()) {
    $form{$p} = param($p);
    #print "$p = $form{$p}<br>\n";
}


my $create=gestione_sessione::createSession();
gestione_sessione::setParam("location","/cgi-bin/seleziona_voli.cgi");

my $volo_andata=$form{"volo_andata"};
my $volo_ritorno=$form{"volo_ritorno"};
my $giorno_partenza=$form{"giorno_partenza"};
my $giorno_ritorno=$form{"giorno_ritorno"};
# n ospiti + 1 passeggero principale
my $selezione=0;#se la pagina è stata caricata in seguito ad un back

if($volo_andata eq ""){#forse sono tornato indietro o sono appena arrivato?
	$volo_andata=gestione_sessione::getParam("volo_andata");
}else{
	gestione_sessione::setParam("volo_andata",$volo_andata);
}
if($giorno_partenza eq ""){#forse sono tornato indietro o sono appena arrivato?
	$giorno_partenza=gestione_sessione::getParam("giorno_partenza");
}else{
	gestione_sessione::setParam("giorno_partenza",$giorno_partenza);
}

if($volo_ritorno eq ""){#forse sono tornato indietro o sono appena arrivato?
	$volo_ritorno=gestione_sessione::getParam("volo_ritorno");
}else{
	gestione_sessione::setParam("volo_ritorno",$volo_ritorno);
}

if($giorno_ritorno eq ""){#forse sono tornato indietro o sono appena arrivato?
	$giorno_ritorno=gestione_sessione::getParam("giorno_ritorno");
}else{
	gestione_sessione::setParam("giorno_ritorno",$giorno_ritorno);
}

sub getVoli
{
	my ($giorno, $partenza, $arrivo, $passeggeri)=@_;
	my $aereoporto_partenza=get_aereoporto($partenza);
	my $aereoporto_arrivo=get_aereoporto($arrivo);
	my $voli=database::getVoli($aereoporto_partenza, $aereoporto_arrivo,$passeggeri,$giorno);
	return $voli;
}

sub get_aereoporto
{
	#Parigi - Charles De Gaulle
	my ($nome_completo)=@_;
	$nome_completo =~/([a-zA-Z.]+)([ \- ]+)([a-zA-Z. ]+)/;
	return $3;
}

#dati recuperati dalle variabili di sessione

my $andata=gestione_sessione::getParam("AR");
my $select_partenza=gestione_sessione::getParam("partenza");
my $select_arrivo=gestione_sessione::getParam("arrivo");
my $data_partenza=gestione_sessione::getParam("data_partenza");
my $data_ritorno=gestione_sessione::getParam("data_ritorno");
my $select_passeggeri=gestione_sessione::getParam("passeggeri");


if(!($volo_andata eq "")){
	$selezione=1;
}
if(!($giorno_partenza eq "")){
	$selezione+=2;
}
if(!($volo_ritorno eq "")){
	$selezione+=4;
}
if(!($giorno_ritorno eq "")){
	$selezione+=8;
}
if(!($form{"visitato"} eq "1")){
	$selezione=0;
}else{
	my $click=gestione_sessione::getParam("numero_selezioni_voli");
	if($form{"andata"}){
		$click|=1;
	}
	if($form{"ritorno"}){
		$click|=2;
	}
	gestione_sessione::setParam("numero_selezioni_voli",$click);
}


if($andata==0){
	if(compareDate($giorno_partenza, $giorno_ritorno)==0){
		$giorno_ritorno=0;
		gestione_sessione::setParam("numero_selezioni_voli",0);
	}
}
if($selezione>0){ #se ho selezionato tutti i valori desiderati
	if($andata==1){
		if(($selezione&3)==3){ #se ho impostato sia la data che l'ora di partenza
			print "Location: dati_passeggeri.cgi\n\n";
			#redirect alla pagina desiderata.
		}
	}
	else {
		if(($selezione&15)==15){ #se ho impostato sia partenza che ritorno
			if(($andata==0)&(gestione_sessione::getParam("numero_selezioni_voli")==3)){
				print "Location: dati_passeggeri.cgi\n\n";
			}
			#redirect alla pagina desiderata.
		}
	}
}

#$andata=0;
#$select_partenza="Milano - Linate";
#$select_arrivo="Roma - Fiumicino";
#$data_partenza="31/01/2016";
#$data_ritorno="28/02/2016";
#$select_passeggeri=2;



my $titolo="Seleziona il tuo volo";



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
my @path=("Home", "index.cgi");
push @path_temp, \@path;
my @path=("Ricerca voli", "search.cgi");
push @path_temp, \@path;
my @path=("Seleziona i voli disponibili", "seleziona_voli.cgi");
push @path_temp, \@path;
print_header::setPath(\@path_temp);



print print_header::print();
print "		<div id=\"main\"><!-- div che contiene tutto il contenuto statico e/o dinamico-->"; #mega div

#print "$data_partenza $data_ritorno ".compareDate($data_partenza, $data_ritorno);

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

print "$giorno_partenza, $giorno_ritorno";

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
	my $data=$dt2->day."/".$dt2->month.'/'.$dt2->year;
	my $temp=\@{getVoli($data, $select_partenza, $select_arrivo, int($select_passeggeri)+1, $dd+4)};
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
			if(((@elemento[$altezza]->[0]) eq $volo_andata) and ((@elemento[$altezza]->[5]) eq $giorno_partenza)){
				$selected="volo_selected";
				gestione_sessione::setParam("Andata_data",$giorno_partenza);
				gestione_sessione::setParam("Andata_id",@elemento[$altezza]->[0]);
				gestione_sessione::setParam("Andata_partenza",@elemento[$altezza]->[1]);
				gestione_sessione::setParam("Andata_arrivo",@elemento[$altezza]->[2]);
				gestione_sessione::setParam("Andata_prezzo",@elemento[$altezza]->[3]);
			}
			$testo.='<td class="'.$classe.' '.$selected.'">';
			my $data_ok=1;
			if($andata==0){
				$data_ok=compareDate(@elemento[$altezza]->[5],$giorno_ritorno);	
			}
			my $classe_cella="seleziona_cella";
			if($data_ok>0 and !(@elemento[$altezza]->[0] eq "")){
				$testo.='		<a href="seleziona_voli.cgi?volo_andata='.@elemento[$altezza]->[0].'&amp;giorno_partenza='.@elemento[$altezza]->[5].'&amp;visitato=1&amp;andata=1">';
				$testo.='			<object>
											<div class="'.$classe_cella.'">
												<p>Volo n:'.@elemento[$altezza]->[0].'</p>
												<p>Partenza ore: '.@elemento[$altezza]->[1].'</p>
												<p>Arrivo ore: '.@elemento[$altezza]->[2].'</p> 
												<p>Prezzo: '.@elemento[$altezza]->[3].'</p>
												<p>Valutazione: '.@elemento[$altezza]->[4].'</p>
											</div>
										</object>';
			}else {
				$classe_cella=" disabled";
			}	
							
						if($data_ok>0){
							$testo.='			</a>	';
						}
$testo.='									</td>';
		}else{
			$testo.='<td>
										<div class="seleziona_cella">
											
										</div>	
									</td>';
		}

	}
	$testo.='</tr>';
}


$testo.='					</tbody>
					</table>';
if($andata==0){
$date_tabella='';
for(my $dd=-3; $dd<=3; $dd++){
	#da -3 giorni a + 3 giorni
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
	#da -3 giorni a + 3 giorni
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
	my $data=$dt2->day."/".$dt2->month.'/'.$dt2->year;
	my $temp=\@{getVoli($data, $select_partenza, $select_arrivo, $select_passeggeri, 3)};
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
			if(((@elemento[$altezza]->[0]) eq $volo_ritorno) and ((@elemento[$altezza]->[5]) eq $giorno_ritorno)){
				$selected="volo_selected";
				gestione_sessione::setParam("Ritorno_id",@elemento[$altezza]->[0]);
				gestione_sessione::setParam("Ritorno_data",$giorno_partenza);
				gestione_sessione::setParam("Ritorno_partenza",@elemento[$altezza]->[1]);
				gestione_sessione::setParam("Ritorno_arrivo",@elemento[$altezza]->[2]);
				gestione_sessione::setParam("Ritorno_prezzo",@elemento[$altezza]->[3]);
				
			}
			if(!(@elemento[$altezza]->[1] eq '')){
				$testo.='<td class="'.$classe.' '.$selected.'">';
				my $data_ok=compareDate($giorno_partenza,@elemento[$altezza]->[5]);	
				my $classe_cella="seleziona_cella";
				my $classe_cella="seleziona_cella";
			if($data_ok>0 and !(@elemento[$altezza]->[0] eq "")){
				$testo.='		<a href="seleziona_voli.cgi?volo_ritorno='.@elemento[$altezza]->[0].'&amp;giorno_ritorno='.@elemento[$altezza]->[5].'&amp;visitato=1&amp;ritorno=1">';
				$testo.='			<object>
											<div class="'.$classe_cella.'">
												<p>Volo n:'.@elemento[$altezza]->[0].'</p>
												<p>Partenza ore: '.@elemento[$altezza]->[1].'</p>
												<p>Arrivo ore: '.@elemento[$altezza]->[2].'</p> 
												<p>Prezzo: '.@elemento[$altezza]->[3].'</p>
												<p>Valutazione: '.@elemento[$altezza]->[4].'</p>
											</div>
										</object>';
			}else {
				$classe_cella=" disabled";
			}	
							if($data_ok>0){		
								$testo.='</a>	';
							}
							$testo.='		</td>';
			}else{
				$testo.="<td></td>";
			}
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