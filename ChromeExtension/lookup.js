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

function charToValue(c)
{
    if (c == 'x' || c == 'X')
    {
        return 10;
    }
    return parseInt(c);
}

function isIsbn10(isbn)
{
    if ( isbn.length != 10) { return false; }

    var total = 0;
    for ( var i = 0; i < isbn.length; i++ )
    {
        var digit = charToValue(isbn[i]);
        total += digit * (i+1);
    }

    return total % 11 == 0;
}

function isIsbn13(isbn)
{
    if ( isbn.length != 13) { return false; }

    var weight = 1;
    var total = 0;
    for ( var i = 0; i < isbn.length; i++ )
    {
        var digit = charToValue(isbn[i]);
        total += digit * weight;
        weight = 4 - weight;
    }

    return total % 10 == 0;
}

function isIsbn(isbn)
{
    return isIsbn13(isbn) || isIsbn10(isbn);
}

function getBestIsbn(text)
{
    var isbnRegex = /\b(\d{9}[0-9xX]|\d{13})\b/g;

    var possibleMatches = text.match(isbnRegex);
    if ( possibleMatches )
    {
        possibleMatches = possibleMatches
            .sort(function(a,b) { return b.length - a.length; }) // prefer ISBN-13 to ISBN-10
            .filter(isIsbn);
        
        if ( possibleMatches )
        {
            return possibleMatches[0];
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
                var isbnLabel = $x("//td[@class='metadata_label']/span[text()='ISBN']")[0];
                if ( isbnLabel )
                {
                    var isbnValueNode = isbnLabel.parentNode.nextSibling;
                    return getBestIsbn(isbnValueNode.innerHTML);
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

                        return getBestIsbn(isbnNode.innerHTML);
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
                return getBestIsbn(location.href);
            },
        }
    ];

var handler = handlers.filter(function(element) { return element.isApplicable(); })[0];
var foundIsbn;
try
{
    foundIsbn = handler.getIsbn();
}
catch ( e )
{
    log.console('error looking for ISBN: ' + e);
}

if ( foundIsbn )
{
    console.log('requesting: foundIsbn = ' + foundIsbn);
    chrome.extension.sendMessage({msg: 'lookup', isbn: foundIsbn});
}

