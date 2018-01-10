LibraryLookup is a two-part application that checks to see if a book you're looking at on the web is
available in your local library.
It consists of two components:


* a backend [Google App Engine](https://cloud.google.com/products/app-engine/)
application that checks the libraries for the presence of certain ISBNs, and
* a Google Chrome extension that triggers the check and reports the results

Currently supports 
* [Waterloo Public Library](http://www.wpl.ca/)
* [Kitchener Public Library](http://www.kpl.org/)
* [OverDrive Download Library](https://downloadlibrary.overdrive.com/)
