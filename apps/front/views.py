from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView as BaseLogin
from django.contrib.auth.decorators import login_required
import requests
from .forms import EventForm, ContractForm, EventEditForm


class LoginView(BaseLogin):
    """
    Overriding Django default login view to get JWT from api at login and
    storing them as cookies
    """

    def form_valid(self, form):
        response = super().form_valid(form)
        endpoint = 'http://127.0.0.1:8000/api/login/'
        username = form['username'].value()
        password = form['password'].value()
        data = {'username': username, 'password': password}
        tokens = requests.post(url=endpoint, data=data).json()
        response.set_cookie('access', tokens['access'])
        response.set_cookie('refresh', tokens['refresh'])
        return response


# TODO: delete cookies at logout

def get_api_mixin(request, endpoint):
    token = request.COOKIES.get('access')
    head = {'Authorization': 'Bearer ' + token}
    data = requests.get(endpoint, headers=head).json()
    return data


def post_api_mixin(request, body, endpoint):
    token = request.COOKIES.get('access')
    head = {'Authorization': 'Bearer ' + token}
    data = requests.post(url=endpoint, data=body, headers=head).json()
    return data


def patch_api_mixin(request, body, endpoint):
    token = request.COOKIES.get('access')
    head = {'Authorization': 'Bearer ' + token}
    requests.patch(endpoint, data=body, headers=head)


def get_group(user):
    group_list = []
    for group in user.groups.all():
        group_list.append(group.name)
    return group_list


@login_required
def home(request):
    if 'support' in get_group(request.user):
        endpoint = 'http://127.0.0.1:8000/api/events?support_contact=' \
                   + str(request.user.id)
        data = get_api_mixin(request, endpoint)
        if 'detail' in data:
            context = {'error': data['detail']}
        else:
            context = {'events': data['results']}

    elif 'sales' in get_group(request.user):
        endpoint = 'http://127.0.0.1:8000/api/contracts?sale_contact=' \
                   + str(request.user.id)
        data = get_api_mixin(request, endpoint)
        if 'detail' in data:
            context = {'error': data['detail']}
        else:
            context = {'contracts': data['results']}
    # TODO: gérer manager
    else:
        context = {'error': {'detail': "Rien pour l'instant"}}
    return render(request, 'front/home.html', context)


@login_required
def customers(request):
    endpoint = 'http://127.0.0.1:8000/api/customers/'
    data = get_api_mixin(request, endpoint)
    if 'detail' in data:
        context = {'error': data['detail']}
    else:
        context = {'clients': data['results']}
    return render(request, 'front/customers.html', context)


@login_required
def customer(request, customer_id):
    endpoint = 'http://127.0.0.1:8000/api/customers/' + str(customer_id) + '/'
    data = get_api_mixin(request, endpoint)
    if 'detail' in data:
        context = {'error': data['detail']}
    else:
        context = {'customer': data}
    return render(request, 'front/customer_details.html', context)


@login_required
def contracts(request):
    endpoint = 'http://127.0.0.1:8000/api/contracts/'
    data = get_api_mixin(request, endpoint)
    if 'detail' in data:
        context = {'error': data['detail']}
    else:
        context = {'contracts': data['results']}
    return render(request, 'front/contracts.html', context)


# TODO: ajouter un bouton pour aller a l'event depuis le contrat
@login_required
def contract(request, cont_id):
    endpoint = 'http://127.0.0.1:8000/api/contracts/' + str(cont_id) + '/'
    data = get_api_mixin(request, endpoint)
    if 'detail' in data:
        context = {'error': data['detail']}
    else:
        context = {'contract': data}
    return render(request, 'front/contract_details.html', context)


@login_required
def contract_create(request, customer_id):
    contract_form = ContractForm()
    context = {'contract_form': contract_form}
    if request.method == 'POST':
        endpoint = 'http://127.0.0.1:8000/api/contracts/'
        contract_form = ContractForm(request.POST)
        if contract_form.is_valid():
            data = contract_form.cleaned_data
            body = {
                'customer': customer_id,
                'sale_contact': request.user.id,
                'amount': data['amount'],
                'payement_due': data['payement_due']
            }
            post_api_mixin(request, body, endpoint)
            return redirect('home')
    else:
        return render(request, 'front/create_contract.html', context)


@login_required
def events(request):
    endpoint = 'http://127.0.0.1:8000/api/events/'
    data = get_api_mixin(request, endpoint)
    if 'detail' in data:
        context = {'error': data['detail']}
    else:
        context = {'events': data['results']}
    return render(request, 'front/events.html', context)


@login_required
def event(request, event_id):
    endpoint = 'http://127.0.0.1:8000/api/events/' + str(event_id) + '/'
    data = get_api_mixin(request, endpoint)
    if 'detail' in data:
        context = {'error': data['detail']}
    else:
        context = {'event': data}
    return render(request, 'front/event_details.html', context)


@login_required
def event_create(request, contract_id, customer_id):
    event_form = EventForm()
    context = {'event_form': event_form}
    if request.method == 'POST':
        endpoint = 'http://127.0.0.1:8000/api/events/'
        event_form = EventForm(request.POST)
        if event_form.is_valid():
            data = event_form.cleaned_data
            body = {
                'customer': customer_id,
                'support_contact': data['support_contact'].id,
                'contract': contract_id,
                'attendees': data['attendees'],
                'event_date': data['event_date'],
                'note': data['note']
            }
            returned_data = post_api_mixin(request, body, endpoint)
            patch_endpoint = 'http://127.0.0.1:8000/api/contracts/' \
                             + str(contract_id) + '/'
            patch_body = {'event_created': True}
            patch_api_mixin(request, patch_body, patch_endpoint)
            return redirect('event_detail',
                            event_id=str(returned_data['id']))
    else:
        return render(request, 'front/create_event.html', context)


@login_required
def event_edit(request, edit_event_id):
    form = EventEditForm()
    endpoint = 'http://127.0.0.1:8000/api/events/' + str(edit_event_id) + '/'
    if request.method == 'POST':
        event_form = EventEditForm(request.POST)
        if event_form.is_valid():
            body = event_form.cleaned_data
            patch_api_mixin(request, body=body, endpoint=endpoint)
            return redirect('event_detail', event_id=str(edit_event_id))
    else:
        data = get_api_mixin(request, endpoint)
        for key in data:
            try:
                form.fields[key].initial = data[key]
            except KeyError:
                pass
        context = {'event_form': form}
        return render(request, 'front/event_edit.html', context=context)

@login_required
def users(request):
    if 'manager' in get_group(request.user):
        endpoint = 'http://127.0.0.1:8000/api/users/'
        data = get_api_mixin(request, endpoint)
        if 'detail' in data:
            context = {'error': data['detail']}
        else:
            context = {'users': data['results']}
        return render(request, 'front/users.html', context)
    else:
        return redirect('home')


@login_required
def user(request, user_id):
    if 'manager' in get_group(request.user):
        endpoint = 'http://127.0.0.1:8000/api/users/' + str(user_id) + '/'
        data = get_api_mixin(request, endpoint)
        if 'detail' in data:
            context = {'error': data['detail']}
        else:
            context = {'employee': data}
        return render(request, 'front/user_details.html', context)
    else:
        return redirect('home')
