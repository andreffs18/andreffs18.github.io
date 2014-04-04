/*** 
André Silva 1st April 2014  
***/


//Welcome fade in of background
$(window).load(function(){
$('img.bgfade').hide();
	var dg_H = $(window).height();
	var dg_W = $(window).width();

	$('#wrap').css( {'height':dg_H,'width':dg_W} );
	
	function anim() {
		$("#wrap img.bgfade").first().appendTo('#wrap').fadeOut(1000);
		$("#wrap img").first().fadeIn(1000);
		setTimeout(anim, 5000);
	}

	anim();
});

$(window).resize(function(){
	window.location.href=window.location.href
});

$(document).ready(function(){

	setTimeout(function(){
		// Face slide down
		$("#face").animate({top : "+=270px"}, 750);
		// Title fade in
		$("#description h1").animate({opacity : 1, marginTop : "-=25px"}, 350);
		// Subtitle fade in
		$("#description h4").animate({opacity : 1, marginTop : "-=25px"}, 550);
		// Explore link slide up fade in
		$("#explore").animate({opacity : 1, marginTop : "-=25px"}, 900);
	}, 500);

});