var socket = new ReconnectingWebSocket('ws://' + window.location.host + '/ws/chat/', null, {automaticOpen: false});
socket.onmessage = function (e) {
    var d = new Date();
    var t = d.toLocaleTimeString();
    const data = JSON.parse(e.data);
    console.log(data);
    let div;
    if (data.sender == 'customer') {
        div = '<div class="media media-chat media-chat-reverse">\n' +
            '                <div class="media-body">\n' +
            '                    <p>' + data.message + '</p>\n' +
            '                    <p class="meta">\n' +
            '                        <time datetime="2018">' + t + '</time>\n' +
            '                    </p>\n' +
            '                </div>\n' +
            '            </div>'
    } else {
        div = '<div class="media media-chat">\n' +
            '                <img class="avatar"\n' +
            '                     src="https://img.icons8.com/color/36/000000/administrator-male.png"\n' +
            '                     alt="...">\n' +
            '                <div class="media-body">\n' +
            '                    <p>' + data.message + '</p>\n' +
            '                    <p class="meta">\n' +
            '                        <time datetime="2018">' + t + '</time>\n' +
            '                    </p>\n' +
            '                </div>\n' +
            '            </div>'
    }
    $('#chat-content').append(div);
    $('#chat-content').scrollTop($('#chat-content').prop("scrollHeight"));
};
socket.onopen = function (e) {
    console.log('Socket Open')
}
socket.onclose = function (e) {
    console.log('Socket Close')
}

// Attach the event listener
function display_chat() {
    $('#chat-box').show();
    $('#chat-btn').hide();
    socket.open();
}

function hide_chat() {
    $('#chat-box').hide();
    $('#chat-btn').show();
    socket.close();
}

$('#massage').keyup(function (e) {
    if (e.keyCode == 13) {
        if ($(this).val() != '') {
            socket.send(JSON.stringify({
                'message': $(this).val()
            }));
            $(this).val('');
        }
    }
});

function send_massage() {
    const massage = $('#massage')
    if (massage.val() != '') {
        socket.send(JSON.stringify({
            'message': massage.val()
        }));
        massage.val('');
    }
}