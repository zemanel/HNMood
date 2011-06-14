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
        //console.log(linkNode, newsitem);
        if (newsitem.is_sentiment_processed===true) {
            var newDomNode = document.createElement('SPAN');
            var color = null;
            newDomNode.id = "hnmood_"+newsitem.id;
            if ('OK'===newsitem.sentiment_status) {
                if (newsitem.sentiment_type==='positive') {
                    color = 'green';
                } else if (newsitem.sentiment_type==='negative') {
                    color = 'red';
                } else if (newsitem.sentiment_type==='neutral') {
                    color = 'gray';
                }
                newDomNode.innerHTML = '| <span style="color:'+color+';"> Sentiment score:'+newsitem.sentiment_score+' ('+newsitem.sentiment_type+') </span>';
            } else {
                color = 'orange';
                newDomNode.innerHTML = '| <span style="color:'+color+';">'+newsitem.sentiment_status_info+'</span>';
            }
            dojo.place(newDomNode, linkNode, 'after');      
        }
    }

    function processComments() {
        var comments = dojo.query("span.comhead");
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
        });    
    }

    // wait for dojo loading and execute code
    window.setTimeout(function(){
        dojo.require("dojo.io.script");
        dojo.ready(processComments);
    }, 500);

})();