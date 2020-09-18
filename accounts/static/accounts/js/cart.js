var updateBtn = document.getElementsByClassName("update-cart")

for (var i = 0; i < updateBtn.length; i++) {
    updateBtn[i].addEventListener("click", function () {
        var menu_id = this.dataset.product
        var action = this.dataset.action
        console.log(menu_id, action)

        if (user === 'AnonymousUser') {
            console.log("NOT LOGGED IN")
        } else {
            sendingUpdateOrder(menu_id, action)
        }
    }

    )
}

sendingUpdateOrder = (menu_id, action) => {
    console.log(menu_id, action)
    var url = '/customer/create_order/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({ 'menu_id': menu_id, 'action': action })

    }).then((response) => {
        return response.json()
    }).then((data) => {
        console.log("data", data)
    })
}
