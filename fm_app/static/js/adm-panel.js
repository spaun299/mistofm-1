/**
 * Created by apple on 09.10.17.
 */
$(document).ready(function() {

    var loading = $('.loading');
    var curSubmit = $(".submit-row .btn-primary, .submit-row .btn-default");

    curSubmit.on('click', function (e) {
        loading.toggleClass('play')
    });
});