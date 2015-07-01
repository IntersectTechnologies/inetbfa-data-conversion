var APP = APP || {};

APP.notify = function (notice) {

    newNotice = function () {
        return '<div class="alert" hidden="true"><button type="button" class="close" data-dismiss="alert">&times;</button>';
    };

    if (notice.type === 'warning') {
        $('#notice').html('').append(newNotice());
        $('#notice .alert').append("<strong>Warning! </strong>" + notice.message);
    }
    else if (notice.type === 'error') {
        $('#notice').html('').append(newNotice());
        $('#notice .alert').append("<strong>Error! </strong>" + notice.message).addClass('alert-error');
    }
    else if (notice.type === 'success') {
        $('#notice').html('').append(newNotice());
        $('#notice .alert').append("<strong>Success! </strong>" + notice.message).addClass('alert-success');
    }
    else if (notice.type === 'info') {
        $('#notice').html('').append(newNotice());
        $('#notice .alert').append("<strong>Info: </strong>" + notice.message).addClass('alert-info');
    }

    // now show
    $('#notice .alert').prop('hidden', false);
};
