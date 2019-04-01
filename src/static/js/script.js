var btnFunctions = ['sin()', 'cos()', 'tan()', 'arcsin()', 'arccos()', 'arctan()', 'sinh()', 'cosh()', 'tanh()', 'parse()',
    'e', 'AUDI', 'MAYBACK', 'FERRARI', 'TOYOTA', 'LEXUS', 'AUDI', 'MAYBACK', 'FERRARI', 'TOYOTA', 'LEXUS', 'AUDI',
    'MAYBACK', 'FERRARI'
];


$(document).ready(function() {
    // GLOBAL VARIABLES //
    var list = [];
    var keys = [49, 50, 51, 52, 53, 54, 55, 56, 57, 48, 171, 107, 173, 109];
    var changes_inputbox = [];
    var n = 0;
    var p = 0;
    var cursorpos = 0;
    var inputbox = $("#inputbox");
    inputbox.focus();
    var container = $("#container");
    var down = false;


    // GET_REQUEST //
    async function get_result(expression) {
        var result;
        var url = '/calc/' + expression;
        await $.get(url, function(data, status, xhr) {
            result = [data, xhr];
        });
        //console.log(result);
        return result
    }


    // CHECK IF ENTER IS PRESSED, CALL GET REQUEST, CLEAR INPUT, SCROLL DOWN //
    inputbox.keydown(async function(e) {
        cursorpos = inputbox[0].selectionStart;
        if (e.which === 13 && inputbox.val().trim() !== "") {
            if (down) {
                return;
            }
            down = true;
            n = 0;
            changes_inputbox = [];
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


        // GETTING LATEST SENT EXPRESSION | MOVING BACK IN LIST //
        if (e.which === 38) {
            moveBackInList(list)
        }


        // GETTING LATEST SENT EXPRESSION | MOVING FORWARD IN LIST //
        if (e.which === 40) {
            moveForwardInList(list)
        }


        // NEW SPECIFIC UNDO AND REDO FUNCTION //
        if (e.which === 89 && e.ctrlKey) {
            redo(changes_inputbox)

        } else if (e.which === 90 && e.ctrlKey) {
            undo(changes_inputbox)
        }

        // UPDATES CHANGES_INPUTBOX //
        /*if (keys.includes(e.which)) {
            changes_inputbox.push(inputbox.val());
        }*/
        //console.log(e.which);
    });

    inputbox.keyup(async function() {
        // SET KEY DOWN TO FALSE //
        down = false;

        // UPDATES NEW CURSOR PLACEMENT ON KEYUP //
        cursorpos = inputbox[0].selectionStart;
    });


    function undo(listName) {
        if (p === 0){
            p += 1;
        }
        if (0 <= p && p <= listName.length) {
            if (p !== listName.length) {
                p += 1;
                inputbox.val(listName[listName.length - p]);
            }
        }
        down = true;
    }


    function redo(listName) {
        if (listName.length >= p && p > 0) {
            if (p !== 1) {
                p -= 1;
                inputbox.val(listName[listName.length - p]);
            }
        }
        down = true;
    }


    function moveBackInList(listName) {
        if (down) {
            return;
        }
        if (0 <= n && n <= listName.length) {
            if (n !== listName.length) {
                n += 1;
                inputbox.val(listName[listName.length - n]);
            }
        }
        down = true;
    }


    function moveForwardInList(listName) {
        if (down) {
            return;
        }
        if (listName.length >= n && n > 0) {
            if (n !== 1) {
                n -= 1;
                inputbox.val(listName[listName.length - n]);
            } else {
                inputbox.val("");
                n = 0;
            }
        }
        down = true;
    }


    // HAMBURGER BUTTON CLASS ACTIVATION //
    $('.hamburger').click(function() {
        $('#sidebar').toggleClass('extendedsidebar');
        $('.hamburger').toggleClass('is-active');
        $("#container").stop().animate({
            scrollTop: $("#container")[0].scrollHeight
        }, 0);
        inputbox.focus();
    });


    // CREATING BUTTONS AND CORRESPONDING FUNCTION //
    for (var i = 0; i < btnFunctions.length; i++) {
        var btn = document.createElement("button");
        var t = document.createTextNode(btnFunctions[i]);
        btn.classList.add("buttonfunc");
        const paste_name = i;
        $(btn).click(function() {
            cursorpos = inputbox[0].selectionStart;
            changes_inputbox.push(inputbox.val());
            insertAtCursor(inputbox[0], btnFunctions[paste_name], cursorpos);
            changes_inputbox.push(inputbox.val());
            console.log(changes_inputbox);
        });
        btn.appendChild(t);
        $('#sidebar').append(btn);
    }


    // UPDATES NEW CURSOR PLACEMENT ON CLICK //
    inputbox.click(async function() {
        cursorpos = inputbox[0].selectionStart;
    });


    // INSERT AT CURSOR FUNCTION - BUTTON FUNCTIONALITY //
    function insertAtCursor(myField, myValue, cursorpos) {
        //MOZILLA and others
        var array = inputbox[0].selectionStart - inputbox[0].selectionEnd;

        if (array === 0 && myValue.slice(-1) === ')') {
            myField.value = myField.value.substring(0, cursorpos) +
                myValue +
                myField.value.substring(cursorpos, myField.value.length);
            inputbox[0].selectionStart = inputbox[0].selectionEnd = cursorpos + myValue.length - 1;
            inputbox.focus();

        } else if (array !== 0 && myValue.slice(-1) === ')') {
            myField.value = myField.value.substring(0, cursorpos) +
                myValue.slice(0, -1) +
                myField.value.substring(cursorpos, myField.value.length) + myValue.slice(-1);
            inputbox.focus();

        } else {
            myField.value = myField.value.substring(0, cursorpos) +
                myValue +
                myField.value.substring(cursorpos, myField.value.length);
            inputbox[0].selectionStart = inputbox[0].selectionEnd = cursorpos + myValue.length;
            inputbox.focus();
        }
    }


    // DISABLES HTE BROWSERS BUILT-IN UNDO AND REDO FUNCTIONALITY //
    $(window).bind('keydown', function(evt) {
        if ((evt.ctrlKey || evt.metaKey) && String.fromCharCode(evt.which).toLowerCase() == 'z') {
            evt.preventDefault();
        }
    });


    // READY TO START | LOGGING IN CONSOLE //
    console.log("ready!");
});