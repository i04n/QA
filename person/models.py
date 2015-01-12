from django.db import models
from django import forms

# Create your models here.
class profile(models.Model):
	name = models.CharField(max_length = 150)
	email = models.CharField(max_length = 200)
	password = models.CharField(max_length = 50)
	def validate(self,pas):
		if self.password == pas:
			return True
		else:
			return False

class profileForm(forms.Form):
	name = forms.CharField(max_length = 150)
	email = forms.CharField(max_length = 200)
	password = forms.CharField(max_length = 50,widget = forms.PasswordInput())
	confirm_password = forms.CharField(max_length = 50,widget = forms.PasswordInput())

class question(models.Model):
        topic = models.CharField(max_length = 150)
        content = models.TextField()
        answers = models.TextField()
        added_by = models.CharField(max_length = 200)
        time = models.DateTimeField()
        class Meta:
                ordering = ('-time',)

class questionForm(forms.Form):
        # sample 4 topics to add questions
        TOPICS = (('Movies','Movies'),('Funny','Funny'),('Comics','Comics'),('Love','Love'),)
        topic = forms.ChoiceField(choices=TOPICS,widget=forms.Select,required=False)
        question = forms.CharField(widget = forms.TextInput(attrs={'size':100}))

class answer(models.Model):
        content = models.TextField()
        question_id = models.IntegerField()
        upvotes = models.IntegerField()
        upvoted_by = models.TextField()
        added_by = models.CharField(max_length = 200)
        time = models.DateTimeField()
        class Meta:
                ordering = ('-upvotes','-time',)

class answerForm(forms.Form):
        answer = forms.CharField(widget = forms.Textarea)

class comment(models.Model):
        content = models.TextField()
        ans_id = models.IntegerField()
        #par_id = models.IntegerField()
        added_by = models.CharField(max_length = 200)
        time = models.DateTimeField()
        upvotes = models.IntegerField()
        upvoted_by = models.TextField()
        class Meta:
                ordering = ('-upvotes','-time',)

class notification(models.Model):
        from_id = models.CharField(max_length = 200)
        to_id = models.CharField(max_length = 200)
        notify_id = models.IntegerField()
        # 1 - upvote, 2 - comment, 3 - ans, 4 - comment on self
        ques_id = models.IntegerField()
        time = models.DateTimeField()
        read = models.IntegerField()
        class Meta:
                ordering = ('-time',)
