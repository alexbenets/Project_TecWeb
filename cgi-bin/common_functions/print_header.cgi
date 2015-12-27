#!/usr/bin/perl
package print_header;
require      Exporter;

our @ISA       = qw(Exporter);
our @EXPORT    = qw(camel);    # Symbols to be exported by default
our @EXPORT_OK = qw($out);  # Symbols to be exported on request
our $VERSION   = 1.00;         # Version number

### Include your variables and functions here

sub print { return "
		<div id=\"header\">
			<div id=\"banner\">
				<h1>Vola con noi &copy;</h1>
				<h2>Prenota il tuo volo per la destinazione che ti pare e piace :(</h2>
			</div><!-- chiudo banner-->
			
			<div id=\"menu\">
				<a href=\"index.html\" class=\"selected\"  >Home</a>
				<a href=\"#\" >Pagina1</a>
				<a href=\"#\" >Pagina2</a>
			</div><!-- chiudo menu -->
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

" }

$out = "";

1;