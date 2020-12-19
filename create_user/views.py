import csv
from django.http import HttpResponse, JsonResponse
from django.template import loader
# from django.contrib.auth import get_user_model
from django.conf import settings
# User = get_user_model()


def index(request):
    template = loader.get_template('create_user/index.html')
    context = {}
    return HttpResponse(template.render(context, request))


def generate_pass(req):
    line_count = 0
    marked_item = 1
    with open("/home/user/test.csv", 'r') as f:
        reader = csv.reader(f, delimiter=',')

        lines = []
        for line in reader:
            if len(line) > 1 and line[1] == '':
                line_count += 1
                line[1] = 'misho'
            lines.append(line)
    with open("/home/user/test.csv", 'w', newline='') as f:
        writer = csv.writer(f, delimiter=',')
        # writer.writerow(title)
        writer.writerows(lines)
    return JsonResponse('generate pass is now working', safe=False)
