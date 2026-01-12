/** @jest-environment jsdom */
const { renderQuotes } = require('../main');

describe('renderQuotes enhanced', () => {
  test('renders tags and delete button', () => {
    document.body.innerHTML = '<ul id="quotes"></ul>';
    const ul = document.getElementById('quotes');
    const quotes = [
      { id: 1, text: 'Foo', author: 'Bar', tags: ['x','y'] },
      { id: 2, text: 'Baz', author: null }
    ];
    renderQuotes(quotes, ul);
    expect(ul.children.length).toBe(2);
    // first item has tags
    expect(ul.children[0].textContent).toMatch(/Foo/);
    expect(ul.children[0].textContent).toMatch(/\[x, y\]/);
    // delete button present
    expect(ul.children[0].querySelector('button').textContent).toBe('Delete');
  });
});
