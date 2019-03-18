var output;

var lexer = new Lexer(function d() {
    return null;
});

lexer.addRule(/(\d+(\.\d*)?)/, function(lexeme) {
    output = output + "<span class='number'>" + lexeme + '</span>';
    output = output + " ";
}).addRule(/[a-zA-Z]+/, function(lexeme) {
    output = output + "<span class='function'>" + lexeme + "</span>";
    output = output + " ";
}).addRule(/[=\+\-\*^/!]/, function(lexeme) {
    output = output + "<span class='symbol'>" + lexeme + "</span>";
    output = output + " ";
}).addRule(/[\(\)]/, function(lexeme) {
    output = output + "<span class='paren'>" + lexeme + "</span>";
    output = output + " ";
}).addRule(/ /, function() {
    output = output;
});

function highlight(input) {
    output = "";
    lexer.setInput(input).lex();
    return output;
}