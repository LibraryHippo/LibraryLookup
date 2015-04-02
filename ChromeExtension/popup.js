/**
 * Get the current URL.
 *
 * @param {function(string)} callback - called when the ID of the current tab
 *   is found.
 **/
function getCurrentTabId(callback) {
  // Query filter to be passed to chrome.tabs.query - see
  // https://developer.chrome.com/extensions/tabs#method-query
  var queryInfo = {
    active: true,
    currentWindow: true
  };

  chrome.tabs.query(queryInfo, function(tabs) {
    // chrome.tabs.query invokes the callback with a list of tabs that match the
    // query. When the popup is opened, there is certainly a window and at least
    // one tab, so we can safely assume that |tabs| is a non-empty array.
    // A window can only have one active tab at a time, so the array consists of
    // exactly one tab.
    var tab = tabs[0];

    // A tab is a plain object that provides information about the tab.
    // See https://developer.chrome.com/extensions/tabs#type-Tab
    var tabId = tab.id;

    callback(tabId);
  });
}

function makeLinksOpenInNewTabs()
{
    // from http://stackoverflow.com/a/17732667/1199
    var links = document.getElementsByTagName('a');
    for (var i = 0; i < links.length; i++) {
        (function () {
            var ln = links[i];
            var location = ln.href;
            ln.onclick = function () {
                chrome.tabs.create({active: true, url: location});
            };
        })();
    }
}

document.addEventListener('DOMContentLoaded', function() {
  getCurrentTabId(function(tabId) {
      var findings  = chrome.extension.getBackgroundPage().lookupsByPage[tabId];
      var findingsUl = findings.getElementsByTagName('ul')[0];

      var ul = document.getElementsByTagName('ul')[0];
      ul.innerHTML =findingsUl.innerHTML;

      makeLinksOpenInNewTabs();
  });
});

