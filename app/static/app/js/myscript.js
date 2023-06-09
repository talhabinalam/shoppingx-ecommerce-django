$('#slider1, #slider2, #slider3').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 3,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 5,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})

$('.plus-cart').click(function(){
    var id = $(this).attr('pid').toString();
    var eml = this.parentNode.children[2];
    // console.log(id)
    $.ajax({
        type:'GET',
        url:'/pluscart',
        data:{
            pro_id:id
        },
        success: function(data){
            eml.innerText = data.quantity
            document.getElementById('amount').innerText = data.amount
            document.getElementById('total_amount').innerText = data.total_amount
        }
    })
})

$('.minus-cart').click(function(){
    var id = $(this).attr('pid').toString();
    var eml = this.parentNode.children[2];
    // console.log(id)
    $.ajax({
        type:'GET',
        url:'/minuscart',
        data:{
            pro_id:id
        },
        success: function(data){
            eml.innerText = data.quantity
            document.getElementById('amount').innerText = data.amount
            document.getElementById('total_amount').innerText = data.total_amount
        }
    })
})

$('.remove-cart').click(function(){
    var id = $(this).attr('pid').toString();
    var cartItem = $(this).closest('.row');  // Get the parent cart item element
    $.ajax({
        type:'GET',
        url:'/removecart',
        data:{
            pro_id:id
        },
        success: function(data){
            console.log('Delete');
            cartItem.remove();  // Remove the cart item from the HTML
            document.getElementById('amount').innerText = data.amount;
            document.getElementById('total_amount').innerText = data.total_amount;
        }
    });
});


