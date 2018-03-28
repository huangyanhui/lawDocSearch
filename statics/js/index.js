/**
 * Created by hyh on 2017/7/16.
 */
'use strict';

var origin = 'https://en.wikipedia.org';
var api = '/w/api.php';

var fetchSearchResults = function fetchSearchResults(searchText) {
    return new Promise(function (resolve, reject) {
        return $.getJSON(origin + api + '?callback=?', {
            action: 'query',
            format: 'json',
            list: 'search',
            generator: 'search',
            srsearch: searchText,
            gsrsearch: searchText
        }).done(resolve).fail(function (_, __, err) {
            return reject(err);
        });
    });
};

var formatSearchResults = function formatSearchResults(_ref) {
    var query = _ref.query;
    return Object.keys(query.pages).map(function (pageId) {
        var href = origin + '?curid=' + pageId;
        var search = query.search;
        var pages = query.pages;
        var _pages$pageId = pages[pageId];
        var title = _pages$pageId.title;
        var index = _pages$pageId.index;
        var snippet = search[index - 1].snippet;

        return { href: href, title: title, snippet: snippet };
    });
};

var createListItems = function createListItems(results) {
    return results.map(function (_ref2) {
        var href = _ref2.href;
        var title = _ref2.title;
        var snippet = _ref2.snippet;
        return '<li>\n         <a href="' + href + '" target="_blank">\n           <h4>' + title + '</h4>\n         </a>\n         <p>' + snippet + ' <a href="' + href + '" target="_blank">...read more</a></p>\n       </li>';
    }).join('<hr>');
};

var searchWikipedia = function searchWikipedia($input, $results) {
    return function (e) {
        e.preventDefault();
        var searchText = $input.select().val().trim();
        if (!searchText) return $input.val('');
        $results.html('<span class="spinner glyphicon glyphicon-refresh"></span>');
        fetchSearchResults(searchText).then(formatSearchResults).then(createListItems).then($results.html.bind($results)).catch(function (err) {
            return $results.html('Sorry, there was an error and it\'s my fault :(');
        });
    };
};

// main

$().ready(function (_) {
    var $input = $('#text').focus();
    var $results = $('#results');
    var handleSubmit = searchWikipedia($input, $results);
    $('#search').submit(handleSubmit);
});