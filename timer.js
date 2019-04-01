$(document).ready(function() {
  chrome.runtime.sendMessage({ action: "createAlarm" });
  chrome.runtime.onMessage.addListener(function(resp, sender, sendResponse) {
    if (resp.action == "doAlarm") {
      alert('oi');
      console.log('oi');
    }
  });
});
