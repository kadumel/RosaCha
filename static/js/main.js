const menuButton = document.querySelector(".menu-toggle");
const menu = document.querySelector(".site-nav");

if (menuButton && menu) {
    menuButton.addEventListener("click", () => {
        const isOpen = menu.classList.toggle("open");
        menuButton.setAttribute("aria-expanded", String(isOpen));
    });
}

const carousel = document.querySelector("[data-carousel]");

if (carousel) {
    const track = carousel.querySelector(".hero-carousel-track");
    const slides = Array.from(carousel.querySelectorAll("[data-slide]"));
    const dots = Array.from(carousel.querySelectorAll("[data-carousel-dot]"));
    const prevButton = carousel.querySelector("[data-carousel-prev]");
    const nextButton = carousel.querySelector("[data-carousel-next]");
    let currentIndex = 0;
    let autoplayId = null;

    const renderSlide = (index) => {
        if (track) {
            track.style.transform = `translateX(-${index * 100}%)`;
        }
        dots.forEach((dot, dotIndex) => {
            dot.classList.toggle("is-active", dotIndex === index);
        });
        currentIndex = index;
    };

    const nextSlide = () => {
        const nextIndex = (currentIndex + 1) % slides.length;
        renderSlide(nextIndex);
    };

    const prevSlide = () => {
        const prevIndex = (currentIndex - 1 + slides.length) % slides.length;
        renderSlide(prevIndex);
    };

    const startAutoplay = () => {
        if (slides.length <= 1) return;
        autoplayId = window.setInterval(nextSlide, 5000);
    };

    const stopAutoplay = () => {
        if (!autoplayId) return;
        window.clearInterval(autoplayId);
        autoplayId = null;
    };

    if (nextButton) {
        nextButton.addEventListener("click", () => {
            nextSlide();
            stopAutoplay();
            startAutoplay();
        });
    }

    if (prevButton) {
        prevButton.addEventListener("click", () => {
            prevSlide();
            stopAutoplay();
            startAutoplay();
        });
    }

    dots.forEach((dot, index) => {
        dot.addEventListener("click", () => {
            renderSlide(index);
            stopAutoplay();
            startAutoplay();
        });
    });

    carousel.addEventListener("mouseenter", stopAutoplay);
    carousel.addEventListener("mouseleave", startAutoplay);

    renderSlide(0);
    startAutoplay();
}

const telefoneInput = document.querySelector('input[name="telefone"]');

if (telefoneInput) {
    const formatPtPhone = (value) => {
        const digits = value.replace(/\D/g, "");
        let localDigits = digits;

        if (localDigits.startsWith("351")) {
            localDigits = localDigits.slice(3);
        }
        if (localDigits.length > 9) {
            localDigits = localDigits.slice(0, 9);
        }

        const p1 = localDigits.slice(0, 3);
        const p2 = localDigits.slice(3, 6);
        const p3 = localDigits.slice(6, 9);

        let formatted = "+351";
        if (p1) formatted += ` ${p1}`;
        if (p2) formatted += ` ${p2}`;
        if (p3) formatted += ` ${p3}`;
        return formatted;
    };

    telefoneInput.addEventListener("input", (event) => {
        event.target.value = formatPtPhone(event.target.value);
    });

    telefoneInput.addEventListener("blur", (event) => {
        event.target.value = formatPtPhone(event.target.value);
    });
}
