/*
 * ex00 - login and logout over AJAX only.
 *
 * Both handlers are bound to `document` rather than to the form itself: the
 * forms are swapped out of the DOM on every state change, so a handler bound
 * directly to a form would die with it. The page itself is never reloaded.
 */
(function ($) {
    "use strict";

    var $state = $("#account-state");

    // Replace the current state with the markup the server rendered for the
    // new one. This is the only thing that ever changes the page.
    function render(html) {
        $state.html(html);
    }

    $(document).on("submit", "#login-form", function (event) {
        event.preventDefault();

        var $form = $(this);

        $.ajax({
            type: "POST",
            url: $form.attr("action"),
            data: $form.serialize(),
            dataType: "json"
        }).done(function (response) {
            // On success this is the "Logged as <user>" markup; on failure it
            // is the same form re-rendered with its validation errors.
            render(response.html);
        }).fail(function () {
            window.alert("Login request failed. Is the server still running?");
        });
    });

    $(document).on("submit", "#logout-form", function (event) {
        event.preventDefault();

        var $form = $(this);

        $.ajax({
            type: "POST",
            url: $form.attr("action"),
            data: $form.serialize(),
            dataType: "json"
        }).done(function (response) {
            render(response.html);
        }).fail(function () {
            window.alert("Logout request failed. Is the server still running?");
        });
    });
}(jQuery));
