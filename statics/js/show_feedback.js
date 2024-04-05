function change_placeholder(e) {
    var form_input = document.querySelector('.form-input');
    if (e.value == 'time') {
        form_input.setAttribute('placeholder', '请输入时间');
    } else if (e.value == 'state') {
        form_input.setAttribute('placeholder', '请输入状态');
    } else if (e.value == 'ord') {
        form_input.setAttribute('placeholder', '请输入订单号');
    } else {
        form_input.setAttribute('placeholder', '请输入反馈号');
    }
}

function feedback_show_all() {
    // 点击按钮时跳转到相应的链接
    window.location.href = '../showFeedback';
}

function show_mine() {
    window.location.href = '../mineStation';
}

function send_mail() {
    // value是textarea中输入的内容，innerHTML和innvalueerText都不可
    // 47行获取的是dom对象的value，48行获取的是jquery对象
    var text = $('#mail-send')[0].value;
    var mailForm = $('#mail-form');
    var action = 'mailto:644046570@qq.com?subject=来自菜鸟驿站&body=' + text;
    // attr是针对jquery对象的
    mailForm.attr('action', action);
}