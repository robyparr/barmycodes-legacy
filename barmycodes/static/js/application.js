$(document).ready(function() {
  function showError(message) {
    $('#error')
      .html(message)
      .show();
  }

  function hideError() {
    $('#error')
      .html('')
      .hide();
  }

  // Generate button clicked
  $('#btnGenerate').on('click', function() {
    hideError();

    // Get barcode values split by newlines
    var barcode_values = $('#textBarcodes').val();
    var barcode_type = $('#barcodeType').val();
    
    // Current URL
    var url = window.location.protocol + '//' + window.location.host + '/';
  
    // Start building generation URL
    if (barcode_values.length > 0) {
      barcode_values = barcode_values.split('\n');
      url += '?';
    
      for(var i = 0; i < barcode_values.length; i++) {
        url += 'b[]=' + encodeURIComponent(barcode_values[i]) + '&';
      }

      // Set the barcode type
      url += 'type=' + barcode_type;

      ga('send', {
        hitType: 'event',
        eventCategory: 'Barcodes',
        eventAction: 'generate',
        eventLabel: barcode_type,
        eventValue: barcode_values.length
      });
      // Set the URL
      window.location.href = url;
    }
  });
  
  // Ctrl/CMD + Enter pressed in text area
  $('#textBarcodes').on('keydown', function(e) {
    // http://stackoverflow.com/a/36478923
    if ((e.ctrlKey || e.metaKey) && (e.keyCode == 13 || e.keyCode == 10)) {
      $('#btnGenerate').click();
    }
  });

  // PDF button clicked
  $('#btnPdf').on('click', function() {
    hideError();

    // Set the url value
    var url = window.location.protocol + '//' + window.location.host + '/pdf'
      + window.location.search;

    // Add custom sizes to the url
    var measurement = $('#pdfUnit').val();

    if (measurement != 'auto') {
      var barcode_type = $('#barcodeType').val();
      var width = $('#pdfWidth').val();
      var height = $('#pdfHeight').val();

      // Error checking
      if (barcode_type === 'QR' && (width != '' && height != '' && width != height)) {
        showError('QR Codes should have the same width and height.');
        return;
      }

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

    // Open the PDF
    window.open(url, '_blank');
    ga('send', {
      hitType: 'event',
      eventCategory: 'PDF',
      eventAction: 'generate multi',
      eventLabel: measurement
    });
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

  $('.barcode-pdf-link').on('click', function() {
    ga('send', {
      hitType: 'event',
      eventCategory: 'PDF',
      eventAction: 'generate single'
    });
  });

  $('.barcode-png-link').on('click', function() {
    ga('send', {
      hitType: 'event',
      eventCategory: 'PNG',
      eventAction: 'generate single'
    });
  });
});
