/*!
 * Start Bootstrap - Creative v6.0.4 (https://startbootstrap.com/theme/creative)
 * Copyright 2013-2020 Start Bootstrap
 * Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-creative/blob/master/LICENSE)
 */
(function($) {
    "use strict"; // Start of use strict

    // Smooth scrolling using jQuery easing
    $('a.js-scroll-trigger[href*="#"]:not([href="#"])').click(function() {
        if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
            var target = $(this.hash);
            target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
            if (target.length) {
                $('html, body').animate({
                    scrollTop: (target.offset().top - 72)
                }, 1000, "easeInOutExpo");
                return false;
            }
        }
    });

    // Closes responsive menu when a scroll trigger link is clicked
    $('.js-scroll-trigger').click(function() {
        $('.navbar-collapse').collapse('hide');
    });

    // Activate scrollspy to add active class to navbar items on scroll
    $('body').scrollspy({
        target: '#mainNav',
        offset: 75
    });

    // Collapse Navbar
    var navbarCollapse = function() {
        if ($("#mainNav").offset().top > 100) {
            $("#mainNav").addClass("navbar-scrolled");
        } else {
            $("#mainNav").removeClass("navbar-scrolled");
        }
    };
    // Collapse now if page is not at top
    navbarCollapse();
    // Collapse the navbar when page is scrolled
    $(window).scroll(navbarCollapse);

    // Magnific popup calls
    $('#portfolio').magnificPopup({
        delegate: 'a',
        type: 'image',
        tLoading: 'Loading image #%curr%...',
        mainClass: 'mfp-img-mobile',
        gallery: {
            enabled: true,
            navigateByImgClick: true,
            preload: [0, 1]
        },
        image: {
            tError: '<a href="%url%">The image #%curr%</a> could not be loaded.'
        }
    });

    $("#img-dislike").click(function() {
        var value_tmp = $("#img-dislike").val();
        let cookie = document.cookie
        let csrfToken = cookie.substring(cookie.indexOf('=') + 1)
        $.ajax({
            /*ajax it's a function with send a http request to the server in the url @url*/
            type: 'POST',
            url: "../like_dislike/",
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            headers: {
                'X-CSRFToken': csrfToken
            },
            data: JSON.stringify({ "dislike": value_tmp }),

            success: function(response) {
                var text = ""
                if ('text' in response) {
                    text = response.text + " dislike"
                } else {
                    text = response.err
                }
                var div = document.getElementById('div_for_text_like_dislike');
                div.innerHTML = text

            },
            error: function(error) {
                var div = document.getElementById('div_for_text_like_dislike');
                div.innerHTML = "Une erreur dans ajax désolé"
            }
        });
    });
    $("#img-like").click(function() {
        var value_tmp = $("#img-like").val();
        let cookie = document.cookie
        let csrfToken = cookie.substring(cookie.indexOf('=') + 1)
        $.ajax({
            /*ajax it's a function with send a http request to the server in the url @url*/
            type: 'POST',
            url: "../like_dislike/",
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            headers: {
                'X-CSRFToken': csrfToken
            },
            data: JSON.stringify({ "like": value_tmp }),

            success: function(response) {
                var text = ""
                if ('text' in response) {
                    text = response.text + " like"
                } else {
                    text = response.err
                }
                var div = document.getElementById('div_for_text_like_dislike');
                div.innerHTML = text

            },
            error: function(error) {
                var div = document.getElementById('div_for_text_like_dislike');
                div.innerHTML = "Une erreur dans ajax désolé"
            }
        });
    });

})(jQuery); // End of use strict