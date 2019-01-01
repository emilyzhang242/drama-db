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
   			search_navbar();
   		}
   	});

   	$("#navbar-search-btn").on("click", function(e) {
   		//if it's the enter key
   		if (e.which === 13) { 
   			search_navbar();
   		}
   	});
});

function search_navbar() {
	$.ajax({
		type: "POST",
		url: "/search/",
		data: {
			csrfmiddlewaretoken: csrf_token,
			search: $("#navbar-search-input").val()
		},
		error: function(response) {
			console.log(response);
		}
	});
}