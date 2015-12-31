#!/usr/bin/perl

use CGI;
use CGI::Carp qw/fatalsToBrowser/;
use DBI;


1 ;
#################################################################################
sub Get_Header {

$localdb   = shift ;
$master    = shift ;

my $dbpw    = &PW() ;
my $dbus    = &USR() ;

$dbh = DBI->connect("DBI:mysql:orgmyr5_$localdb:localhost","$dbus","$dbpw") ;
$dbh2 = DBI->connect("DBI:mysql:orgmyr5_$master:localhost","$dbus","$dbpw") ;

#########################################################################################
# Table of booking parameters - table can be expanded with as many parameters as we need
# Logo    - site specific logo
# Phone   - 0 = do not display, 1 = display (in this example it is set to 1)
# Address - 0 = do not display, 1 = display (in this example it is set to 1)
# Hours   - 0 = do not display, 1 = display (in this example it is set to 0)
# Home    - url of Home page for navigation ;
$sql = "select `Logo`, `Phone`, `Address`, `Hours`, `Home` from `rm1_booking_parameters` where 1";
$sth = $dbh->prepare($sql) ;
$sth->execute() ;
while (@row = $sth->fetchrow_array()){
	$logo          = $row[0] ;
	$show_phone    = $row[1] ;
	$show_location = $row[2] ;
	$show_hours    = $row[3] ;
	$home_path     = $row[4] ;
}
$sth->finish() ;

# End of booking parameters
########################################################################################

########################################################################################
# Table of site specifics for this shop
$sql = "select `Name`,`Address`,`City`,`State`,`Zip`,`Phone` from `rm1_shop` where 1";
$sth = $dbh->prepare($sql) ;
$sth->execute() ;
my @shop_data = $sth->fetchrow_array() ;
$sth->finish() ;

$shop_name    = $shop_data[0] ;
$shop_address = $shop_data[1] ;
$shop_city    = $shop_data[2] ;
$shop_state   = $shop_data[3] ;
$shop_zip     = $shop_data[4] ;
$shop_phone   = $shop_data[5] ;

$sql = "select `Open`, `Close`, `Day`, `DOW` from `rm1_range_hours` where 1";
$sth = $dbh->prepare($sql) ;
$sth->execute() ;
while (@row = $sth->fetchrow_array()){
	$open      = $row[0] ;
	$close     = $row[1] ;
	$dayofweek = $row[2] ;
	$dow       = $row[3] ;
	if ($open ne "Closed"){$open = &Format($open)}
	if ($close ne "Closed"){$close = &Format($close)}
	if ($dow == 1){
		$q = "$open - $close";
		if ($open eq "Closed"){$q = "Closed"}
		$sun_hours = $q;
	}
	if ($dow == 2){
		$q = "$open - $close";
		if ($open eq "Closed"){$q = "Closed"}
		$mon_hours = $q;
	}
	if ($dow == 3){
		$q = "$open - $close";
		if ($open eq "Closed"){$q = "Closed"}
		$tue_hours = $q;
	}
	if ($dow == 4){
		$q = "$open - $close";
		if ($open eq "Closed"){$q = "Closed"}
		$wed_hours = $q;
	}
	if ($dow == 5){
		$q = "$open - $close";
		if ($open eq "Closed"){$q = "Closed"}
		$thu_hours = $q;
	}
	if ($dow == 6){
		$q = "$open - $close";
		if ($open eq "Closed"){$q = "Closed"}
		$fri_hours = $q;
	}
	if ($dow == 7){
		$q = "$open - $close";
		if ($open eq "Closed"){$q = "Closed"}
		$sat_hours = $q;
	}
}
$sth->finish() ;

# End of shop parameters
########################################################################################

$dbh->disconnect ;
$dbh2->disconnect ;

$shop_city_state = "$shop_city, $shop_state" ;

print <<WEB ;

	<div id="wrapper">
	  <div id="header">
		<span class="left">
		  <!-- $home_path = the Home parameter from the booking_paramaters table -->
		  <!-- $logo = the Logo parameter from the booking_paramaters table -->
		  <a href="$home_path" class="logo">
			<img alt="" src="$logo" /></a>
        </span>
		<div class="right">
WEB
		  ########## the following conditionals are site dependent based on values in the booking_parameters table
		  if ($show_phone == 1){
			print qq[
			<div class="section">
				<label for="phone">
					Phone:
				</label>
				<span class="phone">
					$shop_phone
				</span>
			</div>
			] ;
		  }
		  if ($show_location == 1){
			print qq[
			<div class="section">
				<label for="location">
					Location:
				</label>
				<span class="address">
					<span class="street">
						$shop_address
					</span>
					<span class="city">
						$shop_city,
					</span>
					<span class="state">
						$shop_state
					</span>
					<span class="zip">
						$shop_zip
					</span>
				</span>
			</div>
			] ;
		  }
		  if ($show_hours == 1){
			print qq[
				<div class="section hours-box">
					<label for="hours">
						Hours:
					</label>
					<span class="mon">
						Mon: $mon_hours
					</span>
					<span class="tue">
						Tue: $tue_hours
					</span>
					<span class="wed">
						Wed: $wed_hours
					</span>
					<span class="thu">
						Thu: $thu_hours
					</span>
					<span class="fri">
						Fri: $fri_hours
					</span>
					<span class="sat">
						Sat: $sat_hours
					</span>
					<span class="sat">
						Sun: $sun_hours
					</span>
				</div>
			  ] ;
		 }
		  print <<WEB ;
		</div>
	  </div>
		</div>
WEB
#########################################################################
sub Format{
	my $tm = shift ;
	$tm = "$tm:00";
	$tm = "$ymd $tm" ;
	$sql2 = "SELECT DATE_FORMAT('$tm', '%l %p')";
	$sth2 = $dbh->prepare($sql2) ;
	$sth2->execute() ;
	$format = $sth2->fetchrow_array() ;
	$sth2->finish() ;
	$format = lc($format);
	return $format ;
}
############################################################################
}
