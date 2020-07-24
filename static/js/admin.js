var Admin = {}

/*
################################################################################################
MANAGE POSTS
################################################################################################
*/
Admin.post = {}
Admin.post.create = function(){

    var t = confirm("POST CREATION\nDo you confirm?");
    if(t){

        document.location.href = '/admin/post/create';

    }

}

Admin.post.view = function(id){

    document.location.href = '/admin/post/' + id;

}

Admin.post.save = function(){

    var valid = 1, description;
    $('#frmLoginMsg').addClass("hidden");
    $("input, selected").removeClass("redborder");

    var title = document.getElementById("title").value;
    if(title.length===0){
        valid = 0;
        description = "Title is requested";
        $("#title").addClass("redborder");
    }

    var url = document.getElementById("url").value;
    if(url.length === 0){
        valid = 0;
        description = "You cannot publish this post without a valid URL";
    }

    var is_visible = parseInt($("#is_visible option:selected").val());
    if(is_visible === 1){



    }

    // devo popolare una hidden con il testo della textbox
    document.getElementById("editor_html").value = $("#editor").find("div.ql-editor").html();

    if(valid === 1){

        $("#frm1").submit();

    }else{
        $('#frmLoginMsg').html(description).removeClass("hidden");
    }

}

Admin.post.delete = function(id){

    var t = confirm("POST DELETE\nYou are deleting the post with id ["+id+"]\nDo you confirm?");
    if(t){

        // call Flask to create and return JSON when finished with [post_id]
        // go to post_manage [post_id]
        document.location.href = '/admin/post/delete?id=' + id;

    }

}

Admin.post.load_content = function(quill, id){

    $.ajax({
        url: "/admin/post_content/" + id,
        type: "GET"
    }).done(function(data){
        console.log("load_content", data);
        if(data.html){
            quill.clipboard.dangerouslyPasteHTML(0,data.html);
        }
    })

}



/*
################################################################################################
MANAGE PAGES
################################################################################################
*/

Admin.page = {}

Admin.page.delete = function(id){

    var t = confirm("PAGE DELETE\nYou are deleting the page with id ["+id+"]\nDo you confirm?");
    if(t){

        // call Flask to create and return JSON when finished with [post_id]
        // go to post_manage [post_id]
        document.location.href = '/admin/pages/delete?id=' + id;

    }

}

Admin.page.create = function(){

    var t = confirm("PAGE CREATION\nDo you confirm?");
    if(t){

        document.location.href = '/admin/pages/create';

    }

}

Admin.page.view = function(id){

    document.location.href = '/admin/pages/' + id;

}

Admin.page.load_content = function(quill, id){

    $.ajax({
        url: "/admin/page_content/" + id,
        type: "GET"
    }).done(function(data){
        console.log("load_content", data);
        if(data.html){
            quill.clipboard.dangerouslyPasteHTML(0,data.html);
        }
    })

}

Admin.page.save = function(){

    var valid = 1, description;
    $('#frmLoginMsg').addClass("hidden");
    $("input, selected").removeClass("redborder");
    
    var locked = parseInt(document.getElementById("locked").value);

    if(locked === 0){

        var title = document.getElementById("title").value;
        if(title.length===0){
            valid = 0;
            description = "Title is requested";
            $("#title").addClass("redborder");
        }

        var url = document.getElementById("url").value;
        if(url.length === 0){
            valid = 0;
            description = "You cannot publish this post without a valid URL";
        }

    }

    // devo popolare una hidden con il testo della textbox
    document.getElementById("editor_html").value = $("#editor").find("div.ql-editor").html();

    if(valid === 1){

        $("#frm1").submit();

    }else{
        $('#frmLoginMsg').html(description).removeClass("hidden");
    }

}


/*
################################################################################################
MANAGE USERS
################################################################################################
*/

Admin.user = {}
Admin.user.create = function(){

    var t = confirm("USER CREATION\nDo you confirm?");
    if(t){

        document.location.href = '/admin/users/create';

    }

}

Admin.user.delete = function(id){

    var t = confirm("USER DELETE\nYou are deleting the user with id ["+id+"]\nDo you confirm?");
    if(t){

        // call Flask to create and return JSON when finished with [post_id]
        // go to post_manage [post_id]
        document.location.href = '/admin/users/delete?id=' + id;

    }

}

Admin.user.view = function(id){

    document.location.href = '/admin/users/' + id;

}


Admin.user.save = function(){

    var valid = 1, description;
    $('#frmLoginMsg').addClass("hidden");
    $("input, selected").removeClass("redborder");


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

    let name = document.getElementById("name").value;
    if(name.length === 0){
        valid = 0;
        description = "Name cannot be empty";
        $("#name").addClass("redborder");
    }

    let password = document.getElementById("password").value;
    let password2 = document.getElementById("password2").value;

    if(password.length > 0 || password2.length > 0){

        if(password.length < 5){
            valid = 0;
            description = "Password cannot be less than 5 characters";
            $("#password").addClass("redborder");
        }

        if(password !== password2){
            valid = 0;
            description = "Confirmed password is different: pay attention!";
            $("#password, #password2").addClass("redborder");
        }   

    }

    if(valid === 1){

        $("#frm1").submit();

    }else{
        $('#frmLoginMsg').html(description).removeClass("hidden");
    }


}

/*
################################################################################################
MANAGE PROFILE
################################################################################################
*/

Admin.profile = {}

Admin.profile.save = function(){

    var valid = 1, description;
    $('#frmLoginMsg').addClass("hidden");
    $("input, selected").removeClass("redborder");
    
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

    let name = document.getElementById("name").value;
    if(name.length === 0){
        valid = 0;
        description = "Name cannot be empty";
        $("#name").addClass("redborder");
    }

    let password = document.getElementById("password").value;
    let password2 = document.getElementById("password2").value;

    console.log("password", password);
    console.log("password2", password2);

    if(password.length > 0 || password2.length > 0){

        if(password.length < 5){
            valid = 0;
            description = "Password cannot be less than 5 characters";
            $("#password").addClass("redborder");
        }

        if(password !== password2){
            valid = 0;
            description = "Confirmed password is different: pay attention!";
            $("#password, #password2").addClass("redborder");
        }   

    }

    

    if(valid === 1){
        $("#frm1").submit();
    }else{
        $('#frmLoginMsg').html(description).removeClass("hidden");
    }

}

/*
################################################################################################
FUNCS
################################################################################################
*/
var title_to_url = function(){

    var title = document.getElementById('title').value.trim();
    var regex = /([^A-Za-z ])/g;
    var url = title.replace(regex,"").toLowerCase().replace(/ /g,"-");

    // check for eventual - chars at the string end
    var lock_status = parseInt($("#url_locked:checked").val());
    if(lock_status===1){
        document.getElementById("url").value = url;
    }

}

var status_locker = function(){
    var lock_status = parseInt($("#url_locked:checked").val());
    if(lock_status === 1){
        $("#url").prop("disabled", false);
    }else{
        $("#url").prop("disabled", true);
    }
}

$("#lock-container input").click(function(){

    var lock_status = parseInt($(this).val());
    console.log("url_locked: ", lock_status);
    status_locker();

});



var editor, quill;
// if #editor is in page, let's substitute
$(document).ready(function(){

    // if EDITOR is in page, let's substitute with QUILL
    if($("#editor").length!==0){
        quill = new Quill('#editor', {
            theme: 'snow'
        });



    }

    // if keyup on TITLE, try to create URL
    $( "#title" ).keyup(function() {
        title_to_url();
    });

    // check lock status
    status_locker();


})

