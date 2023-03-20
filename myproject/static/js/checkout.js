
//     $(document).ready(function () {
//     $('.payWithRazorpay').click(function (e) {
//         e.preventDefault();
//         console.log('haello')


//         var first_name = $("[name='Name']").val();   
//         var address = $("[name='address']").val();
//         var city = $("[name='city']").val();
//         var state = $("[name='state']").val();
//         var country = $("[name='country']").val();
//         var postal_code = $("[name='post_code']").val();
//         var phone = $("[name='phone']").val();
//         var email = $("[name='email']").val();
//         var order_note = $("[name='order_note']").val();
//         var token = $("[name='csrfmiddlewaretoken']").val();
//         console.log(token)
//         var grand_total = $('.grand_total').attr('grand-total');
//         console.log(grand_total);

//         if(first_name=="" || address=="" || city=="" || state=="" || country=="" || postal_code=="" || phone=="" || email=="")
//         {
//             swal("Alert!","All fields are mandatory!","error");

//             return false;
//         }

//         // console.log(order_number)

//         else
//         {
           
          



//             var options = {
//                 "key": "rzp_test_xDSPKfOJ3QTf4e", // Enter the Key ID generated from the Dashboard
//                 "amount": grand_total * 100 ,//response.total_price * 100, // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
//                 "currency": "INR",
//                 "name": "MINA's",
//                 "description": "Thank you for buying from us",
//                 "image": "https://example.com/your_logo",
//                 // "order_id": "order_IluGWxBm9U8zJ8", //This is a sample Order ID. Pass the `id` obtained in the response of Step 1
//                 "handler": function (responseb){
//                 //    alert(responseb.razorpay_payment_id);
//                     // alert(response.razorpay_order_id);
//                     // alert(response.razorpay_signature)
//                     data = {
//                         'Name':first_name,
//                         'address':address,
//                         'city':city,
//                         'state':state,
//                         'country':country,
//                         'post_code':postal_code,
//                         'phone':phone,
//                         'email':email,
//                         'order_note':order_note,
//                         'grand_total':grand_total,

//                         'payment_mode':'Payment with Razorpay',
//                         'payment_id':responseb.razorpay_payment_id,
//                         'grand_total':grand_total,
//                         csrfmiddlewaretoken: token
//                     }
//                     $.ajax({
//                         method: "POST",
//                         url: "/products/place_order/",
//                         data: data,
//                         success: function (response) {
//                             console.log(response)
//                             swal(
//                                 'Congratulations!',
//                                 response.status,
//                                 'success'
//                             ).then((value) => {
//                                 console.log(order_number)
//                                 window.location.href = '/orders/order-completed'+'?order_number='+order_number
//                                 console.log(order_number)
//                             });

//                         }
//                     });
//                 },
//                 "prefill": {
//                     "name": first_name,
//                     "email": email,
//                     "contact": phone
//                 },
//                 "theme": {
//                     "color": "#3399cc"
//                 }
//             };
//             var rzp1 = new Razorpay(options);
//             rzp1.open();



//         }


//     });

//     //END OF RAZORPAY

//     //CASH ON DELIVERY
//     $('.cod').click(function (e) {
//         e.preventDefault();



       
//         var token = $("[name='csrfmiddlewaretoken']").val();
//         console.log(token+"hiiiiiiiiiiiiiiii")
//         var order_number = $('.order_number').attr('order_number');
//         var grand_total = $('.grand_total').attr('grand-total');

//         console.log(grand_total+'banna')
//         console.log(order_number+'order done')

//         // if(first_name == "" || last_name == "" || email == "" || phone == "" || address == "" || city == "" || state == "" || country == "" || order_note == "")
//         // {
//         //     alert("All fields are mandatory");
//         //     console.log('all fields are mandatory')
//         //     return false;
//         // }else



//         data = {
//             'payment_mode':'Cash On Delivery',
//             // 'payment_id':responseb.razorpay_payment_id,
//             'order_no':order_number,
//             'grand_total':grand_total,
//             csrfmiddlewaretoken: token
//         }
//         $.ajax({
//             method: "POST",
//             url: "proceed-to-pay/",
//             data: data,

//             success: function (responseb) {
//                 console.log('success')
//                 swal(
//                     responseb.status,
//                     'Congratulations!',
//                     'success'
//                 ).then((value) => {

//                     window.location.href = '/orders/order-completed'+'?order_number='+order_number
//                     console.log(order_number)
//                 });

//             }
//         });






//     });


    
// });



$(document).ready(function () {
  $("#payWithRazorpay").click(function (e) {
    console.log("im g=here");
    e.preventDefault();

    var fname = $("[name='Name']").val();
  
    var email = $("[name='email']").val();
    var phone = $("[name='phone']").val();
    var address = $("[name='address']").val();
  
   
    var city = $("[name='city']").val();
    var state = $("[name='state']").val();
    var country = $("[name='country']").val();
    var postal_code = $("[name='post_code']").val();
    // var order_note = $("[name='order_note']").val();
   
    
    var grand_total = $('.grand_total').attr('grand-total');
             console.log(grand_total);
    var token = $("[name='csrfmiddlewaretoken']").val();
    console.log(grand_total);
    if (
      fname == "" ||
     
      email == "" ||
      phone == "" ||
      address == "" ||
      city == "" ||
      state == "" ||
      country == "" ||
      postal_code == ""
      
    ) {
      swal("alert", "All fields are mandatory", "error");
      return false;
    } else {
    
      
      $.ajax({
        method: "GET",
        url: "/products/proceed-to-pay/",
        contentType: "application/json",
        success: function (response) {
          // console.log(grand_total);
          var walletz=response.wallet_balance
          if(response.remaining_amount==0){

            $.ajax({
              method: "POST",
              url: "/products/place_order/",
              data : data = {
                'Name':fname,
                'address':address,
                'city':city,
                'state':state,
                'country':country,
                'post_code':postal_code,
                'phone':phone,
                'email':email,
                'phone':phone,
                
              
                'payment_mode':'Payment with wallet',
                'payment_id' : 'walet239024',
                'grand_total':grand_total,
                csrfmiddlewaretoken: token
              },
              success: function (responsef) {
                swal("Congratulations!","success", responsef.status ).then(
                  (value) => {
                    window.location.href =
                      "/products/orders/" +
                      "?payment_id=" +
                      data.payment_id;
                  }
                );
                
              },
            }); 

          }
          else{
            var options = {
              key: "rzp_test_k6Ms2BWCn74AHT", // Enter the Key ID generated from the Dashboard
              amount: response.remaining_amount * 100 || grand_total * 100,   //response.total_price * 100, //response.total_price *100 , // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
              currency: "INR",
              name: "MINA's",
              description: "Thank you",
              image: "https://example.com/your_logo",
              // "order_id": "order_IluGWxBm9U8zJ8", //This is a sample Order ID. Pass the `id` obtained in the response of Step 1
              handler: function (responseb) {
                // alert(responseb.razorpay_payment_id);
                // alert(response.razorpay_order_id);
                // alert(responseb.razorpay_payment_id);
                data = {
                    'Name':fname,
                    'address':address,
                    'city':city,
                    'state':state,
                    'country':country,
                    'post_code':postal_code,
                    'phone':phone,
                    'email':email,
                    'wallet_balance':walletz,
                    'phone':phone,
                  
                    'payment_mode':'Payment with Razorpay',
                    'payment_id':responseb.razorpay_payment_id,
                    'grand_total':grand_total,
                    csrfmiddlewaretoken: token
                  
                };

        

                $.ajax({
                  method: "POST",
                  url: "/products/place_order/",
                  data: data,
                  success: function (responsec) {
                    swal("Congratulations!","success", responsec.status ).then(
                      (value) => {
                        window.location.href =
                          "/products/orders/" +
                          "?payment_id=" +
                          data.payment_id;
                      }
                    );
                    
                  },
                }); 
              },
              prefill: {
              
                email: email,
                contact: phone,
              },
              notes: {
                address: "MINA's shopping site",
              },
              theme: {
                color: "#3399cc",
              },
            };
        }
          var rzp1 = new Razorpay(options);
          rzp1.open();
        },
      });
    }
  });
});