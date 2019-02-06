$(document).ready(function() {
	$("#show-ordering").change(function() {

		location.href = "?sort="+$("#show-ordering option:checked").val();

		// $.ajax({
		// 	type: "POST",
		// 	data: {
		// 		csrfmiddlewaretoken: '{{csrf_token}}',
		// 	},
		// 	url: "/shows?filter="+$("#show-ordering option:checked").val(),
		// 	success: function(result) {
		// 		console.log("YYYYEEHHHH");
		// 	},
		// 	error: function(result) {
		// 		console.log(result);
		// 	}
		// });
	});
});