#!/usr/bin/perl


package registrati_page;
use CGI::Carp qw(fatalsToBrowser);
use strict;

use CGI qw(:standard);
use CGI;



require "common_functions/print_header.cgi";
require "common_functions/print_search.cgi";
require "common_functions/print_content.cgi";
require "common_functions/print_footer.cgi";
require "common_functions/check_form.cgi";
require "common_functions/Session.cgi";
require "common_functions/database.cgi";

print CGI::header();#imposto il cookie di sessione

my @passeggeri;
my @passeggero=("Marco","Pettenuzzo", "PTTMRC87A12L840W", "12/01/1987");
push @passeggeri, \@passeggero;
my @passeggero=("Test","Cognome", "CNMTST87A12L840W", "12/01/1987");
push @passeggeri, \@passeggero;

my @servizi;
push @servizi, 1;

my $id= database::prenota(1, "12/02/2016","T3V6", \@passeggeri,\@servizi);
print $id;

#print database::salvaServizio(1,2);