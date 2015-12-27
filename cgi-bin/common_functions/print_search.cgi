#!/usr/bin/perl
package print_search;
require      Exporter;

our @ISA       = qw(Exporter);
our @EXPORT    = qw(camel);    # Symbols to be exported by default
our @EXPORT_OK = qw($out);  # Symbols to be exported on request
our $VERSION   = 1.00;         # Version number

### Include your variables and functions here

sub print { return "
		<div id=\"prenota\"><!-- div che contiene il box per la prenotazione-->
				<form action=\"#\" method=\"post\">
					<fieldset>
						<div class=\"casella_form\">
							<label for=\"partenza\">Partenza:</label>
							<input type=\"text\" name=\"partenza\" id=\"partenza\" value=\"Da\"></input>
						</div>
						<div class=\"casella_form\">					
							<label for=\"arrivo\">Arrivo:</label>
							<input type=\"text\" name=\"arrivo\" id=\"arrivo\" value=\"A\"></input>
						</div>
						<div class=\"button_form\">									
							<button type=\"submit\" name=\"cerca\" id=\"cerca\">
								<span>cerca</span>
							</button>
						</div>
						<div class=\"clearer\"></div>
						<div class=\"casella_AR\">
							<label for=\"andata\">andata e ritorno </label>
							<input type=\"checkbox\" name=\"AR\" id=\"andata\" value=\"1\" checked=\"checked\" />
						</div>
						
						
						<div class=\"clearer\"></div>
					</fieldset>
				</form>
			</div><!-- chiudo prenota -->

" }

$out = "";

1;