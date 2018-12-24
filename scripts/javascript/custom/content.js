$(document).ready(function() {
	//scrollbar 
	$(window).scroll(function() {
		var offset = $('a[href$="#actor-overview"]').offset().top;
		var scroll = $(window).scrollTop();
		$(".scrollable-point").each(function(f){
			var id = $(this).attr("id");
			if (scroll >= $("#"+id).offset().top) {
				// this changes which link shows blue
				$(".content-nav a").removeClass("active-link");
				$('a[href$="#'+id+'"]').addClass("active-link");
				// this changes where the blue dot is
				var y_index = $('a[href$="#'+id+'"]').offset().top;
				var dot_left = $("#scrollbar-dot").offset().left;
				$("#scrollbar-dot").offset({top: y_index, left: dot_left});
				// COMMENTED OUT ATTEMPT AT ANIMATION
				// var sign = "-";
				// if (offset >= y_index) {
				// 	sign = "+";
				// }
				// console.log(sign+"="+Math.abs(offset-y_index));
				// $("#scrollbar-dot").animate({top: sign+"="+Math.abs(offset-y_index), left: 0}, 2000);
				// offset = y_index;
			}
		});
	});
});