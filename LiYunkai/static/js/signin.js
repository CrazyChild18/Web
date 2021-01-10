let email = document.getElementById("email");
email.onblur = function(){
    let input = document.getElementById("email");
    let submit = document.getElementById('submitBtn');
    let regexp = /^[^.@]+([^.@]*[.]?[^.@]+)+@[^.@]+[.][^.@]+/i
    if(regexp.test(input.value)){
        submit.disabled = false;
    }
    else{
        alert('Error email format')
        input.style.backgroundColor='red';
        submit.disabled = true;
    }
}
