$(document).ready(function() {
    current = window.location.pathname;
    $('#sidebar .nav li a').each(function() {
        var link = $(this).attr('href');
        if (link.search(current) != -1) {
            $(this).parent().addClass('active').siblings().removeClass('active');
        }
    });
});
