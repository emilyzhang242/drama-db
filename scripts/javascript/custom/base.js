$(document).ready(function() {

	var page = $("#navbar-choice").val();
	$(".navbar-highlight").removeClass("navbar-active");
   	$("#navbar-"+page).siblings(".navbar-highlight").addClass("navbar-active");

   	//tooltip
   	$("i").tooltip({content:"test", tooltipClass: "tooltip-css"});

});