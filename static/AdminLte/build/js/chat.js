let socket = []
let sock_num = 0

class main_sock extends ReconnectingWebSocket {
    constructor(url) {
        super(url); // Now 'this' is initialized by calling the parent constructor.
    }

    onmessage(e) {
        const data = JSON.parse(e.data);
        if (data.message == 'open_new_socket') {
            socket.push(new sock('ws://' + window.location.host + '/ws/chat/?type=seller_socket', sock_num))
            sock_num = sock_num + 1
        } else {
            console.log(data.message)
        }
    }

    onopen(e) {
        console.log('Main Socket Open')
    }

    onclose(e) {
        console.log('Socket Close')
    }
}


class sock extends ReconnectingWebSocket {
    constructor(url, socket_num) {
        super(url); // Now 'this' is initialized by calling the parent constructor.
        this.socket_num = socket_num
    }

    onmessage(e) {
        const d = new Date();
        const t = d.toLocaleTimeString();
        const data = JSON.parse(e.data);
        console.log(data);
        if (data.message == 'close_socket') {
            this.close();
            $('#chat-body' + this.socket_num).remove();
        } else if (data.message == 'connect_massage') {
            console.log(data.message);
            this.room_name = data.room_name
            this.url = 'ws://127.0.0.1:8000/ws/chat/?type=reconnect&room_name=' + this.room_name
            const chat_box = '<div id="chat-body' + this.socket_num + '" style="float: right !important;" class="col-md-3">\n' +
                '    <div class="card card-primary card-outline direct-chat direct-chat-primary">\n' +
                '        <div class="card-header">\n' +
                '            <h3 class="card-title">' + this.socket_num + '</h3>\n' +
                '            <div class="card-tools">\n' +
                '                <button type="button" class="btn btn-tool" data-card-widget="collapse">\n' +
                '                    <i class="fas fa-minus"></i>\n' +
                '                </button>\n' +
                '            </div>\n' +
                '        </div>\n' +
                '        <div class="card-body">\n' +
                '            <div id="chat-box' + this.socket_num + '" class="direct-chat-messages"></div>\n' +
                '        </div>\n' +
                '        <div class="card-footer">\n' +
                '            <div class="input-group">\n' +
                '                <input type="text" onkeyup="massage(event,this)" id="message' + this.socket_num + '" socket_num="' + this.socket_num + '" placeholder="Type Message ..." class="form-control">\n' +
                '                <span class="input-group-append"><button onclick="send_massage(this)" id="send' + this.socket_num + '" socket_num="' + this.socket_num + '" class="btn btn-primary">Send</button></span>\n' +
                '            </div>\n' +
                '        </div>\n' +
                '    </div>\n' +
                '</div>'
            $('#chat_row').append(chat_box)
        } else if (data.sender == 'seller') {
            const div = '<div class="direct-chat-msg right">\n' +
                '            <div class="direct-chat-infos clearfix">\n' +
                '                <span class="direct-chat-name float-right">' + name + '</span>\n' +
                '                <span class="direct-chat-timestamp float-left">' + t + '</span>\n' +
                '            </div>\n' +
                '            <img class="direct-chat-img" src="' + image + '"\n' +
                '                 alt="Message User Image">\n' +
                '            <div class="direct-chat-text">\n' + data.message +
                '            </div>\n' +
                '        </div>\n'
            $('#chat-box' + this.socket_num).append(div)
            $('#chat-box' + this.socket_num).scrollTop($('#chat-box' + this.socket_num).prop("scrollHeight"));
        } else if (data.sender == 'customer') {
            const div = '<div class="direct-chat-msg">\n' +
                '            <div class="direct-chat-infos clearfix">\n' +
                '                <span class="direct-chat-name float-left">Customer</span>\n' +
                '                <span class="direct-chat-timestamp float-right">' + t + '</span>\n' +
                '            </div>\n' +
                '            <img class="direct-chat-img" src="https://img.icons8.com/color/36/000000/administrator-male.png"\n' +
                '                 alt="Message User Image">\n' +
                '            <div class="direct-chat-text">\n' + data.message +
                '            </div>\n' +
                '        </div>'
            $('#chat-box' + this.socket_num).append(div)
            $('#chat-box' + this.socket_num).scrollTop($('#chat-box' + this.socket_num).prop("scrollHeight"));
        }

    }

    onopen(e) {
        console.log('Socket Open')
        console.log(this.socket_num)
    }

    onclose(e) {
        console.log('Socket Close')
    }
}

let main = new main_sock('ws://' + window.location.host + '/ws/chat/?type=main_seller');
socket[0] = new sock('ws://' + window.location.host + '/ws/chat/?type=seller_socket', sock_num);
sock_num = sock_num + 1

$('#massage').keyup(function (e) {
    if (e.keyCode == 13) {
        if ($(this).val() != '') {
            socket[$(this)].send(JSON.stringify({
                'message': $(this).val()
            }));
            $(this).val('');
        }
    }
});

function massage(e, input) {
    if (e.keyCode == 13) {
        const socket_num = input.getAttribute("socket_num");
        const message = input.value;
        socket[socket_num].send(JSON.stringify({
            'message': message
        }));
        input.value = '';
    }
}

function send_massage(btn) {
    const socket_num = btn.getAttribute("socket_num");
    const message = $('#message' + socket_num);
    socket[socket_num].send(JSON.stringify({
        'message': message.val()
    }));
    message.val('');
}