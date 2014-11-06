
var iplayerDownloader = {
  requestDownload: function() {
    chrome.tabs.query({active: true, lastFocusedWindow: true}, function(tabs) {
      var tab = tabs[0];
      var location = "http://localhost:8000/" + escape(tab.url);
      var req = new XMLHttpRequest();      
      req.open("GET", location, true);
      req.send(null);
    })
  }
};

document.addEventListener('DOMContentLoaded', function () {
  iplayerDownloader.requestDownload();
});
