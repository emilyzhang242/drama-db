$(document).ready(function(){
	//* Loop through all dropdown buttons to toggle between hiding and showing its dropdown content - This allows the user to have multiple dropdowns without any conflict */
	var dropdown = document.getElementsByClassName("dropdown-btn");

	for (var i = 0; i < dropdown.length; i++) {
		dropdown[i].addEventListener("click", function() {
			this.classList.toggle("active");
			var dropdownContent = this.nextElementSibling;
			if (dropdownContent.style.display === "block") {
				dropdownContent.style.display = "none";
			} else {
				dropdownContent.style.display = "block";
			}
			// add the boxshadow if active 
			$(".sidebar-main").removeClass("sidenav-boxshadow");
			$(".sidebar-main.active").addClass("sidenav-boxshadow");
		});
	}

	//Figure out which part in sidebar to highlight
	var page = $(".sidenav").data("page");
	console.log(page);
	$("#"+page).addClass("background-light-blue");

	//add lists functionality! 
	$("#add-list-link").on("click", function(e) {
		if (!$(this).hasClass("writing")) {
			var html = '<div class="input-group input-group-sm ml-4 mr-0" id="list-input-div">';
			html += '<input id="add-list-input" type="text" class="form-control" aria-label="Small" aria-describedby="inputGroup-sizing-sm">';
			html += '</div>';
			$("#add-list-span").html(html);
			$(this).addClass("writing");
		}
	});

	$(document).on("keyup", "#add-list-input", function(e) {
		if (e.which === 13) { //if it's the enter key
			$.ajax({
				type: "POST",
				url: "/profile/lists/add/",
				data: {
					csrfmiddlewaretoken: csrf_token,
					title: $("#add-list-input").val()
				},
				success: function(response) {
					$("#add-list-span").html(response.message);
				},
				error: function(response) {
					console.log(response);
				}
			});
		}
	});
});