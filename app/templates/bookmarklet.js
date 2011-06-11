(function(){
  var baseurl = '{{baseurl}}';
//  var icons = {{icons|safe}};
//  console.debug(icons.sentiment_negative)

  function loadDojo(){
    _s=document.createElement('SCRIPT');
    _s.type='text/javascript';
    _s.src='http://ajax.googleapis.com/ajax/libs/dojo/1.6/dojo/dojo.xd.js';
    document.getElementsByTagName('head')[0].appendChild(_s);
  }
  
  function processComments() {
    // http://news.ycombinator.com/item?id=2634985
    var links = dojo.query("span.comhead a:last-child");
    links.style("color","red");
    links.forEach(function(node, index, array){
      //console.debug(node, index, array)
      var itemid = node.href.split('=')[1];
      //console.log(itemid);
      var xhrArgs = {
          url: baseurl+'item/'+itemid,
          callbackParamName: "jsoncallback",
          load: function(data) {
              console.log(data);
          },
          error: function(error) {
            console.error(error);
          }
      }
      dojo.io.script.get(xhrArgs);
    });
    
  }
  
  // Load Dojo
  loadDojo();

  // wait for dojo loading and execute code
  window.setTimeout(function(){
    dojo.require("dojo.io.script");
    dojo.ready(processComments);
  }, 500);

})();