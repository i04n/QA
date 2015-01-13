from django.shortcuts import render,render_to_response,get_object_or_404
from django.template import loader, Context, RequestContext
from django.http import HttpResponse,HttpResponseRedirect
from person.models import *
from datetime import datetime
from django.core import serializers
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

def intialize_session(request):
    request.session["user"] = ""
    request.session["login"] = False
    request.session["id"] = None

def register(request):

    # would be used for logoff
    intialize_session(request)

    # creating user
    if request.POST and "dd" in request.POST:
        pp = profileForm(request.POST)
        if pp.is_valid():
            if request.POST["password"]==request.POST["confirm_password"]:
                name = request.POST["name"]
                email = request.POST["email"]
                password = request.POST["password"]
                register = profile(name = name,email = email,password = password)
                register.save()
                return HttpResponseRedirect('/login/')
            else:
                return HttpResponse("Password not matched")
    elif request.POST and "login" in request.POST:
        # login existing user
        pp = profileForm()
        try:
            pop = get_object_or_404(profile,email = request.POST["email"])
            if pop.password == request.POST["password"]:
                request.session["user"] = pop.name
                request.session["login"] = True
                request.session["id"] = pop.id
                    
                # need a better url for same names, email id would be better
                return HttpResponseRedirect('/profile/'+pop.name.replace(' ','_'))
                
            else:
                return HttpResponse("failure")
        except:
            return HttpResponse("no user")
    else:
        pp = profileForm()
    return render_to_response("register.html",{'form':pp},context_instance = RequestContext(request))

def login(request):
    if request.POST and "login" in request.POST:
        try:
            pop = get_object_or_404(profile,email = request.POST["email"])
            if pop.password == request.POST["password"]:
                request.session["user"] = pop.name
                request.session["login"] = True
                request.session["id"] = pop.id
                return HttpResponseRedirect('/profile/'+pop.name.replace(' ','_'))
            else:
                return HttpResponse("failure")
        except:
            return HttpResponse("no user")
    else:
        intialize_session(request)
    return render_to_response("thanks.html",{},context_instance = RequestContext(request))

def display(request,name):
    
    # better to use email id here (remove afer '@')
    name = name.replace('_',' ')
    
    if request.session["login"] == False or request.session["user"] != name:
        logged_in = False
    else:
        logged_in = True
    if request.POST:
        
        # add a new question
        pp = questionForm(request.POST)
        if pp.is_valid():
            topic = request.POST["topic"]
            content = request.POST["question"]
            answers = ""
            added_by = request.session["id"]
            time = datetime.now()
            ques = question(topic = topic,content = content,answers = answers,added_by = added_by,time = time)
            ques.save()
            pp = questionForm()
    else:
        pp = questionForm()
    qq = question.objects.all()

    # get name from session id for each answer added
    # need to replace name with hyperlink to profle (change in profile.html)
    for item in qq:
        item.user = get_name(item.added_by)
    user = request.session["user"]
    return render_to_response("profile.html",{'ques':qq,'form':pp,'name':name,'logged_in':logged_in,'user':user},context_instance = RequestContext(request))

def answer_it(request,ques,ans=None):
    # ques/1 = Question 1
    # ques/1/2 = 2nd answer to question 1
    
    logged_in = request.session["login"]
    qq = question.objects.filter(id = ques)
    user = request.session["user"]
    if request.POST and "ans" in request.POST:

        # add a new answer
        pans = answerForm(request.POST)
        if pans.is_valid():
            content = request.POST["answer"]
            upvotes = 0
            added_by = request.session["id"]
            upvoted_by = ""
            time = datetime.now()
            question_id = ques
            answ = answer(upvotes = upvotes,content = content,added_by = added_by,time = time,question_id = question_id)
            answ.save()

            # code to add answer to list of existing answers for this question
            qt = question.objects.get(id = ques)
            # to fetch the answer just added, could be a better way.
            an = answer.objects.get(question_id = question_id,added_by = request.session["id"])
            if qt.answers == "":
                qt.answers = str(an.id)
            else:
                qt.answers = qt.answers + "," + str(an.id)
            qt.save()

            # notification 3 = answer added
            create_notification(added_by,qt.added_by,3,ques)

            # blank the form
            pans = answerForm()
    elif request.POST and "upvote" in request.POST:

        # register upvote
        # code required to prevent upvoting your own answer
        pans = answerForm()
        this_ans = answer.objects.get(id = request.POST["ans_id"])
        this_ans.upvotes = this_ans.upvotes + 1
        # adding session id to upvote list
        if this_ans.upvoted_by == "":
            this_ans.upvoted_by = str(request.session["id"])
        else:
            this_ans.upvoted_by = this_ans.upvoted_by + "," + str(request.session["id"])
        this_ans.save()

        # notification 1 = upvoted
        create_notification(request.session["id"],this_ans.added_by,1,ques)
    elif request.POST and "comment" in request.POST:

        # adding comment
        pans = answerForm()
        content = request.POST["com"]
        ans_id = request.POST["ans_id"]
        added_by = request.session["id"]
        time = datetime.now()
        upvotes = 0
        upvoted_by = ""
        this_com = comment(content = content,ans_id = ans_id,added_by = added_by,time = time,upvotes = upvotes,upvoted_by = upvoted_by)
        this_com.save()

        # notifcation 2 = comment
        create_notification(request.session["id"],get_object_or_404(answer,id = ans_id).added_by,2,ques)
    else:
        pans = answerForm()
    # fetch answers
    if ans == None:
        # fetch all answers in case url is of type ques/1/
        answ = answer.objects.filter(question_id = ques)
    else:
        # fetch answer in case url is of type ques/1/2/
        answ = answer.objects.filter(question_id = ques).filter(id = ans)
    comm = comment.objects.all()
    
    # get name for id in comments
    for item in comm:
        item.user = get_name(item.added_by)

    # get name for id in each answer and upvotes in each answer
    for item in answ:
        item.user = get_name(item.added_by)
        item.upv = ""
        if item.upvoted_by != "":
            for dd in item.upvoted_by.split(','):
                pq = get_name(int(dd))
                if item.upv == "":
                    item.upv = pq
                else:
                    item.upv = item.upv + "," + pq
    return render_to_response("answer.html",{'ques':qq,'user':user,'logged_in':logged_in,'ans':pans,'answers':answ,'comm':comm},context_instance = RequestContext(request))


def tester(request):
    response = HttpResponse()
    response['Content-type'] = "text/javascript"
    response.write(serializers.serialize("json",answer.objects.all()))
    return response

def create_notification(from_id,to_id,notify_id,ques_id):
    note = notification(from_id = from_id,to_id = to_id,notify_id = notify_id,ques_id = ques_id,time = datetime.now(),read = 0)
    note.save()

def notifs(request):
    if request.session["login"] == False:
        logged_in = False
    else:
        logged_in = True
    note = notification.objects.filter(to_id=request.session["id"])
    if request.POST:
        note.update(read = 1)
    for item in note:
        item.name = get_object_or_404(profile,id=item.from_id).name
        item.question = get_object_or_404(question,id= item.ques_id).content
        if item.notify_id == 3 or item.notify_id == 4:
            item.ans_id = answer.objects.get(question_id = item.ques_id,added_by = item.from_id).id
        else:
            item.ans_id = answer.objects.get(question_id = item.ques_id,added_by = item.to_id).id
        if item.read == 0:
            item.color = "Red"
        else:
            item.color = "Blue"
    user = request.session["user"]
    return render_to_response("notification.html",{'logged_in':logged_in,'note':note,'user':user},context_instance = RequestContext(request))

def user_view(request,usr):
    usrr = get_object_or_404(profile,id = usr)
    if request.session["login"] == False:
        logged_in = False
    else:
        logged_in = True
    user = request.session["user"]
    return render_to_response("user.html",{'logged_in':logged_in,'usrr':usrr,'user':user},context_instance = RequestContext(request))

def get_name(user_id):
    # return name for id
    pro = get_object_or_404(profile,id = user_id)
    return pro.name

def view_content(request):
    current_user = request.session["id"]
    answ = answer.objects.filter(added_by = current_user)
    for item in answ:
        qq = get_object_or_404(question,id = item.question_id)
        item.ques = qq.content
    user = request.session["user"]
    return render_to_response("content.html",{'answ':answ,'user':user},context_instance = RequestContext(request))

def logout(request):
    if request.POST and "login" in request.POST:
        try:
            pop = get_object_or_404(profile,email = request.POST["email"])
            if pop.password == request.POST["password"]:
                request.session["user"] = pop.name
                request.session["login"] = True
                request.session["id"] = pop.id
                return HttpResponseRedirect('/profile/'+pop.name.replace(' ','_'))
            else:
                return HttpResponse("failure")
        except:
            return HttpResponse("no user")
    else:
        intialize_session(request)
    return render_to_response("logout.html",{},context_instance = RequestContext(request))
