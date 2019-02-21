alert("Welcome to the website Markus Solecki Ellyton, hope you enjoy!!")


// A $( document ).ready() block.
$(document).ready(function () {
	var inputbox = $("#inputbox")
	var container = $("#container")
	var down = false
	inputbox.keydown(function (e) {
		if (e.which === 13 && inputbox.val().trim() !== "") {
			if (down) {
				return;
			}
			down = true
			console.log("keydown")
			var inputbox_content = inputbox.val()
			container.append(inputbox_content)
			container.append("<br>")
            inputbox.val("")
            $("#container").animate({scrollTop:$("#container")[0].scrollHeight}, 1000);
		}
	})
	inputbox.keyup(function (e) {
		down = false
		console.log("keyup")
	})
	console.log("ready!");
});