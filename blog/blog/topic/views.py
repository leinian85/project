import json

from django.http import JsonResponse
from django.shortcuts import render
from tools.login_check import login_check, get_user_by_request
from .models import Topic
from user.models import UserProfile
from message.models import Message

# Create your views here.
@login_check('POST', 'DELETE')
def topics(request, author_id):
    #127.0.0.1:8000/v1/topics/<author_id>?category=[tec|no-tec]
    if request.method == 'GET':
        #获取用户博客数据
        #前端地址 -> http://127.0.0.1:5000/<username>/topics
        #author_id 被访问的博客的博主用户名

        #visitor 访客 【1，登陆了 2，游客（未登录）】
        #author  博主  当前被访问博客的博主
        authors = UserProfile.objects.filter(username=author_id)
        if not authors:
            result = {'code':308, 'error': 'no author'}
            return JsonResponse(result)
        #取出结果中的博主
        author = authors[0]

        #visitor ?
        visitor = get_user_by_request(request)
        visitor_name = None
        if visitor:
            visitor_name = visitor.username

        t_id = request.GET.get('t_id')
        #获取 t_id
        if t_id:
            #当前是否为 博主访问自己的博客
            is_self = False
            # 根据t_id进行查询
            t_id = int(t_id)
            if author_id == visitor_name:
                is_self = True
                #博主访问自己的博客
                try:
                    author_topic = Topic.objects.get(id=t_id)
                except Exception as e:
                    result = {'code':312, 'error': 'no topic'}
                    return JsonResponse(result)
            else:
                #访客访问博主的博客
                try:
                    author_topic = Topic.objects.get(id=t_id, limit='public')
                except Exception as e:
                    result = {'code':313, 'error': 'no topic !'}
                    return JsonResponse(result)

            # 拼前端返回值
            res = make_topic_res(author, author_topic, is_self)
            return JsonResponse(res)

        else:
            # 127.0.0.1:8000/v1/topics/<author_id>?category=[tec|no-tec]
            category = request.GET.get('category')
            if category in ['tec', 'no-tec']:
                # /v1/topics/<author_id>?category=[tec|no-tec]
                if author_id == visitor_name:
                    #博主访问自己的博客
                    topics = Topic.objects.filter(author_id=author_id, category=category)
                else:
                    #访客来了
                    topics = Topic.objects.filter(author_id=author_id, category=category, limit='public')

            else:
                # /v1/topics/<author_id> 用户全量数据
                if author_id == visitor_name:
                    #博主访问自己的博客 获取全部博客数据
                    topics = Topic.objects.filter(author_id=author_id)
                else:
                    #访客来了, 非博主本人  只获取public数据
                    topics = Topic.objects.filter(author_id=author_id, limit='public')

            #返回
            res = make_topics_res(author,topics)
            return JsonResponse(res)

    elif request.method == 'POST':
        #创建用户博客数据
        json_str = request.body
        if not json_str:
            result = {'code':301, 'error': 'Please give me json'}
            return JsonResponse(result)
        json_obj = json.loads(json_str)
        title  = json_obj.get('title')

        #xss注入
        import html
        #进行转义
        title = html.escape(title)

        if not title:
            result = {'code':302, 'error': 'Please give me title'}
            return JsonResponse(result)
        content = json_obj.get('content')
        if not content:
            result = {'code': 303, 'error': 'Please give me content'}
            return JsonResponse(result)
        #获取纯文本内容 - 用于切割文章简介
        content_text = json_obj.get('content_text')
        if not content_text:
            result = {'code': 304, 'error': 'Please give me content_text'}
            return JsonResponse(result)
        #切割简介
        introduce = content_text[:30]
        limit = json_obj.get('limit')
        if limit not in ['public', 'private']:
            result = {'code': 305, 'error': 'Your limit is wrong'}
            return JsonResponse(result)
        category = json_obj.get('category')
        #Todo 检查 same to 'limit'

        #创建数据
        Topic.objects.create(title=title,category=category,limit=limit,content=content,introduce=introduce,author=request.user)
        result = {'code':200, 'username':request.user.username}
        return JsonResponse(result)

    elif request.method == 'DELETE':
        #博主删除自己的文章
        #/v1/topics/<author_id>
        # token存储的用户
        author = request.user
        token_author_id = author.username
        #url中传过来的author_id 必须与token中的用户名相等
        if author_id != token_author_id:
            result = {'code':309, 'error': 'You can not do it '}
            return JsonResponse(result)

        topic_id = request.GET.get('topic_id')

        try:
            topic = Topic.objects.get(id=topic_id)
        except:
            result = {'code':310, 'error': 'You can not do it !'}
            return JsonResponse(result)

         #删除
        if topic.author.username != author_id:
            result = {'code': 311, 'error': 'You can not do it !! '}
            return JsonResponse(result)

        topic.delete()
        res = {'code':200}
        return JsonResponse(res)



















    return JsonResponse({'code':200, 'error': 'this is test'})


def make_topics_res(author, topics):

    res = {'code':200 , 'data':{}}
    data = {}
    data['nickname'] = author.nickname
    topics_list = []
    for topic in topics:
        d = {}
        d['id'] = topic.id
        d['title'] = topic.title
        d['category'] = topic.category
        d['introduce'] = topic.introduce
        d['author'] = author.nickname
        d['created_time'] = topic.created_time.strftime('%Y-%m-%d %H:%M:%S')
        topics_list.append(d)

    data['topics'] = topics_list
    res['data'] = data
    return res


def make_topic_res(author, author_topic, is_self):
    '''
    拼接详情页 返回的数据
    :param author:
    :param author_topic:
    :param is_self:
    :return:
    '''
    if is_self:
        #博主访问自己博客
        #下一个文章： 取出ID大于当前博客ID的第一个 且 author为
        #当前作者的
        next_topic = Topic.objects.filter(id__gt=author_topic.id, author=author).first()
        #上一篇文章: 取出ID小于当前博客ID的最后一个 且author 为当前作者
        last_topic = Topic.objects.filter(id__lt=author_topic.id, author=author).last()
    else:
        #访客访问博主的
        #下一篇 考虑limit = public
        next_topic = Topic.objects.filter(id__gt=author_topic.id, author=author, limit='public').first()
        #上一篇 同上
        last_topic = Topic.objects.filter(id__lt=author_topic.id, author=author, limit='public').last()
    #判断下一个是否存在
    if next_topic:
        next_id = next_topic.id
        next_title = next_topic.title
    else:
        next_id = None
        next_title = None

    if last_topic:
        last_id = last_topic.id
        last_title = last_topic.title
    else:
        last_id = None
        last_title = None


    all_messages = Message.objects.filter(topic=author_topic).order_by('-created_time')
    #所有的留言
    msg_list = []
    #留言&回复的映射字典
    reply_dict = {}
    msg_count = 0
    for msg in all_messages:
        msg_count += 1
        if msg.parent_message == 0:
            #当前是留言
            msg_list.append({'id':msg.id, 'content':msg.content, 'publisher': msg.publisher.nickname, 'publisher_avatar': str(msg.publisher.avatar), 'created_time': msg.created_time.strftime('%Y-%m-%d'), 'reply':[]})
        else:
            #当前是回复
            reply_dict.setdefault(msg.parent_message, [])
            reply_dict[msg.parent_message].append({'msg_id':msg.id,'content':msg.content,'publisher':msg.publisher.nickname, 'publisher_avatar':str(msg.publisher.avatar), 'created_time': msg.created_time.strftime('%Y-%m-%d')})

    #合并  msg_list 和 reply_dict
    for _msg in msg_list:
        if _msg['id'] in reply_dict:
            _msg['reply'] = reply_dict[_msg['id']]

    res = {'code':200, 'data':{}}
    res['data']['nickname'] = author.nickname
    res['data']['title'] = author_topic.title
    res['data']['category'] = author_topic.category
    res['data']['created_time'] = author_topic.created_time.strftime('%Y-%m-%d %H:%M:%S')
    res['data']['content'] = author_topic.content
    res['data']['introduce'] = author_topic.introduce
    res['data']['author'] = author.nickname
    res['data']['next_id'] = next_id
    res['data']['next_title'] = next_title
    res['data']['last_id'] = last_id
    res['data']['last_title'] = last_title
    #messages 暂时为假数据
    res['data']['messages'] = msg_list
    res['data']['messages_count'] = msg_count
    return res





















































