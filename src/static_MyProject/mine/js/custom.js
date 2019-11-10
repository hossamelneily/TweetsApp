var NextUrl = ""
var users_list_global
var Reply_to_user_data

function getParameterByName(name, url) {
    if (!url) url = window.location.href;
    name = name.replace(/[\[\]]/g, '\\$&');
    var regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)'),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, ' '));
}

function stopPropagation(){
    $('a').click(function(event){      // any anchor inside the preview-box
        var $this_ = $(this)
        if($this_.closest(".preview-box").length){
            event.stopPropagation();
            // $this_.find($('.dropdown-menu')).toggle();
            // $('.dropdown-menu').toggle();
        }
    });


     $("div.opts > button.dropdown-toggle , .drop-div a").click(function(e){
       var $this_ = $(this)
        e.stopPropagation();

         // console.log( $this_.next())

        $this_.next().toggle();
    });

     // "<div class=\"dropdown float-right opts\">" +
     //        "<button   style=\"color: grey\" class=\"btn dropdown-toggle\" type=\"button\"  id=\"dropdownMenu\" role=\"button\" data-toggle=\"dropdown\" aria-haspopup=\"true\" aria-expanded=\"false\" >" +
     //        "</button>" +
     //        "<div  class=\"dropdown-menu dropdown-menu-right drop-div\" aria-labelledby=\"dropdownMenu\">" +
     //        "<a style='color: #E0245E' class=\"dropdown-item\" href=\"\">" +
     //        "<i class=\"fas fa-trash-alt\"></i>  Delete</a></div></div>"


}

function CreateObj(name,profile_url) {

     this.username = name;
     this.profile_url = profile_url;

 }

// function profileViewClickEventListner(elems) {
//       Array.from(elems).forEach( v => v.addEventListener('click', function(e) {
//            var $this_ = $(this)
//            var url = $this_.attr('href')
//           var sent_url = '/api/accounts/profile/'+ url.match(/[\w.@+-]+/g)[2] +'/'
//           alert(sent_url)
//           Ajaxfnc(sent_url,'GET',{})
//       }));
//  }
 function TweetClickEventListner(elems) {
      Array.from(elems).forEach( v => v.addEventListener('click', function(e) {
           var $this_ = $(this)
           var url = $this_.data('url')
           window.location.href=url
      }));
 }
 function TweetReplyClickEventListner(elems) {

    Array.from(elems).forEach( v => v.addEventListener('click', function(e) {
        e.preventDefault()
        var img = empty_img
        var Login_user_image = empty_img
        var $this_ = $(this)
        var data = $this_.data('parent')

        if(data.parent){
            data=data.parent
        }
        console.log(data)
        Reply_to_user_data = data
        if(data.user.profile.image){
            img = data.user.profile.image
        }

        var TweetImageHtml = "<a class=\"pull-left profile-view\" href='"+data.user.profile.profile_url+"'> <img class=\"media-object rounded-circle d-flex align-self-start mr-3 img-fluid\" alt=\"\" style=\"width:60px\" src=" + img +  "></a> "
        var TweetHeadingHtml = "<p class=\"mt-0 media-heading font-weight-bold\"><a class='profile-view' id='LinkBlueColor' href='"+data.user.profile.profile_url+"' >"+data.user.username+"</a><small><i><a id='LinkBlueColor' href=\\\"\\\">  Posted on "+ data.time_since+ "</a></i></small></p>"
        var VerticallineHtml = "<div  class=\"\" style=\"height:65px;border-left: 5px solid #CCD6DD;margin-left: -19px;margin-top: -11px;\"></div>"
        var TextArea = "<textarea id=\"TweetTA\" name=\"content\" placeholder=\"Tweet your reply\" class=\"form-control \" maxlength=\"140\" style='border: none;margin-top: -48px;margin-left: 47px;'></textarea>"


        var RequestUserHtml =
            "<div class=\"ml-n4 media\"><a class=\"pull-left\" href=\" \"> <img class=\"media-object rounded-circle d-flex align-self-start mr-3 \" alt=\"\" style=\"width:60px\" src=" + Login_user_image +  "></a></div>"

        var ModalTweetHtml =

            "<div class=\"ml-n5 media\">" +
            TweetImageHtml+
            "<div class=\"media-body \">" +
            TweetHeadingHtml +
            "<p>"+data.content+"</p>" +

             "</div></div>"+
            VerticallineHtml+"<a style='margin-left: 27px;' id=\"LinkBlueColor\" href=''>Replying to @"+data.user.username+"</a>"+
            "<div class='row'>"+ RequestUserHtml+

            TextArea+"<input type=\"hidden\" name=\"isreply\" value=\"True\">" +
            "<input type=\"hidden\" name=\"parent_id\" value='"+data.id+"'></div>"
//<input type=\"hidden\" name=\"Reply_to_user_timesince\" value='"+data.time_since+"'>

        $('#ReplyModal').modal({})
        $('.modal-body').html(ModalTweetHtml)
        // $('#ReplyModal').on('shown.bs.modal',function () {
        //     $('#TweetTA').focus()
        // })
    }));

}
function TweetLikeClickEventListner(elems) {

    Array.from(elems).forEach( v => v.addEventListener('click', function(e) {
        e.preventDefault()
        var $this_ = $(this)

        $.ajax({
        url:$this_.attr('href'),
        method:'GET',
        data: {},
        success:function (data) {
            console.log(data.parent_object_id)
            var count =  data.likes_count
            var parent_tweet = $('a[href="/api/tweet/'+data.parent_object_id+'/like"]')
            var parent_count_likes
            $this_.find("[id='heart']").toggleClass('fas selected-heart',data.liked)
            if(data.parent_object_id){
                parent_count_likes = data.parent_likes_count
                parent_tweet.find("[id='heart']").toggleClass('fas selected-heart',data.liked && parent_count_likes>0)
            }

            if(data.liked){
                count++;
                $this_.find("[id='likes_count']").text(count)
                if(data.parent_object_id){
                    parent_count_likes++;
                    parent_tweet.find("[id='likes_count']").text(parent_count_likes)
                }
            }else{
                 count--;
                  $this_.find("[id='likes_count']").text(count)
                 if(data.parent_object_id){
                      parent_count_likes--;
                      parent_tweet.find("[id='likes_count']").text(parent_count_likes)
                  }
            }
            console.log(count)
            // console.log($('a[href="/api/tweet/'+data.parent_object_id+'/like"]').html())
             // Array.from(elems).filter(a => a.find() === '/api/tweet/'+data.parent_object_id+'/like' )
        },
        error:function (error) {

        }
    })
    }));

}
function GetExistingUsers(url,method,data) {
    var users_list =[]
    $.ajax({
        url:url,
        method:method,
        // async: false,
        data: data,
        success:function (data) {
            $.each(data,function (key,value) {
                users_list.push(new CreateObj( value.username,value.profile.profile_url))
            })
            if(window.location.pathname === '/'){
                 Ajaxfnc('/api/tweet/','GET',data={})
            }
            profileViewdetails()
            SingleDetailView()
            HashtagViewdetails()
            Search_form()

        },
        error:function (error) {

        }
    })
     users_list_global = users_list

}
function PutDataOnMedia(data,IdMedia,prepend = false,single_detail_view=false){
    var img = empty_img
    var data_content
    var parentHtml_Trigger = false
    var parentHtml = ''
    var style_retweet_icon_trigger = false
    var style_retweet_icon = ''
    var class_like_icon
    var retweeted  = false
    var likes_count
    var child_data = data
    var ReplyHtml = ''
    var ReplyHtml_trigger = false
    var single_detail_view_html =''



    if(data.retweeted){
        retweeted = true
    }










     if(data.parent && !data.Reply){
      style_retweet_icon_trigger = true
      parentHtml_Trigger = true
      likes_count = data.likes
      data = data.parent


    }else if(data.parent && data.Reply){

        ReplyHtml_trigger = true
        style_retweet_icon_trigger = false
         parentHtml_Trigger = false
    }else{

        likes_count = data.likes
        parentHtml_Trigger = false
        if(retweeted){
            style_retweet_icon_trigger = true
        }
    }













    if(likes_count){
            class_like_icon = "fas selected-heart"
        }else{
            class_like_icon =''
    }
    if(data.user.profile.image){
        img = data.user.profile.image
    }










    if(data.content){

        data_content=data.content.replace(/(^|\s)#([\w\d-]+)/g,"$1<a id='LinkBlueColor' href='/tags/$2/'>#$2</a>")
        $.each((data.content.match(/(^|\s)@([\w\d-]+)/g)),function (key,value) {
            // console.log(Array.from(users_list_global))
            var iterate_var = users_list_global.filter(user => user.username == value.trim().substr(1))
                    if(value && iterate_var.length && iterate_var){
                        data_content=data_content.replace(/(^|\s)@([\w\d-]+)/g,"$1<a id='LinkBlueColor' href='"+iterate_var[0].profile_url+"'>@$2</a>")
                    }


        })


    }

    if(parentHtml_Trigger){
        parentHtml = "<span class='ml-4'><small><a style='color:grey' class='addons' href=''><i class=\"fas fa-retweet\"></i>"+child_data.user.username +" Retweeted on "+child_data.time_since + "</a></small></span>"
    }
    if(style_retweet_icon_trigger){
        style_retweet_icon = "style='color:#17BF63;pointer-events:none;cursor: default'"
    }
    if(ReplyHtml_trigger){
        ReplyHtml="</br><span id=\"LinkgreyColor\" ><small><i  class=\"far fa-comment-dots\"></i>Replying to <a id=\"LinkBlueColor\" href='"+data.parent.user.profile.profile_url+"'> @"+data.parent.user.username +" </a></small></span>"
    }


    if(single_detail_view == child_data.id){   // will not used === beacsue triple equal test bot values and type

        single_detail_view_html = "media-focus"
        setTimeout(function () {
            $('.media-focus').css("background-color",'#fff')
        },3000)
        
    }

    var TweetDropDownMenu =

        "<div class=\"dropdown float-right opts\">" +
        "<button   style=\"color: grey\" class=\"btn dropdown-toggle\" type=\"button\"  id=\"dropdownMenu\" role=\"button\" data-toggle=\"dropdown\" aria-haspopup=\"true\" aria-expanded=\"false\" >" +
        "</button>" +
        "<div  class=\"dropdown-menu dropdown-menu-right drop-div\" aria-labelledby=\"dropdownMenu\">" +
        "<a style='color: #E0245E' class=\"dropdown-item\" href=\"www.google.com\">" +
        "<i class=\"fas fa-trash-alt\"></i>  Delete</a></div></div>"

    var TweetImageHtml = "<a class=\"pull-left profile-view\" href='"+data.user.profile.profile_url+"'> <img class=\"media-object rounded-circle d-flex align-self-start mr-3 img-fluid\" alt=\"\" style=\"width:60px\" src=" + img +  "></a> "
    var TweetHeadingHtml = "<p class=\"mt-0 media-heading font-weight-bold\"><a id='LinkBlueColor' class=\"profile-view\" href='"+data.user.profile.profile_url+"' >"+data.user.username+"</a><small><i><a id='LinkBlueColor' href=\\\"\\\">  Posted on "+ data.time_since+ "</a></i></small>"+ReplyHtml+"</p>"


    var TweetLikeHtml = "<a   href='"+child_data.Tweet_url_API+"/like' class=\"TweetLike mr-5 \" ><i id='heart'  class=\"far fa-heart border-heart fa-lg" +class_like_icon +"\" title=\"Like\"></i> <span style='color:#E0245E' id='likes_count' data-count=\"8,888,888\">"+likes_count+"</span> </a>"
    var TweetRetweetHtml = "<a id='LinkgreyColor' "+ style_retweet_icon + " class='mr-5' href='"+child_data.Tweet_url+"retweet'><i id='retweet-icon'  class=\"fas fa-retweet fa-lg\" title=\"Retweet\"></i></a>"
    var TweetReplyHtml =  "<a id='LinkgreyColor'  class='TweetReply mr-5'  data-parent='"+JSON.stringify(data)+"'  href='#'><i id='reply-icon'  class=\"far fa-comment-dots fa-lg\" title=\"Reply\"></i></a>"



    TweetHtml=


        "<div data-apiurl='"+child_data.Tweet_url_API+"' data-url='"+child_data.Tweet_url+"' class=\"preview-box "+single_detail_view_html+"\">"+
        TweetDropDownMenu +
        parentHtml +
        "<li class=\"media\">" +
        TweetImageHtml+

        "<div class=\"media-body \">" +
        TweetHeadingHtml +

        "<p>"+data_content+"</p>" +
         "<div class='text-center'>"+TweetLikeHtml+TweetRetweetHtml+TweetReplyHtml+"</div>"+
         "</div></li></div>" +
         "<br>"

    if(prepend){
                IdMedia.prepend(TweetHtml)
            }else{
            IdMedia.append(TweetHtml)
        }


}


function FetchTweets(data ,single_detail_view=false ){
var IdMedia = $("#IdMedia")
            if (data) {
                $.each(data, function (key, value) {
                        // console.log(value)
                        PutDataOnMedia(value,IdMedia,false,single_detail_view)

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
            async: false,
            data: data,
            success: function (data) {
                // console.log(data)
                if(url != '/api/tweet/create/'  )   // List all tweets case
                {

                    NextUrl = data.next
                    if (!NextUrl) {
                        $('.JS-LoadMoreTweets').css('display', 'none')
                    }


                    if ('/api/tweet/search/' == url) {

                        $('#search-form input[name="q"]').val($.trim( $('#search-form input[name="q"]').val()));
                        $('#search-form input[name="q"]').css({'font-weight': 'bolder','font-family': 'Gill Sans Extrabold, sans-serif', 'color': 'rgba(232,24,44,0.82)'})
                        if ($.trim($('div #tweets').find('ul #IdMedia').html())==''){
                          $('#IdMedia').html('<li class="lead">Sorry, no tweets found.</li>')

                        }
                    }

                    if(/(api\/tweet\/)([\d-]+)/g.test(url)) {

                        var selected_tweet = url.match(/[\d-]+/g)[0]
                        // console.log(url.match(/[\d-]+/g)[0])
                        // single_detail_view=true
                        if (data.length > 1) {

                            FetchTweets(data, selected_tweet)
                        } else {
                            PutDataOnMedia(data[0], IdMedia, false, selected_tweet)
                        }
                    }else {
                        FetchTweets(data.results)
                    }
                }else{                                           //create case
                    $('#TweetTA').val('');
                    PutDataOnMedia(data,IdMedia,true)
                }

                TweetLikeClickEventListner($(".TweetLike"))
                TweetReplyClickEventListner($(".TweetReply"))
                TweetClickEventListner($(".preview-box"))
                stopPropagation()

            },
            error: function (error) {
                console.log(error)

            }

        })
    }
}

function CreateTweetAPIRest(){
    var tweetform = $('.tweet_form')
    tweetform.submit(function (e) {
        var this_ = $(this)
        e.preventDefault()
        methode = 'POST'
        url = '/api/tweet/create/'
        data = this_.serialize()
        console.log(data)
        Ajaxfnc(url,methode,data)   //New  tweet is added here
        $('#ReplyModal').modal('hide')
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
    var searchParams = new URLSearchParams(window.location.search)
    if(searchParams.has('q') && searchParams.get('q').trim().length){
        Ajaxfnc('/api/tweet/search/','GET',data={'q':searchParams.get('q').trim()})
    }
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
// function Tweetlike(e) {
//    e.preventDefault()
//     // var $this_ = $(this)
//     alert(e.currentTarget.getAttribute('href'))
// }
//
// function changeColor()
// {
//    var icon = document.getElementById('heart');
//    icon.toggleClass('fas fa-heart')
// }




function SingleDetailView() {
    if(window.location.pathname.match(/(tweet\/)([\d-]+)/g)){
       var tweet_id=window.location.pathname.match(/([\d-]+)/g)
        Ajaxfnc('/api/tweet/'+tweet_id+'/','GET',data={})
    }
}

function profileViewdetails(){
    if(window.location.pathname.match(/(accounts\/profile\/)([\w.@-]+)/g)){
       var user_name=window.location.pathname.match(/([\w.@-]+)/g)[2]
        var sent_url = '/api/accounts/profile/'+ user_name +'/'
        Ajaxfnc(sent_url,'GET',{})
    }
}

function HashtagViewdetails(){
    if(window.location.pathname.match(/(tags\/)([\w\d-]+)/g)){
       var tag_name=window.location.pathname.match(/([\w\d-]+)/g)[1]
        var sent_url = '/api/tags/'+ tag_name +'/'
        Ajaxfnc(sent_url,'GET',{})
    }
}

function closeopenLeftsidebar() {
    $("#close-sidebar").click(function() {
      $(".page-wrapper").removeClass("toggled");
    });
    $("#show-sidebar").click(function() {
      $(".page-wrapper").addClass("toggled");
    });
}

function FollowBtnAPICall() {
    $('.api-follow-btn').click(function (e) {
        e.preventDefault()
        var $this_ =$(this)
        var url=$this_.attr('href')
       $.ajax({
            url: url,
            // async:false,
            method: 'Get',
           success: function (data) {
                console.log(data)
               //update the css of the button
               if(data.follow){
                   $this_.removeClass('followbtn')
                   // $this_.find('$.followtxt').text('')
                   $this_.addClass('unfollowbtn')
                   $this_.html('<span>Following</span>')

               }else{
                    $this_.removeClass('unfollowbtn')
                    $this_.addClass('followbtn')
                    $this_.text('Follow')
               }
               //update the numbers of follower/following
               $(".remove-decoration").find(".following").text(data.following_count+" Following")
               $(".remove-decoration").find(".unfollow").text(data.followers_count+" Followers")
           },
           error:function (error) {}


    })
    })
}


$(document).ready(function() {


    GetExistingUsers('/api/accounts/users/','Get',data={})  // get users list then get all the tweets


    TweetTACharCount()
    LoadMoreTweets()
    // Search_form()

    // stopPropagation()
    CreateTweetAPIRest()
    PrvImage_Profile()
    closeopenLeftsidebar()
    FollowBtnAPICall()





    // alert(x)
    // console.log(window.location.pathname)
    // console.log(window.location)

    // var tweetform = $('#tweet_form')
    // // var tweetform = $('#tweet_form')
    // console.log(Array.from(tweetform))
    // UserDetailView()
    // var user_name_tag = $('#LinkBlueColor')


    //
    // $("button.dropdown-toggle").click(function(e) {
    //     e.stopPropagation();
    //     $('.dropdown-menu').toggle();
    // })


     // var TweetDropDownMenu =
     //        "<div  class=\"dropdown float-right\">" +
     //        "<button  style=\"color: grey\" class=\"btn dropdown-toggle\" type=\"button\"  id=\"dropdownMenu\" role=\"button\" data-toggle=\"dropdown\" aria-haspopup=\"true\" aria-expanded=\"false\" >" +
     //        "</button>" +
     //        "<div class=\"dropdown-menu dropdown-menu-right \" aria-labelledby=\"dropdownMenu\">" +
     //        "<a style='color: #E0245E' class=\"dropdown-item\" href=\"\">" +
     //        "<i class=\"fas fa-trash-alt\"></i>  Delete</a></div></div>"








});

