var updateBtns=document.getElementsByClassName('update-cart')
for(var i=0;i<updateBtns.length;i++){
    updateBtns[i].addEventListener('click',function(){
        var productId=this.dataset.product
        var action=this.dataset.action
        console.log('productId:',productId,'action:',action)
        console.log(user)
        if (user === "AnonymousUser" ){
            console.log('not logged in')

        }else{
           updateUserOrder(productId,action)
        }
       
     })
}
function updateUserOrder(productId,action){
    console.log('user is logged in , sending data ...')
    var url='/updateItem/'
    fetch(url,{
        method:'POST',
        headers:{
            'content-type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'productId':productId,'action':action})
    })
    .then((Response) =>{
        return Response.json()
    })
    .then((data) =>{
        location.reload()
    })
}