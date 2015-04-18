function getLibraries(host, callback, errorCallback)
{
    var url = 'http://' + host + '/libraries';

    var x = new XMLHttpRequest();
    x.open('GET', url);
    x.responseType = 'json';
    x.onload = function()
    {
        var response = x.response;
        callback(response);
    };
    x.onerror = function()
    {
        errorCallback('Network error.');
    };
    x.send();
}

function createLibaryLogo(host, key)
{
    var img = document.createElement('img');

    var src = document.createAttribute('src');
    src.value = 'http://' + host + '/static/library_icons/' + key + '_64.png';
    img.setAttributeNode(src);

    var height = document.createAttribute('height');
    height.value = '16';
    img.setAttributeNode(height);

    var weight = document.createAttribute('weight');
    weight.value = '16';
    img.setAttributeNode(weight);

    return img;
}

function createLibraryCheckbox(favourite_libraries, key)
{
    var input = document.createElement('input');
    var type = document.createAttribute('type');
    type.value = 'checkbox';
    var value = document.createAttribute('value');
    value.value = key;

    for ( var l = 0; l < favourite_libraries.length; l++ )
    {
        if (key == favourite_libraries[l] )
        {
            input.checked = 'true';
            break;
        }
    }

    input.setAttributeNode(type);
    input.setAttributeNode(value);

    return input;
}

function loadFavouriteLibraries()
{
            var favourite_libraries = localStorage["favLibraries"];
            if ( ! favourite_libraries)
            {
                favourite_libraries = 'wpl,kpl,rwl';
            }

            return favourite_libraries.split(',');
 }

function loadOptions()
{
    var host = chrome.extension.getBackgroundPage().getServerHost();
    getLibraries(
        host,
        function(response)
        {
            var favourite_libraries = loadFavouriteLibraries();

            var fieldset = document.getElementsByTagName('fieldset')[0];

            for (var key in response)
            {
                if ( response.hasOwnProperty(key) )
                {
                    var library_name = document.createTextNode('\u00A0' + response[key]['name']);

                    var label = document.createElement('label');
                    label.appendChild(createLibraryCheckbox(favourite_libraries, key));
                    label.appendChild(createLibaryLogo(host, key));
                    label.appendChild(library_name);

                    var br = document.createElement('br');

                    fieldset.appendChild(label);
                    fieldset.appendChild(br);
                }
            }
        },
        function(error){alert('Error: ' + error);}
    );
}

function saveOptions()
{
    var libraries = new Array();
    var checkboxes = document.getElementsByTagName("input");
    for (var i = 0; i < checkboxes.length; i++)
    {
        var child = checkboxes[i];
        if ( child.checked )
        {
            libraries.push(child.value);
        }
    }
    localStorage["favLibraries"] = libraries;

    showSaved();
}

function clearStatus()
{
    var status = document.getElementById("status");
    status.innerHTML = '';
}

function showSaved()
{
    var status = document.getElementById("status");
    status.innerHTML = 'saved';
    window.setTimeout(clearStatus, 1000);
}

function eraseOptions()
{
    localStorage.removeItem("favLibraries");
    location.reload();
}

function hookUpSaveEvent()
{
    document.getElementById("saveButton").addEventListener("click", saveOptions);
}

document.addEventListener('DOMContentLoaded', loadOptions);
document.addEventListener('DOMContentLoaded', hookUpSaveEvent);
