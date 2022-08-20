
var DOMAIN_FRONTEND = 'http://127.0.0.1:5500/frontend'
var DOMAIN_BACKEND = 'http://127.0.0.1:9005'
// var DOMAIN_FRONTEND = 'http://jasonisgod.xyz/chatdisplay'
// var DOMAIN_BACKEND = 'http://jasonisgod.xyz:9005'

const queryString = window.location.search
const urlParams = new URLSearchParams(queryString)

var VID = urlParams.get('vid') || '' //'PTUafmTYrsA'
var LIMIT = urlParams.get('limit') || 50
var POLL = urlParams.get('poll') || 1000
var SIZE = urlParams.get('size') || 30
var DELAY = urlParams.get('delay') || 0 
var CONSOLE = urlParams.get('console') || "0" 

function getData() {
    var url = DOMAIN_BACKEND + '/api/data'
    var data = { 'vid': VID, 'limit': LIMIT, 'console':CONSOLE }
    $.get(url, data, function(res) {
        $("#chat-box").html(res)
        updateScroll()
        updateSize()
    });
}

function updateScroll(){
    var element = $("#chat-box")
    element.scrollTop = element.scrollHeight
}

function updateSize() {
    // $('.author').css('font-size', SIZE + 'px')
    // $('.emoji').css('width', SIZE + 'px')
    // $('.text').css('font-size', SIZE + 'px')
}

function getStart() {
    var VID = $("#vid").val()
    var LIMIT = $("#limit").val()
    var SIZE = $("#size").val()
    var POLL = $("#poll").val()
    var DELAY = $("#delay").val()
    var CONSOLE = $("#console").val()
    var url = 'index.html?vid=' + VID + '&limit=' + 
        LIMIT + '&size=' + SIZE + '&poll=' + POLL + '&delay=' + DELAY + '&console=' + CONSOLE
    window.location.href = url
}
            
function sendPublicMsg() {
    var publicMsg = $('#public-msg').val()
    $('#public-msg').val('')
    setTimeout(function() {
        var url = DOMAIN_BACKEND + '/api/add'
        var data = {
            'author': $('#author').val() || '???',
            'content': publicMsg || '???',
            'type': 'public'
        }
        $.get(url, data)
    }, DELAY)
}

function sendPrivateMsg() {
    var privateMsg = $('#private-msg').val()
    $('#private-msg').val('')
    setTimeout(function() {
        var url = DOMAIN_BACKEND + '/api/add'
        var data = {
            'author': '',
            'content': privateMsg || '???',
            'type': 'private'
        }
        $.get(url, data)
    }, DELAY)
}

function sendReset() {
    var url = DOMAIN_BACKEND + '/api/reset'
    $.get(url)
    $('#reset-span').hide();
}

function tryReset() {
    $('#reset-span').show();
}

function cancelReset() {
    $('#reset-span').hide();
}

function copyToClipboard(text) {
    var sampleTextarea = document.createElement("textarea");
    document.body.appendChild(sampleTextarea);
    sampleTextarea.value = text; //save main text in it
    sampleTextarea.select(); //select textarea contenrs
    document.execCommand("copy");
    document.body.removeChild(sampleTextarea);
}

function copyUrl() {
    copyToClipboard($('#url').val());
}

function clickBack() {
    window.location.href = 'index.html'
}

$(document).on('keypress', function(e) {
    if(e.which == 13 && VID != '') {
        if ($("#public-msg").is(":focus")) sendPublicMsg()
        if ($("#private-msg").is(":focus")) sendPrivateMsg()
    }
});

$(() => {
    if (VID == '') {
        $('#setup-box').show()
    } else {
        var root = document.querySelector(':root');
        root.style.setProperty('--SIZE', SIZE + 'px');
        setInterval(getData, POLL)
        $('#chat-box').show()
        if (CONSOLE == "1") {
            var url = 'index.html?vid=' + VID + '&limit=' + LIMIT + '&size=' + SIZE + '&poll=' + POLL
            $('#url').val(DOMAIN_FRONTEND + '/' + url)
            $('#console-box').show()
        }
    }
})
