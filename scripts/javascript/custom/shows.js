$(document).ready(function() {
	var year = new Date().getFullYear();
	for (var i = 0; i < 5; i++) {
		//$("#show-year-"+i).html(year);
		year = year - 1;
	}
});