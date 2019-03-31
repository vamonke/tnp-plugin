console.log("background.js");
const morning = "tab-icon.png";
const afternoon = "tab-icon-green.png";
const night = "tab-icon-blue.png";
let current = null;

chrome.runtime.onMessage.addListener(function(msg, sender, sendResponse) {
  if (msg.action === "updateIcon") {
    console.log("updateIcon");
    let today = new Date();
    let curHr = today.getHours();
    let change;

    if (curHr < 12) {
      change = morning;
    } else if (curHr < 18) {
      change = afternoon;
    } else {
      change = night
    }

    if (change !== current) {
      console.log('Change to', change);
      chrome.browserAction.setIcon({
        path: change
      });
      current = change;
    }
  }
});
