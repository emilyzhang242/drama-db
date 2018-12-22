$(document).ready(function() {
	//navbar 
   	var page = $("#navbar-choice").val();
   	$("#navbar-"+page).siblings(".navbar-highlight").addClass("navbar-active");

});