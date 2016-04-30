#!/usr/bin/perl
package commenti;
use strict;
use DateTime;  #utilizzato per validare la data inserita
use Time::Piece;
use CGI::Carp qw(fatalsToBrowser);
use CGI qw(:standard);
use CGI;

my $q = new CGI; #parte mia


require "common_functions/print_header.cgi";
#require "common_functions/print_search.cgi"; #inutile: non viene sfruttato in questa pagina.
require "common_functions/print_content.cgi";
require "common_functions/print_footer.cgi";
require "common_functions/Session.cgi";
require "common_functions/check_form.cgi";
require "common_functions/database.cgi";
require "common_functions/menu.cgi";

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
my $form_control='<form action="script_commenti.cgi" method="post"> 
						<fieldset>
							<legend>commento</legend>
							<input type=”hidden” name=”idC” value=”$idC”>
							<input type=”hidden” name=”idV” value=”$idV”>
							<input type=”hidden” name=”idUR” value=”$idUR”>';

my error_count=0;
if($c1{idC}==0 and $c1{submit}==true and $q->param()){

	#il commento non esiste e devo salvarlo => creo un nuovo hash e lo stampo
		my $idC = $q->param('idC');
        my $idV = $q->param('idV');
        my $idUR = $q->param('idUR');
        my $valutazione = $q->param('valutazzione');
        my $titolo = $q->param('titolo');
        my $testo= $q->param('testo');
        if($valutazione==0){
        	print "<p> il tuo commento non ha un voto, vuoi inserirlo?</p>";
        		$form_control.='Valutazione:
							<select name="valutazione">
								<option value="0" checked="checked">non valutato</option>
								<option value="1">1</option>
								<option value="2">2</option>
								<option value="3">3</option>
								<option value="4">4</option>
								<option value="5">5</option>
							</select>
							</br>';
        }
        if($titolo==""){
        	print"<p>il tuo commento non ha un titolo vuoi inserirlo?</p>";
        	$form_control.='</br>
							<label for="titolo">Titolo:</label>
							<input type="text" name="titolo" id="titolo">$titolo</br>
							;'
        }
        if(testo==""){
        	if($valutazione >=1 or $titolo!=""){
        		print "<p>il tuo commento /&egrave privo di testo vuoi inserirne uno o lasciare solo una valutazione</p>";
        		$form_control.='<textarea name="testo" rows="5" col="30">$testo</br>';
        	}
        	else{
        		print "il tuo commento non &grave valido in quanto non fornisce sufficente informazione sul volo che hai effettuato";
        		$form_control.='<textarea name="testo" rows="5" col="30">$testo</textarea></br>';
        	}
        	
        }
        $form_control.='<input type="submit" value="Salva"></fieldset></form>'; #ve bene così??? temo che possa fare ciclo infinito xhe non so come passare i dati 
        #gia corretti forse devo tenere SEMPRE TUTTA la form?  
        if ($error_count!=0){
        	print '$form_control';
        }
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
else {
	if($c1{idC}!=0 and $c1{submit}==true){
		#il commento esiste e devo salvarlo => cerco l'hash con i giusti id e lo modifico
		
     	my $idC = $q->param('idC');
        my $idV = $q->param('idV');
        my $idUR = $q->param('idUR');
        my $valutazione = $q->param('valutazzione');
        my $titolo = $q->param('titolo');
        my $testo= $q->param('testo');

        if($valutazione==0){
        	print "<p> il tuo commento non ha un voto, vuoi inserirlo?</p>";
        		$form_control.='Valutazione:
							<select name="valutazione">
								<option value="0" checked="checked">non valutato</option>
								<option value="1">1</option>
								<option value="2">2</option>
								<option value="3">3</option>
								<option value="4">4</option>
								<option value="5">5</option>
							</select>
							</br>';
        }
        if($titolo==""){
        	print"<p>il tuo commento non ha un titolo vuoi inserirlo?</p>";
        	$form_control.='</br>
							<label for="titolo">Titolo:</label>
							<input type="text" name="titolo" id="titolo">$titolo</br>
							;'
        }
        if(testo==""){
        	if($valutazione >=1 or $titolo!=""){
        		print "<p>il tuo commento /&egrave privo di testo vuoi inserirne uno o lasciare solo una valutazione</p>";
        		$form_control.='<textarea name="testo" rows="5" col="30">$testo</br>';
        	}
        	else{
        		print "il tuo commento non &grave valido in quanto non fornisce sufficente informazione sul volo che hai effettuato";
        		$form_control.='<textarea name="testo" rows="5" col="30">$testo</textarea></br>';
        	}
        	
        }
        $form_control.='<input type="submit" value="Salva"></fieldset></form>'; #ve bene così??? temo che possa fare ciclo infinito xhe non so come passare i dati 
        #gia corretti forse devo tenere SEMPRE TUTTA la form?  
        if ($error_count!=0){
        	print '$form_control';
        }

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
		#il commento esiste e devo eliminarlo, questo va fatto direttamente sul database ma prima controllo che l'autore voglia davvero eliminarlo
		print"vuoi eliminare il commento sul volo $V?"# dal database troveremo poi altri dati da scrivere x identificare il commento: data ecc
		
		for (keys %c1){
        	delete $c1{$_}; #ok?
    	}
    	print "il commento effettuato dall'utente $idUR sul volo $idV è stato eliminato"
	}
}
