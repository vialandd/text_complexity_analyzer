"""
Views for handling text document listing, detail, and creation.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import TextDocument
from .forms import TextDocumentForm
from .utils import analyze_text_complexity


def document_list(request):
    """
    Display a list of all text documents.
    """
    documents = TextDocument.objects.all().order_by("-created_at")
    return render(request, "analyzer/document_list.html", {"documents": documents})


def document_detail(request, pk):
    """
    Display details of a single text document and its complexity analysis.
    """
    document = get_object_or_404(TextDocument, pk=pk)

    # Phase 4: Integration of Complexity Module
    word_count, sentence_count, graph = analyze_text_complexity(document.content)

    context = {
        "object": document,
        "word_count": word_count,
        "sentence_count": sentence_count,
        "graph": graph,
    }
    return render(request, "analyzer/document_detail.html", context)


def document_create(request):
    """
    Handle the creation of a new text document.
    """
    if request.method == "POST":
        form = TextDocumentForm(request.POST)
        if form.is_valid():
            doc = form.save()
            messages.success(request, "Text analyzed successfully!")
            return redirect("document_detail", pk=doc.pk)
    else:
        form = TextDocumentForm()

    return render(request, "analyzer/document_form.html", {"form": form})

