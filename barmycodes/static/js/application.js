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
		// Set the url value
		var url = window.location.protocol + '//' + window.location.host + '/pdf'
			+ window.location.search;

		// Add custom sizes to the url
		var measurement = $('#pdfUnit').val();

		if (measurement != 'auto') {
			var width = $('#pdfWidth').val();
			var height = $('#pdfHeight').val();

			if (width != '' || height != '') {
				url += '&measurement=' + measurement;
			}

			if (width != '') {
				url += '&width=' + width;
			}

			if (height != '') {
				url += '&height=' + height;
			}
		}

		// Change the url
		window.location.href = url;
	});

	// PDF export measurement listener
	$('#pdfUnit').on('change', function() {
		var select = $(this);

		if (select.val() != 'auto') {
			$('.pdf-export-dimensions').show();
		} else {
			$('.pdf-export-dimensions').hide();
		}
	});
});