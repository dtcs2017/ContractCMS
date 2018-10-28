// 消息框在底部中央，5秒钟后消失

let message = $('.message');
message.css({bottom: '10%', width: '30%'});
let viewWidth = $(window).width();
let messageWidth = message.width();
let leftPixel = (viewWidth - messageWidth) / 2;
message.css({'right': leftPixel});

$(window).resize(function () {

    let viewWidth = $(window).width();
    let messageWidth = message.width();
    let leftPixel = (viewWidth - messageWidth) / 2;
    message.css({'right': leftPixel})
});

setTimeout(function () {
    $('.message').fadeOut('slow');
}, 5000);