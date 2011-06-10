(function(){
  var baseurl = '{{baseurl}}';
  function loadDojo(){
    _s=document.createElement('SCRIPT');
    _s.type='text/javascript';
    _s.src='http://ajax.googleapis.com/ajax/libs/dojo/1.6/dojo/dojo.xd.js';
    document.getElementsByTagName('head')[0].appendChild(_s);
  }
  loadDojo();  
  console.debug(dojo)
  // http://news.ycombinator.com/item?id=2634985
  var links = dojo.query("span.comhead a:last-child");
  //links.style("color","red");
  links.forEach(function(node, index, array){
    //console.debug(node, index, array)
    var id = node.href.split('=')[1];
    //console.log(id);
  });
  
  var xhrArgs = {
      url: "http://localhost:8080/",
      postData: "Some random text",
      handleAs: "text",
      load: function(data) {
          console.log(data);
      },
      error: function(error) {
        console.error(error);
      }
  }
  //Call the asynchronous xhrPost
  var deferred = dojo.xhrPost(xhrArgs);
  
  
  //console.dir(  );
})();