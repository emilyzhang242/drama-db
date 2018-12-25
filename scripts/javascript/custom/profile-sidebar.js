$(document).ready(function(){
	//* Loop through all dropdown buttons to toggle between hiding and showing its dropdown content - This allows the user to have multiple dropdowns without any conflict */
	var dropdown = document.getElementsByClassName("dropdown-btn");
	var i;

	for (i = 0; i < dropdown.length; i++) {
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
	var page = $("#sidebar-input").data("page");
	$("#"+page).addClass("background-light-blue");
});