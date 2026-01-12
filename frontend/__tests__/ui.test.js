/** @jest-environment jsdom */
const { renderQuotes } = require('../main');

describe('renderQuotes', () => {
  test('renders list items', () => {
    document.body.innerHTML = '<ul id="quotes"></ul>';
    const ul = document.getElementById('quotes');
    const quotes = [
      { id: 1, text: 'Foo', author: 'Bar', tags: ['x'] },
      { id: 2, text: 'Baz', author: null }
    ];
    renderQuotes(quotes, ul);
    expect(ul.children.length).toBe(2);
    expect(ul.children[0].textContent).toMatch(/Foo/);
    expect(ul.children[1].textContent).toMatch(/Baz/);
  });
});