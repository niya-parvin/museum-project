$(document).ready(function() {
    "use strict";

    // Set window dimensions and header heights
    var window_width = $(window).width(),
        window_height = window.innerHeight,
        header_height = $(".default-header").height(),
        header_height_static = $(".site-header.static").outerHeight(),
        fitscreen = window_height - header_height;

    $(".fullscreen").css("height", window_height);
    $(".fitscreen").css("height", fitscreen);

    // Initialize niceSelect for dropdowns
    if (document.getElementById("default-select")) {
        $('select').niceSelect();
    }

    // Initialize Magnific Popup for images
    $('.img-pop-up, .single-gallery, .recent-project').magnificPopup({
        type: 'image',
        gallery: {
            enabled: true
        }
    });

    // Initialize Magnific Popup for video
    $('.play-btn').magnificPopup({
        type: 'iframe',
        mainClass: 'mfp-fade',
        removalDelay: 160,
        preloader: false,
        fixedContentPos: false
    });

    // Initiate superfish on nav menu
    $('.nav-menu').superfish({
        animation: {
            opacity: 'show'
        },
        speed: 400
    });

    // Mobile Navigation
    if ($('#nav-menu-container').length) {
        var $mobile_nav = $('#nav-menu-container').clone().prop({
            id: 'mobile-nav'
        });
        $mobile_nav.find('> ul').attr({
            'class': '',
            'id': ''
        });
        $('body').append($mobile_nav);
        $('body').prepend('<button type="button" id="mobile-nav-toggle"><i class="lnr lnr-menu"></i></button>');
        $('body').append('<div id="mobile-body-overly"></div>');
        $('#mobile-nav').find('.menu-has-children').prepend('<i class="lnr lnr-chevron-down"></i>');

        // Toggle submenu on click
        $(document).on('click', '.menu-has-children i', function(e) {
            $(this).next().toggleClass('menu-item-active');
            $(this).nextAll('ul').eq(0).slideToggle();
            $(this).toggleClass("lnr-chevron-up lnr-chevron-down");
        });

        // Toggle mobile navigation
        $(document).on('click', '#mobile-nav-toggle', function(e) {
            $('body').toggleClass('mobile-nav-active');
            $('#mobile-nav-toggle i').toggleClass('lnr-cross lnr-menu');
            $('#mobile-body-overly').toggle();
        });

        // Close mobile navigation when clicking outside
        $(document).click(function(e) {
            var container = $("#mobile-nav, #mobile-nav-toggle");
            if (!container.is(e.target) && container.has(e.target).length === 0) {
                if ($('body').hasClass('mobile-nav-active')) {
                    $('body').removeClass('mobile-nav-active');
                    $('#mobile-nav-toggle i').toggleClass('lnr-cross lnr-menu');
                    $('#mobile-body-overly').fadeOut();
                }
            }
        });
    } else if ($("#mobile-nav, #mobile-nav-toggle").length) {
        $("#mobile-nav, #mobile-nav-toggle").hide();
    }

    // Smooth scroll for the menu and links with .scrollto classes
    $('.nav-menu a, #mobile-nav a, .scrollto').on('click', function() {
        if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
            var target = $(this.hash);
            if (target.length) {
                var top_space = 0;

                if ($('#header').length) {
                    top_space = $('#header').outerHeight();
                    if (!$('#header').hasClass('header-fixed')) {
                        top_space = top_space;
                    }
                }

                $('html, body').animate({
                    scrollTop: target.offset().top - top_space
                }, 1500, 'easeInOutExpo');

                if ($(this).parents('.nav-menu').length) {
                    $('.nav-menu .menu-active').removeClass('menu-active');
                    $(this).closest('li').addClass('menu-active');
                }

                if ($('body').hasClass('mobile-nav-active')) {
                    $('body').removeClass('mobile-nav-active');
                    $('#mobile-nav-toggle i').toggleClass('lnr-times lnr-bars');
                    $('#mobile-body-overly').fadeOut();
                }
                return false;
            }
        }
    });

    // Handle page load with hash
    
    $('html, body').hide();
    if (window.location.hash) {
        setTimeout(function() {
            $('html, body').scrollTop(0).show();
            $('html, body').animate({
                scrollTop: $(window.location.hash).offset().top - 100
            }, 1000);
        }, 0);
    } else {
        $('html, body').show();
    }

    //  Header scroll class
$(window).scroll(function() {
    if ($(this).scrollTop() > 100) {
        $('#header').addClass('header-scrolled');  // Add the 'header-scrolled' class when scrolled
        $('#header-main .nav-menu li.menu-has-children > a').addClass('scrolled'); // Add the 'scrolled' class to the menu items
    } else {
        $('#header').removeClass('header-scrolled');  // Remove the 'header-scrolled' class when back to top
        $('#header-main .nav-menu li.menu-has-children > a').removeClass('scrolled'); // Remove the 'scrolled' class from the menu items
    }
});

    // Carousel initialization
    $('.active-about-carusel').owlCarousel({
        items: 1,
        loop: true,
        margin: 30,
        dots: true
    });

    $('.active-exibition-carusel').owlCarousel({
        items: 3,
        margin: 30,
        autoplay: true,
        loop: true,
        dots: true,
        responsive: {
            0: {
                items: 1
            },
            480: {
                items: 1
            },
            768: {
                items: 2
            },
            900: {
                items: 3
            }
        }
    });

    // Gallery initialization
    var parameters = {
        gridContainer: '#grid-container',
        gridItems: '.grid-item',
        gutter: 15,
        enableImagesLoaded: true
    };
    var grid = new justifiedGrid(parameters);
    $('body').imagesLoaded(function() {
        grid.initGrid();
    });

    // Google Map initialization
    if (document.getElementById("map")) {
        google.maps.event.addDomListener(window, 'load', init);
        function init() {
            var mapOptions = {
                zoom: 11,
                center: new google.maps.LatLng(40.6700, -73.9400), // New York
                styles: [
                    {"featureType": "water", "elementType": "geometry", "stylers": [{"color": "#e9e9e9"}, {"lightness": 17}]},
                    {"featureType": "landscape", "elementType": "geometry", "stylers": [{"color": "#f5f5f5"}, {"lightness": 20}]},
                    {"featureType": "road.highway", "elementType": "geometry.fill", "stylers": [{"color": "#ffffff"}, {"lightness": 17}]},
                    {"featureType": "road.highway", "elementType": "geometry.stroke", "stylers": [{"color": "#ffffff"}, {"lightness": 29}, {"weight": 0.2}]},
                    {"featureType": "road.arterial", "elementType": "geometry", "stylers": [{"color": "#ffffff"}, {"lightness": 18}]},
                    {"featureType": "road.local", "elementType": "geometry", "stylers": [{"color": "#ffffff"}, {"lightness": 16}]},
                    {"featureType": "poi", "elementType": "geometry", "stylers": [{"color": "#f5f5f5"}, {"lightness": 21}]},
                    {"featureType": "poi.park", "elementType": "geometry", "stylers": [{"color": "#dedede"}, {"lightness": 21}]},
                    {"elementType": "labels.text.stroke", "stylers": [{"visibility": "on"}, {"color": "#ffffff"}, {"lightness": 16}]},
                    {"elementType": "labels.text.fill", "stylers": [{"saturation": 36}, {"color": "#333333"}, {"lightness": 40}]},
                    {"elementType": "labels.icon", "stylers": [{"visibility": "off"}]},
                    {"featureType": "transit", "elementType": "geometry", "stylers": [{"color": "#f2f2f2"}, {"lightness": 19}]},
                    {"featureType": "administrative", "elementType": "geometry.fill", "stylers": [{"color": "#fefefe"}, {"lightness": 20}]},
                    {"featureType": "administrative", "elementType": "geometry.stroke", "stylers": [{"color": "#fefefe"}, {"lightness": 17}, {"weight": 1.2}]}
                ]
            };

            var mapElement = document.getElementById('map');
            var map = new google.maps.Map(mapElement, mapOptions);

            var marker = new google.maps.Marker({
                position: new google.maps.LatLng(40.6700, -73.9400),
                map: map,
                title: 'Snazzy!'
            });
        }
    }

    // Mailchimp signup
    $('#mc_embed_signup').find('form').ajaxChimp();

    // // Scanner icon redirect
    // const scannerIcon = document.getElementById('scanner-icon');
    // if (scannerIcon) {
    //     scannerIcon.addEventListener('click', function() {
    //         window.location.href = '/scanner/';  // Redirect to the scanner page
    //     });
    // }

    // Header scroll effect
    const header = document.getElementById('header-main');
    if (header) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 30) {
                header.classList.add('scrolled'); // Add 'scrolled' class when scrolled
            } else {
                header.classList.remove('scrolled'); // Remove 'scrolled' class when not scrolled
            }
        });
    }
});
$(document).ready(function() {
    // Cache selectors
    const $mobileNav = $('#mobile-nav');
    const $mobileNavToggle = $('#mobile-nav-toggle');
    const $body = $('body');

    // Mobile Navigation Toggle
    $mobileNavToggle.on('click', function(e) {
        e.stopPropagation(); // Prevent the click from bubbling up to the document
        $mobileNav.toggleClass('active'); // Toggle the mobile navigation
        $body.toggleClass('mobile-nav-active'); // Toggle body class for styling
        $(this).find('i').toggleClass('lnr-menu lnr-cross'); // Change the icon

        // Update aria-expanded attribute
        const isExpanded = $mobileNav.hasClass('active');
        $mobileNavToggle.attr('aria-expanded', isExpanded);
    });

    // Close mobile nav when clicking or touching outside
    $(document).on('click touchstart', function(e) {
        const container = $mobileNav.add($mobileNavToggle); // Combine selectors
        if (!container.is(e.target) && container.has(e.target).length === 0) {
            if ($body.hasClass('mobile-nav-active')) {
                $body.removeClass('mobile-nav-active'); // Remove body class
                $mobileNav.removeClass('active'); // Hide the mobile navigation
                $mobileNavToggle.find('i').removeClass('lnr-cross').addClass('lnr-menu'); // Reset the icon
                $mobileNavToggle.attr('aria-expanded', 'false'); // Update aria-expanded
            }
        }
    });
});

// scanner icon scroll
window.addEventListener('resize', function() {
    const scannerIcon = document.getElementById('scanner-icon');
    const scannerIconMobile = document.getElementById('scanner-icon-mobile');
    const headerTop = document.getElementById('header-top');
    const headerMain = document.getElementById('header-main');

    if (window.innerWidth <= 768) {
        if (scannerIcon.parentNode === headerTop) {
            headerMain.appendChild(scannerIconMobile);
            scannerIconMobile.style.display = 'inline-block';
            scannerIcon.style.display = 'none';
        }
    } else {
        if (scannerIconMobile.parentNode === headerMain) {
            headerTop.querySelector('.top-head-right').appendChild(scannerIcon);
            scannerIcon.style.display = 'inline-block';
            scannerIconMobile.style.display = 'none';
        }
    }
});

// event carousel scroll
// Initial check on page load
window.dispatchEvent(new Event('resize'));

// For swipe-like scrolling on touch devices
document.addEventListener('DOMContentLoaded', () => {
    const eventsCarousel = document.querySelector('.events-carousel');
    // Reset scroll position to the start
    eventsCarousel.scrollLeft = 0;

    let isDown = false;
    let startX;
    let scrollLeft;

    // Mouse drag for desktop users
    eventsCarousel.addEventListener('mousedown', (e) => {
        isDown = true;
        startX = e.pageX - eventsCarousel.offsetLeft;
        scrollLeft = eventsCarousel.scrollLeft;
    });

    eventsCarousel.addEventListener('mouseleave', () => {
        isDown = false;
    });

    eventsCarousel.addEventListener('mouseup', () => {
        isDown = false;
    });

    eventsCarousel.addEventListener('mousemove', (e) => {
        if (!isDown) return;
        e.preventDefault();
        const x = e.pageX - eventsCarousel.offsetLeft;
        const walk = (x - startX) * 2; // Scroll speed factor
        eventsCarousel.scrollLeft = scrollLeft - walk;
    });

    // For touch devices (mobile/tablets)
    eventsCarousel.addEventListener('touchstart', (e) => {
        isDown = true;
        startX = e.touches[0].pageX - eventsCarousel.offsetLeft;
        scrollLeft = eventsCarousel.scrollLeft;
    });

    eventsCarousel.addEventListener('touchend', () => {
        isDown = false;
    });

    eventsCarousel.addEventListener('touchmove', (e) => {
        if (!isDown) return;
        e.preventDefault();
        const x = e.touches[0].pageX - eventsCarousel.offsetLeft;
        const walk = (x - startX) * 2; // Scroll speed factor
        eventsCarousel.scrollLeft = scrollLeft - walk;
    });
});

// history section image transition
let currentImageIndex = 0;
const images = document.querySelectorAll('#image-container img');

// Ensure the first image is visible
images[currentImageIndex].style.opacity = 1;

function changeImage() {
    // Hide the current image
    images[currentImageIndex].style.opacity = 0;

    // Update index
    currentImageIndex = (currentImageIndex + 1) % images.length;

    // Show the next image
    images[currentImageIndex].style.opacity = 1;
}

// Call the function every 3 seconds
setInterval(changeImage, 3000);

const scannerIcon = document.getElementById('scanner-icon-mobile');

if (scannerIcon) {
    scannerIcon.addEventListener('click', function(event) {
        event.stopPropagation(); // Prevents other elements from interfering
        console.log('Scanner icon clicked');
        openScanner(); // Call your scanner function
    });

    scannerIcon.addEventListener('touchstart', function(event) {
        event.stopPropagation();
        console.log('Scanner icon touched');
        openScanner(); // Call your scanner function
    });
}

function openScanner() {
    alert('Scanner activated'); // Replace with actual scanner logic
}

