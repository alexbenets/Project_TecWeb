#!/usr/bin/perl
package print_content;
require      Exporter;

our @ISA       = qw(Exporter);
our @EXPORT    = qw(camel);    # Symbols to be exported by default
our @EXPORT_OK = qw($out);  # Symbols to be exported on request
our $VERSION   = 1.00;         # Version number

### Include your variables and functions here

sub print { return "
		<div id=\"contenuto\">
				<div id=\"secondo_menu\">
					<ul>
						<li><a href=\"#S1\">Paragrafo 1</a></li>
						<li><a href=\"#S2\">Paragrafo 2</a></li>
						<li><a href=\"#S3\">Paragrafo 2</a></li>
						<li><a href=\"#S4\">Paragrafo 2</a></li>
						<li><a href=\"#S5\">Paragrafo 2</a></li>
						<li><a href=\"#S6\">Paragrafo 2</a></li>
					</ul>
				</div><!-- chiudo secondo menu -->
				<div id=\"contenitore_sezioni\"><!-- apro maxi contenitore per le sezioni -->
					<div class=\"sezione\" id=\"S1\"><!-- inizio div che contiene titolo e sezione dell'articolo -->
						<h3>Paragrafo</h3>
						<p>Qui ci v&agrave; qualcosa come un contenuto statico, automaticamente generato, form di prenotazione, ecc...</p>
						<p>Qui ci v&agrave; qualcosa come un contenuto statico, automaticamente generato, form di prenotazione, ecc...</p>
						<p>Qui ci v&agrave; qualcosa come un contenuto statico, automaticamente generato, form di prenotazione, ecc...</p>
						<p>Qui ci v&agrave; qualcosa come un contenuto statico, automaticamente generato, form di prenotazione, ecc...</p>
						<p>Qui ci v&agrave; qualcosa come un contenuto statico, automaticamente generato, form di prenotazione, ecc...</p>
					</div><!-- chiudo sezione -->
					<div class=\"sezione\" id=\"S2\"><!-- inizio div che contiene titolo e sezione dell'articolo -->
						<h3>Paragrafo</h3>
						<p>Qui ci v&agrave; qualcosa come un contenuto statico, automaticamente generato, form di prenotazione, ecc...</p>
						<p>Qui ci v&agrave; qualcosa come un contenuto statico, automaticamente generato, form di prenotazione, ecc...</p>
						<p>Qui ci v&agrave; qualcosa come un contenuto statico, automaticamente generato, form di prenotazione, ecc...</p>
						<p>Qui ci v&agrave; qualcosa come un contenuto statico, automaticamente generato, form di prenotazione, ecc...</p>
						<p>Qui ci v&agrave; qualcosa come un contenuto statico, automaticamente generato, form di prenotazione, ecc...</p>
					</div><!-- chiudo sezione -->
					<div class=\"sezione\" id=\"S3\"><!-- inizio div che contiene titolo e sezione dell'articolo -->
						<h3>Paragrafo</h3>
						<p>Qui ci v&agrave; qualcosa come un contenuto statico, automaticamente generato, form di prenotazione, ecc...</p>
						<p>Qui ci v&agrave; qualcosa come un contenuto statico, automaticamente generato, form di prenotazione, ecc...</p>
						<p>Qui ci v&agrave; qualcosa come un contenuto statico, automaticamente generato, form di prenotazione, ecc...</p>
						<p>Qui ci v&agrave; qualcosa come un contenuto statico, automaticamente generato, form di prenotazione, ecc...</p>
						<p>Qui ci v&agrave; qualcosa come un contenuto statico, automaticamente generato, form di prenotazione, ecc...</p>
					</div><!-- chiudo sezione -->
					<div class=\"sezione\" id=\"S4\"><!-- inizio div che contiene titolo e sezione dell'articolo -->
						<h3>Paragrafo</h3>
						<p>Qui ci v&agrave; qualcosa come un contenuto statico, automaticamente generato, form di prenotazione, ecc...</p>
						<p>Qui ci v&agrave; qualcosa come un contenuto statico, automaticamente generato, form di prenotazione, ecc...</p>
						<p>Qui ci v&agrave; qualcosa come un contenuto statico, automaticamente generato, form di prenotazione, ecc...</p>
						<p>Qui ci v&agrave; qualcosa come un contenuto statico, automaticamente generato, form di prenotazione, ecc...</p>
						<p>Qui ci v&agrave; qualcosa come un contenuto statico, automaticamente generato, form di prenotazione, ecc...</p>
					</div><!-- chiudo sezione -->
					<div class=\"sezione\" id=\"S5\"><!-- inizio div che contiene titolo e sezione dell'articolo -->
						<h3>Paragrafo</h3>
						<p>Qui ci v&agrave; qualcosa come un contenuto statico, automaticamente generato, form di prenotazione, ecc...</p>
						<p>Qui ci v&agrave; qualcosa come un contenuto statico, automaticamente generato, form di prenotazione, ecc...</p>
						<p>Qui ci v&agrave; qualcosa come un contenuto statico, automaticamente generato, form di prenotazione, ecc...</p>
						<p>Qui ci v&agrave; qualcosa come un contenuto statico, automaticamente generato, form di prenotazione, ecc...</p>
						<p>Qui ci v&agrave; qualcosa come un contenuto statico, automaticamente generato, form di prenotazione, ecc...</p>
					</div><!-- chiudo sezione -->
					<div class=\"sezione\" id=\"S6\"><!-- inizio div che contiene titolo e sezione dell'articolo -->
						<h3>Paragrafo</h3>
						<p>Qui ci v&agrave; qualcosa come un contenuto statico, automaticamente generato, form di prenotazione, ecc...</p>
						<p>Qui ci v&agrave; qualcosa come un contenuto statico, automaticamente generato, form di prenotazione, ecc...</p>
						<p>Qui ci v&agrave; qualcosa come un contenuto statico, automaticamente generato, form di prenotazione, ecc...</p>
						<p>Qui ci v&agrave; qualcosa come un contenuto statico, automaticamente generato, form di prenotazione, ecc...</p>
						<p>Qui ci v&agrave; qualcosa come un contenuto statico, automaticamente generato, form di prenotazione, ecc...</p>
					</div><!-- chiudo sezione -->
					
					<div id=\"torna_su\">
						<a href=\"#header\">Torna su</a>
					</div>
				</div><!-- chiudo contenitore_sezioni -->	
				<div id=\"news\"><!-- apro news-->
					<ul>
						<li>
							<a href=\"#\" >
								<span class=\"riquadro_news\">
									<span class=\"titolo_news\">News1</span>
									<span class=\"descrizione_news_breve\">Descrizione</span>
								</span>
							</a>
						</li>
						<li>
							<a href=\"#\" >
								<span class=\"riquadro_news\">
									<span class=\"titolo_news\">News1</span>
									<span class=\"descrizione_news_breve\">Descrizione</span>
								</span>
							</a>
						</li>
						<li>
							<a href=\"#\" >
								<span class=\"riquadro_news\">
									<span class=\"titolo_news\">News1</span>
									<span class=\"descrizione_news_breve\">Descrizione</span>
								</span>
							</a>
						</li>
						
					</ul>
				</div>
				<!-- chiudo news -->
				<div class=\"clearer\"></div>
			</div><!-- chiudo contenuto-->

" }

$out = "";

1;