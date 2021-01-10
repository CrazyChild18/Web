let birthday = document.getElementById("birthday");
birthday.onblur = function(){
    let submit = document.getElementById('submitBtn');
    let regexp = /^[0-9][0-9][0-9][0-9][-][0-9][0-9][-][0-9][0-9]$/
    if(regexp.test(birthday.value)){
        submit.disabled = false;
    }
    else{
        alert('Error birthday format')
        birthday.style.backgroundColor='red';
        submit.disabled = true;
    }
}
