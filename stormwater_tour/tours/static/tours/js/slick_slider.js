//Javascript code to get the slider up

$('.gallery').slick({
	dots: true,
	autoplay: false,
	speed: 300,
	slidesToShow: 1,
	centerMode: true,
	//adaptiveHeight: true,
	adaptiveWidth: true,
	onInit: function onInit() {
		console.log('slick initialised');
	}
});

