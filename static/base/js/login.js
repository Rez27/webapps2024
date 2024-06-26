$(document).ready(function () {

    'use strict';

    // Detect browser for css purpose
    if (navigator.userAgent.toLowerCase().indexOf('firefox') > -1) {
        $('.form form label').addClass('fontSwitch');
    }

    // Label effect
    $('input').focus(function () {

        $(this).siblings('label').addClass('active');
    });

    // Form validation
    $('input').blur(function () {

        // label effect
        if ($(this).val().length > 0) {
            $(this).siblings('label').addClass('active');
        } else {
            $(this).siblings('label').removeClass('active');
        }
    });


    // form switch
    $('a.switch').click(function (e) {
        $(this).toggleClass('active');
        e.preventDefault();
        //
        // if ($('a.switch').hasClass('active')) {
        //     $(this).parents('.form-piece').addClass('switched').siblings('.form-piece').removeClass('switched');
        // } else {
        //     $(this).parents('.form-piece').removeClass('switched').siblings('.form-piece').addClass('switched');
        // }
    });


    // Form submit
    $('form.signup-form').submit(function (event) {
        // event.preventDefault();
        $('.signup, .login').addClass('switched');

        setTimeout(function () { $('.signup, .login').hide(); }, 700);
        setTimeout(function () { $('.brand').addClass('active'); }, 300);
        setTimeout(function () { $('.heading').addClass('active'); }, 600);
        setTimeout(function () { $('.success-msg p').addClass('active'); }, 900);
        setTimeout(function () { $('.success-msg a').addClass('active'); }, 1050);
        setTimeout(function () { $('.form').hide(); }, 700);

    });

    // Reload page
    $('a.profile').on('click', function () {
        location.reload(true);
    });


});
