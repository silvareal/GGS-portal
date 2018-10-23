
$(document).ready(function() {
	$('#student').DataTable({

		responsive: true,
		"processing": true,
		'serverSide': true,
		'ajax': 'api/student/?format=datatables',
		'columns': [

			// Get the student data in json format 
			{'data': 'students.user.username', 'username': 'user.user.username'},
			{'data': 'students.first_name'},
			{'data': 'students.last_name'},
			{'data': 'parents_or_guidian_number'},
			{'data': 'class_name.class_name'},
			{'data': 'year_of_reg'},
		]

	});
});

$(document).ready(function() {
	$('#student_payment').DataTable({
		"columnDefs": [
			{ "searchable": false,
			"orderable": false,
			 "targets": 6
			}
		  ],
		responsive: true,
		"processing": true,
		'serverSide': true,
		'ajax': 'api/student_payment/?format=datatables',
		'columns': [
			{'data': 'students.students.username'},
			{'data': 'sessions.sessions', 'session': 'sessions.sessions'},
			{'data': 'class_name.class_name'},
			{'data': 'payment_completed'},
			{'data': 'school_fees'},
			{'data': 'paid'},
            {'data': 'balance'},
            {'data': 'date_of_payment'},
		]

	});
});
