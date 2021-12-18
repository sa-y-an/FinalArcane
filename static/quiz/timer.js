// Set the date we're counting down to
var countDownDate = new Date("Oct 23, 2021 19:00:00").getTime();
// Update the count down every 1 second
var x = setInterval(function () {
	// Get today's date and time
	var now = new Date().getTime();

	// Find the distance between now and the count down date
	var distance = countDownDate - now;

	// Time calculations for days, hours, minutes and seconds
	var days = Math.floor(distance / (1000 * 60 * 60 * 24));
	var hours = Math.floor(
		(distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)
		);
	var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
	var seconds = Math.floor((distance % (1000 * 60)) / 1000);

	$("#days").html(days + "<span>: </span>");
    $("#hours").html(hours + "<span>: </span>");
	$("#mins").html(minutes + "<span>: </span>");
	$("#seconds").html(seconds);

	// If the count down is over, go back to home
	if (distance < 0) {
		clearInterval(x);
		document.getElementById("endinfo").innerHTML =
			"<p style='font-size: 0.4em'><a href='{% url 'home:home' %}'>Go back to home</a></p>";
		document.getElementById("countdownblock").innerHTML = "";
		$("#countdownblock").addClass("timeexp");
		$("#endinfo").css("display", "block");
	}
});