from django.forms import modelformset_factory, ModelForm, ValidationError
from django.utils.translation import ugettext_lazy as _
from .models import Stereotype, StereotypeVote


class StereotypeForm(ModelForm):
    class Meta:
        model = Stereotype
        fields = ['name', 'description']

    def __init__(self,*args,**kwargs):
        #use self to store id
        self.conversation = kwargs.pop("conversation")
        super(StereotypeForm, self).__init__(*args,**kwargs)

    def clean(self):
        super(StereotypeForm, self).clean()
        name = self.cleaned_data.get('name')

        stereotype_exists = Stereotype.objects.filter(name=name, conversation=self.conversation).exists()
        if stereotype_exists:
            msg = _('Stereotype for this conversation with this name already exists.')
            raise ValidationError(msg)
        return self.cleaned_data


class StereotypeVoteForm(ModelForm):
    class Meta:
        model = StereotypeVote
        fields = ['comment', 'choice']


StereotypeVoteFormSet = modelformset_factory(
    StereotypeVote,
    form=StereotypeVoteForm,
)
