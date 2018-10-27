// 消息框固定在顶部，8秒钟后消失
$(window).resize(function () {
    let message = $('.message');
    let viewWidth = $(window).width();
    let messageWidth = message.width();
    let leftPixel = (viewWidth - messageWidth)/2;
    message.css({'left':leftPixel})
});

setTimeout(function () {
    $('.message').fadeOut('slow');
},6000);