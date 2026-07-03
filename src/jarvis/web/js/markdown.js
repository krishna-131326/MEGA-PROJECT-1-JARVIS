// markdown.js
// Handles markdown rendering using marked.js and highlight.js

class MarkdownRenderer {
    constructor() {
        if (typeof marked !== 'undefined') {
            marked.setOptions({
                breaks: true,
                gfm: true,
                highlight: function (code, lang) {
                    if (lang && hljs.getLanguage(lang)) {
                        try {
                            return hljs.highlight(code, { language: lang }).value;
                        } catch (__) {}
                    }
                    return hljs.highlightAuto(code).value;
                }
            });
        } else {
            console.warn("marked.js is not loaded.");
        }
    }

    render(text) {
        if (typeof marked !== 'undefined') {
            return marked.parse(text);
        }
        // Fallback if marked is missing
        return text.replace(/\n/g, '<br>');
    }
}

window.markdownRenderer = new MarkdownRenderer();
