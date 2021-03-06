#!/usr/bin/env python

from django import forms
from django.db import transaction
from hunchworks import models
from hunchworks.fields import EvidenceField, VoteField


class HunchEvidenceForm(forms.ModelForm):
  evidence = EvidenceField()

  vote = VoteField(help_text="How is this evidence relevant to the hunch?")

  #vote = forms.ChoiceField(, widget=forms.RadioSelect(),
  #  )

  comment = forms.CharField(widget=forms.Textarea, required=False)

  class Meta:
    model = models.HunchEvidence
    fields = ("hunch", "evidence")
    widgets = {
      "hunch": forms.HiddenInput()
    }

  def save(self, creator):
    with transaction.commit_on_success():

      hunch_evidence = super(HunchEvidenceForm, self).save(commit=False)
      hunch_evidence.creator = creator
      hunch_evidence.save()

      if self.cleaned_data["comment"]:
        comment = models.Comment.objects.create(
          hunch_evidence=hunch_evidence,
          creator=creator,
          text=self.cleaned_data["comment"])

      vote = models.Vote.objects.create(
        hunch_evidence=hunch_evidence,
        user_profile=creator,
        choice=self.cleaned_data["vote"])

      return hunch_evidence
