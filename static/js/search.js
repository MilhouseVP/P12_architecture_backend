let customer = document.getElementById('customer')
let contract = document.getElementById('contract')
let event = document.getElementById('event')
let input_field = document.getElementById('search_input')

let search_type = document.getElementById('choices')


let customer_choices = '<option value="last_name">Nom</option>' +
    '<option value="email">Email</option>' +
    '<option value="company">Société</option>'

let contract_choices = '<option value="customer__last_name">Nom</option>' +
    '<option value="customer__email">Email</option>' +
    '<option value="customer__company">Société</option>' +
    '<option value="date_created">Date</option>' +
    '<option value="amount">Montant</option>'

let event_choices = '<option value="customer__last_name">Nom</option>' +
    '<option value="customer__email">Email</option>' +
    '<option value="customer__company">Société</option>' +
    '<option value="event_date">Date</option>'

customer.addEventListener('click', function customer_change(event) {
    search_type.innerHTML = customer_choices;
});

contract.addEventListener('click', function contract_change(event) {
    search_type.innerHTML = contract_choices;
});

event.addEventListener('click', function event_change(event) {
    search_type.innerHTML = event_choices;
});

search_type.addEventListener('input', function input_change() {
   if ((search_type.value === 'date_created') || (search_type.value === 'event_date')) {
        input_field.type = 'date';
    }
   else {
       input_field.type = 'text';
   }
});