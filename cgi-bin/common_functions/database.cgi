#!/usr/bin/perl
package database;
use XML::LibXML;
#use XML::XPath;
#use XML::XPath::XMLParser;
require      Exporter;
require 'common_functions/check_form.cgi';
my @ISA       = qw(Exporter);
my $VERSION   = 1.00;         # Version number

use Time::Piece;
use CGI::Carp qw(fatalsToBrowser);
use strict;

my $filename="database.xml";

#funzioni base
my $xp=undef;
sub get{
	#ritorna il nodo in base alla stringa xpath
	my ($xpath)=@_;
	if($xp==undef){
		#$xp = XML::XPath->new(filename => $filename);
		$xp=XML::LibXML->load_xml(location => $filename);
	}
	return $xp->findnodes($xpath); # find 
}

sub set{
	#SOVRASCRIVE IL DATABASE in base a quanto inserito nella stringa
	$xp=undef;
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
	push @out, get('/database/tabUtente/utente[@idU='.$id.']/nome/text()');
	push @out, get('/database/tabUtente/utente[@idU='.$id.']/cognome/text()');
	push @out, get('/database/tabUtente/utente[@idU='.$id.']/codiceFiscale/text()');
	push @out, get('/database/tabUtente/utente[@idU='.$id.']/dataNascita/text()');
	return \@out;
}


#ritorna 1 se la password iniziale è corretta (ed ha aggiornato il database)
#ritorna 0 se la password è errata
sub aggiornaUtente{
	my ($id, $nome, $cognome, $cf, $nascita, $password, $nuova_password)=@_;
	my $parser = XML::LibXML->new();
	my $db = $parser->parse_file($filename) or die;
	my $utente=$db->findnodes('/database/tabUtente/utente[@idU='.$id.']')->[0];
	if ($utente->toString(1) eq ""){
		return -1;
		#utente non trovato
	}
	my $utente_registrato=$db->findnodes('/database/tabUtenteRegistrato/utenteRegistrato[@idUR='.$id.']')->[0];
	my $psw_database=$utente_registrato->findnodes('password/text()')->[0];
	if(!($psw_database eq $password)){
		return 0;
		#password errata
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
	
	$psw_database=$utente_registrato->findnodes('password/text()')->[0];
	if(!($psw_database eq $nuova_password) and ! ($nuova_password eq "**********") and ! ($nuova_password eq "")){
		$psw_database->setData($nuova_password);
	}
	
	set($db->toString(1));
	return 1;
}
### INIZIO FUNZIONI RELATIVE ALLA PRENOTAZIONE
my $prenotazioni;
my $id_ur_prenotazione;
my @nodi_prenotazione;

sub getPrenotazioni{
	my ($id, $id_P)=@_;
	my $miss_id=0;
	if ($id_ur_prenotazione!=$id){
		$id_ur_prenotazione=$id;
		$miss_id=1;
	}
	if($id_P eq ''){
		if($miss_id==1){
			$prenotazioni=get('/database/tabPrenotazione/prenotazione[@idUR='.$id.']');
			@nodi_prenotazione=$prenotazioni->get_nodelist;
		}
	}else{
		$prenotazioni=get('/database/tabPrenotazione/prenotazione[@idUR='.$id.' and @idP='.int($id_P).']');
		@nodi_prenotazione=$prenotazioni->get_nodelist;
	}
	my @out_prenotazioni;
	
	#variabili per cache
	my $id_volo=-1;
	my $tratta;
	my $ora_partenza;
	my $prezzo;
	my $aereoporto_partenza;
	my $aereoporto_arrivo;
	
	foreach my $prenotazione (@nodi_prenotazione){
		#<prenotazione idP="1" idUR="1" idU="1,2" idV="3">
		#<data>2016-02-12</data>
		#		<dataPartenza>2016-03-12</dataPartenza>
		#		<numeroBagagli>1</numeroBagagli>
		my $id=$prenotazione->getAttribute("idP");
		#my $idU=$prenotazione->getAttribute("idU");
		
		#my @id_utenti=split /,/ , $idU;
		#ora ottengo un array contenente tutti gli utenti di quella prenotazione
		my $nodo_passeggeri=$tratta=get('/database/tabPasseggeriPrenotazione/passeggeriPrenotazione[@idP='.$id.']');
		my @utenti;
		my $posti_occupati =1;
		foreach my $ut ($nodo_passeggeri->get_nodelist){
			my $tmp=getUtente($ut->getAttribute('idU'));
			push @utenti, $tmp;
			$posti_occupati=$posti_occupati+1;
		}
		
		my $miss=0;
		
		my $id_volo_temp=int($prenotazione->getAttribute("idV"));
		if($id_volo_temp!=$id_volo){
			$id_volo=$id_volo_temp;
			$miss=1;
		}
		my $data_prenotazione=$prenotazione->find("data");
		my $data_partenza=$prenotazione->find("dataPartenza");
		my $bagagli=$prenotazione->find("numeroBagagli");
		
		if($miss==1){ #se l'ID del volo è cambiato, allora rigenero tutto
			$tratta=get('/database/tabVolo/volo[@idV='.$id_volo.']/@idT');
			$ora_partenza=get('/database/tabVolo/volo[@idV='.$id_volo.']/oraPartenza');
			$prezzo=get('/database/tabVolo/volo[@idV='.$id_volo.']/prezzo');
			my $idAaP;
			my $idAaA;
			my $tratta=get('/database/tabTratta/tratta[@idT='.$tratta.']');
			foreach my $t ($tratta->get_nodelist){
				$idAaP=int($t->getAttribute('idApP'));
				$idAaA=int($t->getAttribute('idApA'));
				
			}
			$aereoporto_partenza=get('(/database/tabCitta/citta[@idC=(/database/tabAereoporto/aereoporto[@idAp=('.$idAaP.')]/@idC)])/nome')." ".get('/database/tabAereoporto/aereoporto[@idAp=('.$idAaP.')]/nome');
			$aereoporto_arrivo=get('(/database/tabCitta/citta[@idC=(/database/tabAereoporto/aereoporto[@idAp=('.$idAaA.')]/@idC)])/nome')." ".get('/database/tabAereoporto/aereoporto[@idAp=('.$idAaA.')]/nome');
		}
		my $servizi=get('/database/tabServizioPrenotato/servizioPrenotato[@idP='.int($id_P).']');
		my @servizi_prenotati;
		foreach my $temp ($servizi->get_nodelist){
			my @s_temp=(get('/database/tabServizio/servizio[@idS='.$temp->getAttribute("idS").']/nome'),get('/database/tabServizio/servizio[@idS='.$temp->getAttribute("idS").']/prezzo'));
			push @servizi_prenotati, \@s_temp;
		}
		#print "<p>$id, $posti_occupati, $tratta $id_volo, $aereoporto_partenza,$aereoporto_arrivo,$data_prenotazione, $data_partenza, $ora_partenza, $prezzo, $bagagli, \@servizi_prenotati</p>";
		my @temp=($id, $posti_occupati, "T$tratta"."V$id_volo", $aereoporto_partenza,$aereoporto_arrivo,$data_prenotazione, $data_partenza, $ora_partenza, $prezzo, $bagagli, \@servizi_prenotati,\@utenti); 
		push @out_prenotazioni, \@temp;
		
	}
	return \@out_prenotazioni;
}

sub salva_utente{
	my ($nome, $cognome, $cf, $nascita)=@_;
	my $presente=int(get('/database/tabUtente/utente[codiceFiscale="'.$cf.'"]/@idU'));
	if ($presente>0){ #è inutile aggiungere un utente con il codice fiscale duplicato!
		return $presente;
	}
	my $id=int(get('/database/tabUtente/utente/@idU[ not (.</database/tabUtente/utente/@idU)]'))+1;
	
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
	
	my $id=int(get('/database/tabServizioPrenotato/servizioPrenotato/@idSP[ not (.</database/tabServizioPrenotato/servizioPrenotato/@idSP)]'))+1;
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
	my @ser=@{$servizi};
	for (my $i=0; $i<scalar(@ser); $i++){
		#print "<p>$id_prenotazione, @ser[$i]->[0]</p>";
		salvaServizio($id_prenotazione,@ser[$i]->[0]);
	}
	#return 0;
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
	#devo prima aggiungere i servizi altrimenti, avendo già letto il file, mi annullerà tutte le altre modifiche!
	my $parser = XML::LibXML->new();
	my $db = $parser->parse_file($filename) or die;
	
	my $tab_prenotazioni=$db->findnodes('/database/tabPrenotazione')->[0];
	my $nodo=XML::LibXML::Element->new("prenotazione");
	
	my $today = Time::Piece->new();
	my $oggi=(($today->year))."-".$today->mon."-".$today->mday;
	
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
	
	my $string_passeggeri;
	#aggiungo i nodi per la prenotazione di piu' utenti.
	my $nodo_tabPasseggeriPrenotazione=$db->findnodes('/database/tabPasseggeriPrenotazione')->[0];
	
	my $max_id_passeggeriPrenotazione=int(get('/database/nodo_tabPasseggeriPrenotazione/passeggeriPrenotazione/@idPP[ not (.</database/nodo_tabPasseggeriPrenotazione/passeggeriPrenotazione/@idPP)]'))+1;
	for (my $i=0; $i<scalar(@passeggeri_id); $i++){
		
		my $nodo_passeggeriPrenotazione_temp=XML::LibXML::Element->new("passeggeriPrenotazione");
		$nodo_passeggeriPrenotazione_temp->setAttribute("idPP",$max_id_passeggeriPrenotazione);
		$nodo_passeggeriPrenotazione_temp->setAttribute("idP",$id_prenotazione);
		$nodo_passeggeriPrenotazione_temp->setAttribute("idU",$passeggeri_id[$i]);
		$max_id_passeggeriPrenotazione=$max_id_passeggeriPrenotazione+1;
		
		$nodo_tabPasseggeriPrenotazione->appendChild($nodo_passeggeriPrenotazione_temp);
		#<passeggeriPrenotazione idPP="1" idU="2" idP="1"/>
		#$string_passeggeri.=@passeggeri_id[$i];
		#if($i<(scalar(@passeggeri_id)-1)){
		#	$string_passeggeri.=",";
		#}
	}
	
	#$nodo->setAttribute("idU",$string_passeggeri);
	
	$tab_prenotazioni->addChild($nodo);
	
	set($db->toString(1));
	return $id_prenotazione;
}

sub modificaPrenotazione{
	my ($id_utente, $id_prenotazione, $rimuovi)=@_;
	my $parser = XML::LibXML->new();
	my $db = $parser->parse_file($filename) or die;
	my $test=get('/database/tabPrenotazione/prenotazione[@idP='.$id_prenotazione.' and @idUR='.$id_utente.']/data');
	if("".$test eq ""){
		return -1;
		#l'id non è stato trovato o l'utente non è lo stesso che ha prenotato
	}
	my $prenotazione=$db->findnodes('/database/tabPrenotazione/prenotazione[@idP='.$id_prenotazione.']')->[0];#rimuovo la prenotazione
	if($rimuovi==1){ 
		
		my $tab_p=$db->findnodes('/database/tabPrenotazione')->[0];
		$tab_p->removeChild($prenotazione);
		
		#ora rimuovo i vari servizi relativi alla prenotazione
		#in questo modo ottengo un database consistente, senza "sporcizia" causata da parziali rimozioni
		my $servizi=$db->findnodes('/database/tabServizio/servizioPrenotato[@idP='.$id_prenotazione.']');
		my $tab_servizi=$db->findnodes('/database/tabServizioPrenotato')->[0];
		foreach my $servizio ($servizi->get_nodelist){
			$tab_servizi->removeChild($servizio);
		}
	}
	#print $db->toString(1);
	return set( $db->toString(1));
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
	#$utenti=get('/database/tabUtente/utente/codiceFiscale="'.$cf.'"');
	#if(int($utenti)==1){
	#	return -2;
	#}
	my $max_id=salva_utente($nome, $cognome, $cf, $nascita);
				
	my $parser = XML::LibXML->new();
	my $db = $parser->parse_file($filename) or die;
	my $tab_utenti=$db->findnodes('/database/tabUtenteRegistrato')->[0];
	my $nodo=XML::LibXML::Element->new("utenteRegistrato");
	$nodo->setAttribute("idUR",$max_id);
	
	my $nodo_ban=XML::LibXML::Element->new("flagBann");
	my $n_n=XML::LibXML::Text->new("false");
	$nodo_ban->appendChild($n_n);
	$nodo->appendChild($nodo_ban);
	
	
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
		
		my $id="".$utente->getAttribute("idUR");
		my $admin=int(get('/database/tabAmministratore/amministratore[@idA='.$id.']/@idA'));
		if($admin > 0){
			$admin=1;
		}
		my $psw="".$utente->find("password");
		my $nome="".get('/database/tabUtente/utente[@idU='.$id.']/nome');
		my $cognome="".get('/database/tabUtente/utente[@idU='.$id.']/cognome');
		if($psw eq $password){
			@out=(1,$nome,$cognome, $id, $admin);
			return \@out;
		}
		@out=(-1,"","");
		return \@out;
	}
	@out=(-2,"","");
	return \@out;
}

### INIZIO FUNZIONI INERENTI AI VOLI
#variabili di cache: nel caso cui alcuni valori siano identici, allora non effettuo chiamate XPath
#migliora l'efficienza nell'esecuzione del codice. (nel caso cui sia richiamato nella funzione di "scacchiera" per la selezione dei voli).
#visto che questa funzione viene ripetuta 7 volte durante la generazione della scacchiera, alcuni valori rimangono costanti.
#Avendo una visualizzazione per tratta, i dati inerenti alla tratta rimarranno costanti, quindi è inutile ripetere la loro interrogazione.
#la libreria Exporter introduce i namespace, quindi le variabili "globali" all'interno di questa libreria rimangono interne alla libreria
#consentendo il riciclo dei nomi nelle altre librerie.


#sezione inerente agli aereoporti
my $id_partenza_getVoli=0;
my $volo_aereoporto_andata_getVoli; #nome dell'aereoporto d'andata

my $id_arrivo_getVoli=0;
my $volo_aereoporto_ritorno_getVoli; #nome dell'aereoporto di ritorno

#sezione inerente alla tratta
my $tratta_getVoli=0;
my $durata_getVoli=0;
my $id_tratta_getVoli=0;

#sezione inerente ai voli
my $voli_db_getVoli;
my @nodo_voli_getVoli;

#sezione inerente agli aerei
my $id_aereo_getVoli;
my $posti_disponibili_getVoli;
sub getVoli{

	#funzionamento:
	#- lista voli per tratta
	#- elenco prenotazioni per quel volo
	#- escludo se n°posti>posti disponibili per l'aereo
	my ($nome_andata, $nome_ritorno, $passeggeri, $data)=@_;
	#ora mi recupero l'ID tratta
	my $miss=0; #se i valori non sono identici alle variabili in cache
	
	if($nome_andata ne $volo_aereoporto_andata_getVoli){
		$miss=1; #la cache dev'essere rigenerata
		$volo_aereoporto_andata_getVoli=$nome_andata;
		my $aereoporto_partenza=get('/database/tabAereoporto/aereoporto[nome="'.$nome_andata.'" and flagAttivo="true"]');
		foreach my $aereoporto ($aereoporto_partenza->get_nodelist){
			$id_partenza_getVoli=$aereoporto->getAttribute("idAp");
		}
		if($id_partenza_getVoli==0){
			return undef;
		}
	}
	if($nome_ritorno ne $volo_aereoporto_ritorno_getVoli){
		$miss=1; #la cache dev'essere rigenerata
		$volo_aereoporto_ritorno_getVoli=$nome_ritorno;
		my $aereoporto_arrivo=get('/database/tabAereoporto/aereoporto[nome="'.$nome_ritorno.'" and flagAttivo="true"]');
		foreach my $aereoporto ($aereoporto_arrivo->get_nodelist){
			$id_arrivo_getVoli=$aereoporto->getAttribute("idAp");
		}
		if($id_arrivo_getVoli==0){
			return undef;
		}
	}
	if($miss==1){
		#rigenero la cache della tratta
		$tratta_getVoli=get('/database/tabTratta/tratta[@idApP='.$id_partenza_getVoli.' and @idApA='.$id_arrivo_getVoli.']');
	
		foreach my $tratta_temp ($tratta_getVoli->get_nodelist){
			$durata_getVoli=int($tratta_temp->find("durata"));
			$id_tratta_getVoli=$tratta_temp->getAttribute("idT");
		}
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
	
	my $mese=@gma[1];
	my $anno=@gma[2];
	
	if($miss==1){
		$voli_db_getVoli=get('/database/tabVolo/volo[@idT='.$id_tratta_getVoli.' and flagAttivo="true"]');
		@nodo_voli_getVoli=$voli_db_getVoli->get_nodelist;
	}
	my @voli;
	#<oraPartenza>00:00:00</oraPartenza>
	#<prezzo>12</prezzo>
	#<giorno>2</giorno>	
	#my @voli;
	#for (my $i=0; $i<$n; $i++){
	#	my @volo=('AZ000'.$i, '8:00', '10:00', '160', '4.75', $giorno);
	#	push @voli, \@volo; 
	#}
	foreach my $volo (@nodo_voli_getVoli){
		my $id_aereo_temp=int($volo->getAttribute("idAe"));
		if($id_aereo_temp!=$id_aereo_getVoli){
			$id_aereo_getVoli=$id_aereo_temp;
			my $aerei=get('/database/tabAereo/aereo[@idAe='.$id_aereo_getVoli.']');
			#mi ricavo i posti totali in base all'aereo che effettua il volo
			foreach my $aereo ($aerei->get_nodelist){
				my $id_tipo=int($aereo->getAttribute("idTA"));
				$posti_disponibili_getVoli=int(get('/database/tabTipoAereo/tipoAereo[@idTA='.$id_tipo.']/numeroPosti'));
			}
		}
		my $id_volo=int($volo->getAttribute("idV"));
		#print '/database/tabPrenotazione/prenotazione[@idV='.$id_volo.' and dataPartenza="'.$anno.'-'.$mese.'-'.$giorno.'"]';
		
		#questa query XPath è inevitabile e non può essere messa in cache: varia a seconda del volo.
		#ora sottraggo i posti disponibili in base alle prenotazioni
		my $prenotazioni=get('/database/tabPrenotazione/prenotazione[@idV='.$id_volo.' and dataPartenza="'.$anno.'-'.$mese.'-'.$giorno.'"]');
		#print $prenotazioni;
		
		# variabile che assume il valore dei posti disponibili per quel volo.
		#non modifico posti_disponibili, in quanto è una variabile che è paragonabile ad una costante
		#per il tipo di aereo.
		my $posti_disponibili_volo=$posti_disponibili_getVoli;
		foreach my $prenotazione ($prenotazioni->get_nodelist){
			#ora mi ricavo il numero di passeggeri + il prenotante.
			my $idPrenotazione=$prenotazione->getAttribute("idP");
			
			#tabPasseggeriPrenotazione
			my $nodo_passeggeri_prenotati=get('/database/tabPasseggeriPrenotazione/passeggeriPrenotazione[@idP="'.$idPrenotazione.'"]');
			foreach my $n_temp ($nodo_passeggeri_prenotati->get_nodelist){
				$posti_disponibili_volo -= 1;
			}
			$posti_disponibili_volo-=1;
			#visto che non mi interessa sapere chi c'è in quel volo, allora sottraggo semplicemente la grandezza del vettore + 1, in quanto è presente pure il passeggero prenotante
		}
		#print "<p>$posti_disponibili - $passeggeri</p>";
		my $orario="".$volo->find("oraPartenza");
		my $prezzo="".$volo->find("prezzo");
		my $giorno="".$volo->find("giorno");
		
		#conoscendo l'orario di partenza e la durata (in minuti), conosco l'orario di arrivo.
		my $t_andata =Time::Piece->strptime($orario, '%H:%M');
		#my $t_durata =Time::Piece->strptime((int(int($durata)/60)).":".int(int($durata)%60), '%H:%M');
		my $orario_arrivo=($t_andata+int($durata_getVoli)*60)->strftime('%H:%M');
		#my $t_andata = Time::Piece->strptime('%T', $orario);
		#my $t_arrivo=$t_andata;
		#<commento idCo="1" idUR="1" idA="2" idV="1">
		#my $commenti=get('//commento[@idV='.$id_volo.']');
		my $valutazione="N/D";
		#my $contatore=0;
		#foreach my $commento ($commenti->get_nodelist){
		#	$contatore++;
		#	$valutazione+=int($commento->find("voto"));
		#}
		#if($contatore>0){
		#	$valutazione=int($valutazione/$contatore);
		#}
		#if($valutazione==0){
		#	$valutazione="";
		#}
		my @v_temp=("T".$id_tratta_getVoli."V".$id_volo,$orario, $orario_arrivo,$prezzo,$valutazione, $data, $posti_disponibili_volo);
		if($posti_disponibili_volo>=($passeggeri)){
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

#mi genero l'array delle tratte
my %partenze;
my $nazioni_get= get('/database/tabNazione/nazione');
foreach my $node ($nazioni_get->get_nodelist) {
        my $id=$node->getAttribute("idN");
        my $nome_nazione=$node->find('nome');
        my $citta=get('/database/tabCitta/citta[@idN='.$id.']');
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


sub addStato{
	my ($stato, $id)=@_;
	if(int($id)==0){
		#aggiungo da zero
		my $id_stato=int(get('/database/tabNazione/nazione/@idN[ not (.</database/tabNazione/nazione/@idN)]'))+1;
		my $presente=int(get('/database/tabNazione/nazione[nome="'.$stato.'"]/@idN'));
		if($presente>0){
			return -1;
		}
		my $parser = XML::LibXML->new();
		my $db = $parser->parse_file($filename) or die;
		
		my $tab_nazioni=$db->findnodes('/database/tabNazione')->[0];
		my $nodo=XML::LibXML::Element->new("nazione");
		$nodo->setAttribute("idN",$id_stato);
	
		my $nodo_nome=XML::LibXML::Element->new("nome");
		my $n_n=XML::LibXML::Text->new($stato);
		$nodo_nome->appendChild($n_n);
		$nodo->appendChild($nodo_nome);
	
		$tab_nazioni->addChild($nodo);
		return set( $db->toString(1));
		
		
		}else{
			#modifico
			
			my $parser = XML::LibXML->new();
			my $db = $parser->parse_file($filename) or die;
			my $nazione=$db->findnodes('/database/tabNazione/nazione[@idN='.$id.']/nome/text()')->[0];
			if ($nazione eq ""){
				return -1;
				#utente non trovato
			}
			$nazione=$db->findnodes('/database/tabNazione/nazione[@idN='.$id.']')->[0];
			my $nome_nazione=$nazione->findnodes('nome/text()')->[0];
			$nome_nazione->setData($stato);
	
	
			set($db->toString(1));
			
		}
}
sub listStati{
	my @list_stati;
	my $db_stati=get('/database/tabNazione/nazione');
	foreach my $stato ($db_stati->get_nodelist){
		my @tmp=($stato->getAttribute("idN"), $stato->find("nome"));
		push @list_stati, \@tmp;
	}
	return \@list_stati;
}
sub addCitta
{
	my ($nome_citta, $stato,$id)=@_;
	if(int($id)==0){
		#aggiungo da zero
		my $id_citta=int(get('/database/tabCitta/citta/@idC[ not (.</database/tabCitta/citta/@idC)]'))+1;
		my $presente=int(get('/database/tabCitta/citta[nome="'.$nome_citta.'"]/@idN'));
		if($presente>0){
			return -1;
		}
		my $id_stato=int(get('/database/tabNazione/nazione[nome="'.$stato.'"]/@idN')); #mi ricavo l'id dello stato
		if($id_stato==0){
			return -1;
		}
		my $parser = XML::LibXML->new();
		my $db = $parser->parse_file($filename) or die;
		
		my $tab_nazioni=$db->findnodes('/database/tabCitta')->[0];
		my $nodo=XML::LibXML::Element->new("citta");
		$nodo->setAttribute("idN",$id_stato);
		$nodo->setAttribute("idC",$id_citta);
		# <citta idC="1" idN="1">
		my $nodo_nome=XML::LibXML::Element->new("nome");
		my $n_n=XML::LibXML::Text->new($nome_citta);
		$nodo_nome->appendChild($n_n);
		$nodo->appendChild($nodo_nome);
	
		$tab_nazioni->addChild($nodo);
		return set( $db->toString(1));
	}else{
		#modifico
			my $parser = XML::LibXML->new();
			my $db = $parser->parse_file($filename) or die;
			
			my $citta=$db->findnodes('/database/tabCitta/citta[@idC='.$id.']/nome/text()')->[0];
			if ($citta eq ""){
				return -1;
				#città non trovata
			}
			my $id_stato=int(get('/database/tabNazione/nazione[nome="'.$stato.'"]/@idN')); #mi ricavo l'id dello stato
			if($id_stato==0){
				return -1;
			}
			$citta=$db->findnodes('/database/tabCitta/citta[@idC='.$id.']')->[0];
			$citta->setAttribute("idN", $id_stato);
			my $nodo_nome_citta=$citta->findnodes('nome/text()')->[0];
			$nodo_nome_citta->setData($nome_citta);
			set($db->toString(1));
	}
}
sub listCitta{
	my ($stato)=@_;
	my @list_citta;
	my $id_stato=int(get('/database/tabNazione/nazione[nome="'.$stato.'"]/@idN')); #mi ricavo l'id dello stato
	if($id_stato==0){
		my $db_citta=get('/database/tabCitta/citta');
		foreach my $citta ($db_citta->get_nodelist){
		my @tmp=($citta->getAttribute("idC"), $citta->find("nome"));
		push @list_citta, \@tmp;
		}
		return \@list_citta;
	}
	my $db_citta=get('/database/tabCitta/citta[@idN='.$id_stato.']');
	foreach my $citta ($db_citta->get_nodelist){
		my @tmp=($citta->getAttribute("idC"), $citta->find("nome"));
		push @list_citta, \@tmp;
	}
	return \@list_citta;
}
sub addAereoporto	
{
	my ($aereoporto, $nome_citta, $id)=@_;
	if(int($id)==0){
		#aggiungo da zero
		#aggiungo da zero
		my $id_aereoporto=int(get('/database/tabAereoporto/aereoporto/@idAp[ not (.</database/tabAereoporto/aereoporto/@idAp)]'))+1;
		
		my $presente=int(get('/database/tabAereoporto/aereoporto[nome="'.$aereoporto.'"]/@idAp'));
		if($presente>0){
			return -1;
		}
		my $id_citta=int(get('/database/tabCitta/citta[nome="'.$nome_citta.'"]/@idC'));
		if($id_citta==0){
			return -1;
		}
		my $parser = XML::LibXML->new();
		my $db = $parser->parse_file($filename) or die;
		
		my $tab_aereoporti=$db->findnodes('/database/tabAereoporto')->[0];
		my $nodo=XML::LibXML::Element->new("aereoporto");
		
		$nodo->setAttribute("idAp",$id_aereoporto);
		$nodo->setAttribute("idC",$id_citta);
		# <citta idC="1" idN="1">
		my $nodo_attivo=XML::LibXML::Element->new("flagAttivo");
		my $n_n=XML::LibXML::Text->new("true");
		$nodo_attivo->appendChild($n_n);
		$nodo->appendChild($nodo_attivo);
		
		
		my $nodo_nome=XML::LibXML::Element->new("nome");
		my $n_n=XML::LibXML::Text->new($aereoporto);
		$nodo_nome->appendChild($n_n);
		$nodo->appendChild($nodo_nome);
	
		$tab_aereoporti->addChild($nodo);
		return set( $db->toString(1));
	}else{
		#modifico
			my $parser = XML::LibXML->new();
			my $db = $parser->parse_file($filename) or die;
			
			my $id_citta=int(get('/database/tabCitta/citta[nome="'.$nome_citta.'"]/@idC'));
			if($id_citta==0){
				return -1;
			}
			#print $id_citta;
			if(int(get('/database/tabAereoporto/aereoporto[@idAp='.$id.']/@idAp'))==0)
			{
				return -1;#l'aereoporto con questo id non esiste
			}
			my $nodo_aereoporto=$db->findnodes('/database/tabAereoporto/aereoporto[@idAp='.$id.']')->[0];
			$nodo_aereoporto->setAttribute("idC", $id_citta);
			my $nodo_nome_aereoporto=$nodo_aereoporto->findnodes('nome/text()')->[0];
			$nodo_nome_aereoporto->setData($aereoporto);
			set($db->toString(1));
	}
}
sub listAereoporti{
	my ($citta)=@_;
	my @list_aereoporti;
	my $id_citta=int(get('/database/tabCitta/citta[nome="'.$citta.'"]/@idC')); #mi ricavo l'id dello stato
	if($id_citta==0){
		my $db_aereoporti=get('/database/tabAereoporto/aereoporto');
		foreach my $aereoporto ($db_aereoporti->get_nodelist){
			my @tmp=($aereoporto->getAttribute("idAp"), $aereoporto->find("nome"));
			push @list_aereoporti, \@tmp;
		}
		return \@list_aereoporti;
	}
	my $db_aereoporti=get('/database/tabAereoporto/aereoporto[@idC='.$id_citta.']');
	foreach my $aereoporto ($db_aereoporti->get_nodelist){
		my @tmp=($aereoporto->getAttribute("idAp"), $aereoporto->find("nome"));
		push @list_aereoporti, \@tmp;
	}
	return \@list_aereoporti;
}
sub addTratta{
	my ($partenza, $arrivo, $durata, $id)=@_;
	
	if(int($id)==0){
		#aggiungo da zero
			if(int($durata)<1){
				return -10;
			}
			my $id_aereoporto_partenza=int(get('/database/tabAereoporto/aereoporto[nome="'.$partenza.'"]/@idAp'));
			if($id_aereoporto_partenza==0){
				return -8; #l'aereoporto non esiste
			}
			my $id_aereoporto_arrivo=int(get('/database/tabAereoporto/aereoporto[nome="'.$arrivo.'"]/@idAp'));
			if($id_aereoporto_arrivo==0){
				return -7; #l'aereoporto non esiste
			}
			if($id_aereoporto_partenza==$id_aereoporto_arrivo){
				return -5; #non posso decollare ed atterrare nello stesso aereoporto!
			}
			my $id_tratta=int(get('/database/tabTratta/tratta/@idT[ not (.</database/tabTratta/tratta/@idT)]'))+1;
			my $presente=int(get('/database/tabTratta/tratta[@idApP='.$id_aereoporto_partenza.' and @idApA='.$id_aereoporto_arrivo.']/@idT'));
			if($presente>0){
				return -1;
			}
			
			my $parser = XML::LibXML->new();
			my $db = $parser->parse_file($filename) or die;
		
			my $tab_tratte=$db->findnodes('/database/tabTratta')->[0];
			my $nodo=XML::LibXML::Element->new("tratta");
		
			$nodo->setAttribute("idT",$id_tratta);
			$nodo->setAttribute("idApP",$id_aereoporto_partenza);
			$nodo->setAttribute("idApA",$id_aereoporto_arrivo);
			# <citta idC="1" idN="1">
			my $nodo_durata=XML::LibXML::Element->new("durata");
			my $n_n=XML::LibXML::Text->new($durata);
			$nodo_durata->appendChild($n_n);
			$nodo->appendChild($nodo_durata);
		
			$tab_tratte->addChild($nodo);
			return set( $db->toString(1));
			
			
	}else{
		#modifico
			if(int($durata)<1){
				return -10;
			}
			
			my $id_aereoporto_partenza=int(get('/database/tabAereoporto/aereoporto[nome="'.$partenza.'"]/@idAp'));
			if($id_aereoporto_partenza==0){
				return -8; #l'aereoporto non esiste
			}
			my $id_aereoporto_arrivo=int(get('/database/tabAereoporto/aereoporto[nome="'.$arrivo.'"]/@idAp'));
			if($id_aereoporto_arrivo==0){
				return -7; #l'aereoporto non esiste
			}
			if($id_aereoporto_partenza==$id_aereoporto_arrivo){
				return -5; #non posso decollare ed atterrare nello stesso aereoporto!
			}
			my $id_tratta=int(get('/database/tabTratta/tratta[@idT='.$id.']/@idT'));
			if($id_tratta==0){
				return -1; #la tratta non esiste
			}
			
			my $parser = XML::LibXML->new();
			my $db = $parser->parse_file($filename) or die;
			
			my $nodo_tratta=$db->findnodes('/database/tabTratta/tratta[@idT='.$id.']')->[0];
			$nodo_tratta->setAttribute("idApP",$id_aereoporto_partenza);
			$nodo_tratta->setAttribute("idApA",$id_aereoporto_arrivo);
			my $nodo_tratta_durata=$nodo_tratta->findnodes('durata/text()')->[0];
			$nodo_tratta_durata->setData($durata);
			set($db->toString(1));
			
	}
}
sub getTratta{
			my ($partenza, $arrivo)=@_;
			if(($partenza eq "") and ($arrivo eq "")){
				my $tratte=get('/database/tabTratta/tratta');
				my @list_tratte;
				foreach my $tratta ($tratte->get_nodelist){
					my $id_partenza=$tratta->getAttribute("idApP");
					my $id_arrivo=$tratta->getAttribute("idApA");
					my $cittaP=get('/database/tabAereoporto/aereoporto[@idAp='.$id_partenza.']/nome');
					
					my $cittaA=get('/database/tabAereoporto/aereoporto[@idAp='.$id_arrivo.']/nome');
					my $durata=get('/database/tabTratta/tratta[@idT='.$tratta->getAttribute("idT").']/durata');
					#print "$id_partenza";
					my @temp=(
						$tratta->getAttribute("idT"),
						$cittaP,
						$cittaA,
						$durata
					);
					push @list_tratte, \@temp;
				}
				return \@list_tratte;
			}
			my $id_aereoporto_partenza=int(get('/database/tabAereoporto/aereoporto[nome="'.$partenza.'"]/@idAp'));
			if($id_aereoporto_partenza==0){
				return -8; #l'aereoporto non esiste
			}
			my $id_aereoporto_arrivo=int(get('/database/tabAereoporto/aereoporto[nome="'.$arrivo.'"]/@idAp'));
			if($id_aereoporto_arrivo==0){
				return -7; #l'aereoporto non esiste
			}
			if($id_aereoporto_partenza==$id_aereoporto_arrivo){
				return -5; #non posso decollare ed atterrare nello stesso aereoporto!
			}
			return get('/database/tabTratta/tratta[@idApP='.$id_aereoporto_partenza.' and @idApA='.$id_aereoporto_arrivo.']/@idT');
			
}
sub addVolo{
	my ($tratta, $orario_partenza, $prezzo, $attivo,$id)=@_;
	if(int($id)==0){
		#aggiungo da zero
			if(int($prezzo)<1){
				return -10;
			}
			my $id_tratta=int(get('/database/tabTratta/tratta[@idT='.$tratta.']/@idT'));
			if($id_tratta==0){
				return -1; #la tratta non esiste
			}
			
			if($orario_partenza eq ""){
				return -1;# non ho un orario!
			}
			
			
			my $id_volo=int(get('/database/tabVolo/volo/@idV[ not (.</database/tabVolo/volo/@idV)]'))+1;
			
			my $parser = XML::LibXML->new();
			my $db = $parser->parse_file($filename) or die;
			
			my $tab_voli=$db->findnodes('/database/tabVolo')->[0];
			my $nodo=XML::LibXML::Element->new("volo");
		
		#<flagAttivo>true</flagAttivo>
		#		<oraPartenza>00:00</oraPartenza>
		#		<prezzo>12</prezzo>
		#		<giorno>2</giorno>			
		#	</volo>
		
			$nodo->setAttribute("idV",$id_volo);
			$nodo->setAttribute("idT",$id_tratta);
			$nodo->setAttribute("idAe",1);
			# <citta idC="1" idN="1">
			
			my $nodo_attivo=XML::LibXML::Element->new("flagAttivo");
			if ($attivo>0){
				$attivo="true";
			}else{
				$attivo="false";
			}
			my $n_n=XML::LibXML::Text->new($attivo);
			$nodo_attivo->appendChild($n_n);
			$nodo->appendChild($nodo_attivo);
			
			my $nodo_partenza=XML::LibXML::Element->new("oraPartenza");
			my $n_n=XML::LibXML::Text->new($orario_partenza);
			$nodo_partenza->appendChild($n_n);
			$nodo->appendChild($nodo_partenza);
		
			my $nodo_prezzo=XML::LibXML::Element->new("prezzo");
			my $n_n=XML::LibXML::Text->new($prezzo);
			$nodo_prezzo->appendChild($n_n);
			$nodo->appendChild($nodo_prezzo);
			
			my $nodo_giorno=XML::LibXML::Element->new("giorno");
			my $n_n=XML::LibXML::Text->new(2);
			$nodo_giorno->appendChild($n_n);
			$nodo->appendChild($nodo_giorno);
		
			$tab_voli->addChild($nodo);
			return set( $db->toString(1));
			
	}else{
		#modifico
			if(int($prezzo)<1){
				return -10;
			}
			my $id_tratta=int(get('/database/tabTratta/tratta[@idT='.$tratta.']/@idT'));
			if($id_tratta==0){
				return -1; #la tratta non esiste
			}
			my $id_volo=int(get('/database/tabVolo/volo[@idV='.$id.']/@idV'));
			if($id_volo==0){
				return -1; #il volo non esiste
			}
			if($orario_partenza eq ""){
				return -1;# non ho un orario!
			}
			my $parser = XML::LibXML->new();
			my $db = $parser->parse_file($filename) or die;
			
			my $nodo_volo=$db->findnodes('/database/tabVolo/volo[@idV='.$id_volo.']')->[0];
			$nodo_volo->setAttribute("idT",$id_tratta);
			my $nodo_volo_attivo=$nodo_volo->findnodes('flagAttivo/text()')->[0];
			if($attivo==1){
				$nodo_volo_attivo->setData("true");
			}else{
				$nodo_volo_attivo->setData("false");
			}
			
			my $nodo_volo_orario=$nodo_volo->findnodes('oraPartenza/text()')->[0];
			$nodo_volo_orario->setData($orario_partenza);
			
			my $nodo_volo_prezzo=$nodo_volo->findnodes('prezzo/text()')->[0];
			$nodo_volo_prezzo->setData($prezzo);
			
			
			return set($db->toString(1));
			
	}
}

sub getVoli_totali{
	my @voli;
	my $tab_voli=get('/database/tabVolo/volo');
	foreach my $volo ($tab_voli->get_nodelist){
		my $id_volo=$volo->getAttribute("idV");
		my $id_tratta=$volo->getAttribute("idT");
		my $orario=$volo->find("oraPartenza");
		my $tratte=get('/database/tabTratta/tratta[@idT='.$id_tratta.']');
		my $tratta;
		foreach my $tmp ($tratte->get_nodelist){
			$tratta=$tmp;
			my $aereoporto_partenza=get('/database/tabAereoporto/aereoporto[@idAp='.$tratta->getAttribute('idApP').']/nome/text()');
			my $aereoporto_arrivo=get('/database/tabAereoporto/aereoporto[@idAp='.$tratta->getAttribute('idApA').']/nome/text()');
			my $prezzo=$volo->find('prezzo');
			my @v_t=(
				$id_volo,
				$orario,
				$aereoporto_partenza,
				$aereoporto_arrivo,
				$prezzo
			);
			push @voli, \@v_t;
		}
	}
	return \@voli;
}

sub addServizio{
	my ($nome, $descrizione, $prezzo, $id)=@_;
	if(int($id)==0){
		if(($nome eq "") | ($descrizione eq "") | ($prezzo eq "")){
			return -1;
		}
		#aggiungo da zero
		
			my $id_servizio=int(get('/database/tabServizio/servizio/@idS[ not (.</database/tabServizio/servizio/@idS)]'))+1;
			
			my $parser = XML::LibXML->new();
			my $db = $parser->parse_file($filename) or die;
			
			my $tab_servizi=$db->findnodes('/database/tabServizio')->[0];
			my $nodo=XML::LibXML::Element->new("servizio");
			$nodo->setAttribute("idS", $id_servizio);
			
			my $nodo_nome=XML::LibXML::Element->new("nome");
			my $n_n=XML::LibXML::Text->new($nome);
			$nodo_nome->appendChild($n_n);
			$nodo->appendChild($nodo_nome);
			
			my $nodo_descrizione=XML::LibXML::Element->new("descrizione");
			my $n_n=XML::LibXML::Text->new($descrizione);
			$nodo_descrizione->appendChild($n_n);
			$nodo->appendChild($nodo_descrizione);
			
			my $nodo_prezzo=XML::LibXML::Element->new("prezzo");
			my $n_n=XML::LibXML::Text->new($prezzo);
			$nodo_prezzo->appendChild($n_n);
			$nodo->appendChild($nodo_prezzo);
			
			
			$tab_servizi->addChild($nodo);
			return set($db->toString(1));
		
	}else{
		#modifico
		my $id_servizio=int(get('/database/tabServizio/servizio[@idS='.$id.']/@idS'));
		if($id_servizio==0){
			return -1;
			#servizio non trovato
		}
		if(($nome eq "") | ($descrizione eq "") | ($prezzo eq "")){
			return -1;
		}
		my $parser = XML::LibXML->new();
		my $db = $parser->parse_file($filename) or die;
			
		my $servizio=$db->findnodes('/database/tabServizio/servizio[@idS='.$id.']')->[0];
		
		my $nodo_nome=$servizio->findnodes('nome/text()')->[0];
		$nodo_nome->setData($nome);
		
		my $nodo_descrizione=$servizio->findnodes('descrizione/text()')->[0];
		$nodo_descrizione->setData($descrizione);
		
		my $nodo_prezzo=$servizio->findnodes('prezzo/text()')->[0];
		$nodo_prezzo->setData($prezzo);
		
		return set($db->toString(1));
	}
}

sub removeServizio {
	my ($id)=@_;
	my $parser = XML::LibXML->new();
	my $db = $parser->parse_file($filename) or die;
	my $test=get('/database/tabServizio/servizio[@idS='.$id.']/@idS');
	if("".$test eq ""){
		return -1;
		#l'id non è stato trovato
	}
	my $servizio=$db->findnodes('/database/tabServizio/servizio[@idS='.$id.']')->[0];#rimuovo la prenotazione
	my $tab_p=$db->findnodes('/database/tabServizio')->[0];
	$tab_p->removeChild($servizio);
		
	#print $db->toString(1);
	return set( $db->toString(1));
}

#sezione commenti
sub readCommenti {
	my ($idU, $idCO)=@_;
	my @contenitore_commenti;
	#commento: ID Valutazione Titolo Testo Volo
	my $path2='';
	if ($idCO > 0){
		$path2=' and @idCo='.$idCO;
	}
	my $tab_commenti_utente=get('/database/tabCommento/commento[@idUR='.$idU.$path2.']');
	foreach my $commento_node ($tab_commenti_utente->get_nodelist){
		my @commento_temp;
		push(@commento_temp, $commento_node->getAttribute('idCo'));
		push(@commento_temp, $commento_node->find('voto/text()'));
		push(@commento_temp, $commento_node->find('testo/titolo/text()'));
		push(@commento_temp, $commento_node->find('testo/contenuto/text()'));
		
		my $id_volo=$commento_node->getAttribute('idV');
		
		my $nodo_volo=get('/database/tabVolo/volo[@idV='.$id_volo.']')->[0];
		
		
		my $testo_volo='';
		my $id_tratta=$nodo_volo->getAttribute('idT');
		
		my $id_aereoporto_partenza=get('/database/tabTratta/tratta[@idT='.$id_tratta.']/@idApP');
		my $id_aereoporto_arrivo=get('/database/tabTratta/tratta[@idT='.$id_tratta.']/@idApA');
		
		my $aereoporto_partenza=get('/database/tabAereoporto/aereoporto[@idAp='.$id_aereoporto_partenza.']')->[0];
		my $nome_citta_partenza=get('/database/tabCitta/citta[@idC='.$aereoporto_partenza->getAttribute('idC').']/nome');
		my $aereoporto_arrivo=get('/database/tabAereoporto/aereoporto[@idAp='.$id_aereoporto_arrivo.']')->[0];
		my $nome_citta_arrivo=get('/database/tabCitta/citta[@idC='.$aereoporto_arrivo->getAttribute('idC').']/nome');
		
		my $orario=$nodo_volo->find('oraPartenza/text()');
		$testo_volo.=$nome_citta_partenza.' - '.$aereoporto_partenza->find('nome').' &rarr; '.$nome_citta_arrivo.' - '.$aereoporto_arrivo->find('nome').' ['.$orario.']';
		
		push(@commento_temp, $testo_volo);
		
		push(@contenitore_commenti, \@commento_temp);
	}
	return \@contenitore_commenti;
}

sub modificaCommento {
	my ($id, $titolo, $valutazione, $testo, $idUR)=@_;
	if(		(int($id)<1)|
			(length($titolo)<1) | 
			(int($valutazione) <1) | 
			(int($valutazione) >5) | 
			(length($testo)<1) | 
			(int($idUR) <1 )){
				return -1;
		}
	#print $titolo.' '.length($titolo);
	#verificare se id volo e id ur sono corretti:
	# se esistono tabUtenteRegistrato/UtenteRegistrato/@idUR=$idUR 
	# <tabCommento>
	#		<commento idCo='' idUR='' idA='' idV=''>
	#			<abilitato>1</abilitato>
	#			<voto>$valutazione</voto>
	#			<testo>
	#				<data>32/02/293939</data> <!-- data del commento-->
	#				<titolo></titolo>
	#				<contenuto>dfdsf</contenuto>
	
	my $id_commento=int(get('/database/tabCommento/commento[@idCo='.$id.' and @idUR='.$idUR.']/@idCo'));
	if ($id_commento==0){
		#commento non esiste
		return -1;
	}
	my $parser = XML::LibXML->new('1.0','UTF-8');
	my $db = $parser->parse_file($filename) or die;
			
	my $tab_commento=$db->findnodes('/database/tabCommento/commento[@idCo='.$id.']')->[0];
	
	my $nodo_abilitato=$tab_commento->findnodes('abilitato/text()')->[0];
	$nodo_abilitato->setData('1');
		
	my $nodo_voto=$tab_commento->findnodes('voto/text()')->[0];
	$nodo_voto->setData($valutazione);
		
	my $nodo_testo=$tab_commento->findnodes('testo')->[0];	
	
	my $nodo_data=$nodo_testo->findnodes('data/text()')->[0];
	
	my $today = Time::Piece->new();
	my $giorno=$today->mday;
	
	if (int($giorno)<10){
		$giorno='0'.$giorno;
	}
	my $mese=$today->mon;
	
	if (int($mese)<10){
		$mese='0'.$mese;
	}
	my $anno=$today->year;
	
	my $oggi=$giorno."/".$mese."/".$anno;
	
	$nodo_data->setData($oggi);
	
	my $nodo_titolo=$nodo_testo->findnodes('titolo/text()')->[0];
	$nodo_titolo->setData($titolo);
	
	my $nodo_contenuto=$nodo_testo->findnodes('contenuto/text()')->[0];
	$nodo_contenuto->setData($testo);
	
	#print $tab_commento->toString(1);
	return set($db->toString(1));
}

sub addCommento {
	my ($titolo, $valutazione, $testo, $idV, $idUR)=@_;
	
	if( 	($titolo eq "") | 
			(int($valutazione) <1) | 
			(int($valutazione) >5) | 
			($testo eq "") | 
			(int($idV) <1) | 
			(int($idUR) <1 ))
		{
				return -1;
		}
	#my $id_volo=int(get('/database/tabCommento/commento/@idCo[ not (.</database/tabCommento/commento/@idCo)]'))+1;
	#<commento idCo="1" idUR="1" idA="2" idV="1">
	#			<abilitato>1</abilitato>
	#			<voto>5</voto> 
	#			<testo>
	#				<data>28/12/2013</data>
	#				<titolo>wes</titolo>
	#				<contenuto>asjb</contenuto>
	#			</testo>
	#		</commento>
	#
	
	my $id_commento=int(get('/database/tabCommento/commento/@idCo[ not (.</database/tabCommento/commento/@idCo)]'))+1;
			
	my $parser = XML::LibXML->new('1.0','UTF-8');
	my $db = $parser->parse_file($filename) or die;
			
	my $tab_commenti=$db->findnodes('/database/tabCommento')->[0];
	my $nodo=XML::LibXML::Element->new("commento");
	$nodo->setAttribute("idCo", $id_commento);
	$nodo->setAttribute("idUR", $idUR);
	$nodo->setAttribute("idA", '1');
	$nodo->setAttribute("idV", $idV);
			
	my $nodo_abilitato=XML::LibXML::Element->new("abilitato");
	my $n_ab=XML::LibXML::Text->new('1');
	$nodo_abilitato->appendChild($n_ab);
	$nodo->appendChild($nodo_abilitato);
	
	my $nodo_voto=XML::LibXML::Element->new("voto");
	my $n_vo=XML::LibXML::Text->new($valutazione);
	$nodo_voto->appendChild($n_vo);
	$nodo->appendChild($nodo_voto);
	
	my $nodo_testo=XML::LibXML::Element->new("testo");
	
	my $nodo_data=XML::LibXML::Element->new("data");
	my $today = Time::Piece->new();
	my $giorno=$today->mday;
	
	if (int($giorno)<10){
		$giorno='0'.$giorno;
	}
	my $mese=$today->mon;
	
	if (int($mese)<10){
		$mese='0'.$mese;
	}
	my $anno=$today->year;
	
	my $oggi=$giorno."/".$mese."/".$anno;
	
	my $n_da=XML::LibXML::Text->new($oggi);
	
	$nodo_data->appendChild($n_da);
	
	$nodo_testo->appendChild($nodo_data);
	
	$nodo->appendChild($nodo_testo);
	
	
			
			
	$tab_commenti->addChild($nodo);
	#print $tab_commenti->toString(1);
	return set($db->toString(1));

}

1;