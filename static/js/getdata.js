$(document).ready(function() {

	$('form').on('submit', function(event) {

		$.ajax({
			data : {
				issue_no : $('#issue_no').val()
			},
			type : 'POST',
			url : '/processdata'
		})
		.done(function(data) {

			if (data.error) {
				$('#errorAlert').text(data.error).show();
				$('#successAlert').hide();
			}
			else {
				$('#successAlert').text(data.issue_no).show();
				$('#errorAlert').hide();
			}

		});

		event.preventDefault();

	});

});