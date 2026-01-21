// Modal functions
function showModalFilter() {
    const modalContainer = document.getElementById('modal-filter-container');
    const modal = document.querySelector('.modal-filter');

    if (modalContainer && modal) {
        modalContainer.style.display = 'flex';
        setTimeout(() => {
            modal.classList.add('active');
        }, 10);
    }
}

function modalOff() {
    const modalContainer = document.getElementById('modal-filter-container');
    const modal = document.querySelector('.modal-filter');

    if (modal) {
        modal.classList.remove('active');
        setTimeout(() => {
            if (modalContainer) {
                modalContainer.style.display = 'none';
            }
        }, 300);
    }
}

function smoothNavigate(event, url) {
    event.preventDefault();
    document.body.classList.add('fade-out');
    setTimeout(() => {
        window.location.href = url;
    }, 500); // Delay to allow animation
}

// Add CSS animation styles
const style = document.createElement('style');
style.textContent = `
    .testimonial-section {
        opacity: 0;
        transform: translateY(50px);
        transition: all 0.8s ease;
    }

    .testimonial-section.animate-in {
        opacity: 1;
        transform: translateY(0);
    }
`;
document.head.appendChild(style);

// Main initialization function
document.addEventListener('DOMContentLoaded', function() {
    // Initialize paragraph ellipsis
    initializeParagraphEllipsis();

    // Initialize testimonial swiper
    initializeTestimonialSwiper();

    // Initialize scroll animations
    initializeScrollAnimations();

    // Set current year in footer
    setCurrentYear();
});

// Paragraph ellipsis functionality
function initializeParagraphEllipsis() {
    const paragraphs = document.querySelectorAll(".service-paragraph");
    const maxLength = 100;

    paragraphs.forEach(paragraph => {
        const fullText = paragraph.textContent;

        if (fullText.length > maxLength) {
            paragraph.setAttribute('title', fullText);
            const truncatedText = fullText.substring(0, maxLength) + "...";
            paragraph.textContent = truncatedText;
        }
    });
}

// Testimonial Swiper initialization
function initializeTestimonialSwiper() {
    const testimonialSwiperElement = document.querySelector('.testimonialSwiper');

    if (!testimonialSwiperElement) {
        return; // Exit if swiper element doesn't exist
    }

    try {
        const testimonialSwiper = new Swiper('.testimonialSwiper', {
            slidesPerView: 1,
            spaceBetween: 30,
            loop: true,
            autoplay: {
                delay: 5000,
                disableOnInteraction: false,
            },
            pagination: {
                el: '.testimonial-pagination',
                clickable: true,
                dynamicBullets: true,
            },
            navigation: {
                nextEl: '.testimonial-btn-next',
                prevEl: '.testimonial-btn-prev',
            },
            breakpoints: {
                640: {
                    slidesPerView: 1,
                    spaceBetween: 20,
                },
                768: {
                    slidesPerView: 2,
                    spaceBetween: 30,
                },
                1024: {
                    slidesPerView: 3,
                    spaceBetween: 40,
                },
            },
            effect: 'slide',
            speed: 800,
            grabCursor: true,
            watchSlidesProgress: true,
            on: {
                init: function () {
                    // Add fade-in animation to cards
                    this.slides.forEach((slide, index) => {
                        slide.style.opacity = '0';
                        slide.style.transform = 'translateY(50px)';
                        setTimeout(() => {
                            slide.style.transition = 'all 0.6s ease';
                            slide.style.opacity = '1';
                            slide.style.transform = 'translateY(0)';
                        }, index * 100);
                    });
                },
                slideChange: function () {
                    // Add gentle scale animation on slide change
                    this.slides.forEach(slide => {
                        const card = slide.querySelector('.testimonial-card');
                        if (card) {
                            card.style.transform = 'scale(0.95)';
                            setTimeout(() => {
                                card.style.transform = 'scale(1)';
                            }, 100);
                        }
                    });
                }
            }
        });

        // Add hover effects for testimonial cards
        addTestimonialHoverEffects();

    } catch (error) {
        console.warn('Swiper initialization failed:', error);
    }
}

// Add hover effects for testimonial cards
function addTestimonialHoverEffects() {
    const testimonialCards = document.querySelectorAll('.testimonial-card');
    testimonialCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px) scale(1.02)';
        });

        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
}

// Initialize scroll animations
function initializeScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
            }
        });
    }, observerOptions);

    // Observe testimonial section
    const testimonialSection = document.querySelector('.testimonial-section');
    if (testimonialSection) {
        observer.observe(testimonialSection);
    }
}

// Set current year in footer
function setCurrentYear() {
    const yearElement = document.getElementById('year');
    if (yearElement) {
        yearElement.textContent = new Date().getFullYear();
    }
}

  // Initialize AOS
  AOS.init();

  // Set current year in footer or any other element
  document.getElementById("year").textContent = new Date().getFullYear();
