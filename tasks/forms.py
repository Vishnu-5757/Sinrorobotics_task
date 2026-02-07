# tasks/forms.py
from django import forms
from .models import Task, User
from django.contrib.auth.forms import UserCreationForm
from rest_framework import serializers


class UserCreateForm(UserCreationForm):
    role = forms.ChoiceField(choices=User.ROLE_CHOICES)
    manager = forms.ModelChoiceField(queryset=User.objects.filter(role=User.ROLE_ADMIN),
                                     required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'role', 'manager')



class TaskAssignForm(forms.ModelForm):
   
    assigned_to = forms.ModelChoiceField(queryset=User.objects.filter(role=User.ROLE_USER))

    class Meta:
        model = Task
        fields = ['title', 'description', 'assigned_to', 'due_date']



class UserManagementForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput, 
        required=False, 
        help_text="Leave blank to keep current password"
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'manager', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        

        self.fields['manager'].queryset = User.objects.filter(role=User.ROLE_ADMIN)


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            'title', 
            'description', 
            'assigned_to', 
            'due_date', 
            'status', 
            'completion_report', 
            'worked_hours'
        ]
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
            'completion_report': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
       
        user_qs = User.objects.filter(role='user')
        
        if self.user:
            if self.user.is_superadmin():
               
                pass 
            elif self.user.role == 'admin':
               
                user_qs = user_qs.filter(manager=self.user)
            elif self.user.role == 'user':
              
                user_qs = user_qs.filter(id=self.user.id)
                
        self.fields['assigned_to'].queryset = user_qs

        
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

        if self.user and self.user.role == 'user':
            readonly_fields = ['title', 'description', 'assigned_to', 'due_date']
            for field_name in readonly_fields:
                if field_name in self.fields:
                  
                    self.fields[field_name].disabled = True
                    
                    self.fields[field_name].required = False

        
        if not self.instance.pk:
            if 'completion_report' in self.fields:
                self.fields['completion_report'].widget = forms.HiddenInput()
            if 'worked_hours' in self.fields:
                self.fields['worked_hours'].widget = forms.HiddenInput()

    def clean(self):
      
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        report = cleaned_data.get('completion_report')
        hours = cleaned_data.get('worked_hours')

       
        if status == 'completed':
            if not report:
                self.add_error('completion_report', "You must provide a report to mark this as completed.")
            if hours is None or hours <= 0:
                self.add_error('worked_hours', "Please specify valid worked hours.")
        
        return cleaned_data




class UserTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'due_date', 'status', 'completion_report', 'worked_hours']
        read_only_fields = ['id', 'title', 'description', 'due_date']

    def validate_worked_hours(self, value):
        if value < 0:
            raise serializers.ValidationError("Worked hours cannot be negative.")
        return value      
