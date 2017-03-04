$(document).ready(function() {

	// Generate button clicked
	$('#btnGenerate').on('click', function() {
		// Get barcode values split by newlines
		var barcode_values = $('#textBarcodes').val();
		
		// Current URL
		var url = window.location.protocol + '//' + window.location.host + '/';
	
		// Start building generation URL
		if (barcode_values.length > 0) {
			barcode_values = barcode_values.split('\n');
			url += '?';
		
			for(var i = 0; i < barcode_values.length; i++) {
				url += 'b[]=' + barcode_values[i] + '&';
			}

			// Remove the final '&'' from the url
			url = url.slice(0, -1);

			// Set the URL
			window.location.href = url;
		}
	});

	// PDF button clicked
	$('#btnPdf').on('click', function() {
		var url = window.location.protocol + '//' + window.location.host + '/pdf?'
			+ window.location.search;

			window.location.href = url;
	});
});