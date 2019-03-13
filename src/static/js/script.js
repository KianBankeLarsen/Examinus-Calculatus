$(document).ready(function() {
    var list = [];
    var n = 0;
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
            n = 0;
            var inputbox_content = inputbox.val();
            var result = await get_result(inputbox_content);
            container.append(highlight(inputbox_content));
            list.push(inputbox_content);
            container.append("<br>");
            container.append(highlight("= " + result));
            container.append("<br>" + "<br>");
            inputbox.val("");
            $("#container").stop().animate({
                scrollTop: $("#container")[0].scrollHeight
            }, 1500);
        }
        if (e.which === 38) {
            if (down) {
                return;
            }
            if (0 <= n && n <= list.length) {
                if (n !== list.length) {
                    n += 1;
                    inputbox.val(list[list.length-n]);
                }
            }
            down = true;
        }

        if (e.which === 40) {
            if (down) {
                return;
            }
            if (list.length >= n && n > 0) {
                if (n !== 1) {
                    n -= 1;
                    inputbox.val(list[list.length-n]);
                } else {
                    inputbox.val("");
                    n = 0;
                }
            }
            down = true;
        }
    });
    inputbox.keyup(function(e) {
        down = false;
    });
    $('.hamburger').click(function() {
        $('#sidebar').toggleClass('extendedsidebar');
        $('.hamburger').toggleClass('is-active')
        $("#container").stop().animate({
                scrollTop: $("#container")[0].scrollHeight
            }, 0);
    });

    $('.buttonfunc').click(function() {
        alert('Wham!')
    });
    console.log("ready!");
});