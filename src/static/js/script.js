// A $( document ).ready() block.
$(document).ready(function() {
    var inputbox = $("#inputbox")
    inputbox.focus()
    var container = $("#container")
    var down = false
    inputbox.keydown(function(e) {
        if (e.which === 13 && inputbox.val().trim() !== "") {
            if (down) {
                return;
            }
            down = true
            console.log("keydown")
            var inputbox_content = inputbox.val()
            container.append(inputbox_content)
            container.append("<br>")
            container.append("= " + math.eval(inputbox_content))
            container.append("<br>" + "<br>")
            inputbox.val("")
            $("#container").stop().animate({
                scrollTop: $("#container")[0].scrollHeight
            }, 1500);
        }
    })
    inputbox.keyup(function(e) {
        down = false
        console.log("keyup")
    })
    console.log("ready!");

    $('.hamburger').click(function() {
        $('#sidebar').toggleClass('extendedsidebar')
        $('.hamburger').toggleClass('is-active')
    })
});