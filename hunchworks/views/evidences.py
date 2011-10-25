#!/usr/bin/env python
# encoding: utf-8

import json
from hunchworks import forms, models
from hunchworks.utils.pagination import paginated
from django.template import RequestContext
from django.template.loader import render_to_string
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django import http
from django.contrib.auth.decorators import login_required


def _render(req, template, more_context):
  return render_to_response(
    "evidences/" + template +".html",
    RequestContext(req, more_context)
  )

@login_required
def index(req):
  evidences = paginated(req, models.Evidence.objects.all(), 10)

  return _render(req, "index", {
    "evidences": evidences
  })

@login_required
def show(req, evidence_id):
  evidence = get_object_or_404(
    models.Evidence,
    pk=evidence_id)

  return _render(req, "show", {
    "evidence": evidence
  })

@login_required
def edit(req, evidence_id):
  evidence = get_object_or_404(
    models.Evidence,
    pk=evidence_id)

  form = forms.EvidenceForm(
    req.POST or None,
    instance=evidence)

  if form.is_valid():
    evidence = form.save()
    return redirect(evidence)

  return _render(req, "edit", {
    "evidence": evidence,
    "form": form
  })

@login_required
def create(req):
  form = forms.EvidenceForm(req.POST or None)

  if form.is_valid():
    evidence = form.save(creator=req.user.get_profile())
    return redirect(evidence)

  return _render(req, "create", {
    "form": form
  })

@login_required
def _preview(evidence):
  return render_to_string("evidences/short.html", {
    "evidence": evidence
  })

def _search_results(query_set):
  return [
    { "id": evidence.pk, "preview": _preview(evidence) }
    for evidence in query_set]

def search(req):
  query_set = models.Evidence.search(
    req.GET["q"], req.user.get_profile())

  return http.HttpResponse(
    json.dumps(_search_results(query_set)),
    content_type="application/json"
  )