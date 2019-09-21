resmsg = {
    "200": "",

    # user
    "301": "用户名不能为空",
    "302": "密码不能为空",
    "303": "2次输入的密码不一致",
    "304": "邮箱不能为空",
    "305": "用户已存在",

    "311": "用户名和密码不能为空",
    "312": "用户名或密码错误",

    "321": "no avatar",
    "322": "昵称不能为空",
    "323": "昵称不能为空",


    "370": "无效的请求",
    "371": "无效的请求",


    "390": "系统繁忙",
    "391": "系统繁忙",
    "392": "系统繁忙",
    "393": "系统繁忙",
    "394": "系统繁忙",
    "395": "系统繁忙",
    "396": "系统繁忙",
    "397": "系统繁忙",
    "398": "系统繁忙",
    "399": "系统繁忙",

    # index
    "401": "用户不存在",
    "470": "无效的请求",
    "499": "系统繁忙",


    # topic
    "515": "数据错误",
    "516": "数据错误",
    "517": "数据错误",
    "518": "数据错误",
    "570": "无效的请求",
    "598": "系统繁忙",
    "599": "系统繁忙",

    # token
    "601": "no token",
}

key = "myname"

def error_msg(code,msg=None):
    error = msg if msg else resmsg.get(code)
    return {"code":code,"error":str(code)+error}
