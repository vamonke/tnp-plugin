console.log("background.js");
var alarmName;

var now = new Date();

var nowHour = now.getHours();
var nextEditionHour;
var nextEditionDate = now.getDate();

if (nowHour < 12) {
  alarmName = 'noon';
  nextEditionHour = 12;
} else if (nowHour < 18) {
  alarmName = 'evening';
  nextEditionHour = 18;
} else {
  alarmName = 'morning';
  nextEditionDate += 1;
  nextEditionHour = 9;
}

// var nextEdition = new Date(now.getFullYear(), now.getMonth(), nextEditionDate, nextEditionHour, 0, 0);
var nextEdition = new Date(now.getFullYear(), now.getMonth(), now.getDate(), now.getHours(), now.getMinutes()+1, now.getSeconds()+10);
console.log(now.toLocaleString());
console.log(nextEdition.toLocaleString());
var whenToRing = (nextEdition.getTime() - now.getTime());
// console.log(whenToRing);

chrome.alarms.clearAll(function() {
  chrome.alarms.create(alarmName, { when: whenToRing });
  chrome.alarms.getAll(function(alarms) {
    console.log(alarms.length + ' alarm(s) currently');
  });
});

chrome.alarms.onAlarm.addListener(function(alarm) {
  console.log("Alarm fired:", alarm);
  alert(alarm.name);
});

// chrome.runtime.onMessage.addListener(function(msg, sender, sendResponse) {
//   if (msg.action === "updateIcon") {
//     console.log("updateIcon");
//     var today = new Date();
//     var nowHour = today.getHours();
//     var change;

//     if (nowHour < 12) {
//       change = morning;
//     } else if (nowHour < 18) {
//       change = afternoon;
//     } else {
//       change = night
//     }

//     if (change !== current) {
//       console.log('Change to', change);
//       chrome.browserAction.setIcon({
//         path: change
//       });
//       current = change;
//     }
//   }
// });
