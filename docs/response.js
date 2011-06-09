//http://api.thriftdb.com/api.hnsearch.com/items/_search?q=facebook&weights[title]=1.1&weights[text]=0.7&weights[domain]=2.0&weights[username]=0.1&weights[type]=0.0&boosts[fields][points]=0.15&boosts[fields][num_comments]=0.15&boosts[functions][pow(2,div(div(ms(create_ts,NOW),3600000),72))]=200.0&pretty_print=true
{
    "facet_results": {
        "fields": {},
        "queries": {}
    },
    "hits": 42853,
    "request": {
        "boosts": {
            "fields": {
                "num_comments": 0.14999999999999999,
                "points": 0.14999999999999999
            },
            "filters": {},
            "functions": {
                "pow(2,div(div(ms(create_ts,NOW),3600000),72))": 200.0
            }
        },
        "facet": {
            "fields": {},
            "queries": []
        },
        "filter": {
            "fields": {},
            "queries": []
        },
        "highlight": {
            "fragments": {
                "include": false,
                "markup_text": false,
                "maxchars": 100
            },
            "include_matches": false,
            "markup_items": false
        },
        "limit": 10,
        "q": "facebook",
        "sortby": "score desc",
        "start": 0,
        "weights": {
            "discussion.sigid": 1.0,
            "domain": 2.0,
            "parent_sigid": 1.0,
            "text": 0.69999999999999996,
            "title": 1.1000000000000001,
            "type": 0.0,
            "url": 1.0,
            "username": 0.10000000000000001
        }
    },
    "results": [
        {
            "item": {
                "_id": "2632762-e0272",
                "cache_ts": "2011-06-08T14:50:32Z",
                "create_ts": "2011-06-08T11:59:52Z",
                "discussion": null,
                "domain": "nicolaerusan.tumblr.com",
                "id": 2632762,
                "num_comments": 0,
                "parent_id": null,
                "parent_sigid": null,
                "points": 1,
                "text": null,
                "title": "Facebook Connect + Facebook Payments = World Domination",
                "type": "submission",
                "url": "http://nicolaerusan.tumblr.com/post/6317545774/facebook-connect-facebook-payments-world-domination",
                "username": "nicoslepicos"
            },
            "score": 0.97438769999999997
        },
        {
            "item": {
                "_id": "2632801-f7b08",
                "cache_ts": "2011-06-08T14:50:32Z",
                "create_ts": "2011-06-08T12:13:27Z",
                "discussion": null,
                "domain": "bbc.co.uk",
                "id": 2632801,
                "num_comments": 16,
                "parent_id": null,
                "parent_sigid": null,
                "points": 11,
                "text": null,
                "title": "Facebook sorry over face tagging launch",
                "type": "submission",
                "url": "http://www.bbc.co.uk/news/technology-13693791",
                "username": "colinprince"
            },
            "score": 0.95752630000000005
        },
        {
            "item": {
                "_id": "2631996-f1943",
                "cache_ts": "2011-06-08T09:06:11Z",
                "create_ts": "2011-06-08T04:15:06Z",
                "discussion": null,
                "domain": "thefastertimes.com",
                "id": 2631996,
                "num_comments": 0,
                "parent_id": null,
                "parent_sigid": null,
                "points": 1,
                "text": null,
                "title": "Confessions of a Facebook Stalker",
                "type": "submission",
                "url": "http://thefastertimes.com/college/2011/06/07/21st-century-love-we-met-online/",
                "username": "dreambird"
            },
            "score": 0.9063234
        },
        {
            "item": {
                "_id": "2633208-1fe42",
                "cache_ts": "2011-06-08T14:50:32Z",
                "create_ts": "2011-06-08T14:28:22Z",
                "discussion": {
                    "id": 2632801,
                    "sigid": "2632801-f7b08",
                    "title": "Facebook sorry over face tagging launch"
                },
                "domain": null,
                "id": 2633208,
                "num_comments": 0,
                "parent_id": 2632801,
                "parent_sigid": "2632801-f7b08",
                "points": null,
                "text": "How would Facebook be able to innovate if everything they released was opt-out?  This isn't some privacy-leaking piece of the site, it is a feature that helps one of their core components be better.<p>If you are that much of a privacy freak, don't make a Facebook account.  It's that simple - either you want your data out there to some degree or not (and don't glorify Facebook into something that it is not).",
                "title": null,
                "type": "comment",
                "url": null,
                "username": "invisible"
            },
            "score": 0.88859546
        },
        {
            "item": {
                "_id": "2633093-e21c2",
                "cache_ts": "2011-06-08T14:50:32Z",
                "create_ts": "2011-06-08T13:56:35Z",
                "discussion": {
                    "id": 2632801,
                    "sigid": "2632801-f7b08",
                    "title": "Facebook sorry over face tagging launch"
                },
                "domain": null,
                "id": 2633093,
                "num_comments": 2,
                "parent_id": 2632801,
                "parent_sigid": "2632801-f7b08",
                "points": null,
                "text": "No they're not.<p>If you're sorry, you don't do it again.<p>Facebook do this again and again and again and again.",
                "title": null,
                "type": "comment",
                "url": null,
                "username": "nodata"
            },
            "score": 0.88811379999999995
        },
        {
            "item": {
                "_id": "2633237-7ed82",
                "cache_ts": "2011-06-08T14:50:32Z",
                "create_ts": "2011-06-08T14:36:43Z",
                "discussion": {
                    "id": 2632801,
                    "sigid": "2632801-f7b08",
                    "title": "Facebook sorry over face tagging launch"
                },
                "domain": null,
                "id": 2633237,
                "num_comments": 1,
                "parent_id": 2633170,
                "parent_sigid": "2633170-fe210",
                "points": null,
                "text": "I may be wrong, but the impression I'm getting is that people are offended that facebook have used the photos that have people tagged them in as data for training their facial recognition software without them agreeing to it.<p>It's the fact that they now have the power to determine whether you're in a photo, any photo, or even any video, anywhere in the world, that has people worried. What might facebook end up doing with that?<p>Of course there was nothing stopping them doing this without it being obvious to anyone.",
                "title": null,
                "type": "comment",
                "url": null,
                "username": "rodh"
            },
            "score": 0.88376635000000003
        },
        {
            "item": {
                "_id": "2633113-dd2ef",
                "cache_ts": "2011-06-08T14:50:32Z",
                "create_ts": "2011-06-08T14:04:56Z",
                "discussion": {
                    "id": 2632801,
                    "sigid": "2632801-f7b08",
                    "title": "Facebook sorry over face tagging launch"
                },
                "domain": null,
                "id": 2633113,
                "num_comments": 2,
                "parent_id": 2632801,
                "parent_sigid": "2632801-f7b08",
                "points": null,
                "text": "Until Facebook adds the possibility to prevent people from tagging me completely, then I don't believe they are sorry.<p>However, such an option is not available ... you have to untag yourself after the fact and some people just keep re-adding you ... how do you explain to people to fucking stop tagging you without hurting their feelings and without sounding like a weirdo?<p>I loved Facebook in the beginning, but their intrusion on my privacy is getting too damn annoying. I wish there was an alternative.",
                "title": null,
                "type": "comment",
                "url": null,
                "username": "bad_user"
            },
            "score": 0.88158643000000003
        },
        {
            "item": {
                "_id": "2633187-594ad",
                "cache_ts": "2011-06-08T14:50:32Z",
                "create_ts": "2011-06-08T14:24:18Z",
                "discussion": {
                    "id": 2632801,
                    "sigid": "2632801-f7b08",
                    "title": "Facebook sorry over face tagging launch"
                },
                "domain": null,
                "id": 2633187,
                "num_comments": 1,
                "parent_id": 2633113,
                "parent_sigid": "2633113-dd2ef",
                "points": null,
                "text": "Tagging is a pretty fundamental feature of Facebook, in my opinion.  That being said, there actually already is an option in the privacy settings to prevent anyone from seeing the images you're tagged in.  That's slightly different from preventing the tagging in the first place, but the effect is the same.",
                "title": null,
                "type": "comment",
                "url": null,
                "username": "ryusage"
            },
            "score": 0.88083929999999999
        },
        {
            "item": {
                "_id": "2633285-23688",
                "cache_ts": "2011-06-08T14:50:32Z",
                "create_ts": "2011-06-08T14:46:37Z",
                "discussion": {
                    "id": 2632801,
                    "sigid": "2632801-f7b08",
                    "title": "Facebook sorry over face tagging launch"
                },
                "domain": null,
                "id": 2633285,
                "num_comments": 0,
                "parent_id": 2633237,
                "parent_sigid": "2633237-7ed82",
                "points": null,
                "text": "Got it.  That does make sense; the article and comments just didn't really seem like that was specifically what people were worried about.  Given that I see no other reason to care, though, I assume you're correct.<p>Personally, I'm not so worried about Facebook being able to recognize me.  I'd be more concerned about to whom they might give that data.  I can definitely see room for a lot of concern there.",
                "title": null,
                "type": "comment",
                "url": null,
                "username": "ryusage"
            },
            "score": 0.87949449999999996
        },
        {
            "item": {
                "_id": "2633192-22c7b",
                "cache_ts": "2011-06-08T14:50:32Z",
                "create_ts": "2011-06-08T14:24:53Z",
                "discussion": {
                    "id": 2632801,
                    "sigid": "2632801-f7b08",
                    "title": "Facebook sorry over face tagging launch"
                },
                "domain": null,
                "id": 2633192,
                "num_comments": 0,
                "parent_id": 2632951,
                "parent_sigid": "2632951-88d9f",
                "points": null,
                "text": "Of course they get it. They just don't care.<p>If this was opt-in by default, it wouldn't get nearly the same adoption. Lots of people would click no, then never change the setting.<p>The general public will eventually get over it, the same way they got over {the news feed, suggest a friend, changing interests to likes, letting people without .edu accounts sign up, ...}. Facebook knows this. PR probably had the apology written before the feature was turned on.",
                "title": null,
                "type": "comment",
                "url": null,
                "username": "pflats"
            },
            "score": 0.87944036999999997
        }
    ],
    "time": 0.062556028366088867,
    "warnings": []
}