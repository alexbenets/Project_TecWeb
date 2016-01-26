#!/usr/bin/perl
package database;
use XML::LibXML;
use XML::XPath;
use XML::XPath::XMLParser;
require      Exporter;
my @ISA       = qw(Exporter);
my $VERSION   = 1.00;         # Version number

use Time::Piece;
use CGI::Carp qw(fatalsToBrowser);
use strict;

my $filename="database.xml";

sub get{
	my ($xpath)=@_;
	my $xp = XML::XPath->new(filename => $filename);
	return $xp->find($xpath); # find 
}

sub set{
	my ($valore)=@_;
	open (my $fh,'>',$filename) or die return 0;
	print $fh $valore;
	close $fh;
	return 1;
}

sub registrati{
	#ritorna 1 se la registrazione è avvenuta correttamente, 0 altrimenti
	my ($nome, $cognome, $cf, $nascita, $email, $password)=@_;
	my $utenti=get('/database/tabUtenteRegistrato/utenteRegistrato[mail="'.$email.'"]');
	foreach my $utente ($utenti->get_nodelist){
		return 0;
	}
	my $max_id;
	my $utenti=get('/database/tabUtenteRegistrato/utenteRegistrato');
	foreach my $utente ($utenti->get_nodelist){
		my $id=int($utente->getAttribute("idUR"));
		if($max_id<$id){
			$max_id=$id;
		}
	}
	$max_id++;
	my $parser = XML::LibXML->new();
	my $db = $parser->parse_file($filename) or die;
	my $tab_utenti=$db->findnodes('/database/tabUtenteRegistrato')->[0];
	my $nodo=XML::LibXML::Element->new("utenteRegistrato");
	$nodo->setAttribute("idUR",$max_id);
	my $nodo_nome=XML::LibXML::Element->new("nome");
	my $n_n=XML::LibXML::Text->new($nome);
	$nodo_nome->appendChild($n_n);
	$nodo->appendChild($nodo_nome);
	
	my $nodo_cognome=XML::LibXML::Element->new("cognome");
	$n_n=XML::LibXML::Text->new($cognome);
	$nodo_cognome->appendChild($n_n);
	$nodo->appendChild($nodo_cognome);
		
	my $nodo_cf=XML::LibXML::Element->new("codiceFiscale");
	$n_n=XML::LibXML::Text->new($cf);
	$nodo_cf->appendChild($n_n);
	$nodo->appendChild($nodo_cf);
	
	my $nodo_nascita=XML::LibXML::Element->new("dataNascita");
	$n_n=XML::LibXML::Text->new($nascita);
	$nodo_nascita->appendChild($n_n);
	$nodo->appendChild($nodo_nascita);
	
	my $nodo_email=XML::LibXML::Element->new("email");
	$n_n=XML::LibXML::Text->new($email);
	$nodo_email->appendChild($n_n);
	$nodo->appendChild($nodo_email);
	
	my $nodo_password=XML::LibXML::Element->new("password");
	$n_n=XML::LibXML::Text->new($password);
	$nodo_password->appendChild($n_n);
	$nodo->appendChild($nodo_password);
	
	$tab_utenti->addChild($nodo);
	return set( $db->toString(1));
	
	
}

sub login{
	#ritorna -2 se l'utente non è registrato o è stato bannato
	#ritorna 1 se credenziali corrette
	#ritorna -1 se password errata
	my ($username, $password)=@_;
	my $utenti=get('/database/tabUtenteRegistrato/utenteRegistrato[mail="'.$username.'" and flagBann="false"]');
	foreach my $utente ($utenti->get_nodelist){
		my $psw="".$utente->find("password");
		if($psw eq $password){
			return 1;
		}
		return -1;
	}
	return -2;
}

sub getVoli{

	#funzionamento:
	#- lista voli per tratta
	#- elenco prenotazioni per quel volo
	#- escludo se n°posti>posti disponibili per l'aereo
	my ($nome_andata, $nome_ritorno, $passeggeri, $data)=@_;
	
	#ora mi recupero l'ID tratta
	my $aereoporto_partenza=get('/database/tabAereoporto/aereoporto[nome="'.$nome_andata.'"][flagAttivo="true"]');
	my $id_partenza=0;
	foreach my $aereoporto ($aereoporto_partenza->get_nodelist){
		$id_partenza=$aereoporto->getAttribute("idAp");
	}
	if($id_partenza==0){
		return undef;
	}
	my $aereoporto_arrivo=get('/database/tabAereoporto/aereoporto[nome="'.$nome_ritorno.'"][flagAttivo="true"]');
	my $id_arrivo=0;
	foreach my $aereoporto ($aereoporto_arrivo->get_nodelist){
		$id_arrivo=$aereoporto->getAttribute("idAp");
	}
	if($id_arrivo==0){
		return undef;
	}
	my $tratta=get('/database/tabTratta/tratta[@idApP='.$id_partenza.' and @idApA='.$id_arrivo.']');
	my $durata=0;
	my $id_tratta=0;
	foreach my $tratta_temp ($tratta->get_nodelist){
		$durata=int($tratta_temp->find("durata"));
		$id_tratta=$tratta_temp->getAttribute("idT");
	}
	if($durata==0){ #se, per esempio, è il ritorno
		$tratta=get('/database/tabTratta/tratta[@idApP='.$id_arrivo.' and @idApA='.$id_partenza.']');
		foreach my $tratta_temp ($tratta->get_nodelist){
			$durata=$tratta_temp->find("durata");
			$id_tratta=$tratta_temp->getAttribute("idT");
		}
	}
	
	#visto che perl non è OOP, allora non posso riciclare il codice già definito in check_form
	$data =~/^([\d]{1,2})([\/-:\.\\]{1})+([\d]{1,2})([\/-:\.\\]{1})+([\d]{4})$/;
	my $giorno=$1;
	if(int($giorno)<10){
		$giorno="0$giorno";
	}
	my $mese=$3;
	if(int($mese)<10){
		$mese="0$mese";
	}
	my $anno=$5;
	
	my $voli_db=get('/database/tabVolo/volo[@idT='.$id_tratta.' and flagAttivo="true"]');
	my @voli;
	#<oraPartenza>00:00:00</oraPartenza>
	#<prezzo>12</prezzo>
	#<giorno>2</giorno>	
	#my @voli;
	#for (my $i=0; $i<$n; $i++){
	#	my @volo=('AZ000'.$i, '8:00', '10:00', '160', '4.75', $giorno);
	#	push @voli, \@volo; 
	#}
	foreach my $volo ($voli_db->get_nodelist){
		my $id_aereo=int($volo->getAttribute("idAe"));
		my $aerei=get('/database/tabAereo/aereo[@idAe='.$id_aereo.']');
		my $posti_disponibili=0;
		#mi ricavo i posti totali in base all'aereo che effettua il volo
		foreach my $aereo ($aerei->get_nodelist){
			my $id_tipo=int($aereo->getAttribute("idTA"));
			my $tipologie_aerei=get('/database/tabTipoAereo/tipoAereo[@idTA='.$id_tipo.']');
			foreach my $tipoAereo ($tipologie_aerei->get_nodelist){
				$posti_disponibili=int($tipoAereo->find("numeroPosti"));
			}
		}
		my $id_volo=int($volo->getAttribute("idV"));
		#ora sottraggo i posti disponibili in base alle prenotazioni
		my $prenotazioni=get('/database/tabPrenotazione/prenotazione[@idV='.$id_volo.' and dataPartenza="'.$anno.'-'.$mese.'-'.$giorno.'"]');
		foreach my $prenotazione ($prenotazioni->get_nodelist){
			#ora mi ricavo il numero di passeggeri + il prenotante.
			my $idU=$prenotazione->getAttribute("idU");
			my @id_utenti=split /,/ , $idU;
			#ora ottengo un array contenente tutti gli utenti di quella prenotazione
			$posti_disponibili -= scalar(@id_utenti);
			#visto che non mi interessa sapere chi c'è in quel volo, allora sottraggo semplicemente la grandezza del vettore
		}
		#print "<p>$posti_disponibili - $passeggeri</p>";
		my $orario="".$volo->find("oraPartenza");
		my $prezzo="".$volo->find("prezzo");
		my $giorno="".$volo->find("giorno");
		
		#conoscendo l'orario di partenza e la durata (in minuti), conosco l'orario di arrivo.
		my $t_andata =Time::Piece->strptime($orario, '%H:%M');
		#my $t_durata =Time::Piece->strptime((int(int($durata)/60)).":".int(int($durata)%60), '%H:%M');
		my $orario_arrivo=($t_andata+int($durata)*60)->strftime('%H:%M');
		#my $t_andata = Time::Piece->strptime('%T', $orario);
		#my $t_arrivo=$t_andata;
		my @v_temp=("I".$id_tratta."V".$id_volo."P".$id_partenza,$orario, $orario_arrivo,$prezzo,'4.3', $data, $posti_disponibili);
		if($posti_disponibili>=($passeggeri)){
			push @voli, \@v_temp;
		}
	}
	return \@voli;
}


sub listServizi{
	my @servizi;
	my $lista_servizi=get('/database/tabServizio/servizio');
	foreach my $servizio ($lista_servizi->get_nodelist){
		my $id_servizio=$servizio->getAttribute("idS");
		my $nome_servizio=$servizio->find("nome");
		my $descrizione=$servizio->find("descrizione");
		my $costo=$servizio->find("prezzo");
		my @temp=($id_servizio, $nome_servizio, $costo, $descrizione);
		push @servizi,\@temp;
	}
	return \@servizi;
}

sub listTratte{


#funzionamento: 
#creo array associativo {ID, valore} di Nazione
#per ogni ID Nazione, mi creo l'array associativo di città
#per ogni città, mi creo l'array associativo degli aereoporti



	#my @aereoporti_temp=("Linate", "Malpensa");
	#my %temp;
	
	#$temp{"Milano"}=\@aereoporti_temp;
	
	#my @aereoporti_temp=("Fiumicino");
	#$temp{"Roma"}=\@aereoporti_temp;
	#$partenze {"Italia"}=\%temp;
	
	#my @aereoporti_temp=( "Charles de gaulle");
	#	my %temp;
	#	$temp{"Parigi"}=\@aereoporti_temp;
	#	$partenze {"Francia"}=\%temp;
	

#mi genero l'array delle tratte
my %partenze;
my $nazioni_get= get('/database/tabNazione/nazione');
foreach my $node ($nazioni_get->get_nodelist) {
        my $id=$node->getAttribute("idN");
        my $nome_nazione=$node->find('nome');
        my $citta=get('/database/tabCitta/citta[@idN='.$id.'][flagServita="true"]');
        my %citta_temp;
        my $count_stato=0;
        foreach my $node_citta($citta->get_nodelist){
        	my $count_citta=0;
        	my $id_citta= $node_citta->getAttribute("idC");
        	my $nome_citta= $node_citta->find('nome');
        	my $aereoporti=get('/database/tabAereoporto/aereoporto[@idC='.$id_citta.'][flagAttivo="true"]');
        	my @aereoporti_temp;
        	foreach my $aereoporto($aereoporti->get_nodelist){
        		$count_stato++;
        		$count_citta++;
        		my $id_aereoporto=$aereoporto->getAttribute("idAp");
        		my @nome_aereoporto=($aereoporto->find('nome'),$aereoporto->getAttribute("idAp"));
        		#print "<p>$nome_nazione: $nome_citta - $nome_aereoporto</p>";
        		push @aereoporti_temp, \@nome_aereoporto;
        	}
        	if($count_citta>0){#se esistono aereoporti nella città
        		$citta_temp{"$nome_citta"}=\@aereoporti_temp;
        	}
        }
        if($count_stato>0){#se esistono aereoporti nello stato
        	$partenze {"$nome_nazione"}=\%citta_temp;
        }
}
#foreach my $node ($nazioni_get->get_nodelist) {
#	print $node;
#}
return %partenze;

}