var NextUrl = ""

function getParameterByName(name, url) {
    if (!url) url = window.location.href;
    name = name.replace(/[\[\]]/g, '\\$&');
    var regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)'),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, ' '));
}

function PutDataOnMedia(data,IdMedia,prepend){
    TweetHtml=

            "<div class=\"preview-box\">"+
            "<li class=\"media\">" +
            "<a class=\"pull-left\" href=\" \"> " +
            "<img class=\"media-object rounded-circle d-flex align-self-start mr-3 \" alt=\"\" style=\"width:60px\" src=" + data.image +  ">" +
            "</a>"+



            "<div class=\"media-body \">" +
            "<h4 class=\"mt-0 media-heading font-weight-bold\">" +
                    "<a href='#'>"+ data.user.username+ "<small>" +
                    "<i><a id='addons' href=\"\">Posted on "+ data.time_since+ "</a></i></small></a>" +
            "</h4>" +
            "<p>" +
            data.content  + "<br>" +
            "<a id='addons' href=\"\">Like.</a>" +
            "<a id='addons' href=\"\">Reply.</a>" +
            "</p></div></li></div><br>"

    if(prepend == true){
        IdMedia.prepend(TweetHtml)
    }else{
        IdMedia.append(TweetHtml)
    }
}


function FetchTweets(data){
var IdMedia = $("#IdMedia")
            if (data.length >  0) {
                $.each(data, function (key, value) {
                        console.log(value)
                        PutDataOnMedia(value,IdMedia,false)

                })
            }
            else {

                IdMedia.text("No tweets found!")
            }

}

function Ajaxfnc(url,method,data) {
    var IdMedia = $("#IdMedia")
    if(url != null){
        $.ajax({
            url: url,
            method: method,
            data: data,
            success: function (data) {
                if(url != '/api/tweet/create')
                {
                    NextUrl = data.next
                    if(!NextUrl){$('.LoadMoreTweets').css('display','none')}
                    FetchTweets(data.results)

                }
                else{
                    $('#TweetTA').val('');
                    PutDataOnMedia(data,IdMedia,true)
                }

            },
            error: function (error) {
                console.log(error)

            }

        })
    }
}

function CreateTweetAPIRest(){
    var tweetform = $('#tweet_form')
    tweetform.submit(function (e) {
        var this_ = $(this)
        e.preventDefault()
        methode = 'POST'
        url = '/api/tweet/create/'
        data = this_.serialize()
        Ajaxfnc(url,methode,data)   //New  tweet is added here

    })
}


function TweetTACharCount(){
     var count = $('#TweetTA').attr('maxlength')
    $('.count').text(count)
    $('#TweetTA').on("input", function(){
    var maxlength = $(this).attr("maxlength");
    var currentLength = $(this).val().length;

    if( currentLength >= maxlength ){
        $('.count').text(maxlength - currentLength);
    }else{
        $('.count').text(maxlength - currentLength);
    }
});
}

function LoadMoreTweets(){
    $('.LoadMoreTweets').click(function (e) {
        Ajaxfnc(NextUrl, 'GET', {})
    })
}

function EditBtn(){
    var b = $("#button");
    var w = $("#wrapper");
    var l = $("#list");
}
$(document).ready(function() {
    TweetTACharCount()
    LoadMoreTweets()
    Ajaxfnc('/api/tweet/','GET',data={})
    CreateTweetAPIRest()




});

