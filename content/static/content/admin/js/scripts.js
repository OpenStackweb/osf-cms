$('#slug-form').submit(function(e) {
    window.location.replace( $('select[name="header-select"]').val());
    e.preventDefault();
    return false;
});
