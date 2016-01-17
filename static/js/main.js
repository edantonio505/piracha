$(".alert").fadeOut(5000);


$("#submit").click(function(e){
	var username = $("#username").val();
	var email = $("#email").val();
	var password = $("#password").val();
	var idea_name = $("#idea_name").val();
	var brief = $("#brief").val();
	var description = $("#description").val();
	var admin = $("#admin").val();


	if(username == '' || email == '' || password == '' || idea_name == '' || brief == '' || description == '' || admin == ''){
		$("#alert").fadeIn();
		return false;
	}
});