"""
Views for handling text document listing, detail, and creation.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.views.decorators.cache import cache_page
from .models import TextDocument
from .forms import TextDocumentForm
from .utils import analyze_text_complexity


def document_list(request):
    """
    Display a list of all text documents with pagination.
    """
    documents_list = TextDocument.objects.all().order_by("-created_at")
    paginator = Paginator(documents_list, 6) # Show 6 documents per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "analyzer/document_list.html", {"page_obj": page_obj})


# Cache the analysis result for 15 minutes to improve performance
@cache_page(60 * 15)
def document_detail(request, pk):
    """
    Display details of a single text document and its complexity analysis.
    """
    document = get_object_or_404(TextDocument, pk=pk)

    # Phase 4: Integration of Complexity Module
    analysis_stats = analyze_text_complexity(document.content)

    context = {
        "object": document,
        "metrics": analysis_stats, # Pass the entire dict
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

