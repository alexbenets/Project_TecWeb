#!/usr/bin/perl

package print_search;

use strict;

require      Exporter;

my @ISA       = qw(Exporter);
my $VERSION   = 1.00;         # Version number

### Include your variables and functions here


sub list_tratte {
	
	my %partenze;
	my @aereoporti_temp=("Linate", "Malpensa");
	my %temp;
	
	$temp{"Milano"}=\@aereoporti_temp;
	
	my @aereoporti_temp=("Fiumicino");
	$temp{"Roma"}=\@aereoporti_temp;
	$partenze {"Italia"}=\%temp;
	
	my @aereoporti_temp=( "Charles de gaulle");
		my %temp;
		$temp{"Parigi"}=\@aereoporti_temp;
		$partenze {"Francia"}=\%temp;
	
	return %partenze;
	
	#funzionamento:
	# ARRAY associativo di paesi (Italia, Francia, ecc...)	
	# Ad ogni paese viene associato un array associativo di città
	# Ogni città contiene un array di nomi di aereoporti.
	#
	#   ITALIA ---->  MILANO ---> Linate
	#         |              |--> Malpensa
	#         |
	#         |---->  ROMA -----> Fiumicino
	#
	#
}

sub print { 
	my ($errori, $andata, $partenza, $arrivo, $data_partenza, $data_ritorno, $passeggeri, $vuoto)=@_;
	#vuoto:bypass per evitare di stampare errori nella pagina index.cgi
	if(!defined $data_partenza | $data_partenza==0){
		$data_partenza="Data partenza";
	}
	if(!defined $data_ritorno| $data_ritorno==0){
		$data_ritorno="Data ritorno";
	}
	if ((defined $data_partenza & $data_partenza>0)&(defined $data_ritorno & $data_ritorno>0)){
		$errori|=8;
	}
	if($vuoto==1){
		$errori=0;
	}
my $testo= "
		<div id=\"prenota\"><!-- div che contiene il box per la prenotazione-->
				<form action=\"../cgi-bin/search.cgi\" method=\"post\">
					<fieldset>
						";
						if(($errori & 3)>0){
							$testo.="<div>
										<h3 class=\"errore\">Attenzione: alcune date non sono corrette!</h3>
										<h3 class=\"errore\">Puoi prenotare solo voli da domani all'anno prossimo</h3>
									</div>";
						}
						if(($errori & 8)>0){
							$testo.="<div>
										<h3 class=\"errore\">L'aereoporto di destinazione non pu&ograve; essere lo stesso di partenza!</h3>
									</div>";
						}
						$testo.="<div class=\"casella_AR\">
							<label for=\"andata\">solo andata</label>
							<input type=\"radio\" name=\"AR\" id=\"andata\" value=\"andata\"  ";
							if($andata==1){
								$testo.="checked=\"checked\"";
							}
							$testo.="/>
						</div>
						<div class=\"casella_AR\">
							<label for=\"ritorno\">andata e ritorno</label>
							<input type=\"radio\" name=\"AR\" id=\"ritorno\" value=\"ritorno\"  ";
							if($andata==0){
								$testo.="checked=\"checked\"";
							}
							$testo.="/>
						</div>
						<div class=\"clearer\"></div>";
						
						
						$testo.="<div class=\"casella_partenza\">
							<label for=\"partenza\">Partenza:</label>
							<select id=\"partenza\" name=\"partenza\" class=\"partenza\">";
						my %lista_partenze=list_tratte();
						while ((my $paese, my $citta) = each(%lista_partenze))
						{
							$testo.= "<optgroup label=\"$paese\">\n";
							while ((my $nome_citta, my $aereoporto) = each(%{$citta}))
							{
								while ((my $id, my $nome_aereoporto) = each(@{$aereoporto}))
								{
									$testo.="<option";
									if("$nome_citta - $nome_aereoporto" eq $partenza){
										$testo.=" selected=\"selected\" ";
									}
									$testo.=">$nome_citta - $nome_aereoporto</option>";
								}
							}
							$testo.= "</optgroup>";
						}
							
							$testo.="</select>
						</div>
						<div class=\"casella_arrivo\">					
							<label for=\"arrivo\">Arrivo:</label>
							<select id=\"arrivo\" name=\"arrivo\" class=\"arrivo\">";
						my %arrivi=list_tratte();
						while ((my $paese, my $citta) = each(%arrivi))
						{
							$testo.= "<optgroup label=\"$paese\"> \n";
							while ((my $nome_citta, my $aereoporto) = each(%{$citta}))
							{
								while ((my $id, my $nome_aereoporto) = each(@{$aereoporto}))
								{
									$testo.="<option";
									if("$nome_citta - $nome_aereoporto" eq $arrivo){
										$testo.=" selected=\"selected\" ";
									}
									$testo.=">$nome_citta - $nome_aereoporto</option>";
								}
							}
							$testo.= "</optgroup>";
						}
							
							$testo.="</select>
						</div>
						
						<div class=\"casella_dataPartenza\">
							<label for=\"data_partenza\">Data Partenza:</label>
							<input type=\"text\" name=\"data_partenza\" id=\"data_partenza\" value=\"$data_partenza\" class=\"";
							if($errori & 1){
								$testo.= "errore";
							}
							$testo.="\"></input>
						</div>
						<div class=\"casella_dataArrivo\">
							<label for=\"data_ritorno\">Data Ritorno:</label>
							<input type=\"text\" name=\"data_ritorno\" id=\"data_ritorno\" value=\"$data_ritorno\" class=\"";
							if($errori & 2){
								$testo.= "errore";
							}
							$testo.="\"></input>
						</div>

						<div class=\"casella_passeggeri\">
							<label for=\"n_passeggeri\">numero Passeggeri:</label>
							<select id=\"n_passeggeri\" name=\"passeggeri\" class=\"passeggeri\">";
							for(my $i=0; $i<=10; $i++){
								if($i<2){
									$testo.="<option";
									if($passeggeri==$i){
										$testo.=" selected=\"selected\"";
									}
									$testo.=">";
									if($i==1){
										$testo.="1 passeggero";
									}else{
										$testo.="Nessun passeggero";
									}
									$testo.="</option>";
								}else{
									$testo.="<option";
									if($passeggeri==$i){
										$testo.=" selected=\"selected\"";
									}
									$testo.=">$i passeggeri</option>";
								}
							}
							$testo.="</select>
						</div>

						<div class=\"button_form\">									
							<button type=\"submit\" name=\"cerca\" id=\"cerca\">
								<span>cerca voli</span>
							</button>
						</div>
						<div class=\"clearer\"></div>
					</fieldset>
				</form>
			</div><!-- chiudo prenota -->

";
return $testo;
}
