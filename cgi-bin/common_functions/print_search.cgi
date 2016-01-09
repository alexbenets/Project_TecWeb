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
				<form action=\"../cgi-bin/search.cgi\" method=\"post\">
					<fieldset>
						<div class=\"casella_AR\">
							<label for=\"andata\">solo andata</label>
							<input type=\"radio\" name=\"AR\" id=\"andata\" value=\"andata\"  checked=\"checked\"/>
						</div>
						<div class=\"casella_AR\">
							<label for=\"ritorno\">andata e ritorno</label>
							<input type=\"radio\" name=\"AR\" id=\"ritorno\" value=\"ritorno\"/>
						</div>
						<div class=\"clearer\"></div>

						<div class=\"casella_partenza\">
							<label for=\"partenza\">Partenza:</label>
							<select name=\"partenza\" class=\"partenza\">
								<optgroup label=\"ITALIA\">
									<option>Milano - Malpensa</option>
									<option>Milano - Linate</option>
								</optgroup>
							</select>
						</div>
						<div class=\"casella_arrivo\">					
							<label for=\"arrivo\">Arrivo:</label>
							<select name=\"arrivo\" class=\"arrivo\">
								<optgroup label=\"ITALIA\">
									<option>Milano - Malpensa</option>
									<option>Milano - Linate</option>
								</optgroup>
							</select>
						</div>
						
						<div class=\"casella_dataPartenza\">
							<label for=\"data_partenza\">Data Partenza:</label>
							<input type=\"text\" name=\"data_partenza\" id=\"data_partenza\" value=\"Data Partenza\"></input>
						</div>
						<div class=\"casella_dataRitorno\">
							<label for=\"data_ritorno\">Data Ritorno:</label>
							<input type=\"text\" name=\"data_ritorno\" id=\"data_ritorno\" value=\"Data Ritorno\"></input>
						</div>

						<div class=\"casella_passeggeri\">
							<label for=\"n_passeggeri\">numero Passeggeri:</label>
							<select name=\"passeggeri\" class=\"passeggeri\">
								<option>1 passeggero</option>
								<option>2 passeggeri</option>
								<option>3 passeggeri</option>
								<option>4 passeggeri</option>
								<option>5 passeggeri</option>
								<option>6 passeggeri</option>
								<option>7 passeggeri</option>
								<option>8 passeggeri</option>
								<option>9 passeggeri</option>
								<option>10 passeggeri</option>
							</select>
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

" }

$out = "";

1;