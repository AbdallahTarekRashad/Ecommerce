var Toast = Swal.mixin({
    toast: true,
    position: 'top-end',
    showConfirmButton: false,
    timer: 5000
});

function add_cart(btn, quantity = false) {
    let product_id = btn.getAttribute('product_id');
    let q = 'plus'
    if (quantity) {
        q = quantity.value;
    }
    let data = [{
        'product_id': product_id,
        'quantity': q
    }]
    $.ajax({
        url: cart,
        data: {'cart_list': JSON.stringify(data)}
        ,
        success: function (data, status, xhr) {
            document.getElementById('cart_count').innerText = data.cart_count
            Toast.fire({
                icon: 'success',
                text: 'Cart Updated'
            })
        }
    });
}

function del_cart(btn) {
    let product_id = btn.getAttribute('product_id');
    $.ajax({
        url: cart_del,
        data:
            {'product_id': product_id},
        success: function (data, status, xhr) {
            document.getElementById('cart_count').innerText = data.cart_count
            var $b = btn.closest("tr");
            $b.remove();
            Toast.fire({
                icon: 'success',
                text: 'Cart Updated'
            })
        }
    });
}

function up_cart(btn) {
    btn.disabled = true;
    $(btn).children().addClass('icon_loading')
    let data = [];
    $(".shoping__cart__table :input").each(function () {
        let temp = {
            'product_id': $(this).attr('product_id'),
            'quantity': $(this).val(),
        };
        data.push(temp);
    });
    $.ajax({
        url: cart,
        dataType: 'json',
        data: {'cart_list': JSON.stringify(data)},
        success: function (data, status, xhr) {
            btn.disabled = false;
            $(btn).children().removeClass('icon_loading')
            document.getElementById('cart_count').innerText = data.cart_count
            $("tbody tr").each(function () {
                let price = $(this).find(".shoping__cart__price").text();
                let quantity = $(this).find("input").val();
                $(this).find(".shoping__cart__total").text(price * quantity);
            });
            Toast.fire({
                icon: 'success',
                text: 'Cart Updated'
            })
        }
    });
}

function add_wish(btn) {
    let product_id = btn.getAttribute('product_id');
    $.ajax({
        url: wish,
        data: {'product_id': product_id,},
        success: function (data, status, xhr) {
            document.getElementById('wish_count').innerText = data.wish_count
            Toast.fire({
                icon: 'success',
                text: 'Wish List Updated'
            })
        }
    });
}

function delete_wish(btn) {
    let product_id = btn.getAttribute('product_id');
    $.ajax({
        url: wish_del,
        data: {'product_id': product_id,},
        success: function (data, status, xhr) {
            document.getElementById('wish_count').innerText = data.wish_count
            var $b = btn.closest(".delete-class");
            $b.remove();
            Toast.fire({
                icon: 'success',
                text: 'Wish List Updated'
            })
        }
    });
}