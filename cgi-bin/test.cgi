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
require "common_functions/menu.cgi";

print CGI::header();#imposto il cookie di sessione


print database::aggiornaUtente(3, "Nome", "cognome", "CF", "32/02/1987", "password", "ajeje");

#print database::salvaServizio(1,2);