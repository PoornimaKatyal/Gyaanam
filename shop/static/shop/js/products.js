$(document).ready(function(){	
		alert("i m working!");	
		$("#menu-toggle").on('click', function(e){			
			e.preventDefault();
    		$("#wrapper").toggleClass("menuDisplayed");

		})
	})

	/*$(document).ready(function(){	
		alert("i m working!");
    });*/