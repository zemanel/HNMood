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
  
  function getCommentAnalisysCallback(linkNode, newsitem) {
    console.log(linkNode, newsitem);
    if (newsitem.is_sentiment_processed===true) {
      var newDomNode = document.createElement('SPAN');
      newDomNode.id = "hnmood_"+newsitem.id;
      newDomNode.innerHTML = '| Sentiment score:'+newsitem.sentiment_score+' ('+newsitem.sentiment_type+')';
      dojo.place(newDomNode, linkNode, 'after');      
    }
  }
  
  function processComments() {
    // http://news.ycombinator.com/item?id=2634985
    var comments = dojo.query("span.comhead");
    // comments.style("color","red");
    var links = null;
    var newsitemId = null;
    var newDomNodeId = null;
    comments.forEach(function(commentNode, index, array){
      links = dojo.query(commentNode).query("a:last-child");
      if (links.length>0) {
        links.forEach(function(linkNode, index, array){
          newsitemId = linkNode.href.split('=')[1];
          newDomNodeId = "hnmood_"+newsitemId;
          // check if it was already processed
          if (dojo.query(commentNode).query('#'+newDomNodeId).length==0) {
            // Analisys node does not exist, create it
            var xhrArgs = {
                url: baseurl+'item/'+newsitemId,
                callbackParamName: "jsoncallback",
                load: dojo.partial(getCommentAnalisysCallback, linkNode),
                error: function(error) {
                  console.error(error);
                }
            }
            dojo.io.script.get(xhrArgs);
          }
        });
      }
      //console.debug();
    });
    
    
    
    //links.style("color","red");
    links.forEach(function(node, index, array){
      //console.debug(node, index, array)
      var itemid = node.href.split('=')[1];
      //console.log(itemid);

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