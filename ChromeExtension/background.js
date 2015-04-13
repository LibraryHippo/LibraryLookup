var lookupsByPage = new Array();

// Listen for any changes to the URL of any tab.
chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse) 
    {
        if ( request.msg == 'lookup' )
        {
            chrome.pageAction.setTitle({tabId: sender.tab.id, title: 'LibraryLookup: searching'});
            chrome.pageAction.show(sender.tab.id);

            var searching_images = ['searching_eye_down_19.png',
                                    'searching_eye_right_19.png',
                                    'searching_eye_down_19.png',
                                    'searching_eye_left_19.png'];

            var image_index = 0;
            
            var keep_switching_icon = true;
            function rotateIcon()
            {               
                if ( keep_switching_icon )
                {
                    console.log('switching icon');
                    chrome.pageAction.setIcon({tabId: sender.tab.id, path: searching_images[image_index]});
                    image_index = (image_index + 1) % searching_images.length ;
                    window.setTimeout(rotateIcon, 300);
                }
            }

            window.setTimeout(rotateIcon, 300);
            var libraries = localStorage["favLibraries"];
            if ( ! libraries )
            {
                libraries = 'wpl,kpl';
            }
            libraries = libraries.split(',');
            
            var url = 'http://librarylookup-hrd.appspot.com/isbn/' + request.isbn + '?lib=';
            // var url = 'http://localhost:8080/isbn/' + request.isbn + '?lib=';

            url = url + libraries.join('&lib=');
            
            var xhr = new XMLHttpRequest();
            xhr.open("GET", url, true);
            xhr.onreadystatechange = function() 
            {
                if (xhr.readyState == 4) 
                {
                    keep_switching_icon = false;
                    // 200 = OK
                    // 204 = No Content - when Google returns cached content
                    if ( xhr.status != 200 && xhr.status != 204 )
                    {
                        console.log('error: xhr.status = ' + xhr.status);
                        chrome.pageAction.setTitle({tabId: sender.tab.id, title: 'LibraryLookup: Error while searching'});
                        chrome.pageAction.setIcon({tabId: sender.tab.id, path: 'error_19.png'});
                        return;
                    }

                    lookupDom = new DOMParser().parseFromString(xhr.responseText, "text/html");
                    lookupsByPage[sender.tab.id] = lookupDom;
                    
                    if ( lookupDom.getElementsByTagName("li").length )
                    {
                        chrome.pageAction.setTitle({tabId: sender.tab.id, title: 'LibraryLookup: Found'});
                        chrome.pageAction.setPopup({tabId: sender.tab.id, popup: 'popup.html'});
                        chrome.pageAction.setIcon({tabId: sender.tab.id, path: 'found_19.png'});
                    }
                    else
                    {
                        chrome.pageAction.setTitle({tabId: sender.tab.id, title: 'LibraryLookup: Not found'});
                        chrome.pageAction.setIcon({tabId: sender.tab.id, path: 'not_found_19.png'});
                    }
                }
            };
            xhr.send();
        }
    }
);

