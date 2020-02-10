from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, reverse, get_object_or_404
from django.views.generic import View
from todo.models import Todo
from todo.forms import TodoForm

class AllTodoView(View):
    model = Todo
    template_name = 'todo/all_todo.html'
    context_object_name = 'todos'

    def query_set(self):
        query = self.model.objects.all()
        return query

    def get(self, request):
        todos = self.query_set()
        return render(request, template_name=self.template_name,
                      context={self.context_object_name: todos})

    def post(self, request):
        datas = request.POST
        if "add" in datas:
            return HttpResponseRedirect(reverse(viewname='add'))
        try:
            todo =  get_object_or_404(Todo, pk=request.POST['id'])
        except Exception:
            return Http404()

        if "status" in datas:
            todo.status = not todo.status
            todo.save()
        elif "view" in datas:
            return HttpResponseRedirect(reverse(viewname='todo_detail', kwargs={'pk': todo.pk}))
        elif "delete" in datas:
            todo.delete()
        else:
            return HttpResponseRedirect(reverse(viewname='home_page'))
        return HttpResponseRedirect(reverse(viewname='home_page'))


class TodoDetail(View):
    model = Todo
    template_name = 'todo/todo_detail.html'
    context_object_name = 'todo'

    def query_set(self, pk):
        query = get_object_or_404(self.model, pk=pk)
        return query

    def get(self, request, pk):
        todo = self.query_set(pk=pk)
        return render(request, template_name=self.template_name,
                      context={self.context_object_name: todo})

    def post(self, request, pk):
        todo = get_object_or_404(Todo, pk=pk)
        datas = request.POST
        if "status" in datas:
            todo.status = not todo.status
            todo.save()
        elif "edit" in datas:
            return HttpResponseRedirect(reverse(viewname='edit', kwargs={'pk': todo.pk}))
        elif "delete" in datas:
            todo.delete()
            return HttpResponseRedirect(reverse(viewname="home_page"))
        else:
            return HttpResponseRedirect(reverse(viewname="todo_detail", kwargs={'pk': pk}))

        return HttpResponseRedirect(reverse(viewname="todo_detail", kwargs={'pk': pk}))


class AddNewView(View):
    model = Todo
    template_name = 'todo/todo_form.html'
    title = 'Add New'
    form = TodoForm()

    def get(self, request):
        return render(request, template_name=self.template_name,
                      context={'form': self.form, 'title': self.title})

    def post(self, request):
        form = TodoForm(data=request.POST)
        if form.is_valid():
            form.save()

        return HttpResponseRedirect(reverse(viewname='add'))


class EditTodoView(View):
    model = Todo
    template_name = 'todo/todo_form.html'

    def query_set(self, pk):
        query = get_object_or_404(self.model, pk=pk)
        return query

    def get(self, request, pk):
        todo = self.query_set(pk=pk)
        form = TodoForm(instance=todo)
        return render(request, template_name=self.template_name,
                      context={'form': form, 'title': todo.title})

    def post(self, request, pk):
        form = TodoForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            status = form.cleaned_data['status']
            todo = self.query_set(pk=pk)
            todo.title = title
            todo.content = content
            todo.status = status
            todo.save()
            return HttpResponseRedirect(reverse(viewname='todo_detail', kwargs={'pk': pk}))

        return HttpResponseRedirect(reverse(viewname='edit', kwargs={'pk': pk}))
