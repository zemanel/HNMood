(function(){
    var baseurl = '{{baseurl}}';

    function loadDojo(){
        _s=document.createElement('SCRIPT');
        _s.type='text/javascript';
        _s.src='http://ajax.googleapis.com/ajax/libs/dojo/1.6/dojo/dojo.xd.js';
        document.getElementsByTagName('head')[0].appendChild(_s);
    }

    // Load Dojo
    loadDojo();

    function getCommentAnalisysCallback(linkNode, newsitem) {
        if (newsitem.is_sentiment_processed===true) {
            var newDomNode = document.createElement('SPAN');
            var color = null;
            newDomNode.id = "hnmood_"+newsitem.itemid;
            if ('OK'===newsitem.sentiment_status) {
                if (newsitem.sentiment_type==='positive') {
                    color = 'green';
                } else if (newsitem.sentiment_type==='negative') {
                    color = 'red';
                } else if (newsitem.sentiment_type==='neutral') {
                    color = 'gray';
                }
                newDomNode.innerHTML = '| <span style="color:'+color+';"> Sentiment analysis score:'+newsitem.sentiment_score+' ('+newsitem.sentiment_type+') </span> [itemid: '+newsitem.itemid+']';
                dojo.place(newDomNode, linkNode.parentNode, 'last');
            } else if ('ERROR'===newsitem.sentiment_status){
                color = 'orange';
                newDomNode.innerHTML = '| <span style="color:'+color+';">Sentiment analysis error: '+newsitem.sentiment_status_info+'</span> [itemid: '+newsitem.itemid+']';
                dojo.place(newDomNode, linkNode.parentNode, 'last');
            }
        }
    }

    function processComments() {
        var comments = dojo.query("span.comhead");
        var links = null;
        var newsitemId = null;
        var newDomNodeId = null;
        comments.forEach(function(commentNode, index, array){
            links = dojo.query(commentNode).query("a").filter(':contains("link")');
            //links.style('color', 'red');
            //console.debug(links);
            links.forEach(function(linkNode, index, array){
                newsitemId = linkNode.href.split('=')[1];
                newDomNodeId = "hnmood_"+newsitemId;
                // check if it was already processed
                if (dojo.query(commentNode).query('#'+newDomNodeId).length==0) {
                    // Analisys node does not exist, create it
                    var xhrArgs = 
                    dojo.io.script.get({
                        url: baseurl+'item/'+newsitemId,
                        callbackParamName: "jsoncallback",
                        load: dojo.partial(getCommentAnalisysCallback, linkNode),
                        error: function(error) {
                            if (window.console) {
                                console.error(error);    
                            }
                        }
                    });
                }
            });
        });    
    }

    // wait for dojo loading and execute code
    window.setTimeout(function(){
        dojo.require("dojo.io.script");
        dojo.ready(processComments);
    }, 500);

})();