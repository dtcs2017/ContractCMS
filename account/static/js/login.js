$(document).ready(function () {
    let label = $('label');
    $(".form-group input").addClass('form-input');
    label.addClass('form-label');
    $('input[name="email"]').attr('required', true);
    $("label[for='id_username']").text('用户名：');
    $("label[for='id_email']").text('电子邮件：');
    $("label[for='id_password']").text('密码：');
    $("label[for='id_password2']").text('重复密码：');
    label.addClass('text-primary');
    label.addClass('text-left');
    $("ul.errorlist").text('用户名密码错误或未激活用户');
});
