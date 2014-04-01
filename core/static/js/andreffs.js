/*** 
André Silva 1st April 2014  
***/


$(document).ready(function(){

	// Zoom efect on logo and text
	$("#logo").hover(function(){
		$(this).stop().animate({ marginTop : "+=5px" }, 100).find("span").stop().animate({ fontSize : "30px" }, 100);
	}, function(){
		$(this).stop().animate({ marginTop : "-=5px" }, 100).find("span").stop().animate({ fontSize : "28px" }, 100);
	});

	// Opacity effect on navigation bar
	$('.h-link').hover(function(){
		//ANIMATIONS FOR THE THUMBS
		$('.h-link').not(this).animate({opacity:.5, boxShadow: "0px 0px 7px #000"},{queue:false,duration:100});
		//$(this).css("cursor","crosshair");
		}, function(){
		//(this).children('.portSecRollOver').css("display","none");
		$('.h-link').not(this).animate({opacity:1, boxShadow: "0px 0px 0px #000"},{queue:false,duration:100});
	});
	

});

	// // Hide opacity and arrow
	// $(".work-wrapper div").hide();

	// $('div.work-wrapper').hover(function() {
	// 	$("div.work-wrapper").not($(this)).find("div.work-wrapper-opacity").toggle();
	// 	$(this).toggleClass("work-wrapper-hover").find("div.arrow").toggle();
	// });
