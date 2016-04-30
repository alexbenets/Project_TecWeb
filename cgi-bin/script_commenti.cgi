use strict;
 use warnings;
 use CGI;
 use CGI::Carp qw(fatalsToBrowser); # Remove this in production

 my $q = new CGI;
#form da manipolare NB SERVE UNA FUNZIONE PER VALIDARLA
#SE la form deve essere SALVATA
#la funzione controllerà se esistono campi vuoti:
#se il select valutazione è vuoto ""=>$errore.=non è stata  impostata una valutazione
#se il titolo è ""=>$errore.=non si è dato titolo al commento
#se il testo è""=>$errore.=il commento è vuoto
#puo esseci solo voto o solo commento con titolo MA l'utente deve dare conferma che è proprio quello che vuole inserire(!!! troppo complicato?)
#SE INVECE la form va ELIMINATA
#chiedo conferma e chiudo


my %c1= {
			idC => ""
			idV => "" #usando local posso creare variabili del pachage x passare?
			idUR => ""
			valutazione =>""
			titolo =>""
			testo =>""
			submit =>"" #usiamo un valore booleano? T<=> ho analizzato la form e devo salvare; F altrimenti
			cancella =>  ""#usiamo un valore booleano? T<=> ho analizzato la form, è un commento scritto da cancellare; F altrimenti
		}


if($c1{idC}==0 and $c1{submit}==true and $q->param()){
	#il commento non esiste e devo salvarlo => creo un nuovo hash e lo stampo
		my $idC = $q->param('idC');
        my $idV = $q->param('idV');
        my $idUR = $q->param('idUR');
        my $valutazione = $q->param('valutazzione');
        my $titolo = $q->param('titolo');
        my $testo= $q->param('testo');


        print $q->("utente $idUR");
        print $q->p("volo $idV, valutazione $valutazione, titolo $titolo, testo $testo");

     	%c1= {
			idC => 0
			idV => $idV #usando local posso creare variabili del pachage x passare?
			idUR => $idUR
			valutazione =>$valutazione
			titolo =>$titolo
			testo =>$testo
			submit =>true #usiamo un valore booleano? T<=> ho analizzato la form e devo salvare; F altrimenti
			cancella =>  false#usiamo un valore booleano? T<=> ho analizzato la form, è un commento scritto da cancellare; F altrimenti
		}
}

else {
	if($c1{idC}!=0 and $c1{submit}==true){
		#il commento esiste e devo salvarlo => cerco l'hash con i giusti id e lo modifico
		
     	my $idC = $q->param('idC');
        my $idV = $q->param('idV');
        my $idUR = $q->param('idUR');
        my $valutazione = $q->param('valutazzione');
        my $titolo = $q->param('titolo');
        my $testo= $q->param('testo');


        print $q->("utente $idUR");
        print $q->p("volo $idV, valutazione $valutazione, titolo $titolo, testo $testo");

     	%c1= {
			idC => $idC
			idV => $idV #usando local posso creare variabili del pachage x passare?
			idUR => $idUR
			valutazione =>$valutazione
			titolo =>$titolo
			testo =>$testo
			submit =>true #usiamo un valore booleano? T<=> ho analizzato la form e devo salvare; F altrimenti
			cancella =>  false#usiamo un valore booleano? T<=> ho analizzato la form, è un commento scritto da cancellare; F altrimenti
		}
	}
	else{
		#il commento esiste e devo eliminarlo
		for (keys %c1){
        	delete $c1{$_}; #ok?
    	}
    	print "il commento effettuato dall'utente $idUR sul volo $idV è stato eliminato"
	}
}
