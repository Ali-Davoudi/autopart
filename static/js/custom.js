function sendBlogComment(blog_id) {
    var comment = $('#comment_text').val();
    var parentId = $('#parent_id').val();

    $.post('/blog/add-blog-comment/', {
        comment_text: comment,
        blog_id: blog_id,
        parent_id: parentId,
        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
    }).then(res => {
        $('#comments_area').html(res);
        $('#comment_text').val('');
        $('#parent_id').val('');
        Swal.fire({
            title: res.title,
            text: res.text,
            icon: res.icon,
            confirmButtonColor: '#006B1B',
            confirmButtonText: 'آگاه شدم !'
        });
    });
}

function fillParentId(parent_id) {
    $('#parent_id').val(parent_id);
    document.getElementById('blog_comment_form').scrollIntoView({behavior: 'smooth'});
}

function sendProductComment(product_id) {
    var comment = $('#comment_text').val();

    $.post('/products/add-product-comment', {
        comment_text: comment,
        product_id: product_id,
        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
    }).then(res => {
        $('#comment_text').val('');
        Swal.fire({
            title: res.title,
            text: res.text,
            icon: res.icon,
            confirmButtonColor: '#006B1B',
            confirmButtonText: 'آگاه شدم !'
        });
    });
}

function addProductToOrder(product_id) {
    const productCount = $('#product-count').val();

    $.get('/my-basket-order/add-to-order?product_id=' + product_id + '&count=' + productCount).then(res => {
        console.log(res.status);
        Swal.fire({
            title: res.title,
            text: res.text,
            icon: res.icon,
            confirmButtonColor: res.confrim_button_color,
            confirmButtonText: res.confrim_button_text,
            cancelButtonColor: '#d33',
            showCancelButton: res.show_bool_cancel_button,
            cancelButtonText: res.cancel_button_text,
        }).then(result => {
            location.reload();
        });
    });
}

function removeAnUserOrder(detail_id) {
    $.get('/my-basket-order/remove-order?detail_id=' + detail_id).then(res => {
        console.log(res.status)
        if (res.status === 'success') {
            Swal.fire({
                title: 'اعلان سبد خرید!',
                text: "محصول از سبد خرید شما حذف شد.",
                icon: 'warning',
                confirmButtonColor: '#3085d6',
                confirmButtonText: 'متوجه شدم',
            });
            $('#user-order-detail-content').html(res.body);
        }
    });
}

function addProductToWishlist(product_id) {
    $.get('/my-wishlist/add-to-wishlist?product_id=' + product_id).then(res => {
        console.log(res.status);
        Swal.fire({
            title: res.title,
            text: res.text,
            icon: res.icon,
            showCancelButton: res.show_bool_cancel_button,
            confirmButtonColor: res.confrim_button_color,
            cancelButtonColor: res.cancel_button_color,
            confirmButtonText: res.confrim_button_text,
            cancelButtonText: res.cancel_button_text
        }).then(result => {
            location.reload();
        });
    });
}

function removeFavProduct(detail_id) {
    $.get('/my-wishlist/remove-product-from-wishlist?detail_id=' + detail_id).then(res => {
        console.log(res.status);
        if (res.status === 'success') {
            Swal.fire({
                title: 'اعلان لیست علاقه مندی ها!',
                text: "محصول انتخابی از لیست علاقه مندی های شما حذف شد.",
                icon: 'warning',
                confirmButtonColor: '#3085d6',
                confirmButtonText: 'متوجه شدم',
            });
            $('#wishlist-content').html(res.body);
        }
    })
}

function applyCoupon() {
    $.post('/my-basket-order/apply-coupon/', {
        coupon_code: $('#coupon-code').val(),
        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
    }).then(function (res) {
        if (res.status === 'success') {
            Swal.fire(
                'عملیات موفقیت آمیز!',
                res.message,
                'success'
            ).then(() => {
                location.reload(); // Reload the page
            });
        } else if (res.status === 'error') {
            Swal.fire(
                'خطا!',
                res.message,
                'error',
                $('#coupon-code').val('')
            );
        }
    });
}