function loadOptions() 
{
   var libraries = localStorage["favLibraries"];
   if ( ! libraries )
   {
      libraries = 'wpl,kpl,rwl';
   }
   libraries = libraries.split(',');
   
   var checkboxes = document.getElementsByTagName("input");
   for (var i = 0; i < checkboxes.length; i++) 
   {
      var child = checkboxes[i];
      for ( var l = 0; l < libraries.length; l++ )
      {
         if (child.value == libraries[l] ) 
         {
            child.checked = "true";
            break;
         }
      }
   }
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
