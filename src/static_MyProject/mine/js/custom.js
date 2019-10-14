var NextUrl = ""
var query_flag2=true

function getParameterByName(name, url) {
    if (!url) url = window.location.href;
    name = name.replace(/[\[\]]/g, '\\$&');
    var regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)'),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, ' '));
}

function PutDataOnMedia(data,IdMedia,prepend = false,query_flag=false){
    var img = empty_img
    if(data.user.profile.image){
        img = data.user.profile.image
    }

    TweetHtml=

            "<div class=\"preview-box\">"+
            "<li class=\"media\">" +
            "<a class=\"pull-left\" href=\" \"> " +
            "<img class=\"media-object rounded-circle d-flex align-self-start mr-3 \" alt=\"\" style=\"width:60px\" src=" + img +  ">" +
            "</a>"+



            "<div class=\"media-body \">" +
            "<p class=\"mt-0 media-heading font-weight-bold\"><a id='LinkBlueColor' href='"+data.user.profile.profile_url+"' >"+data.user.username+"</a><small><i><a id='LinkBlueColor' href=\\\"\\\">  Posted on "+ data.time_since+ "</a></i></small></p>" +
            "<p>"+data.content.replace(/(^|\s)#([\w\d-]+)/g,"$1<a id='LinkBlueColor' href='/tags/$2/'>#$2</a>")+"</p><a id='LinkBlueColor' class='addons' href=\\\"\\\"><i class=\"far fa-heart\" title=\"Like\"></i></a> <a id='LinkBlueColor' class='addons' href=\\\"\\\"><i class=\"fas fa-retweet\" title=\"Retweet\"></i></a></div></li></div><br>"

    if(query_flag){
        if(query_flag2){
            IdMedia.empty()
            query_flag2=false
            IdMedia.append(TweetHtml)
        }else{
            IdMedia.append(TweetHtml)
        }
    }else{
        if(prepend){
                IdMedia.prepend(TweetHtml)
            }else{
            IdMedia.append(TweetHtml)
        }
    }

}


function FetchTweets(data , query_flag = false ){
var IdMedia = $("#IdMedia")
            if (data) {
                $.each(data, function (key, value) {

                        PutDataOnMedia(value,IdMedia,false,query_flag)

                })
                // Hashtaglinks()
            }
            else {

                IdMedia.text("No tweets found!")
            }

}

function Ajaxfnc(url,method,data) {
    var IdMedia = $("#IdMedia")
    var query = data.q
    if(url != null){
        $.ajax({
            url: url,
            method: method,
            data: data,
            success: function (data) {
                if(url != '/api/tweet/create/'  )   // List all tweets case
                {
                    NextUrl = data.next
                    if (!NextUrl) {
                        $('.JS-LoadMoreTweets').css('display', 'none')
                    }


                    if (url == '/api/tweet/search/' && query != null) {

                        var query_flag = true
                        window.history.pushState({"html": data.html, "pageTitle": data.pageTitle}, "", '/tweets/search/'+'?q='+query);
                        $('#search-form input[name="q"]').val('');
                    }

                    FetchTweets(data.results,query_flag)


                }else{                                           //create case
                    $('#TweetTA').val('');
                    PutDataOnMedia(data,IdMedia,true)
                    // Hashtaglinks()
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
    $('.JS-LoadMoreTweets').click(function (e) {
        Ajaxfnc(NextUrl, 'GET', {})
    })
}

function EditBtn(){
    var b = $("#button");
    var w = $("#wrapper");
    var l = $("#list");
}

function Search_form(){
    $('#search-form').submit(function (e) {
        e.preventDefault()
        var this_ = $(this)
        var action = this_.attr('action')
        var method = this_.attr('method')
        q =  $("#search-form input[name='q']").val()
        // alert(q)
        Ajaxfnc(action,method,data={'q':q})

    })
}

 function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();

            reader.onload = function (e) {
                $('.prw_img').attr('src', e.target.result);
                $("form input[name='image']").val(e.target.result)
            }

            reader.readAsDataURL(input.files[0]);

        }
    }
function PrvImage_Profile(){
    $("form input[name='image']").change(function(e) {

        readURL(this)

    });
}
//$1<a href='/tags/$2/'>#$2</a>
// function Hashtaglinks(){
//
//     $('.media-body').each(function (data) {
//
//         var $this_ =$(this)
//         var hasttagregex = /(^|\s)#([\w\d-]+)/g
//         // alert($this_.html())
//         var new_string = $this_.html().replace(hasttagregex,"$1<a href='/tags/$2/'>#$2</a>")
//         // alert(new_string)
//         $this_.html(new_string)
//
//     })
// }
$(document).ready(function() {
    TweetTACharCount()
    LoadMoreTweets()
    Search_form()
    Ajaxfnc('/api/tweet/','GET',data={})
    CreateTweetAPIRest()
    PrvImage_Profile()
    // UserDetailView()
    // var user_name_tag = $('#LinkBlueColor')

    // $('#FollowBtn').click(function (e) {
    //     // var $this_ = $(this)
    //     // e.preventDefault()
    //     // alert($this_.attr('href'))
    //     Ajaxfnc('/accounts/profile/follow','POST',data={})
    // })



});

