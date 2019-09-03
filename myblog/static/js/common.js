function makeHeader(blog_username, username){
    //blog_username 当前访问的博客的作者
    //username   登陆的用户

    //博客作者-用户信息url
    var user_info_url = '/' + blog_username + '/' + 'info'
    //登陆用户发博客url
    if (username){
        var topic_release_url = '/' + username + '/' + 'topic/release'
    }else{
        //没有登陆状态直接去登陆
        var topic_release_url = '/login'
    }

    //访问博主的博客文章
    var user_topics_url = '/' + blog_username + '/' + 'topics'

    var header_body = ''
    header_body += '<header id="header">';
    header_body += '<div class="menu">';
    header_body += ' <nav class="nav" id="topnav"> ';
    header_body += '<h1 class="logo"><a href="/index"> ' + blog_username + '的博客</a></h1>';
    header_body += '<li><a href="/index">网站首页</a></li>';
    header_body += '<li>';
    header_body += '<a href=' + '"' + user_topics_url + '"' + '>文章列表</a>';
    header_body += '<ul class="sub-nav">';
    header_body += '<li><a href=' + '"' + user_topics_url + '?category=tec"' + '>技术</a></li>';
    header_body += '<li><a href=' + '"' + user_topics_url + '?category=no-tec"' + '>非技术</a></li>';
    header_body += '</ul>';
    header_body += '</li>';
    header_body += '<li><a href="photo.html">我的相册</a> </li>';
    header_body += '<li><a href=' + '"' + user_info_url + '"' + '>关于我</a> </li>';
    header_body += '<li><a href=' + '"' + topic_release_url + '"' + '>发表博客</a> </li>';
    header_body += '</nav>';
    header_body += '</div>';
    if (username){
        header_body += '<li><a href= /' + username + '/change_info id="change_info" target="_blank">编辑</a></li>';
        //header_body += '<li><a href="/" id="login_out" target="_blank">登出</a></li>';
        header_body += '<li><span id="login_out" target="_blank">登出</span></li>';
    }else{
        header_body += '<a href="/login" id="login" target="_blank">登陆</a>';
        header_body += '<a href="register.html" id="register" target="_blank">注册</a>';
    }
    header_body += '</header>';

    return header_body
}