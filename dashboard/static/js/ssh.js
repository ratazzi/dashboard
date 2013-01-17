$(document).ready(function() {
    $('a.delete-ssh-key').click(function() {
        var row = $(this).parents('tr');
        var fingerprint = $(this).attr('rel');
        var data = {fingerprint: fingerprint};
        $.post('/settings/ssh/key/delete', data, function(resp) {
            if (resp.status == 0) {
                row.remove();
            }
        }, 'json');
    });
});
