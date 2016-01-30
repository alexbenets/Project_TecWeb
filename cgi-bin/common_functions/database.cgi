#!/usr/bin/perl
package database;
use XML::LibXML;
use XML::XPath;
use XML::XPath::XMLParser;
require      Exporter;
require 'common_functions/check_form.cgi';
my @ISA       = qw(Exporter);
my $VERSION   = 1.00;         # Version number

use Time::Piece;
use CGI::Carp qw(fatalsToBrowser);
use strict;

my $filename="database.xml";

#funzioni base

sub get{
	#ritorna il nodo in base alla stringa xpath
	my ($xpath)=@_;
	my $xp = XML::XPath->new(filename => $filename);
	return $xp->find($xpath); # find 
}

sub set{
	#SOVRASCRIVE IL DATABASE in base a quanto inserito nella stringa
	my ($valore)=@_;
	open (my $fh,'>',$filename);
	print $fh $valore;
	close $fh;
	return 1;
}

###INIZIO FUNZIONI RELATIVE ALL'UTENTE

sub getUtente{
	my ($id)=@_;
	my @out;
	push @out, get('//utenteRegistrato[@idUR='.$id.']/nome');
	push @out, get('//utenteRegistrato[@idUR='.$id.']/cognome');
	push @out, get('//utenteRegistrato[@idUR='.$id.']/codiceFiscale');
	push @out, get('//utenteRegistrato[@idUR='.$id.']/dataNascita');
	return \@out;
}


#ritorna 1 se la password iniziale è corretta (ed ha aggiornato il database)
#ritorna 0 se la password è errata
sub aggiornaUtente{
	my ($id, $nome, $cognome, $cf, $nascita, $password, $nuova_password)=@_;
	my $parser = XML::LibXML->new();
	my $db = $parser->parse_file($filename) or die;
	my $utente=$db->findnodes('/database/tabUtenteRegistrato/utenteRegistrato[@idUR='.$id.']')->[0];
	
	my $psw_database=$utente->findnodes('password/text()')->[0];
	if(!($psw_database eq $password)){
		return 0;
	}
	my $nome_database=$utente->findnodes('nome/text()')->[0];
	if(!($nome_database eq $nome)){
		$nome_database->setData($nome);
	}
	
	my $cognome_database=$utente->findnodes('cognome/text()')->[0];
	if(!($cognome_database eq $cognome)){
		$cognome_database->setData($cognome);
	}
	
	my $cf_database=$utente->findnodes('codiceFiscale/text()')->[0];
	if(!($cf_database eq $cf)){
		$cf_database->setData($cf);
	}
	
	my $nascita_database=$utente->findnodes('dataNascita/text()')->[0];
	if(!($nascita_database eq $nascita)){
		$nascita_database->setData($nascita);
	}
	
	$psw_database=$utente->findnodes('password/text()')->[0];
	if(!($psw_database eq $nuova_password) and ! ($nuova_password eq "**********") and ! ($nuova_password eq "")){
		$psw_database->setData($nuova_password);
	}
	
	set($db->toString(1));
	return 1;
}
### INIZIO FUNZIONI RELATIVE ALLA PRENOTAZIONE

sub getPrenotazioni{
	my ($id)=@_;
	my $prenotazioni=get('//prenotazione[@idUR='.$id.']');
	my @prenotazioni;
	foreach my $prenotazione ($prenotazioni->get_nodelist){
		#<prenotazione idP="1" idUR="1" idU="1,2" idV="3">
		#<data>2016-02-12</data>
		#		<dataPartenza>2016-03-12</dataPartenza>
		#		<numeroBagagli>1</numeroBagagli>
		my $id=$prenotazione->getAttribute("idP");
		my $idU=$prenotazione->getAttribute("idU");
		
		my @id_utenti=split /,/ , $idU;
		#ora ottengo un array contenente tutti gli utenti di quella prenotazione
		my $posti_occupati = (scalar(@id_utenti)+1);
		
		my $id_volo=$prenotazione->getAttribute("idV");
		my $data_prenotazione=$prenotazione->find("data");
		my $data_partenza=$prenotazione->find("dataPartenza");
		my $bagagli=$prenotazione->find("numeroBagagli");
		
		my $tratta=get('//volo[@idV='.$id_volo.']/@idT');
		my $ora_partenza=get('//volo[@idV='.$id_volo.']/oraPartenza');
		my $prezzo=get('//volo[@idV='.$id_volo.']/prezzo');
		
		my $aereoporto_partenza=get('(//citta[@idC=(//aereoporto[@idAp=(//tratta[@idT='.$tratta.']/@idApP)]/@idC)]/nome) | (//aereoporto[@idAp=(//tratta[@idT='.$tratta.']/@idApA)]/nome)');
		my $aereoporto_arrivo=get('(//citta[@idC=(//aereoporto[@idAp=(//tratta[@idT='.$tratta.']/@idApA)]/@idC)]/nome) | (//aereoporto[@idAp=(//tratta[@idT='.$tratta.']/@idApA)]/nome)');
		
		my $servizi=get('//servizioPrenotato[@idP='.$id.']');
		my @servizi_prenotati;
		foreach my $temp ($servizi->get_nodelist){
			my @s_temp=(get('//servizio[@idS='.$temp->getAttribute("idS").']/nome'),get('//servizio[@idS='.$temp->getAttribute("idS").']/prezzo'));
			push @servizi_prenotati, \@s_temp;
		}
		#print "<p>$id, $posti_occupati, $tratta $id_volo, $aereoporto_partenza,$aereoporto_arrivo,$data_prenotazione, $data_partenza, $ora_partenza, $prezzo, $bagagli, \@servizi_prenotati</p>";
		my @temp=($id, $posti_occupati, "T$tratta"."V$id_volo", $aereoporto_partenza,$aereoporto_arrivo,$data_prenotazione, $data_partenza, $ora_partenza, $prezzo, $bagagli, \@servizi_prenotati); 
		push @prenotazioni, \@temp;
		
		#push @prenotazioni \@temp;
		#<volo idV="7" idT="3" idAe="1">
		#		<flagAttivo>true</flagAttivo>
		#		<oraPartenza>08:00</oraPartenza>
		#		<prezzo>12</prezzo>
		#		<giorno>2</giorno>			
		#	</volo>
	}
	return \@prenotazioni;
}

sub salva_utente{
	my ($nome, $cognome, $cf, $nascita)=@_;
	my $presente=int(get('//tabUtente/utente[codiceFiscale="'.$cf.'"]/@idU'));
	if ($presente>0){ #è inutile aggiungere un utente con il codice fiscale duplicato!
		return $presente;
	}
	my $id=int(get('//tabUtente/utente/@idU[ not (.<//tabUtente/utente/@idU)]'))+1;
	
	my $parser = XML::LibXML->new();
	my $db = $parser->parse_file($filename) or die;
	
	my $tab_utenti=$db->findnodes('/database/tabUtente')->[0];
	my $nodo=XML::LibXML::Element->new("utente");
	$nodo->setAttribute("idU",$id);
	
	
	
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
	$tab_utenti->addChild($nodo);
	set($db->toString(1));
	return $id;	
}

#sezione inerenti ai servizi

sub salvaServizio{
	my ($id_prenotazione, $id_servizio)=@_;
	my $id=int(get('/database/tabServizioPrenotato/servizioPrenotato[@idP="'.$id_prenotazione.'" and @idS="'.$id_servizio.'"]/@idSP'));
	if($id>0){
		#il servizio è già presente nella prenotazione.
		#caso molto degenere, ma può capitare in caso di bug nel codice di prenotazione
		#soprattutto, capita durante la fase di test delle funzionalità,
		#così mantengo il database pulito da doppioni di idS.
		return $id;
	}
	#idee: controllo se idS esiste o mi fido?
	
	$id=int(get('/database/tabServizioPrenotato/servizioPrenotato/@idSP[ not (.</database/tabServizioPrenotato/servizioPrenotato/@idSP)]'))+1;
	#ottengo un nuovo id di servizio prenotato
	my $parser = XML::LibXML->new();
	my $db = $parser->parse_file($filename) or die;
	
	my $tab_servizi=$db->findnodes('/database/tabServizioPrenotato')->[0];
	my $nodo=XML::LibXML::Element->new("servizioPrenotato");
	#idP="1" idS="1"
	$nodo->setAttribute("idSP",$id);
	$nodo->setAttribute("idP",int($id_prenotazione));
	$nodo->setAttribute("idS",int($id_servizio));
	
	$tab_servizi->addChild($nodo);
	
	set($db->toString(1));
	return $id;#ritorno l'id della nuova entry nel database
}



sub prenota{
	my ($id_utente,$data, $id_volo, $passeggeri, $servizi, $bagagli)=@_;
	my $id_prenotazione=int(get('/database/tabPrenotazione/prenotazione/@idP[ not (.</database/tabPrenotazione/prenotazione/@idP)]'))+1;
	my $parser = XML::LibXML->new();
	my $db = $parser->parse_file($filename) or die;
	
	my $tab_prenotazioni=$db->findnodes('/database/tabPrenotazione')->[0];
	my $nodo=XML::LibXML::Element->new("prenotazione");
	
	my $today = Time::Piece->new();
	my $oggi=(($today->year)+1)."-".$today->mon."-".$today->mday;
	
	my $nodo_data=XML::LibXML::Element->new("data");
	my $n_n=XML::LibXML::Text->new($oggi);
	$nodo_data->appendChild($n_n);
	$nodo->appendChild($nodo_data);
	
	my $nodo_data_partenza=XML::LibXML::Element->new("dataPartenza");
	my $n_n=XML::LibXML::Text->new($data);
	$nodo_data_partenza->appendChild($n_n);
	$nodo->appendChild($nodo_data_partenza);
	
	my $nodo_bagagli=XML::LibXML::Element->new("numeroBagagli");
	my $n_n=XML::LibXML::Text->new($bagagli);
	$nodo_bagagli->appendChild($n_n);
	$nodo->appendChild($nodo_bagagli);
	
	$nodo->setAttribute("idP",$id_prenotazione);
	$nodo->setAttribute("idUR",$id_utente);
	$nodo->setAttribute("idV",$id_volo);
	my @passeggeri_id;
	if(defined($passeggeri)){
		my @pass=@{$passeggeri};
		foreach my $tmp (@pass){
			my $nome=@{$tmp}[0];
			my $cognome=@{$tmp}[1];
			my $cf=@{$tmp}[2];
			my $nascita=@{$tmp}[3];
			my $id=salva_utente($nome,$cognome,$cf,$nascita);
			push @passeggeri_id, $id;
		}
	}
	my $string_passeggeri;
	#mi genero la stringa contenuta in nel parametro idU di prenotazione: contiene i vari id utente inerenti alla prenotazione.
	for (my $i=0; $i<scalar(@passeggeri_id); $i++){
		$string_passeggeri.=@passeggeri_id[$i];
		if($i<(scalar(@passeggeri_id)-1)){
			$string_passeggeri.=",";
		}
	}
	
	$nodo->setAttribute("idU",$string_passeggeri);
	my @ser=@{$servizi};
	for (my $i=0; $i<scalar(@ser); $i++){
		salvaServizio($id_prenotazione,@ser[$i]);
	}
	$tab_prenotazioni->addChild($nodo);
	
	set($db->toString(1));
	return $id_prenotazione;
}


## INIZIO FUNZIONI INERENTI AL LOGIN ED ALLA REGISTRAZIONE DELL'UTENTE
##
##

sub registrati{
	#ritorna:
	#- 1 se la registrazione è avvenuta correttamente
	# -1 se l'email esiste già nel database
	my ($nome, $cognome, $cf, $nascita, $email, $password)=@_;
	#verifico se $email è già presente nel database
	my $utenti=get('/database/tabUtenteRegistrato/utenteRegistrato/mail="'.$email.'"');
	if(int($utenti)==1){
		return -1;
	}
	my $max_id;
	#prima di creare un nuovo utente, devo sapere il massimo ID
	#funzionamento: controllo se l'elemento attuale non è inferiore ai vari elementi @idUR presenti nell'utente Registrato
	#utilizo //utenteRegistrato/@idUR, visto che la tabella utenteRegistrato non è ripetuta in altri nodi al di fuori di tabUtenteRegistrato
	my $utenti=get('//utenteRegistrato/@idUR[ not (.<//utenteRegistrato/@idUR)]');
	
	$max_id=int($utenti)+1;
				
	my $parser = XML::LibXML->new();
	my $db = $parser->parse_file($filename) or die;
	my $tab_utenti=$db->findnodes('/database/tabUtenteRegistrato')->[0];
	my $nodo=XML::LibXML::Element->new("utenteRegistrato");
	$nodo->setAttribute("idUR",$max_id);
	
	my $nodo_ban=XML::LibXML::Element->new("flagBann");
	my $n_n=XML::LibXML::Text->new("false");
	$nodo_ban->appendChild($n_n);
	$nodo->appendChild($nodo_ban);
	
	
	my $nodo_nome=XML::LibXML::Element->new("nome");
	$n_n=XML::LibXML::Text->new($nome);
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
	
	my $nodo_email=XML::LibXML::Element->new("mail");
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
	my @out;
	foreach my $utente ($utenti->get_nodelist){
	
		my $psw="".$utente->find("password");
		my $nome="".$utente->find("nome");
		my $cognome="".$utente->find("cognome");
		my $id="".$utente->getAttribute("idUR");
		if($psw eq $password){
			@out=(1,$nome,$cognome, $id);
			return \@out;
		}
		@out=(-1,"","");
		return \@out;
	}
	@out=(-2,"","");
	return \@out;
}

### INIZIO FUNZIONI INERENTI AI VOLI

sub getVoli{

	#funzionamento:
	#- lista voli per tratta
	#- elenco prenotazioni per quel volo
	#- escludo se n°posti>posti disponibili per l'aereo
	my ($nome_andata, $nome_ritorno, $passeggeri, $data)=@_;
	#ora mi recupero l'ID tratta
	my $aereoporto_partenza=get('/database/tabAereoporto/aereoporto[nome="'.$nome_andata.'" and flagAttivo="true"]');
	my $id_partenza=0;
	foreach my $aereoporto ($aereoporto_partenza->get_nodelist){
		$id_partenza=$aereoporto->getAttribute("idAp");
	}
	if($id_partenza==0){
		return undef;
	}
	my $aereoporto_arrivo=get('/database/tabAereoporto/aereoporto[nome="'.$nome_ritorno.'" and flagAttivo="true"]');
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
	#if($durata==0){ #se, per esempio, è il ritorno
	#	$tratta=get('/database/tabTratta/tratta[@idApP='.$id_arrivo.' and @idApA='.$id_partenza.']');
	#	foreach my $tratta_temp ($tratta->get_nodelist){
	#		$durata=$tratta_temp->find("durata");
	#		$id_tratta=$tratta_temp->getAttribute("idT");
	#	}
	#}
	
	#visto che ho già definito la funzione di recupero data in check_form, la riciclo qui.
	my @gma=@{check_form::regexp_data($data)};
	my $giorno=@gma[0];
	if(int($giorno)<10){
		$giorno="0$giorno";
	}
	my $mese=@gma[1];
	if(int($mese)<10){
		$mese="0$mese";
	}
	my $anno=@gma[2];
	
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
			$posti_disponibili=int(get('/database/tabTipoAereo/tipoAereo[@idTA='.$id_tipo.']/numeroPosti'));
		}
		my $id_volo=int($volo->getAttribute("idV"));
		#ora sottraggo i posti disponibili in base alle prenotazioni
		my $prenotazioni=get('/database/tabPrenotazione/prenotazione[@idV='.$id_volo.' and dataPartenza="'.$anno.'-'.$mese.'-'.$giorno.'"]');
		foreach my $prenotazione ($prenotazioni->get_nodelist){
			#ora mi ricavo il numero di passeggeri + il prenotante.
			my $idU=$prenotazione->getAttribute("idU");
			my @id_utenti=split /,/ , $idU;
			#ora ottengo un array contenente tutti gli utenti di quella prenotazione
			$posti_disponibili -= (scalar(@id_utenti)+1);
			#visto che non mi interessa sapere chi c'è in quel volo, allora sottraggo semplicemente la grandezza del vettore + 1, in quanto è presente pure il passeggero prenotante
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
		my @v_temp=("T".$id_tratta."V".$id_volo,$orario, $orario_arrivo,$prezzo,'4.3', $data, $posti_disponibili);
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
        my $citta=get('/database/tabCitta/citta[@idN='.$id.' and flagServita="true"]');
        my %citta_temp;
        my $count_stato=0;
        foreach my $node_citta($citta->get_nodelist){
        	my $count_citta=0;
        	my $id_citta= $node_citta->getAttribute("idC");
        	my $nome_citta= $node_citta->find('nome');
        	my $aereoporti=get('/database/tabAereoporto/aereoporto[@idC='.$id_citta.' and flagAttivo="true"]');
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