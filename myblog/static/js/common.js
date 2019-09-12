var mybaseurl = "http://127.0.0.1:8000/"

function makeHeader(blog_username, username){
    //blog_username 当前访问的博客的作者
    //username   登陆的用户

    //博客作者-用户信息url
    var user_info_url = '/' + blog_username + '/' + 'info'
    //登陆用户发博客url
    if (username){
        var topic_release_url = '/release/release/' + username
        var photo_url = '/photo/' + username
    }else{
        //没有登陆状态直接去登陆
        var photo_url = '/users/login'
        var topic_release_url = '/users/login'
    }

    //访问博主的博客文章
    var user_topics_url = '/topics/'
    // var user_topics_url = '/topics/' + blog_username + '/'

    var header_body = ''
    header_body += '<header id="header">';
    header_body += '<div class="menu">';
    header_body += ' <nav class="nav" id="topnav"> ';
    header_body += '<h1 class="logo"><a href="/index/"> ' + blog_username + '的博客</a></h1>';
    header_body += '<li><a href="/index/">网站首页</a></li>';
    header_body += '<li>';
    header_body += '<a href=' + '"' + user_topics_url + '"' + '>文章列表</a>';
    header_body += '</li>';
    header_body += '<li><a href=' + '"' + photo_url + '"' + '>我的相册</a> </li>';
    header_body += '<li><a href=' + '"' + topic_release_url + '"' + '>发表博客</a> </li>';
    header_body += '</nav>';
    header_body += '</div>';
    if (username){
        header_body += '<li><a href= /users/change/' + username + ' id="change_info" target="_blank">编辑</a></li>';
        //header_body += '<li><a href="/" id="login_out" target="_blank">登出</a></li>';
        header_body += '<li><span id="login_out" target="_blank">退出</span></li>';
    }else{
        header_body += '<a href="/users/login" id="login" target="_blank">登陆</a>';
        header_body += '<a href="/users/register" id="register" target="_blank">注册</a>';
    }
    header_body += '</header>';

    return header_body
}

function loginOut(){

    $('#login_out').on('click', function(){

            if(confirm("确定登出吗？")){
                window.localStorage.removeItem('dnblog_token');
                window.localStorage.removeItem('dnblog_user');
                window.location.href= '/index/';
            }
        }
    )

}