from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from random import randint

from . import util

import markdown2

def index(request):
    search_string = request.GET.get("search")
    results = []
    title = "" 

    if search_string != None:
        search_string = search_string.strip()
        search_string_temp = search_string.lower()

        temp_list = util.list_entries()
        for entry in temp_list:
            entry_temp = entry.lower()
            if(entry_temp == search_string_temp):
                title = str(entry)
                return HttpResponseRedirect(reverse('entry_page', kwargs={'title':title}))
            if(search_string_temp in entry_temp):
                results.append(entry)

        results_size = len(results)
        if results_size > 0:
            return render(request, "encyclopedia/search.html", {
                "search_string": search_string,
                "entries": results,
                "results_size": results_size
            })
        else:
            return render(request, "encyclopedia/search.html", {
                "search_string": search_string,
                "results_size": results_size
            })
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(),
        })

def entry_page(request, title):
    valid_entry = True
    if title not in util.list_entries():
        valid_entry = False
        return render(request, "encyclopedia/entry.html",{
            "valid_entry": valid_entry,
            "title": title
        })
    else:
        md = markdown2.markdown(util.get_entry(title))
        return render(request, "encyclopedia/entry.html",{
            "valid_entry": valid_entry,
            "title": title,
            "markdown": md
        })

def new_page(request):
    Entry_exists = False
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("markdown_content")
        title = title.strip() 
        title_temp = title.lower()
        for entry in util.list_entries():
            if entry.lower() == title_temp:
                Entry_exists = True
                return render(request, "encyclopedia/new_page.html",{
                    "Entry_exists": Entry_exists
                })
        if title[0].islower():
            title = title.capitalize()
        util.save_entry(title, f"# {title}" + "\n\n" + content)
        return HttpResponseRedirect(reverse('entry_page', kwargs={'title':title}))
    else:       
        return render(request, "encyclopedia/new_page.html",{
            "Entry_exists": Entry_exists
        })

def edit_page(request, title):
    md_content = util.get_entry(title)
    return render(request, "encyclopedia/edit_page.html", {
       "md_content" : md_content
    })

def process_edit_page(request):
    if request.method == "POST":
        content = request.POST.get("edit_md_content")
        if content.startswith("# "):
            end_title_index = content.find("\r\n")
            title = content[2:end_title_index]
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse('entry_page', kwargs={'title':title}))
        else:
            return HttpResponse("<h2>Error: Your entry doesn't have a Markdown title, please go back and add it.<h2>")

def random_page(request):
    entries_list = util.list_entries()
    size_entries_list = len(entries_list)
    random_number = randint(0,size_entries_list - 1)
    random_entry = entries_list[random_number]
    return HttpResponseRedirect(reverse('entry_page', kwargs={'title':random_entry}))