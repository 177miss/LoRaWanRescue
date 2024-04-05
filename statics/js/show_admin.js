function position() {
    window.location.href = '../position';
}

// 使得更改管理员信息时不能修改其队别
function alt_admin(e) {
    $('#id_team').attr('value', e.value);
    $('#id_team').attr('readonly', 'readonly');
}

function change_placeholder(e) {
    var opt_srch = document.querySelector('opt-srch');
    var form_input = document.querySelector('.form-input');
    if (e.value == 'IP') {
        form_input.setAttribute('placeholder', '请输入用户');
    } else if (e.value == 'Time') {
        form_input.setAttribute('placeholder', '请输入时间');
    } else {
        form_input.setAttribute('placeholder', '请输入内容');
    }
}

function admin_show_all() {
    // 点击按钮时跳转到相应的链接
    window.location.href = '../showAdmin';
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