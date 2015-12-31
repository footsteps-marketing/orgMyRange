#!/usr/bin/perl

print "Content-type: text/html\n\n";

use CGI;
use CGI::Carp qw/fatalsToBrowser/;
use DBI;
use DateTime ;
#use CGI::Cookie;

require("rm_config.cgi") ;
require("rm_dt_now.cgi") ;
require("rm_alert.cgi") ;
require("rm_web_league_header.cgi") ;


print <<WEB ;

<!DOCTYPE html>

<html lang="en">
  <head>
    <title>Archery Training and Classes|$shop</title>

<link rel="stylesheet" type="text/css" href="ata_style.css">
<link rel="stylesheet" type="text/css" href="style.css">

<script>
function loadwindow(){
	//alert("cartid " + document.myform.cartid.value)
}

function checkform(){
	return true;
}

function checkclose(){
	var frm = document.getElementById("close");
	frm.submit();
}

function empty(){
	var r = confirm("Are you sure you want to empty your cart?")
	if (r == true){
		var frm = document.getElementById("emptycart");
		frm.submit();
	}
	return false
}

function reloadPage()
{
	var frm = document.getElementById("foo");
	frm.submit();
}
</script>

<SCRIPT type="text/javascript">
    window.history.forward();
    function noBack() { window.history.forward(); }
</SCRIPT>

<script>
function submit_promo(){
	var frm = document.getElementById("addpromo");
	frm.submit();
}
function checkpromo(){
	return true ;
}
function showGo(v){
	 var n = v.length;
	if (n > 0){
		document.getElementById("HideGo").style.display="inline"
	}
	else{
		document.getElementById("HideGo").style.display="none"
	}
}
</script>

</head>
<body oncontextmenu="return false;" onload="noBack();loadwindow()" onpageshow="if (event.persisted) noBack();" onunload="" >
<!--
<form name="myform" id="myform" method="get" action="" onSubmit="return checkform();">
<input type="hidden" name="cartid" value="$cartid">
<input type="hidden" name="cartnum" value="$cartnum">
-->

<!--<img id="background" src="http://archeryacademy.com/wp-content/uploads/2012/09/background.jpg" alt="" class="bgwidth">-->

<div id="all-web">

WEB


&Get_Header($localdb,$master);



if ($cart_total > 0){
	print qq[
<div id="rm_header">
	<!--<center><h2>$shop</h2></center>-->
	<p class="add_header">
	<font color="white"><b><input type="button" name="post" id="post" value="Checkout" class="button" onclick="return checkclose();"></b>
	<font color="white"><b><input type="button" name="post" id="post" value="Empty Cart" class="button" onclick="return empty();"></b>
	</p>
  </div>
];
}
else{
	print qq[
	<div id="rm_header">
	<form id="addpromo" name="addpromo" action="rm_promo_directory.cgi" method="get">
	<input type="hidden" name="cartid" value="$cartid">
	<input type="hidden" name="cartnum" value="$cartnum">
	<p class="add_header">
	<b><font color="#ffffff" size="+1">Promo Code:&nbsp;</font></b><input type="text" id="promo" name="promo">
	<span id="HideGo" style="display:inline;">
	<input type="submit" id="go" name="go" class="button" value="Submit Promo" onclick="submit_promo()">
	</span>
	</p>
	</form>
</div>
];
}

print <<WEB ;

<div id="content">
<!--<span id="back"><a href="javascript:window.close();">Close</a></span>-->
<div id="title-left">
<h1>Lessons Offered</h1>
<h2>Your Cart: \$$cart_total</h2>
</div>

<div id="title-line_yc"></div>

WEB

foreach $key(@lessons){
	($position,$name, $id) = split(/\^/, $key) ;
	$record = $lesson{$key} ;
	($p1,$p2,$text,$itm1,$btn1,$itm2,$btn2,$itm3,$btn3,$itm4,$btn4,$itm5,$btn5,$itm6,$btn6,$itm7,$btn7,$itm8,$btn8) = split(/\^/, $record) ;
	$image = $images{$key};
	print qq[
		<div class="img_content">
		<img src=$image width="150" height="150" alt="">
		<p><strong>$name</strong><br>$text</p>
	] ;
	if ($itm1 > 0){print qq[<a class="button-shortcode  red" href="rm_web_leagues.cgi?league=$itm1&cartid=$cartid"><span> $btn1 </span></a><br>];}
	if ($itm2 > 0){print qq[<a class="button-shortcode  red" href="rm_web_leagues.cgi?league=$itm2&cartid=$cartid"><span> $btn2 </span></a><br>];}
	if ($itm3 > 0){print qq[<a class="button-shortcode  red" href="rm_web_leagues.cgi?league=$itm3&cartid=$cartid"><span> $btn3 </span></a><br>];}
	if ($itm4 > 0){print qq[<a class="button-shortcode  red" href="rm_web_leagues.cgi?league=$itm4&cartid=$cartid"><span> $btn4 </span></a><br>];}
	if ($itm5 > 0){print qq[<a class="button-shortcode  red" href="rm_web_leagues.cgi?league=$itm5&cartid=$cartid"><span> $btn5 </span></a><br>];}
	if ($itm6 > 0){print qq[<a class="button-shortcode  red" href="rm_web_leagues.cgi?league=$itm6&cartid=$cartid"><span> $btn6 </span></a><br>];}
	if ($itm7 > 0){print qq[<a class="button-shortcode  red" href="rm_web_leagues.cgi?league=$itm7&cartid=$cartid"><span> $btn7 </span></a><br>];}
	if ($itm8 > 0){print qq[<a class="button-shortcode  red" href="rm_web_leagues.cgi?league=$itm8&cartid=$cartid"><span> $btn8 </span></a><br>];}
	print qq[</div><br><br>];
}

print <<WEB ;
<!--</form>-->
<!--<span id="back"><a href="javascript:window.close();">Close</a></span>-->
</div>
</div>


<form id="emptycart" name="emptycart" action="rm_web_cart_empty.cgi" method="get">
<input type="hidden" name="cartid" value="$cartid">
<input type="hidden" name="cartnum" value="$cartnum">
</form>

<form id="close" name="close" action="rm_web_cart_review.cgi" method="get">
<input type="hidden" name="cartid" value="$cartid">
<input type="hidden" name="cartnum" value="$cartnum">
</form>

<form id="foo" name="foo" action="rm_web_league_home.cgi?cartid=$cartid" method="get">
</form>

</body>

</html>

WEB

exit ;
######################################################################
sub generateSession {
    # generate random 8 digit hex session ID
    return sprintf("%0.8x",rand()*0xffffffff);
}
##################################################################
sub CURRENCY {
	$x = shift ;
	($p1,$p2) = split(/\./,$x) ;
	my $places = length($p2) ;
	if ($places == 0){$p2 = "00"}
	if ($places == 1){$p2 = $p2."0"} ;
	if ($places >1){$p2 = substr($p2,0,2)}
	my $return = "$p1.".$p2 ;
	return $return ;
}
#######################################################################
