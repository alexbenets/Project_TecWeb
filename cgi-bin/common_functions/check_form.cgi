#!/usr/bin/perl
package check_form;
require      Exporter;

our @ISA       = qw(Exporter);
our $VERSION   = 1.00;         # Version number

### Include your variables and functions here
# qui vengono dichiarati tutti i metodi per la validazione dei form
# come verifica email, nome, data, ecc...
#
#

use DateTime;  #utilizzato per validare la data inserita
use Time::Piece;

#estraggo i numeri dal select per selezionare i passeggeri
#se non ci sono passeggeri, allora $1 non sarà definito e, quindi, riporto 0.
sub leggi_numeri {
	my ($numeri)=@_;
	$numeri =~/([0-9]+)/;
	if(defined($1)){
		return $1;
	}
	return 0;
}

#funzione per verificare se il formato della data è corretto; recupera il giorno, il mese e l'anno dalla data inserita.
#il formato è GG MM AAAA
# i separatori accettati sono: \ / . : -
sub regexp_data{
	my ($data)=@_;
	if(!defined $data){
		return 0;
	}
	$data =~/^([\d]{1,2})([\/-:\.\\ -]+)([\d]{1,2})([\/-:\.\\ -]+)+([\d]{4})$/;
	my $giorno=$1;
	if (int($giorno)<10){
		$giorno='0'.$giorno;
	}
	my $mese=$3;
	if (int($mese)<10){
		$mese='0'.$mese;
	}
	
	my $anno=$5;
	my @arr=($giorno, $mese, $anno);
	return \@arr;
}

#controlla la data di nascita dei passeggeri, se sono neonati o matusalemme, non possono viaggiare.
sub controlla_data_passeggero {
	my ($data)=@_;
	my $gma=regexp_data($data);
	my $giorno=$gma->[0];
	my $mese=$gma->[1];
	my $anno=$gma->[2];	
	if ($anno<1900){
		return 0;
		#la funzione Time::Piece fallisce se l'anno è inferiore al 1900.
		#questo controllo iniziale evita l'errore.
	}
	eval {
		my $dt1 =  DateTime->new( year => $anno, month => $mese, day => $giorno);
	};
	if($@){
		return 0;#data non valida
	}else{
		my $today = Time::Piece->new();
		my $oggi=$today->year."/".$today->mon."/".$today->mday;
		my $dt1 =  Time::Piece->strptime($oggi, "%Y/%m/%d");
		my $dt2 =  Time::Piece->strptime("$anno/$mese/$giorno", "%Y/%m/%d");
		my $d = ($dt1 - $dt2)->years;
		#controllo se l'utente è troppo giovane o troppo anziano
		#sotto il primo anno, il neonato non può viaggiare in aereo
		#sopra i 100 anni, nonostante i migliori auguri e l'incremento 
		#dell'aspettativa di vita, è improbabile che l'utente  sia ancora tra noi e/o che sia ancora in grado di utilizzare
		#il computer, visto il decadimento delle funzioni cognitive, visive ed uditive.
		if($d<1 | $d>100){
			return 0;
		}
		return 1;
	}
}

#estraggo la data dal form di ricerca: se la data non è valida (nel formato) e non è compresa tra "domani" e +1 anno, ritorno 0
#se la data è valida e rispetta le condizioni di +1d..+365d, allora ritorno la data.
sub leggi_data {
	my ($data)=@_;
	if(!defined $data){
		return 0;
	}
	my $gma=regexp_data($data);
	my $giorno=$gma->[0];
	my $mese=$gma->[1];
	my $anno=$gma->[2];
	if ($anno<1900){
		return 0;
		#la funzione Time::Piece fallisce se l'anno è inferiore al 1900.
		#questo controllo iniziale evita l'errore.
	}
	eval {
		my $dt1 =  DateTime->new( year => $anno, month => $mese, day => $giorno);
	};
	if($@){
		return 0;#data non valida
	}else{
		my $today = Time::Piece->new();
		my $oggi=$today->year."/".$today->mon."/".$today->mday;
		my $dt1 =  Time::Piece->strptime($oggi, "%Y/%m/%d");
		my $dt2 =  Time::Piece->strptime("$anno/$mese/$giorno", "%Y/%m/%d");
		my $d = ($dt2 - $dt1)->days;
		#controllo se la data è troppo avanti o indietro nel tempo
		
		if($d<1 | $d>365){
			return 0;
		}
	}
	
	return "$giorno/$mese/$anno";
}


#controllo se la data inserita è corretta e se l'utente è maggiorenne e non matusalemme.
sub valida_data{
	my ($data)=@_;
	if(!defined $data){
		return 0;
	}
	my $gma=regexp_data($data);
	my $giorno=$gma->[0];
	my $mese=$gma->[1];
	my $anno=$gma->[2];	
	if ($anno<1900){
		return 0;
		#la funzione Time::Piece fallisce se l'anno è inferiore al 1900.
		#questo controllo iniziale evita l'errore.
	}
	eval {
		my $dt1 =  DateTime->new( year => $anno, month => $mese, day => $giorno);
	};
	if($@){
		return 0;#data non valida
	}else{
		my $today = Time::Piece->new();
		my $oggi=$today->year."/".$today->mon."/".$today->mday;
		my $dt1 =  Time::Piece->strptime($oggi, "%Y/%m/%d");
		my $dt2 =  Time::Piece->strptime("$anno/$mese/$giorno", "%Y/%m/%d");
		my $d = ($dt1 - $dt2)->years;
		#controllo se l'utente è troppo giovane o troppo anziano
		#sotto i 18 anni non può prenotare il volo.
		#sopra i 100 anni, nonostante i migliori auguri e l'incremento 
		#dell'aspettativa di vita, è improbabile che l'utente  sia ancora tra noi e/o che sia ancora in grado di utilizzare
		#il computer, visto il decadimento delle funzioni cognitive, visive ed uditive.
		if($d<18 | $d>100){
			return 0;
		}
		return 1;
	}
}


#controllo se l'email è corretta.
sub valida_email {
	my ($email)=@_;
	$email =~/^([\w\-\+\.]+)\@([\w\-\+\.]+)\.([\w\-\+\.]+)$/;
	if ( "$1\@$2.$3" eq $email){
		return 1; #email corretta secondo l'espressione regolare
	}
	return 0;
}

#controllo se il nominativo contiene solo lettere
sub valida_nominativo {
	my ($nome)=@_;
	$nome =~/^([a-zA-Z\s]+)$/;
	if ( "$1" eq $nome){
		return 1; #nominativo corretto, non contiene caratteri differenti da lettere e spazi
	}
	return 0;
}


#controllo se il codice fiscale è nel formato corretto
sub valida_codice_fiscale {
	my ($codice_fiscale)=@_;
	$codice_fiscale =~/^([a-zA-Z]{6}[\d]{2}[a-zA-Z]{1}[\d]{2}[a-zA-Z]{1}[\d]{3}[a-zA-Z]{1})$/;
	#print "$1 $2 $3 $4 $5 $6 $7";
	if( "$1$2$3$4$5$6$7" eq $codice_fiscale){
		return 1;#è corretto
	}
	return 0;#non è corretto
}


sub converti_caratteri {
	my ($testo)=@_;
	my $testo_convertito='';
	
	return $testo_convertito;	
}

1;