from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Topic, Entry
from .forms import TopicForm, EntryForm, DeleteForm

def index(request):
   """The home page for Learning Log"""
   return render(request, 'learning_logs/index.html')

def check_topic_owner(request, topic):
   if topic.owner != request.user:
      raise Http404

@login_required
def topics(request):
   """Show all topics"""
   topics = Topic.objects.filter(owner=request.user).order_by('date_added')
   context = {'topics':topics}
   return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
   """Show a single topic and all its entries."""
   topic = get_object_or_404(Topic, id=topic_id)
   # Make sure the topic belongs to the current user.
   check_topic_owner(request, topic)
   entries = topic.entry_set.order_by('-date_added')
   context = {'topic':topic, 'entries':entries}
   return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
   """Add a new topic."""
   if request.method != 'POST':
      # No data submitted; create a blank form.
      form = TopicForm()
   else:
      # POST data submitted; process data.
      form = TopicForm(request.POST)
      if form.is_valid():
         new_topic = form.save(commit=False)
         new_topic.owner = request.user
         new_topic.save()
         return HttpResponseRedirect(reverse('topics'))

   context = {'form': form}
   return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
   """Add a new entry for a particular topic."""
   topic = get_object_or_404(Topic, id=topic_id)

   if request.method != 'POST':
      # No data submitted; create a blank form.
      form = EntryForm()
   else:
      # POST data submitted; process data.
      form = EntryForm(data=request.POST)
      if form.is_valid():
         new_entry = form.save(commit=False)
         new_entry.topic = topic
         new_entry.save()
         return HttpResponseRedirect(reverse('topic', args=[topic_id]))

   context = {'topic': topic, 'form': form}
   return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
   """Edit an existing entry."""
   entry = get_object_or_404(Entry, id=entry_id)
   topic = entry.topic
   check_topic_owner(request, topic)

   if request.method != 'POST':
      # Initial request; pre-fill form with the current entry.
      form = EntryForm(instance=entry)
   else:
      # POST data submitted; process data.
      form = EntryForm(instance=entry, data=request.POST)
      if form.is_valid():
         form.save()
         return HttpResponseRedirect(reverse('topic', args=[topic.id]))

   context = {'entry': entry, 'topic': topic, 'form': form}
   return render(request, 'learning_logs/edit_entry.html', context)

@login_required
def delete_entry(request, entry_id):

   entry = get_object_or_404(Entry, id=entry_id)
   topic = entry.topic
   check_topic_owner(request, topic)

   if request.method == 'POST':
      form = DeleteForm(request.POST, instance=entry)
      if form.is_valid(): #checks CSRF
         entry.delete()
         return HttpResponseRedirect(reverse('topic', args=[topic.id])) #redirect after deleting

   else:
      form = DeleteForm(instance=entry)

   context = {'entry': entry, 'topic': topic, 'form': form}
   return render(request, 'learning_logs/delete_entry.html', context)

@login_required
def delete_topic(request, topic_id):

   topic = get_object_or_404(Topic, id=topic_id)
   check_topic_owner(request, topic)

   if request.method == 'POST':
      form = DeleteForm(request.POST, instance=topic)
      if form.is_valid(): #checks CSRF
         topic.delete()
         return HttpResponseRedirect(reverse('topics')) #redirect after deleting

   else:
      form = DeleteForm(instance=topic)

   context = {'topic': topic, 'form':form}
   return render(request, 'learning_logs/delete_topic.html', context)


@login_required
def account(request):
   topic = Topic.objects.filter(owner=request.user)
   entry = Entry.objects.filter(topic__owner=request.user)

   context = {'topic':topic.count(),
   'entry':entry.count()}
   return render(request, 'learning_logs/account.html', context)

