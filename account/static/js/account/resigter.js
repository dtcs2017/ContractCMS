$(document).ready(function () {
    $('input[name="email"]').attr('required', true);
    $("label[for='id_username']").text('用户名');
    $("label[for='id_email']").text('电子邮件');
    $("label[for='id_password']").text('密码');
    $("label[for='id_password2']").text('重复密码');
    let errorarea = $('.errorlist');
    errorarea.addClass('no-bullet');
    errorarea.css({'color': 'red'});
});