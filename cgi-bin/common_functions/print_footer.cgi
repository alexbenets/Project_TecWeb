#!/usr/bin/perl
package print_footer;
require      Exporter;

our @ISA       = qw(Exporter);
our @EXPORT    = qw(camel);    # Symbols to be exported by default
our @EXPORT_OK = qw($out);  # Symbols to be exported on request
our $VERSION   = 1.00;         # Version number

### Include your variables and functions here

sub print { return "
		<div id=\"footer\">
			<div id=\"sitemap\">
				<a href=\"#\">Mappa del sito</a>
			</div> <!-- chiudo sitemap -->
			<div id=\"dati_aziendali\">
				<p>Volare con noi soc. irresponsabilit&agrave; illimitata</p>
				<p>P.IVA: Zanicchi</p>
			</div><!-- chiudo dati aziendali -->
			<div id=\"gruppo\">
				<p>An project by: MarAlFraMar</p>
			</div><!-- chiudo div del gruppo -->
			<div id=\"validazione\">
				<p class=\"html_valido\">
    				<a href=\"http://validator.w3.org/check?uri=referer\"><img 
    				src=\"http://www.w3.org/Icons/valid-xhtml10\" alt=\"Valid XHTML 1.0 Strict\" height=\"31\" width=\"88\" /></a>
	  			</p>
				<p class=\"css_valido\">
					<a href=\"http://jigsaw.w3.org/css-validator/check/referer\">
    					<img style=\"border:0;width:88px;height:31px\"
        				src=\"http://jigsaw.w3.org/css-validator/images/vcss-blue\"
        				alt=\"CSS Valido!\" />
    				</a>
				</p>
				<div class=\"clearer\"></div> <!-- chiudo i float -->
			</div><!-- chiudo div validazione -->
		</div><!-- chiudo footer-->

" }

$out = "";

1;