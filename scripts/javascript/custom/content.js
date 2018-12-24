$(document).ready(function() {
	//scrollbar 
	$(window).scroll(function() {
		var scroll = $(window).scrollTop();
		$(".scrollable-point").each(function(f){
			var id = $(this).attr("id");
			if (scroll >= $("#"+id).offset().top) {
				$(".content-nav a").removeClass("active-link");
				$('a[href$="#'+id+'"]').addClass("active-link");
			}
		});
	});
});