$(document).ready(function() {
    var inputbox = $("#inputbox");
    inputbox.focus();
    var container = $("#container");
    var down = false;
    async function get_result(expression) {
        var result;
        var url = '/calc/' + expression;
        await $.get(url, function(data, status) {
            result = data;
        });
        return result
    }
    inputbox.keydown(async function(e) {
        if (e.which === 13 && inputbox.val().trim() !== "") {
            if (down) {
                return;
            }
            down = true;
            console.log("keydown");
            var inputbox_content = inputbox.val();
            var result = await get_result(inputbox_content);
            container.append(highlight(inputbox_content));
            container.append("<br>");
            container.append(highlight("= " + result));
            container.append("<br>" + "<br>");
            inputbox.val("");
            $("#container").stop().animate({
                scrollTop: $("#container")[0].scrollHeight
            }, 1500);
        }
    });
    inputbox.keyup(function(e) {
        down = false;
        console.log("keyup")
    });
    $('.hamburger').click(function() {
        $('#sidebar').toggleClass('extendedsidebar');
        $('.hamburger').toggleClass('is-active')
    });

    $('.buttonfunc').click(function() {
        alert('Wham!')
    });
    console.log("ready!");
});