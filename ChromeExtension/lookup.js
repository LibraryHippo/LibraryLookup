function $x(path, context)
{
    if ( !context )
    {
        context = document;
    }
    var result = [];
    var xpr = document.evaluate(path, context, null,
                                XPathResult.UNORDERED_NODE_SNAPSHOT_TYPE, null);
    for (var i = 0; item = xpr.snapshotItem(i); i++)
    {
        result.push(item);
    }
    return result;
};

function char_to_value(c)
{
    if (c == 'x' || c == 'X')
    {
        return 10;
    }
    return parseInt(c);
}

function is_isbn10(isbn)
{
    if ( isbn.length != 10) { return false; }

    var total = 0;
    for ( var i = 0; i < isbn.length; i++ )
    {
        var digit = char_to_value(isbn[i]);
        total += digit * (i+1);
    }

    return total % 11 == 0;
}

function is_isbn13(isbn)
{
    if ( isbn.length != 13) { return false; }

    var weight = 1;
    var total = 0;
    for ( var i = 0; i < isbn.length; i++ )
    {
        var digit = char_to_value(isbn[i]);
        total += digit * weight;
        weight = 4 - weight;
    }

    return total % 10 == 0;
}

function is_isbn(isbn)
{
    return is_isbn13(isbn) || is_isbn10(isbn);
}

function get_best_isbn(text)
{
    var isbnRegex = /\b(\d{9}[0-9xX]|\d{13})\b/g;

    var possible_matches = text.match(isbnRegex);
    if ( possible_matches )
    {
        possible_matches = possible_matches
            .sort(function(a,b) { return b.length - a.length; }) // prefer ISBN-13 to ISBN-10
            .filter(is_isbn);
        
        if ( possible_matches )
        {
            return possible_matches[0];
        }
    }
    
    return null;
}

var handlers = 
    [
        {
            isApplicable: function()
            {
                return location.href.match(/librarything/);
            },
            
            getIsbn: function()
            {
                return document.body.innerHTML.match(/ISBN:([0-9X]+)/i)[1];
            },
        },
        {
            isApplicable: function()
            {
                return location.href.match(/google/);
            },
            
            getIsbn: function()
            {
                var isbn_label = $x("//td[@class='metadata_label']/span[text()='ISBN']")[0];
                if ( isbn_label )
                {
                    var isbn_value_node = isbn_label.parentNode.nextSibling;
                    return get_best_isbn(isbn_value_node.innerHTML);
                }
                return null;
            },
        },
        {
            isApplicable: function()
            {
                return location.href.match(/goodreads/);
            },
            
            getIsbn: function()
            {
                var isbnHeaderNodeCandidates = $x("//div[@class='infoBoxRowTitle']");

                for ( var i = 0; i < isbnHeaderNodeCandidates.length; i++ )
                {
                    if ( isbnHeaderNodeCandidates[i].innerHTML.match(/isbn/i) )
                    {
                        var isbnNode = isbnHeaderNodeCandidates[i].nextSibling;
                        while ( isbnNode.nodeName != 'DIV' )
                        {
                            isbnNode = isbnNode.nextSibling;
                        }

                        return get_best_isbn(isbnNode.innerHTML);
                    }
                }
                return null;
            },
        },
        {
            // A sentinel. If we don't recognize the current site, see
            // if it has an ISBN in the URL, which is pretty popular.
            // As I write this, Amazon, Chapters, Barnes & Nobel,
            // Powells, and others use this scheme.
            isApplicable: function()
            {
                return true;
            },
            
            getIsbn: function()
            {
                return get_best_isbn(location.href);
            },
        }
    ];

var handler = handlers.filter(function(element) { return element.isApplicable(); })[0];
var found_isbn;
try
{
    found_isbn = handler.getIsbn();
}
catch ( e )
{
    log.console('error looking for ISBN: ' + e);
}

if ( found_isbn )
{
    console.log('requesting: found_isbn = ' + found_isbn);
    chrome.extension.sendMessage({msg: 'lookup', isbn: found_isbn});
}

