// Categories
$(".categories-owl").each(function(){
    $(this).owlCarousel({
    autoplay: true,
    autoplayhoverpause: true,
    autoplaytimeout: 100,
    items:4,
    nav: false,
    loop: true,
    lazyLoad: true,
    responsive: {
        240 : {
            items: 2,
            dots: false,
            nav: false,
        },
        485 : {
            items: 2,
            dots: false,
            nav: false,
        },
        728 : {
            items: 3,
            dots: false,
            nav: false,
        },
        1025 : {
            items: 5,
        }
    }
});
}); 

// Latest Books
$(".latest-books-owl").owlCarousel({
    autoplay: true,
    autoplayhoverpause: true,
    autoplaytimeout: 100,
    items:4,
    nav: false,
    loop: true,
    lazyLoad: true,
    responsive: {
        240 : {
            items: 2,
            dots: false,
            nav: false,
        },
        485 : {
            items: 2,
            dots: false
        },
        728 : {
            items: 3,
            dots: false
        },
        1025 : {
            items: 5,
        }
    }
});

// Popular Books
$(".popular-books-owl").owlCarousel({
    autoplay: true,
    autoplayhoverpause: true,
    autoplaytimeout: 100,
    items:4,
    nav: false,
    loop: true,
    lazyLoad: true,
    responsive: {
        240 : {
            items: 2,
            dots: false,
            nav: false,
        },
        485 : {
            items: 2,
            dots: false
        },
        728 : {
            items: 3,
            dots: false
        },
        1025 : {
            items: 5,
        }
    }
});
