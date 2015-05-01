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

    try
    {
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
    catch ( e )
    {
        console.log("LibaryLookup: error while finding best ISBN. Assuming this isn't a book page.\nError was:\n" + e);
        return null;
    }
}

// Figure out which site the source page comes from.
// To add a new one, make a new block like the "chapters"
// and "amazon" variables below, and extend the "if...else..."
// block at the bottom of this function.
function whichSiteIsThis()
{
   var chapters =
      {
         getIsbn: function()
         {
             return get_best_isbn(location.href);
         },

         getOriginalTitle: function()
         {
            return $x("//h1")[0];
         }
      }

   var allconsuming =
      {
         getIsbn: function()
         {
             var isbnLinkNode = $x("//div[@class='item-header-body']/a[@class='amazon-link']/@href")[0];
             if ( isbnLinkNode )
             {
                 return get_best_isbn(isbnLinkNode.firstChild.nodeValue);
             }
             return null;
         },

         getOriginalTitle: function()
         {
            return $x("//div[@class='item-header-body']/strong")[0];
         }
      }

   var amazon =
     {
         getIsbn: function()
         {
             return get_best_isbn(location.href);
         },

         getOriginalTitle: function()
         {
            return $x("//div[@class='buying']/b[@class='sans']|//div[@class='buying']/b[@class='asinTitle']|//div[@class='buying']//span[@id='btAsinTitle']")[0];
         }
      }

   var librarything =
      {
         getIsbn: function()
         {
             return document.body.innerHTML.match(/ISBN:([0-9X]+)/i)[1];
         },

         getOriginalTitle: function()
         {
            return $x("//div[@id='usercover']")[0];
         }
      }

   var powells =
      {
         getIsbn: function()
         {
             return get_best_isbn(location.href);
         },

         getOriginalTitle: function()
         {
            return $x("//div[@id='seemore']")[0];
         }
      }

   var googleBooks =
      {
         getIsbn: function()
         {
             return get_best_isbn(location.href);
         },

         getOriginalTitle: function()
         {
            return $x("//span[@class='title']")[0];
         }
      }

   var goodReads =
      {
         getIsbn: function()
         {
            try
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
            }
            catch ( e )
            {
               log.console('error looking for ISBN: ' + e);
            }
            return null;
         },

         getOriginalTitle: function()
         {
            return $x("//h1[@id='bookPageTitle']")[0];
         }
      }

   // figure out what site we're looking at
   if ( location.href.match(/chapters/) )
   {
      return chapters;
   }
   else if ( location.href.match(/allconsuming/) )
   {
      return allconsuming;
   }
   else if ( location.href.match(/powells/) )
   {
      return powells;
   }
   else if ( location.href.match(/google/) )
   {
      return googleBooks;
   }
   else if ( location.href.match(/goodreads/) )
   {
      return goodReads;
   }
   else if ( location.href.match(/librarything/) )
   {
      return librarything;
   }
   else
   {
      // Amazon's pretty popular - make it the default
      return amazon;
   }
}

var knownPage = whichSiteIsThis();
if ( knownPage )
{
   var found_isbn = knownPage.getIsbn();
   if ( found_isbn )
   {
      console.log('requesting: found_isbn = ' + found_isbn);
      chrome.extension.sendMessage({msg: 'lookup', isbn: found_isbn});
   }
}
