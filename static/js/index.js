var random_name=Math.random().toString(36).substr(10)
var msg=""
var user=""
var socket = null
socket=io.connect('http://' + document.domain + ':' + location.port);

socket.on('res', function (msg) {
    var name_in=htmlEncodeJQ(msg.name)
    var msg_in=htmlEncodeJQ(msg.data)
    if(name_in==user){
         $('#chat-messages').append('<div class="message right ">' +'<span class="name_tag_right">'+name_in+'</span >'+'<div class="bubble data_msg">'+msg_in+'</div>'+'</div>')

        $('#chat-messages').scrollTop($('#chat-messages')[0].scrollHeight);

    }
    else {
        document.getElementById('chat-messages').innerHTML += `
        <div class="message">
                    <span class="name_tag_left " >${name_in}</span>
                    <div class="bubble data_msg">${msg_in}
                    </div>
                </div>
        `
    }


});

$("#send").click(function() {
    sendMessage()
})

$("#message").attr("value",random_name)
$("#message").click(function () {
    $("#message").attr("value","")
})

$('#message_content').bind('keyup',function (event) {
    if(event.keyCode=='13'){
        $('#send').click(sendMessage())
    }
});

function htmlEncodeJQ(str){
    return $('<span/>').text(str).html();
}

function sendMessage(){
    msg=$('#message_content').val()
    socket.emit("client_event",{data:msg,name:user});
    $('#message_content').val("")
}

function enterChat(){
    
    if($("#message").val()==""){
        user=random_name
    }else{
        user=$("#message").val()
    }
    console.log("enter:"+user)
    socket.emit("register_client",{name:user})
    object=$('#enter_chat')
    var childOffset = object.offset();
    var parentOffset = object.parent().parent().offset();
    var childTop = childOffset.top - parentOffset.top;
    var clone = object.clone();
    var top = childTop + 12 + 'px';
    $(clone).css({ 'top': top }).addClass('floatingImg').appendTo('#chatbox');
    setTimeout(function () {
        $('#profile p').addClass('animate');
        $('#profile').addClass('animate');
    }, 100);
    setTimeout(function () {
        $('#chat-messages').addClass('animate');
        $('.cx, .cy').addClass('s1');
        setTimeout(function () {
            $('.cx, .cy').addClass('s2');
        }, 100);
        setTimeout(function () {
            $('.cx, .cy').addClass('s3');
        }, 200);
    }, 150);
    $('.floatingImg').animate({
        'width': '70px',
        'height':'70px',
        'left': '50%',
        'top': '20px'
    }, 200);
    var name = object.find('p strong').html();
    var email = object.find('p span').html();
    $('#profile p').html(name);
    $('#profile span').html(email);
    $('.message').not('.right').find('img').attr('src', $(clone).attr('src'));
    $('#friendslist').fadeOut();
    $('#chatview').fadeIn();
    $('#close').unbind('click').click(function () {
        $('#chat-messages, #profile, #profile p').removeClass('animate');
        $('.cx, .cy').removeClass('s1 s2 s3');
        $('.floatingImg').animate({
            'width': '40px',
            'top': top,
            'left': '12px'
        }, 200, function () {
            $('.floatingImg').remove();
        });
        setTimeout(function () {
            $('#chatview').fadeOut();
            $('#friendslist').fadeIn();
        }, 50);
    });
}



$(document).ready(function () {

    var preloadbg = document.createElement('img');
    preloadbg.src = '../static/img/timeline1.png';

    $('#sendmessage input').focus(function () {
        if ($(this).val() == '') {
            $(this).val('');
        }
    });
    $('#sendmessage input').focusout(function () {
        if ($(this).val() == '') {
            $(this).val('');
        }
    });
    $('#enter_chat').click(function () {
        enterChat()
        });
    });