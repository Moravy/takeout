var updateBtn = document.getElementsByClassName("update-cart")

for (var i = 0; i < updateBtn.length; i++) {
    updateBtn[i].addEventListener("click", function () {
        var menu_id = this.dataset.product;
        var action = this.dataset.action;
        var customer;
        if (this.dataset.customer) {
            var customer = this.dataset.customer;
        }
        
        
        console.log(menu_id, action, customer, item)
        
        if (user === 'AnonymousUser') {
            console.log("NOT LOGGED IN")
        } else {
            sendingUpdateOrder(menu_id, action, customer)
        }
    })
}

sendingUpdateOrder = (menu_id, action, customer) => {
    console.log(menu_id, action, customer)
    var url = '/customer/update_order/'
    
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({ 'menu_id': menu_id, 'action': action, 'customer': customer })

    }).then((response) => {
        return response.json()
    }).then((data) => {
        console.log("data", data)
    })
}
