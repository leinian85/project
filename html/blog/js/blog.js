// login.html
// 针对log页面定义一个对象
var log = {
    startdt: "2019-8-5",
    enddt: "2019-9-5",
    updatedt: "2019-8-5",
    anchor: "leinian"
}

// 由对象派生业务逻辑
log.submit = {
    check: function (v) {
        return v == "" ? true : false;
    },
    autohide: function (jq) {
        var t = setTimeout(function () {
            jq.hide();
        }, 2000);
    }
}

// 校验用户名和密码不能为空
function checkvalue() {
    var $username = $("#username");
    var $password = $("#password");

    var $errorname = $(".error:eq(0)");
    var $errorpwd = $(".error:eq(1)");

    if (log.submit.check($username.val())) {
        $errorname.show();
        // 2秒之后自动隐藏
        log.submit.autohide($errorname);
        return false;
    }

    if (log.submit.check($password.val())) {
        $errorpwd.show();
        // 2秒之后自动隐藏
        log.submit.autohide($errorpwd);
        return false;
    }
}

$(function () {
    var $form = $("form");
    var $btn = $(".btn>input");
})

// list.html
var lst = {
    template: function (t, u, p1, p2) {
        var HTML = '';
        HTML += '<div class="item">';
        HTML += '  <div class="title">';
        HTML += '    <h3>';
        HTML += t;
        HTML += '    </h3>';
        HTML += '  </div>';
        HTML += '  <div class="con">';
        HTML += '    <div class="cleft">';
        HTML += '      <img src=';
        HTML += u;
        HTML += '      alt="">';
        HTML += '    </div>';
        HTML += '    <div class="cright">';
        HTML += '      <p class="ptop">';
        HTML += p1;
        HTML += '      </p>';
        HTML += '      <p class="pbottom">';
        HTML += p2;
        HTML += '      </p>';
        HTML += '    </div>';
        HTML += '  </div>';
        HTML += '</div>';

        return HTML;
    }
}

var _list = [{
        title: "Python语言在人工智能(AI)中的优势",
        url: "imgs/toppic01.jpg",
        p1: "本文探讨了python语言在AI领域的优势与运用,谁谁成为AI和大数据时代的第一开发语言?这本已是一个不需要争论的问题,如果说三年前,Matlab、Acala、R、Java...",
        p2: "皮皮虾 学无止境 2018-5-13 34567已阅读 9999"
    },
    {
        title: "Python中打开TXT文件报错",
        url: "imgs/toppic02.jpg",
        p1: "Python中打开TXT文件报错Python中打开TXT文件报错Python中打开TXT文件报错Python中打开TXT文件报错",
        p2: "齐天大圣 学无止境 2018-5-13 34567已阅读 9999"
    },
    {
        title: "Python语言在人工智能(AI)中的优势",
        url: "imgs/toppic01.jpg",
        p1: "本文探讨了python语言在AI领域的优势与运用,谁谁成为AI和大数据时代的第一开发语言?这本已是一个不需要争论的问题,如果说三年前,Matlab、Acala、R、Java...",
        p2: "皮皮虾 学无止境 2018-5-13 34567已阅读 9999"
    },
    {
        title: "Python语言在人工智能(AI)中的优势",
        url: "imgs/toppic01.jpg",
        p1: "本文探讨了python语言在AI领域的优势与运用,谁谁成为AI和大数据时代的第一开发语言?这本已是一个不需要争论的问题,如果说三年前,Matlab、Acala、R、Java...",
        p2: "皮皮虾 学无止境 2018-5-13 34567已阅读 9999"
    },
    {
        title: "Python语言在人工智能(AI)中的优势",
        url: "imgs/toppic01.jpg",
        p1: "本文探讨了python语言在AI领域的优势与运用,谁谁成为AI和大数据时代的第一开发语言?这本已是一个不需要争论的问题,如果说三年前,Matlab、Acala、R、Java...",
        p2: "皮皮虾 学无止境 2018-5-13 34567已阅读 9999"
    }
];


$("#list>.top>.tright>p").text("长夜漫漫,无心睡眠");
$("#mypic>.top>.tright>p").text("好东西要与人分享");

for (i = 0; i < _list.length; i++) {
    var _HTML = lst.template(_list[i].title, _list[i].url, _list[i].p1, _list[i].p2);
    $("#list>.body>.list").append(_HTML);
}

var pic = {
    template:function(title,url,tip){
        var HTML = '';
        HTML += '<div class="list">';
        HTML += '  <div class="img">';
        HTML += '    <img src='+url+' alt="">';
        HTML += '    <div class="tip">喜欢 | '+tip+'</div>';
        HTML += '  </div>';
        HTML += '  <div class="title">';
        HTML += '    <p>'+title+'</p>';
        HTML += '  </div>';
        HTML += '</div>';
                    
        return HTML;
    }
};
var arr_pic = [{
    title: "本文探讨了python语言在AI领域的优势与运用",
    url: "imgs/toppic02.jpg",
    tip: 190
}, {
    title: "本文探讨了python语言在AI领域的优势与运用",
    url: "imgs/banner02.jpg",
    tip: 191
}, {
    title: "本文探讨了python语言在AI领域的优势与运用",
    url: "imgs/toppic01.jpg",
    tip: 192
}, {
    title: "本文探讨了python语言在AI领域的优势与运用",
    url: "imgs/banner01.jpg",
    tip: 193
}, {
    title: "本文探讨了python语言在AI领域的优势与运用",
    url: "imgs/commentPhoto.jpg",
    tip: 194
}];

for(i=0;i<arr_pic.length;i++){
    var _html = pic.template(arr_pic[i].title,arr_pic[i].url,arr_pic[i].tip);
    $("#mypic>.body").append(_html);
}