
function btnState(state, id){
    if(state){
        var defState = $('#'+id).html();
        $('#'+id).attr("def-state", defState).attr("disabled", true).html("Attendere prego...");
    }else{
        var defState = $('#'+id).attr("def-state");
        $('#'+id).attr("disabled", false).html(defState);
    }
}

function frmErrorMessages(state, id, text){
    
    if(state){
        document.getElementById(id).innerHTML = text;
        document.getElementById(id).classList.remove('hidden');
    }else{
        document.getElementById(id).innerHTML = "";
        document.getElementById(id).classList.add('hidden');
    }
}

function submitloginForm(){
    var valid = 1, description;
    $("input").removeClass("redborder");
   

    let email = document.getElementById("email").value;
    let regex = /^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})/g;
    if(email.match(regex) !== null){
        if(email.match(regex).length===0){
            valid = 0;
            description = "E-mail address not valid";
            $("#email").addClass("redborder");
        }
    }else{
        valid = 0;
        description = "E-Mail not valid";
        $("#email").addClass("redborder");
    }

    let password = document.getElementById("password").value;
    if(password.length<3){
        valid = 0;
        description = "Password not valid"; 
        $("#password").addClass("redborder");
    }

    if(valid ===1){
        btnState(true, "btnLogin");
        setTimeout(function(){
            console.log("submit");
            $("#frmLogin").submit();
        },200);        

    }else{
        frmErrorMessages(true, 'frmLoginMsg', description);
    }

}

$('#btnLogin').on('click', function(){
    submitloginForm();
});