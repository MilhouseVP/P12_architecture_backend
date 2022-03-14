from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView as BaseLogin
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django import forms
import requests
import apps.front.forms as f
from datetime import datetime


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
        response.set_cookie('access', tokens['access'], httponly=True)
        response.set_cookie('refresh', tokens['refresh'], httponly=True)
        return response


def date_formating(date):
    if len(date) == 27:
        dt = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%fZ')
        return dt.strftime('Le %d/%m/%Y, à %H:%M:%S')
    elif len(date) == 20:
        dt = datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')
        return dt.strftime('Le %d/%m/%Y, à %H:%M:%S')
    else:
        dt = datetime.strptime(date, '%Y-%m-%d')
        return dt.strftime('Le %d/%m/%Y')


def get_api_mixin(request, endpoint):
    url = 'http://127.0.0.1:8000/api/' + endpoint
    token = request.COOKIES.get('access')
    head = {'Authorization': 'Bearer ' + token}
    data = requests.get(url, headers=head).json()
    if 'next' in data:
        while data['next']:
            next_page = requests.get(data['next'], headers=head).json()
            data['results'] = data['results'] + next_page['results']
            data['next'] = next_page['next']
    return data


def post_api_mixin(request, body, endpoint):
    url = 'http://127.0.0.1:8000/api/' + endpoint
    token = request.COOKIES.get('access')
    head = {'Authorization': 'Bearer ' + token}
    data = requests.post(url=url, data=body, headers=head).json()
    return data


def patch_api_mixin(request, body, endpoint):
    url = 'http://127.0.0.1:8000/api/' + endpoint
    token = request.COOKIES.get('access')
    head = {'Authorization': 'Bearer ' + token}
    data = requests.patch(url=url, data=body, headers=head)
    return data


def delete_api_mixin(request, endpoint):
    url = 'http://127.0.0.1:8000/api/' + endpoint
    token = request.COOKIES.get('access')
    head = {'Authorization': 'Bearer ' + token}
    requests.delete(url=url, headers=head)


def get_group(current_user):
    group_list = []
    for group in current_user.groups.all():
        group_list.append(group.name)
    return group_list


@login_required
def home(request):
    if 'support' in get_group(request.user):
        endpoint = 'events?support_contact=' + str(request.user.id)
        data = get_api_mixin(request, endpoint)
        if 'detail' in data:
            context = {'error': data['detail']}
        else:
            for event in data['results']:
                event['event_date'] = date_formating(event['event_date'])
            paginator = Paginator(data['results'], 5)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            context = {'instances': page_obj, 'events': True}

    elif 'sales' in get_group(request.user):
        endpoint = 'contracts?sale_contact=' + str(request.user.id)
        data = get_api_mixin(request, endpoint)
        if 'detail' in data:
            context = {'error': data['detail']}
        else:
            paginator = Paginator(data['results'], 5)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            context = {'instances': page_obj, 'contracts': True}
    else:
        # 'manager' in get_group(request.user):
        return redirect('users')
    # else:
    #     context = {'error': {'detail': "Rien pour l'instant"}}
    return render(request, 'front/home.html', context)


@login_required
def my_customers(request):
    groups = get_group(request.user)
    if 'manager' in groups or 'sales' not in groups :
        return redirect('home')
    else:
        endpoint = 'customers?sale_contact=' + str(request.user.id)
        data = get_api_mixin(request, endpoint)
        if 'detail' in data:
            context = {'error': data['detail']}
        else:
            paginator = Paginator(data['results'], 5)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            context = {'instances': page_obj, 'customers': True}
        return render(request, 'front/my_customers.html', context)


@login_required
def account(request):
    form = f.UserPasswordForm()
    context = {'password_form': form}
    endpoint = 'password_update/'
    if request.method == 'POST':
        password_form = f.UserPasswordForm(request.POST)
        if password_form.is_valid():
            body = password_form.data
            patch_api_mixin(request, body=body, endpoint=endpoint)
            return redirect('login')
        else:
            context = {'error': password_form.data}
            return render(request, 'front/account.html', context)
    else:
        return render(request, 'front/account.html', context)


@login_required
def search(request):
    endpoint = ''
    context = {}

    search_dict = {
        'customer': ['customers?', 'customer'],
        'contract': ['contracts?', 'contract'],
        'event': ['events?', 'event']
    }

    type_dict = {
        'email': 'email=',
        'last_name': 'last_name=',
        'company': 'company=',
        'customer__email': 'customer__email=',
        'customer__last_name': 'customer__last_name=',
        'customer__company': 'customer__company=',
        'date_created': 'date_contains=',
        'amount': 'amount=',
        'event_date': 'date_contains='
    }
    if 'search_sel' in request.GET:
        sel = request.GET['search_sel']
        endpoint = search_dict[sel][0]
        context['type'] = search_dict[sel][1]
        type = request.GET['type']
        endpoint = endpoint + type_dict[type] + request.GET['search_input']

        returned_data = get_api_mixin(request, endpoint)

        if not returned_data['results']:
            context['empty'] = True
        else:
            for event in returned_data['results']:
                if 'event_date' in event:
                    event['event_date'] = date_formating(
                        event['event_date'])
            context['results'] = returned_data['results']

        return render(request, 'front/search.html', context)

    else:
        return render(request, 'front/search.html')


@login_required
def customers(request):
    endpoint = 'customers/'
    data = get_api_mixin(request, endpoint)
    if 'detail' in data:
        context = {'error': data['detail']}
    else:
        paginator = Paginator(data['results'], 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {'instances': page_obj, 'clients': True}
    return render(request, 'front/customers.html', context)


@login_required
def customer(request, customer_id):
    endpoint = 'customers/' + str(customer_id) + '/'
    data = get_api_mixin(request, endpoint)
    if 'detail' in data:
        context = {'error': data['detail']}
    else:
        data['date_created'] = date_formating(data['date_created'])
        data['date_updated'] = date_formating(data['date_updated'])
        context = {'customer': data}
    return render(request, 'front/customer_details.html', context)


@login_required
def customer_create(request):
    groups = get_group(request.user)
    if 'support' in groups :
        return redirect('home')
    else:
        users_endpoint = 'users?role=sales'
        sales_users = get_api_mixin(request, users_endpoint)
        form = f.CustomerEditForm(sales_users['results'])
        endpoint = 'customers/'
        if request.user.role == 'sales':
            form.fields['sale_contact'].widget = forms.HiddenInput()
            form.fields['sale_contact'].initial = request.user.id
        context = {'customer_form': form}
        if request.method == 'POST':
            customer_form = f.CustomerForm(request.POST)
            if customer_form.is_valid():
                data = customer_form.cleaned_data
                result_data = post_api_mixin(request, body=data,
                                             endpoint=endpoint)
                return redirect('customer_detail',
                                customer_id=result_data['id'])
        else:
            return render(request, 'front/customer_create.html', context)


@login_required
def customer_edit(request, edit_customer_id):
    groups = get_group(request.user)
    if 'support' in groups :
        return redirect('home')
    else:
        users_endpoint = 'users?role=sales'
        sales_users = get_api_mixin(request, users_endpoint)
        form = f.CustomerEditForm(sales_users['results'])

        endpoint = 'customers/' \
                   + str(edit_customer_id) + '/'
        if request.method == 'POST':
            form = f.CustomerEditForm(sales_users['results'], request.POST)
            if form.is_valid():
                body = form.data
                patch_api_mixin(request, body=body, endpoint=endpoint)
                return redirect('customer_detail',
                                customer_id=edit_customer_id)
        else:
            data = get_api_mixin(request, endpoint)
            for key in data:
                try:
                    if key == 'sale_contact':
                        form.fields[key].initial = data[key]['id']
                    else:
                        form.fields[key].initial = data[key]
                except KeyError:
                    pass
            context = {'customer_form': form}
            return render(request, 'front/customer_edit.html', context)


@login_required
def contracts(request):
    endpoint = 'contracts/'
    data = get_api_mixin(request, endpoint)
    if 'detail' in data:
        context = {'error': data['detail']}
    else:
        paginator = Paginator(data['results'], 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {'instances': page_obj}
    return render(request, 'front/contracts.html', context)


@login_required
def contract(request, cont_id):
    endpoint = 'contracts/' + str(cont_id) + '/'
    data = get_api_mixin(request, endpoint)
    if 'detail' in data:
        context = {'error': data['detail']}
    else:
        data['date_created'] = date_formating(data['date_created'])
        data['date_updated'] = date_formating(data['date_updated'])
        data['payement_due'] = date_formating(data['payement_due'])
        context = {'contract': data}
    return render(request, 'front/contract_details.html', context)


@login_required
def contract_create(request, customer_id):
    groups = get_group(request.user)
    if 'support' in groups :
        return redirect('home')
    else:
        users_endpoint = 'users?role=sales'
        sales_users = get_api_mixin(request, users_endpoint)
        form = f.ContractForm(sales_users['results'])
        if request.user.role == 'sales':
            form.fields['sale_contact'].widget = forms.HiddenInput()
            form.fields['sale_contact'].initial = request.user.id
        context = {'contract_form': form}
        if request.method == 'POST':
            endpoint = 'contracts/'
            contract_form = f.ContractForm(sales_users['results'],
                                           request.POST)
            if contract_form.is_valid():
                data = contract_form.cleaned_data
                body = {
                    'customer': customer_id,
                    'sale_contact': data['sale_contact'],
                    'amount': data['amount'],
                    'payement_due': data['payement_due']
                }
                post_api_mixin(request, body, endpoint)
                return redirect('home')
        else:
            return render(request, 'front/contract_create.html', context)


@login_required
def contract_edit(request, edit_cont_id):
    groups = get_group(request.user)
    if 'support' in groups:
        return redirect('home')
    else:
        users_endpoint = 'users?role=sales'
        sales_users = get_api_mixin(request, users_endpoint)
        form = f.ContractEditForm(sales_users['results'])
        endpoint = 'contracts/' + str(edit_cont_id) + '/'
        if request.method == 'POST':
            cont_form = f.ContractEditForm(sales_users['results'], request.POST)
            if cont_form.is_valid():
                body = cont_form.cleaned_data
                patch_api_mixin(request, body=body, endpoint=endpoint)
                return redirect('contract_detail', cont_id=edit_cont_id)
        else:
            data = get_api_mixin(request, endpoint)
            for key in data:
                try:
                    if key == 'payement_due':
                        form.fields[key].initial = datetime.strptime(
                            data[key], '%Y-%m-%d')
                    else:
                        form.fields[key].initial = data[key]
                except KeyError:
                    pass
            context = {'contract_form': form}
            return render(request, 'front/contract_edit.html', context=context)


@login_required
def events(request):
    endpoint = 'events/'
    data = get_api_mixin(request, endpoint)
    if 'detail' in data:
        context = {'error': data['detail']}
    else:
        for event in data['results']:
            event['event_date'] = date_formating(event['event_date'])
        paginator = Paginator(data['results'], 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {'instances': page_obj, 'events': True}
    return render(request, 'front/events.html', context)


@login_required
def event(request, event_id):
    endpoint = 'events/' + str(event_id) + '/'
    data = get_api_mixin(request, endpoint)
    if 'detail' in data:
        context = {'error': data['detail']}
    else:
        data['date_created'] = date_formating(data['date_created'])
        data['date_updated'] = date_formating(data['date_updated'])
        data['event_date'] = date_formating(data['event_date'])
        context = {'event': data}
    return render(request, 'front/event_details.html', context)


@login_required
def event_create(request, contract_id, customer_id):
    groups = get_group(request.user)
    if 'support' in groups:
        return redirect('home')
    else:
        users_endpoint = 'users?role=support'
        sales_users = get_api_mixin(request, users_endpoint)
        event_form = f.EventEditForm(sales_users['results'])
        context = {'event_form': event_form}
        if request.method == 'POST':
            endpoint = 'events/'
            event_form = f.EventForm(sales_users['results'], request.POST)
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
                patch_endpoint = 'contracts/' \
                                 + str(contract_id) + '/'
                patch_body = {'event_created': True}
                patch_api_mixin(request, patch_body, patch_endpoint)
                return redirect('event_detail',
                                event_id=str(returned_data['id']))
        else:
            return render(request, 'front/event_create.html', context)


@login_required
def event_edit(request, edit_event_id):
    groups = get_group(request.user)
    if 'sales' in groups:
        return redirect('home')
    else:
        users_endpoint = 'users?role=support'
        support_users = get_api_mixin(request, users_endpoint)
        event_form = f.EventEditForm(support_users['results'])
        endpoint = 'events/' + str(edit_event_id) + '/'
        if request.method == 'POST':
            event_form = f.EventEditForm(support_users['results'], request.POST)
            if event_form.is_valid():
                body = event_form.cleaned_data
                patch_api_mixin(request, body=body, endpoint=endpoint)
                return redirect('event_detail', event_id=str(edit_event_id))
        else:
            data = get_api_mixin(request, endpoint)
            for key in data:
                try:
                    if key == 'event_date':
                        event_form.fields[key].initial = datetime.strptime(
                            data[key], '%Y-%m-%dT%H:%M:%SZ')
                    else:
                        event_form.fields[key].initial = data[key]
                except KeyError:
                    pass
            context = {'event_form': event_form}
            return render(request, 'front/event_edit.html', context=context)


@login_required
def users(request):
    if 'manager' not in get_group(request.user):
        return redirect('home')
    else:
        endpoint = 'users/'
        data = get_api_mixin(request, endpoint)
        if 'detail' in data:
            context = {'error': data['detail']}
        else:
            context = {'users': data['results']}
        return render(request, 'front/users.html', context)


@login_required
def user(request, user_id):
    if 'manager' not in get_group(request.user):
        return redirect('home')
    else:
        endpoint = 'users/' + str(user_id) + '/'
        data = get_api_mixin(request, endpoint)
        if 'detail' in data:
            context = {'error': data['detail']}
        else:
            context = {'employee': data}
        return render(request, 'front/user_details.html', context)


@login_required
def user_create(request):
    if 'manager' not in get_group(request.user):
        return redirect('home')
    else:
        form = f.UserForm()
        context = {'user_form': form}
        if request.method == 'POST':
            endpoint = 'signup/'
            user_form = f.UserForm(request.POST)
            if user_form.is_valid():
                body = user_form.cleaned_data
                returned_data = post_api_mixin(request, body, endpoint)
                return redirect('user_detail',
                                user_id=str(returned_data['id']))
        else:
            return render(request, 'front/user_create.html', context)


@login_required
def user_edit(request, edit_user_id):
    if 'manager' not in get_group(request.user):
        return redirect('home')
    else:
        form = f.UserEditForm()
        context = {'user_form': form}
        endpoint = 'users/' + str(edit_user_id) + '/'
        if request.method == 'POST':
            user_form = f.UserEditForm(request.POST)
            if user_form.is_valid():
                body = user_form.cleaned_data
                patch_api_mixin(request, body=body, endpoint=endpoint)
                return redirect('user_detail', user_id=str(edit_user_id))
        else:
            data = get_api_mixin(request, endpoint)
            for key in data:
                try:
                    form.fields[key].initial = data[key]
                except KeyError:
                    pass
            return render(request, 'front/user_edit.html', context)


@login_required
def user_delete(request, user_id):
    if 'manager' not in get_group(request.user):
        return redirect('home')
    else:
        endpoint = 'users/' + str(user_id) + '/'
        delete_api_mixin(request, endpoint)
        return redirect('users')
