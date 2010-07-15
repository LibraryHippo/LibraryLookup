// // Figure out which site the source page comes from.
// // To add a new one, make a new block like the "chapters"
// // and "amazon" variables below, and extend the "if...else..."
// // block at the bottom of this function.
// function whichSiteIsThis()
// {
//    var chapters =
//       {
//          getIsbn: function()
//          {
//             try
//             {
//                return location.href.match(isbnREdelimited)[1];
//             }
//             catch ( e ) 
//             {
//                return null;
//             }
//          },

//          getOriginalTitle: function()
//          {
//             return $x("//h1")[0];
//          }
//       }

//    var allconsuming =
//       {
//          getIsbn: function()
//          {
//             var isbn = null;
//             isbnLinkNode = $x("//div[@class='item-header-body']/a[@class='amazon-link']/@href")[0];
//             if ( isbnLinkNode )
//             {
//                isbn = isbnLinkNode.firstChild.nodeValue.match(isbnREdelimited)[1];
//             }
//             return isbn;
//          },

//          getOriginalTitle: function()
//          {
//             return $x("//div[@class='item-header-body']/strong")[0];
//          }
//       }

//    var amazon =
//       {
//          getIsbn: function()
//          {
//             try
//             {
//                return location.href.match(isbnREdelimited)[1];
//             }
//             catch ( e ) 
//             {
//                return null;
//             }
//          },

//          getOriginalTitle: function()
//          {
//             return $x("//div[@class='buying']/b[@class='sans']|//div[@class='buying']/b[@class='asinTitle']|//div[@class='buying']//span[@id='btAsinTitle']")[0];
//          }
//       }

//    var librarything =
//       {
//          getIsbn: function()
//          {
//             var isbn = null;
//             isbnLinkNode = $x("//div[@class='isbn']/a")[0];
//             if ( isbnLinkNode )
//             {
//                isbn = isbnLinkNode.firstChild.nodeValue.substr(5);
//             }
//             return isbn;
//          },

//          getOriginalTitle: function()
//          {
//             return $x("//div[@id='usercover']")[0];
//          }
//       }

//    var powells =
//       {
//          getIsbn: function()
//          {
//             try
//             {
//                return location.href.match(isbnREdelimited)[1];
//             }
//             catch ( e ) 
//             {
//                return null;
//             }
//          },

//          getOriginalTitle: function()
//          {
//             return $x("//div[@id='seemore']")[0];
//          }
//       }

//    var googleBooks =
//       {
//          getIsbn: function()
//          {
//             try
//             {
//                return location.href.match(/(\d{9,12}[\dXx])/)[1];
//             }
//             catch ( e ) 
//             {
//                return null;
//             }
//          },

//          getOriginalTitle: function()
//          {
//             return $x("//span[@class='title']")[0];
//          }
//       }

//    var goodReads =
//       {
//          getIsbn: function()
//          {
//             try
//             {
//                var isbnHeaderNodeCandidates = $x("//div[@class='infoBoxRowTitle']");
               
//                for ( var i = 0; i < isbnHeaderNodeCandidates.length; i++ )
//                {
//                   if ( isbnHeaderNodeCandidates[i].innerHTML.match(/isbn/) )
//                   {
//                       var isbnNode = isbnHeaderNodeCandidates[i].nextSibling;
//                       while ( isbnNode.nodeName != 'DIV' )
//                       {
//                           isbnNode = isbnNode.nextSibling;
//                       }
//                       var isbnText = isbnNode.innerHTML.match(isbnREdelimited)[1];
//                       return isbnText;
//                   }
//                }
//             }
//             catch ( e ) 
//             {
//                GM_log('error looking for ISBN: ' + e);
//             }
//             return null;
//          },

//          getOriginalTitle: function()
//          {
//             return $x("//h1[@id='bookPageTitle']")[0];
//          }
//       }

//    // figure out what site we're looking at
//    if ( location.href.match(/chapters/) )
//    {
//       return chapters;
//    }
//    else if ( location.href.match(/allconsuming/) )
//    {
//       return allconsuming;
//    }
//    else if ( location.href.match(/powells/) )
//    {
//       return powells;
//    }
//    else if ( location.href.match(/google/) )
//    {
//       return googleBooks;
//    }
//    else if ( location.href.match(/goodreads/) )
//    {
//       return goodReads;
//    }
//    else if ( location.href.match(/librarything/) )
//    {
//       return librarything;
//    }
//    else
//    {
//       // Amazon's pretty popular - make it the default
//       return amazon;
//    }
// }

chrome.extension.sendRequest(request={msg: 'show'});
// alert('location = ' + location.href);
