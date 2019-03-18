var listBrand = ['sin()', 'cos()', 'tan()', 'arcsin()', 'arccos()', 'arctan()', 'sinh()', 'cosh()', 'tanh()', 'parse()',
    'LEXUS', 'AUDI', 'MAYBACK', 'FERRARI', 'TOYOTA', 'LEXUS', 'AUDI', 'MAYBACK', 'FERRARI', 'TOYOTA', 'LEXUS', 'AUDI',
    'MAYBACK', 'FERRARI', 'TOYOTA'
];
//the array
$(document).ready(function() {
    var list = [];
    var n = 0;
    var cursorpos = 0;
    var inputbox = $("#inputbox");
    inputbox.focus();
    var container = $("#container");
    var down = false;

    async function get_result(expression) {
        var result;
        var url = '/calc/' + expression;
        await $.get(url, function(data, status, xhr) {
            result = [data, xhr];
        });
        console.log(result);
        return result
    }
    inputbox.keydown(async function(e) {
        cursorpos = inputbox[0].selectionStart;
        if (e.which === 13 && inputbox.val().trim() !== "") {
            if (down) {
                return;
            }
            down = true;
            n = 0;
            var inputbox_content = inputbox.val();
            var response = await get_result(inputbox_content);
            var data = response[0];
            var header = response[1];
            container.append(highlight(inputbox_content));
            list.push(inputbox_content);
            if (header.getResponseHeader('Content-Type') === 'text/plain') {
                container.append("<br>");
                container.append(highlight("= " + data));
                container.append("<br>" + "<br>");
            } else if (header.getResponseHeader('Content-Type') === 'image/jpeg') {
                console.log("YES!");
                var img = new Image();
                img.src = "data:image/jpeg;base64," + data;
                container.append("<br>" + "<br>");
                container.append(img);
                container.append("<br>" + "<br>");
            }

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
                    inputbox.val(list[list.length - n]);
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
                    inputbox.val(list[list.length - n]);
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
        $('.hamburger').toggleClass('is-active');
        $("#container").stop().animate({
            scrollTop: $("#container")[0].scrollHeight
        }, 0);
        inputbox.focus();
    });

    for (var i = 0; i < listBrand.length; i++) {
        var btn = document.createElement("button");
        var t = document.createTextNode(listBrand[i]);
        btn.classList.add("buttonfunc");
        const paste_name = i;
        $(btn).click(function() {
            cursorpos = inputbox[0].selectionStart;
            insertAtCursor(inputbox[0], listBrand[paste_name], cursorpos);
            var new_cursorpos = listBrand[paste_name].length - 1;
            console.log(paste_name);
            inputbox[0].selectionStart = inputbox[0].selectionEnd = cursorpos + new_cursorpos;
            inputbox.focus();
        });
        btn.appendChild(t);
        $('#sidebar').append(btn);
    }

    inputbox.click(async function(e) {
        cursorpos = inputbox[0].selectionStart;
    });

    inputbox.keyup(async function(e) {
        cursorpos = inputbox[0].selectionStart;
    });

    function insertAtCursor(myField, myValue, cursorpos) {
        //MOZILLA and others
        if (myField.selectionStart || myField.selectionStart == '0') {
            myField.value = myField.value.substring(0, cursorpos) +
                myValue +
                myField.value.substring(cursorpos, myField.value.length);
        } else {
            myField.value += myValue;
        }
    }
    console.log("ready!");
});