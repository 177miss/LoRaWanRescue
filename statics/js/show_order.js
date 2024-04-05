function del_order() {
    if (confirm('确定删除吗？')) {
        // 点击确认则返回true，执行提交表单的操作，数据被删除
        return true;
    } else {
        return false;
    }
}

// 使得更改订单信息时不能修改其队别
function alt_order(e) {
    $('#id_team').attr('value', e.value);
    $('#id_team').attr('readonly', 'readonly');
}

function change_placeholder(e) {
    var opt_srch = document.querySelector('opt-srch');
    var form_input = document.querySelector('.form-input');
    if (e.value == 'idstu') {
        form_input.setAttribute('placeholder', '请输入学号');
    } else if (e.value == 'shf') {
        form_input.setAttribute('placeholder', '请输入货架号');
    } else {
        form_input.setAttribute('placeholder', '请输入订单号');
    }
}

function order_show_all() {
    // 点击按钮时跳转到相应的链接
    window.location.href = '../showOrder';
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