$(document).ready(function() {

	//highlight correct section
	var page = $("#navbar-choice").val();
	$(".navbar-highlight").removeClass("navbar-active");
	$("#navbar-"+page).siblings(".navbar-highlight").addClass("navbar-active");

   	//tooltip
   	$("i").tooltip({content:"test", tooltipClass: "tooltip-css"});

   	//searchbar functionality!
   	$("#navbar-search").on("keyup", function(e) {
   		//if it's the enter key
   		if (e.which === 13) { 
   			$("#navbar-search").submit();
   		}
   	});

   	$("#navbar-search-btn").on("click", function(e) {
   		$("#navbar-search").submit();
   	});
});