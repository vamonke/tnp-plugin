$(document).ready(function(){
  $("#select1").click(function(){
    $("#home").hide();
    $("#playlist1").show();
    chrome.runtime.sendMessage({ action: 'updateIcon' });
    console.log('sent');
  });
});
