/*
 * ex01-ex04 - the chat client.
 *
 * jQuery is the only library used; the transport is a raw WebSocket (a browser
 * API, not a library). No AJAX request is made from this page.
 */
(function ($) {
    "use strict";

    var $messages = $("#messages");
    var $users = $("#users");
    var $form = $("#chat-form");
    var $input = $("#chat-input");

    var slug = $("#chat-config").data("slug");
    var scheme = window.location.protocol === "https:" ? "wss:" : "ws:";
    var socket = new WebSocket(
        scheme + "//" + window.location.host + "/ws/chat/" + slug + "/"
    );

    // ex04: keep the newest message visible. Called after every append, so the
    // scrollbar always sits at the bottom.
    function scrollToBottom() {
        $messages.scrollTop($messages.prop("scrollHeight"));
    }

    // Appending only ever adds a row: nothing is replaced or reordered, so the
    // message order stays as the server sent it.
    function append($row) {
        $messages.append($row);
        scrollToBottom();
    }

    function appendMessage(username, body) {
        var $row = $("<p>", { "class": "message" });
        // .text() escapes, so a message can never inject markup.
        $row.append($("<span>", { "class": "message-user" }).text(username));
        $row.append(document.createTextNode(" "));
        $row.append($("<span>", { "class": "message-body" }).text(body));
        append($row);
    }

    function appendNotice(text) {
        append($("<p>", { "class": "notice" }).text(text));
    }

    function renderUsers(usernames) {
        $users.empty();
        $.each(usernames, function (_, username) {
            $users.append($("<li>", { "class": "user" }).text(username));
        });
    }

    socket.onmessage = function (event) {
        var data = JSON.parse(event.data);

        if (data.type === "message") {
            appendMessage(data.username, data.body);
        } else if (data.type === "join") {
            appendNotice(data.username + " has joined the chat");
        } else if (data.type === "leave") {
            appendNotice(data.username + " has left the chat");
        } else if (data.type === "users") {
            renderUsers(data.users);
        }
    };

    socket.onclose = function (event) {
        if (event.code === 4401) {
            appendNotice("You must be logged in to join this chat.");
        } else if (event.code === 4404) {
            appendNotice("This chatroom does not exist.");
        } else {
            appendNotice("Disconnected from the chat.");
        }
        $input.prop("disabled", true);
    };

    $form.on("submit", function (event) {
        event.preventDefault();

        var body = $input.val().trim();
        if (!body || socket.readyState !== WebSocket.OPEN) {
            return;
        }

        socket.send(JSON.stringify({ body: body }));
        $input.val("").focus();
    });

    $input.focus();
}(jQuery));
