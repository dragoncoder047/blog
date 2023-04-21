Title: Pickle Tokenizer
Date: 2023-04-20
Modified: 2023-04-21

I'm starting to work on my Pickle programming language, this time in Javascript. After only a few days' work, I'm surprised I got so much working. Currently I have both the tokenizer and the inheritance system working. The syntax of Pickle is pretty much in place now, and I just have a few tweaks left for the tokenizer, and hooking it up to a parser, before I am able to write the evaluator.

## Tokenizer

In contrast to my previous attempt in C, I actually wrote a tokenizer. But in all honesty, the tokenizer really does 90% of the parsing -- it just doesn't recursively build up a tree of expressions using the parens (that will be done by the parser).

I got the tokenizer working in a little demo page I dubbed the "seeder" for some reason. Currently it is able to tokenize this code:

<pre id="picklecode">
defun fib(x):
    if $x == 0 or $x == 1:
        return 1
    else:
        return (fib $x - 1) + (fib $x - 2)
print (fib 10)
</pre>

into this stream of tokens:

<pre id="outputtokens">
</pre>

[EDIT Apr. 21: The above is now a live editor using the tokenizer as it was when I wrote this post -- write away and the tokens will update automatically. The tokenization may have changed since then.]

The tokenizer is also a bit unique in that it can recover from a syntax error and keep scanning, allowing you to see and fix multiple syntax errors all at once. And it's also nice that the [Ace.js](https://ace.c9.io) code editor allows you to place annotation markers in the gutter, which is what I did in the "seeder".

The only bug I can see here with this example is that the colon-block string part consumes the newline at the end of the block, so the `print` is considered to be on the same logical line, but it shouldn't be. A simple `;` before the `print` would fix that, but I feel that this kind of indented block structure where an unindent ends both the block and the line, would be more common than having the string continue the line -- in other words, having the default be to continue it and adding punctuation to end it would result in more "punctuation overload" versus having a special punctuation character mean continue the line and the default be to end it. Unfortunately, the former appears to be whet is implemented in the Javascript tokenizer.

## Inheritance

In [my earlier post about Pickle]({filename}../c/pickles.md), I mentioned that Pickle would have a multiprototype-based inheritance system, a strange mix of Python and Javascript. Python supports multiple inheritance, but chokes on "ambiguous" inheritance trees, while Javascript only supports single inheritance through prototypes. But I think I've found a simple solution that implements multiprototype-based inheritance. Here's a pared-down example:

```js
class PickleObject {
    constructor(name, ...prototypes) {
        this.name = name;
        this.prototypes = prototypes;
    }
    toJSON() {
        return this.name;
    }
    getMRO() {
        var fun = x => [x].concat(x.prototypes.map(fun));
        return fun(this).flat(Infinity);
    }
}

var A = new PickleObject("A");
var B = new PickleObject("B");
var X = new PickleObject("X", A, B);
var Y = new PickleObject("Y", B, A);
var Crash = new PickleObject("Crash", X, Y);
alert(JSON.stringify(Crash.getMRO()));
// -> ["Crash","X","A","B","Y","B","A"]
```

This is exactly the same code that I posted earlier that Python can't handle -- but here, `:::js Crash.getMRO()` simply returns a flat array that can be searched linearly. I'm not sure how fast this is, but I do have some optimization tricks that I could apply.

## What's next?

I don't know exactly what, but Pickle is still only half-written. After I write the parser, I'll need to then write the evaluator. And the evaluator is going to be extremely complicated and probably very slow, although I do hope it will be somewhat readable due to Javascript's built-in functional programming constructs that C doesn't have natively.

Pickle does look like it's going to be simpler than Phoo, certainly. Although Phoo did get complicated because I split everything into a zillion different files. One huge file for everything may be a bit much, but having a bazillion files and none have any more than 100 lines apiece is also a bit much. Aside from the weird operator semantics, I do hope Pickle's flow will be easier to follow.

<script src="https://cdn.jsdelivr.net/npm/ace-builds@1.10.0/src-noconflict/ace.min.js"></script>
<script>
function pickleUnescapeChar(c) {
    switch (c) {
        case 'b': return '\b';
        case 't': return '\t';
        case 'n': return '\n';
        case 'v': return '\v';
        case 'f': return '\f';
        case 'r': return '\r';
        case 'a': return '\a';
        case 'o': return '{';
        case 'c': return '}';
        case '\n': return '';
        default: return c;
    }
}
class PickleToken {
    constructor(type, content, start, end, filename = "", message = "") {
        var types = type.split(".");
        this.type = types[0];
        this.subtypes = types.slice(1);
        this.content = content;
        this.start = start;
        this.end = end;
        this.filename = filename;
        this.message = message;
    }
    toJSON() {
        return {
            type: this.type,
            subtypes: this.subtypes,
            content: this.content,
            start: this.start,
            end: this.end,
            filename: this.filename,
            message: this.message
        };
    }
}
class PickleTokenizer {
    constructor(string, filename) {
        this.string = string;
        this.i = 0;
        this.beginning = null;
        this.bi = 0;
        this.filename = filename;
    }
    lineColumn() {
        var before = this.string.slice(0, this.i);
        var doneLines = before.split("\n");
        var line = doneLines.length;
        var col = doneLines.at(-1).length + 1;
        return { line, col };
    }
    test(what) {
        if (typeof what === "string") return this.string.slice(this.i).startsWith(what);
        else if (what instanceof RegExp) return what.test(this.string.slice(this.i));
        else return false;
    }
    chomp(what) {
        if (!this.test(what)) return undefined;
        if (typeof what === "string") {
            this.i += what.length;
            return what;
        }
        else if (what instanceof RegExp) {
            var match = what.exec(this.string.slice(this.i));
            this.i += match[0].length;
            return match;
        }
        else return undefined;
    }
    done() {
        return this.i >= this.string.length;
    }
    peek(i = 0) {
        var j = this.i + i;
        if (j >= this.string.length) return undefined;
        return this.string[j];
    }
    errorToken(message = "") {
        if (this.bi == this.i) this.i++;
        return this.makeToken("error", this.string.slice(this.bi, this.i), message || `unexpected ${this.peek(-1)}`);
    }
    makeToken(type, content, message = "") {
        return new PickleToken(type, content, this.beginning, this.lineColumn(), this.filename, message);
    }
    nextToken() {
        if (this.done()) return undefined;
        this.beginning = this.lineColumn();
        this.bi = this.i;
        if (this.test(/^:\s*\n/)) {
            var i = this.i;
            var lines = [];
            this.chomp(/^:\s*\n/);
            var indent = this.chomp(/^\s+/);
            if (!indent) {
                this.i = i;
                return this.makeToken("error", this.chomp(/^:\s*\n/)[0], "expected indent after colon");
            }
            indent = indent[0];
            var ensure_same = /^([\t ])\1*/.exec(indent);
            if (!ensure_same) return this.makeToken("error", indent, "mix of tabs and spaces indenting block");
            while (true) {
                var line = this.chomp(/^[^\n]*/);
                lines.push(line[0] || "");
                if (!this.chomp("\n")) break;
                if (!this.chomp(indent)) {
                    var b = this.lineColumn();
                    var bi = this.i;
                    var badIndent = this.chomp(/^(((?!\n)\s)*)(?=\S)/);
                    if (badIndent) {
                        if (badIndent[1].length > 0) {
                            this.beginning = b;
                            this.bi = bi;
                            return this.makeToken("error", badIndent[1], "unexpected unindent");
                        }
                        else break;
                    }
                }
            }
            return this.makeToken("string.block", lines.join("\n"));
        }
        const TOKEN_REGEXES = [
            { type: "comment.line", re: /^#[^\n]*/, significant: false },
            { type: "comment.block", re: /^###[\s\S]*###/, significant: false },
            { type: "paren", re: /^[\(\)\[\]]/, significant: true, groupNum: 0 },
            { type: "space", re: /^(?!\n)\s+/, significant: false },
            { type: "eol", re: /^[;\n]/, significant: true, groupNum: 0 },
            { type: "singleton", re: /^(true|false|nil)/, significant: true, groupNum: 0 },
            { type: "number.complex", re: /^-?[0-9]+(\.[0-9]+)?e[+-]\d+[+-][0-9]+(\.[0-9]+)?e[+-]\d+j/, significant: true, groupNum: 0 },
            { type: "number.rational", re: /^-?[0-9]+\/[0-9]+/, significant: true, groupNum: 0 },
            { type: "number.integer", re: /^-?([1-9][0-9]*|0x[0-9a-f]+|0b[01]+)/i, significant: true, groupNum: 0 },
            { type: "number.float", re: /^-?[0-9]+(\.[0-9]+)?(e[+-]\d+)?/i, significant: true, groupNum: 0 },
            { type: "symbol", re: /^[a-z_][a-z0-9_]*\??/i, significant: true, groupNum: 0 },
            { type: "symbol.operator", re: /^[-~`!@$%^&*_+=[\]|\\:<>,.?/]+/, significant: true, groupNum: 0 },
        ]
        for (var { type, re, significant, groupNum } of TOKEN_REGEXES) {
            if (this.test(re)) {
                var match = this.chomp(re);
                if (significant) return this.makeToken(type, match[groupNum]);
                else return this.nextToken();
            }
        }
        // Try strings
        if (this.test("{")) {
            var j = 0, depth = 0, string = "";
            do {
                var ch = this.peek(j);
                if (ch == undefined) return this.errorToken("unclosed {");
                if (ch == "{") depth++;
                else if (ch == "}") depth--;
                string += ch;
                j++;
            } while (depth > 0);
            this.i += j;
            return this.makeToken("string.curly", string.slice(1, -1));
        }
        else if (this.test(/^['"]/)) {
            var q = this.chomp(/^['"]/)[0];
            var j = 0, string = "";
            while (true) {
                var ch = this.peek(j);
                // newlines must be backslash escaped
                if (ch == undefined || ch == "\n") {
                    this.i += j;
                    return this.errorToken("unterminated string");
                }
                else if (ch == "\\") {
                    ch = pickleUnescapeChar(this.peek(j + 1));
                    j++;
                }
                else if (ch == q) break;
                string += ch;
                j++;
            }
            this.i += j + 1;
            return this.makeToken("string.quote", string);
        }
        return this.errorToken();
    }
}
const SEL = s => document.querySelector(s);
ace.config.set('basePath', 'https://cdn.jsdelivr.net/npm/ace-builds@1.10.0/src-noconflict/');
var editor = ace.edit("picklecode");
function output(x) {
    SEL("#outputtokens").innerHTML += x;
}
function clearOutput() {
    SEL("#outputtokens").innerHTML = "";
}
function foobar() {
    var tokenizer = new PickleTokenizer(editor.getValue());
    var annotations = [];
    clearOutput();
    try {
        while (!tokenizer.done()) {
            var oldi = tokenizer.i;
            var tok = tokenizer.nextToken();
            if (tok) {
                if (tok.type == "error") {
                    gotErrors = true;
                    annotations.push({
                        row: tok.start.line - 1,
                        column: tok.start.col,
                        text: tok.message + (tok.content ? `: ${tok.content}` : ""),
                        type: "error",
                    });
                }
                output(`[${tok.start.line}:${tok.start.col} - ${tok.end.line}:${tok.end.col}]\t${tok.type} ${tok.subtypes.length > 0 ? "(" + tok.subtypes.join(",") + ")" : ""}\t${JSON.stringify(tok.content)}\t${tok.message}\n`);
            }
            if (tokenizer.i == oldi) throw new Error("Tokenizer error");
        }
    } catch (e) {
        output(`<span style="color:red">${e}\n${e.stack}</span>`)
        console.error(e);
    }
    editor.getSession().setAnnotations(annotations);
}
editor.getSession().on('change', foobar);
foobar();
// Dark/light theme
const dmmq = window.matchMedia('(prefers-color-scheme: dark)');
function darkLight() {
    if (dmmq.matches) editor.setTheme("ace/theme/terminal");
    else editor.setTheme("ace/theme/chrome");
}
darkLight();
dmmq.addEventListener("change", darkLight);
</script>
