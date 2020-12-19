import io
import csv
from django.contrib import admin, messages
from django.forms import forms
from django.shortcuts import redirect
from django.urls import path
from django.contrib.auth import get_user_model
User = get_user_model()


class CsvUploadForm(forms.Form):
    csv_file = forms.FileField()


class CsvUploadAdmin(admin.ModelAdmin):

    change_list_template = "custom_admin/csv_form.html"

    def get_urls(self):
        urls = super().get_urls()
        additional_urls = [
            path("upload-csv/", self.upload_csv),
        ]
        return additional_urls + urls

    def changelist_view(self, request, extra_context=None):
        extra = extra_context or {}
        extra["csv_upload_form"] = CsvUploadForm()
        return super(CsvUploadAdmin, self).changelist_view(request, extra_context=extra)

    def upload_csv(self, request):
        if request.method == "POST":
            form = CsvUploadForm(request.POST, request.FILES)
            if form.is_valid():
                if request.FILES['csv_file'].name.endswith('csv'):

                    try:
                        csv_file = request.FILES["csv_file"]
                        data_set = csv_file.read().decode('UTF-8')
                        io_string = io.StringIO(data_set)
                        # next(io_string)
                        data = []
                        for line in csv.reader(io_string, delimiter=',', quotechar="|"):
                            user = User(username=line[0], email=line[2], first_name=line[3],
                                              last_name=line[4])
                            user.set_password(line[1])
                            data.append(user)
                        User.objects.bulk_create(data)
                        self.message_user(request, "Your csv file has been imported")
                        return redirect("..")
                    except UnicodeDecodeError as e:
                        self.message_user(
                            request,
                            "There was an error decoding the file:{}".format(e),
                            level=messages.ERROR
                        )
                        return redirect("..")
                else:
                    self.message_user(
                        request,
                        "Incorrect file type: {}".format(
                            request.FILES['csv_file'].name.split(".")[1]
                        ),
                        level=messages.ERROR
                    )

            else:
                self.message_user(
                    request,
                    "There was an error in the form {}".format(form.errors),
                    level=messages.ERROR
                )
                return redirect("..")


admin.site.unregister(User)
admin.site.register(User, CsvUploadAdmin)
